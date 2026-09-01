"""
矩阵乘法演示 — 手算步骤 + NumPy 验证 + 精美可视化。

包含 3 道不同规模的矩阵乘法题：
  题1: 2×2 × 2×2  (基础入门)
  题2: 3×2 × 2×3  (非方阵相乘)
  题3: 3×3 × 3×3  (方阵进阶)
"""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.font_manager import FontProperties
from typing import List, Tuple
import os

# ─── 尝试设置中文字体 ───────────────────────────────────────────
_FONT_PATHS: list[str] = [
    "C:/Windows/Fonts/msyh.ttc",      # 微软雅黑
    "C:/Windows/Fonts/simhei.ttf",    # 黑体
    "C:/Windows/Fonts/simsun.ttc",    # 宋体
]
_CN_FONT: FontProperties | None = None
for _fp in _FONT_PATHS:
    if os.path.exists(_fp):
        _CN_FONT = FontProperties(fname=_fp, size=11)
        break

plt.rcParams["axes.unicode_minus"] = False
if _CN_FONT:
    plt.rcParams["font.family"] = _CN_FONT.get_name()

# ─── 3 道矩阵乘法题目 ───────────────────────────────────────────

PROBLEMS: list[dict] = [
    {
        "title": "题 1 : 2x2 * 2x2 基础入门",
        "A": np.array([[1, 2],
                        [3, 4]], dtype=float),
        "B": np.array([[5, 6],
                        [7, 8]], dtype=float),
    },
    {
        "title": "题 2 : 3x2 * 2x3 非方阵相乘",
        "A": np.array([[1, 2],
                        [3, 4],
                        [5, 6]], dtype=float),
        "B": np.array([[7, 8, 9],
                        [10, 11, 12]], dtype=float),
    },
    {
        "title": "题 3 : 3x3 * 3x3 方阵进阶",
        "A": np.array([[2, 3, 1],
                        [4, 0, 5],
                        [1, 7, 3]], dtype=float),
        "B": np.array([[3, 1, 2],
                        [0, 4, 1],
                        [2, 5, 0]], dtype=float),
    },
]

# ─── 颜色方案 ───────────────────────────────────────────────────

COLOR_A = "#4ECDC4"       # 青色 — 矩阵 A
COLOR_B = "#FF6B6B"       # 珊瑚 — 矩阵 B
COLOR_C = "#FFE66D"       # 金黄 — 结果矩阵 C
COLOR_BG = "#1A1A2E"      # 深蓝背景
COLOR_CELL_TEXT = "#FFFFFF"
COLOR_HEADER = "#E8E8E8"
COLOR_STEP_BG = "#F7F7F7"

# ─── 矩阵格式化输出 ─────────────────────────────────────────────


def format_matrix(mat: np.ndarray, name: str = "", precision: int = 0) -> str:
    """将矩阵格式化为整齐的字符串。"""
    lines: list[str] = []
    if name:
        lines.append(f"{name} =")
    rows, cols = mat.shape
    for r in range(rows):
        row_vals = "  ".join(f"{mat[r, c]:{precision}.0f}" if mat[r, c] == int(mat[r, c])
                             else f"{mat[r, c]:6.2f}"
                             for c in range(cols))
        lines.append(f"  [ {row_vals} ]")
    return "\n".join(lines)


def manual_multiply(A: np.ndarray, B: np.ndarray) -> Tuple[np.ndarray, str]:
    """手动计算矩阵乘法，返回结果矩阵和详细步骤字符串。"""
    rows_a, cols_a = A.shape
    rows_b, cols_b = B.shape
    assert cols_a == rows_b, "维度不兼容"

    C = np.zeros((rows_a, cols_b), dtype=float)
    steps: list[str] = []

    for i in range(rows_a):
        for j in range(cols_b):
            terms: list[str] = []
            total: float = 0.0
            for k in range(cols_a):
                a_val = A[i, k]
                b_val = B[k, j]
                prod = a_val * b_val
                total += prod
                a_str = f"{a_val:.0f}" if a_val == int(a_val) else f"{a_val:.1f}"
                b_str = f"{b_val:.0f}" if b_val == int(b_val) else f"{b_val:.1f}"
                terms.append(f"{a_str}*{b_str}")
            C[i, j] = total
            result_str = f"{total:.0f}" if total == int(total) else f"{total:.1f}"
            steps.append(f"  C[{i+1},{j+1}] = {' + '.join(terms)} = {result_str}")

    return C, "\n".join(steps)


def print_problem(i: int, prob: dict) -> None:
    """打印单道题的完整手算过程。"""
    A, B = prob["A"], prob["B"]
    title = prob["title"]

    sep = "=" * 60
    print(f"\n{sep}")
    print(f"  {title}")
    print(sep)

    print(format_matrix(A, "A"))
    print()
    print(format_matrix(B, "B"))
    print()

    C_manual, steps = manual_multiply(A, B)
    print("--- 逐元素手算步骤 ---")
    print(steps)

    C_numpy = A @ B
    print()
    print(format_matrix(C_manual, "手动结果 C"))
    print()
    print(format_matrix(C_numpy, "NumPy 验证"))

    match = np.allclose(C_manual, C_numpy)
    status = "PASS" if match else "FAIL"
    print(f"\n  >>> 验证: {status} <<<")


# ─── 可视化 ────────────────────────────────────────────────────


def draw_matrix(ax: plt.Axes, mat: np.ndarray, color: str,
                title: str, show_row_labels: bool = True) -> None:
    """在指定 Axes 上绘制一个矩阵网格。"""
    rows, cols = mat.shape
    ax.clear()
    ax.set_xlim(-1, cols + 0.5)
    ax.set_ylim(-1, rows + 1.5)
    ax.set_aspect("equal")
    ax.axis("off")

    # 标题
    if _CN_FONT:
        ax.set_title(title, fontproperties=_CN_FONT, fontsize=13, fontweight="bold",
                     color=COLOR_HEADER, pad=12)
    else:
        ax.set_title(title, fontsize=13, fontweight="bold", color=COLOR_HEADER, pad=12)

    # 行标签
    if show_row_labels:
        for r in range(rows):
            if _CN_FONT:
                ax.text(-0.6, rows - 1 - r, f"行{r+1}", va="center", ha="right",
                        fontsize=8, color="#AAAAAA", fontproperties=_CN_FONT)
            else:
                ax.text(-0.6, rows - 1 - r, f"r{r+1}", va="center", ha="right",
                        fontsize=8, color="#AAAAAA")

    # 绘制单元格
    for i in range(rows):
        for j in range(cols):
            val = mat[i, j]
            # 根据值大小调整颜色亮度
            alpha = min(1.0, 0.4 + abs(val) / max(1, np.max(np.abs(mat))) * 0.6)
            rect = mpatches.FancyBboxPatch(
                (j, rows - 1 - i), 0.85, 0.85,
                boxstyle="round,pad=0.02",
                facecolor=color, edgecolor="#FFFFFF",
                linewidth=1.5, alpha=alpha,
            )
            ax.add_patch(rect)
            # 数值
            txt = f"{val:.0f}" if val == int(val) else f"{val:.2f}"
            ax.text(j + 0.425, rows - 1 - i + 0.425, txt,
                    ha="center", va="center", fontsize=11, fontweight="bold",
                    color=COLOR_CELL_TEXT)

    # 尺寸标注
    dim_text = f"({rows}x{cols})"
    ax.text(cols / 2 - 0.15, -0.6, dim_text, ha="center", fontsize=9,
            color="#BBBBBB")


def draw_operation_arrow(ax: plt.Axes, x: float, y: float) -> None:
    """绘制乘法运算符。"""
    circle = plt.Circle((x, y), 0.22, facecolor="#FFFFFF", edgecolor="none", alpha=0.9)
    ax.add_patch(circle)
    ax.text(x, y, "x", ha="center", va="center", fontsize=16, fontweight="bold",
            color="#333333")


def create_visualization(problems: list[dict], save_path: str = "matrix_multiplication.png") -> None:
    """创建 3 道题目的精美可视化大图。"""
    fig = plt.figure(figsize=(20, 20), facecolor=COLOR_BG)
    fig.suptitle("Matrix Multiplication 矩阵乘法", fontsize=26, fontweight="bold",
                 color=COLOR_HEADER, y=0.98)

    # 子标题
    if _CN_FONT:
        fig.text(0.5, 0.955, "手算步骤 + NumPy 验证 + 可视化",
                 ha="center", fontsize=14, color="#AAAAAA", fontproperties=_CN_FONT)
    else:
        fig.text(0.5, 0.955, "Manual Calculation + NumPy Verification + Visualization",
                 ha="center", fontsize=14, color="#AAAAAA")

    for idx, prob in enumerate(problems):
        A, B = prob["A"], prob["B"]
        title = prob["title"]
        C = A @ B  # NumPy 计算

        # 三行布局: (A, x, B, =, C) 在一行内
        row_base = 0.75 - idx * 0.30

        # 矩阵 A 区域
        ax_a = fig.add_axes([0.03, row_base, 0.18, 0.18])
        draw_matrix(ax_a, A, COLOR_A, "Matrix A")

        # 乘号
        ax_x = fig.add_axes([0.22, row_base + 0.03, 0.05, 0.10])
        ax_x.axis("off")
        draw_operation_arrow(ax_x, 0.5, 0.55)

        # 矩阵 B 区域
        ax_b = fig.add_axes([0.27, row_base, 0.18, 0.18])
        draw_matrix(ax_b, B, COLOR_B, "Matrix B")

        # 等号
        ax_eq = fig.add_axes([0.46, row_base + 0.03, 0.05, 0.10])
        ax_eq.axis("off")
        ax_eq.text(0.5, 0.55, "=", ha="center", va="center", fontsize=24,
                   fontweight="bold", color="#FFFFFF")

        # 结果矩阵 C 区域
        ax_c = fig.add_axes([0.51, row_base, 0.18, 0.18])
        draw_matrix(ax_c, C, COLOR_C, "Result C")

        # ── 右侧：手算步骤 ──
        _, steps_str = manual_multiply(A, B)
        steps_lines = steps_str.strip().split("\n")

        ax_steps = fig.add_axes([0.72, row_base - 0.04, 0.26, 0.26])
        ax_steps.axis("off")

        # 步骤标题
        if _CN_FONT:
            ax_steps.text(0.0, 1.02, title, fontsize=12, fontweight="bold",
                          color=COLOR_HEADER, fontproperties=_CN_FONT)
            ax_steps.text(0.0, 0.94, "逐元素计算步骤:",
                          fontsize=9, color="#BBBBBB", fontproperties=_CN_FONT)
        else:
            ax_steps.text(0.0, 1.02, title, fontsize=12, fontweight="bold",
                          color=COLOR_HEADER)
            ax_steps.text(0.0, 0.94, "Element-wise steps:",
                          fontsize=9, color="#BBBBBB")

        max_lines = min(len(steps_lines), 9)
        for li, line in enumerate(steps_lines[:max_lines]):
            y_pos = 0.86 - li * 0.09
            color = "#E8E8E8" if li % 2 == 0 else "#CCCCCC"
            ax_steps.text(0.02, y_pos, line, fontsize=7.5, color=color,
                          family="monospace", va="center")

        if len(steps_lines) > max_lines:
            ax_steps.text(0.02, 0.86 - max_lines * 0.09,
                          f"  ... 共 {len(steps_lines)} 个元素，已全部验证",
                          fontsize=7.5, color="#888888")

        # ── 验证标记 ──
        ax_verify = fig.add_axes([0.72, row_base - 0.11, 0.26, 0.06])
        ax_verify.axis("off")
        C_manual, _ = manual_multiply(A, B)
        ok = np.allclose(C_manual, C)
        badge_color = "#2ECC71" if ok else "#E74C3C"
        badge_text = "PASS  NumPy 验证通过" if ok else "FAIL  验证失败"
        ax_verify.text(0.0, 0.5, badge_text, fontsize=11, fontweight="bold",
                       color=badge_color, va="center")

    # ── 底部图例 ──
    legend_ax = fig.add_axes([0.15, 0.01, 0.70, 0.03])
    legend_ax.axis("off")
    legends = [(COLOR_A, "Matrix A"), (COLOR_B, "Matrix B"), (COLOR_C, "Result C")]
    for li, (color, label) in enumerate(legends):
        x_start = 0.1 + li * 0.28
        rect = mpatches.FancyBboxPatch((x_start, 0.2), 0.06, 0.55,
                                        boxstyle="round,pad=0.02",
                                        facecolor=color, edgecolor="#FFFFFF", linewidth=1)
        legend_ax.add_patch(rect)
        legend_ax.text(x_start + 0.08, 0.48, label, fontsize=10, color=COLOR_HEADER,
                       va="center")

    fig.savefig(save_path, dpi=150, bbox_inches="tight",
                facecolor=COLOR_BG, edgecolor="none")
    plt.close(fig)
    print(f"\n可视化已保存至: {save_path}")


# ─── 主程序 ────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "█" * 60)
    print("  矩阵乘法演示 — 手算步骤 + NumPy 验证")
    print("█" * 60)

    for i, prob in enumerate(PROBLEMS):
        print_problem(i + 1, prob)

    print("\n" + "█" * 60)
    print("  生成可视化图表 ...")
    print("█" * 60)

    create_visualization(PROBLEMS)

    print("\n完成! 所有 3 道题均已手算并验证通过。")
