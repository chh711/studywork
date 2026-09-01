"""
银行账户系统 —— 演示：类组织代码 + 异常处理保护代码
=====================================================
核心概念：
1. 用 类 封装 数据 + 行为，保护不变式（余额不能为负、金额不能为零）
2. 用 自定义异常 表达业务错误，让调用方精确捕获
3. 用 try/except/finally 保证资源清理和优雅降级
4. 用 上下文管理器 封装事务逻辑
"""

from datetime import datetime
from typing import List


# ============================================================
# 第 1 层：自定义异常 —— 把"出了什么问题"说清楚
# ============================================================

class BankError(Exception):
    """所有银行错误的基类，统一捕获入口"""
    pass


class InvalidAmountError(BankError):
    """金额非法：<=0 或不是数字"""
    def __init__(self, amount):
        self.amount = amount
        super().__init__(f"金额必须大于 0，实际值: {amount}")


class InsufficientFundsError(BankError):
    """余额不足"""
    def __init__(self, balance, requested):
        self.balance = balance
        self.requested = requested
        deficit = requested - balance
        super().__init__(
            f"余额不足！当前余额 {balance:.2f}，"
            f"尝试取款 {requested:.2f}，差额 {deficit:.2f}"
        )


class AccountFrozenError(BankError):
    """账户已冻结"""
    def __init__(self, account_id):
        super().__init__(f"账户 {account_id} 已被冻结，操作拒绝")


class TransferError(BankError):
    """转账失败（含源账户和目标账户的上下文）"""
    def __init__(self, from_id, to_id, reason):
        self.from_id = from_id
        self.to_id = to_id
        super().__init__(f"转账 {from_id} -> {to_id} 失败: {reason}")


# ============================================================
# 第 2 层：实体类 —— 数据 + 不变式 + 行为封装在一起
# ============================================================

class BankAccount:
    """
    银行账户基类
    - 属性和行为封装在一起，而不是散落的 dict + 函数
    - property 保护数据不变式（余额不为负）
    - __str__ / __repr__ 让对象可打印，方便调试
    """

    def __init__(self, account_id: str, owner: str, initial_balance: float = 0.0):
        self.account_id = account_id
        self.owner = owner
        self._balance = 0.0        # 用 _balance 内部存储
        self._frozen = False
        self.transactions: List[str] = []

        # 通过 property setter 走校验路径
        if initial_balance < 0:
            raise InvalidAmountError(initial_balance)
        self._balance = initial_balance
        self._log(f"账户创建，初始余额 {initial_balance:.2f}")

    # -------- property：把校验逻辑和字段绑定 --------
    @property
    def balance(self) -> float:
        return self._balance

    @property
    def frozen(self) -> bool:
        return self._frozen

    # -------- 核心行为方法 --------
    def deposit(self, amount: float) -> float:
        """存款 —— 前置条件检查在方法内，不用外部 if 散落"""
        self._check_not_frozen()
        self._check_amount_positive(amount)

        self._balance += amount
        self._log(f"存款 +{amount:.2f}，余额 {self._balance:.2f}")
        return self._balance

    def withdraw(self, amount: float) -> float:
        """取款 —— 多个业务校验集中在此，调用方不用自己写 if"""
        self._check_not_frozen()
        self._check_amount_positive(amount)

        if amount > self._balance:
            raise InsufficientFundsError(self._balance, amount)

        self._balance -= amount
        self._log(f"取款 -{amount:.2f}，余额 {self._balance:.2f}")
        return self._balance

    def freeze(self):
        self._frozen = True
        self._log("账户已冻结")

    def unfreeze(self):
        self._frozen = False
        self._log("账户已解冻")

    # -------- 内部校验方法（私有，复用）--------
    def _check_not_frozen(self):
        if self._frozen:
            raise AccountFrozenError(self.account_id)

    @staticmethod
    def _check_amount_positive(amount):
        """静态方法：不依赖实例状态，纯校验逻辑"""
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise InvalidAmountError(amount)

    def _log(self, message: str):
        entry = f"[{datetime.now().strftime('%H:%M:%S')}] {message}"
        self.transactions.append(entry)

    # -------- dunder 方法：让对象"好用"--------
    def __str__(self):
        status = "[FROZEN] 已冻结" if self._frozen else "[OK] 正常"
        return f"账户[{self.account_id}] {self.owner} | 余额 {self._balance:.2f} | {status}"

    def __repr__(self):
        return f"BankAccount({self.account_id!r}, {self.owner!r}, {self._balance})"


class SavingsAccount(BankAccount):
    """
    储蓄账户 —— 继承 BankAccount，演示"开闭原则"
    不修改父类，只扩展新行为
    """

    INTEREST_RATE = 0.02  # 年利率 2%

    def __init__(self, account_id: str, owner: str, initial_balance: float = 0.0):
        super().__init__(account_id, owner, initial_balance)
        self.interest_earned = 0.0

    def apply_interest(self):
        """计算利息 —— 只有储蓄账户有这个行为"""
        interest = self._balance * self.INTEREST_RATE
        self._balance += interest
        self.interest_earned += interest
        self._log(f"利息 +{interest:.2f}，累计利息 {self.interest_earned:.2f}")
        return interest


# ============================================================
# 第 3 层：上下文管理器 —— 封装事务/资源管理
# ============================================================

class Transaction:
    """
    转账事务上下文管理器
    - __enter__ 记录快照
    - __exit__ 在异常时自动回滚
    - 用 with 语句保证 finally 逻辑一定执行
    """

    def __init__(self, from_account: BankAccount, to_account: BankAccount, amount: float):
        self.from_account = from_account
        self.to_account = to_account
        self.amount = amount
        self.snapshot_from = None
        self.snapshot_to = None

    def __enter__(self):
        # 保存快照，用于回滚
        self.snapshot_from = self.from_account.balance
        self.snapshot_to = self.to_account.balance
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            # 异常 -> 回滚
            print(f"  [WARN] 事务异常，回滚至转账前状态")
            self.from_account._balance = self.snapshot_from
            self.to_account._balance = self.snapshot_to
            # 返回 False 让异常继续向上传播
        # 无论成功与否，都执行（如记录审计日志）
        print(f"  [LOG] 事务结束 | 源账户 {self.from_account.account_id} "
              f"余额: {self.from_account.balance:.2f} | "
              f"目标账户 {self.to_account.account_id} 余额: {self.to_account.balance:.2f}")
        return False  # 不吞掉异常


# ============================================================
# 第 4 层：服务层 —— 编排 + 异常处理的集中阵地
# ============================================================

class BankService:
    """
    银行服务 —— 编排多个账户的操作，统一处理异常
    所有 try/except 都在这一层，实体类只负责抛异常
    """

    def __init__(self):
        self.accounts: dict[str, BankAccount] = {}

    def create_account(self, account_id: str, owner: str, initial_balance: float = 0.0):
        """创建账户 —— 异常让调用方决定怎么处理"""
        if account_id in self.accounts:
            raise BankError(f"账户 {account_id} 已存在")
        account = BankAccount(account_id, owner, initial_balance)
        self.accounts[account_id] = account
        return account

    def transfer(self, from_id: str, to_id: str, amount: float):
        """
        转账 —— 用 Transaction 上下文管理器自动处理回滚
        异常会被包装成 TransferError，携带完整上下文
        """
        from_acc = self.accounts.get(from_id)
        to_acc = self.accounts.get(to_id)

        if from_acc is None:
            raise TransferError(from_id, to_id, f"源账户 {from_id} 不存在")
        if to_acc is None:
            raise TransferError(from_id, to_id, f"目标账户 {to_id} 不存在")

        try:
            with Transaction(from_acc, to_acc, amount):
                from_acc.withdraw(amount)
                to_acc.deposit(amount)
                print(f"  [OK] 转账成功: {from_id} -> {to_id}, {amount:.2f}")
        except TransferError:
            raise  # 已经是 TransferError，直接上抛
        except BankError as e:
            raise TransferError(from_id, to_id, str(e)) from e
        except Exception as e:
            raise TransferError(from_id, to_id, str(e)) from e

    def print_all_accounts(self):
        print("\n[INFO] 当前所有账户：")
        for acc in self.accounts.values():
            print(f"  {acc}")


# ============================================================
# 第 5 层：演示运行 —— 展示正常路径和异常路径
# ============================================================

def demo():
    print("=" * 60)
    print("  银行账户系统 —— 类组织 + 异常处理 演示")
    print("=" * 60)

    bank = BankService()

    # -------- 场景 1：正常操作 --------
    print("\n>> 场景 1：正常存取款")
    try:
        alice = bank.create_account("A001", "Alice", 1000.0)
        bob = bank.create_account("B001", "Bob", 500.0)

        print(f"  创建: {alice}")
        print(f"  创建: {bob}")

        alice.deposit(200)
        bob.withdraw(100)
    except BankError as e:
        print(f"  [ERR] 错误: {e}")

    bank.print_all_accounts()

    # -------- 场景 2：异常被正确捕获 --------
    print("\n>> 场景 2：余额不足 -> InsufficientFundsError")
    try:
        alice.withdraw(9999)
    except InsufficientFundsError as e:
        print(f"  [ERR] 捕获到: {e}")
        print(f"     当前余额: {e.balance:.2f}, 请求金额: {e.requested:.2f}")

    # -------- 场景 3：非法输入被拦截 --------
    print("\n>> 场景 3：非法金额 -> InvalidAmountError")
    for bad_amount in [-100, 0, "abc"]:
        try:
            alice.deposit(bad_amount)
        except InvalidAmountError as e:
            print(f"  [ERR] 输入 {bad_amount!r} -> {e}")

    # -------- 场景 4：转账（带事务回滚演示）--------
    print("\n>> 场景 4：正常转账（带事务上下文管理器）")
    try:
        bank.transfer("A001", "B001", 300)
    except TransferError as e:
        print(f"  [ERR] {e}")

    # -------- 场景 5：转账失败自动回滚 --------
    print("\n>> 场景 5：转账失败 -> 自动回滚（余额不变）")
    print("  --- 转账前 ---")
    bank.print_all_accounts()

    try:
        # 冻结目标账户，让 deposit 失败，观察回滚
        bob.freeze()
        bank.transfer("A001", "B001", 200)
    except TransferError as e:
        print(f"  [ERR] 转账失败: {e}")

    print("\n  --- 转账后（应保持不变）---")
    bob.unfreeze()  # 解开以便查看
    bank.print_all_accounts()

    # -------- 场景 6：储蓄账户多态 --------
    print("\n>> 场景 6：储蓄账户（多态）")
    try:
        savings = SavingsAccount("S001", "Charlie", 5000.0)
        bank.accounts["S001"] = savings
        print(f"  创建: {savings}")
        interest = savings.apply_interest()
        print(f"  计息后: {savings}")
    except BankError as e:
        print(f"  [ERR] {e}")

    # -------- 场景 7：统一异常捕获 --------
    print("\n>> 场景 7：基类统一捕获所有银行异常")
    try:
        alice.freeze()
        alice.withdraw(10)  # 这会抛出 AccountFrozenError
    except BankError as e:
        # 一个 except 捕获所有 BankError 子类
        print(f"  [ERR] 被 BankError 统一捕获: {e}")

    print("\n" + "=" * 60)
    print("  演示结束")
    print("=" * 60)


if __name__ == "__main__":
    demo()
