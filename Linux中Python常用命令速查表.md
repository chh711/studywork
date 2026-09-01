# Linux 中 Python 常用命令速查表
## 一、查看与确认环境

| 命令 | 说明 |
|------|------|
| `python3 --version` | 查看 Python 3 版本 |
| `python --version` | 查看默认 python 指向的版本 |
| `which python3` | 查看 python3 可执行文件路径 |
| `whereis python3` | 查找 python3 相关的所有安装位置 |
| `ls /usr/bin/python*` | 查看系统中安装的所有 Python 版本 |
| `python3 -c "import sys; print(sys.version)"` | 查看详细的解释器版本信息 |
| `python3 -c "import sys; print(sys.executable)"` | 查看当前使用的解释器绝对路径 |
| `echo $PATH` | 查看环境变量（确认 Python 路径） |

---

## 二、运行代码

| 命令 | 说明 |
|------|------|
| `python3 script.py` | 运行 Python 脚本 |
| `python3 script.py arg1 arg2` | 运行脚本并传递参数（`sys.argv` 接收） |
| `python3 -m module_name` | 以模块方式运行（如 `python3 -m http.server`） |
| `python3 -c "print('hello')"` | 直接执行一行代码 |
| `python3 -i script.py` | 运行脚本后进入交互模式 |
| `./script.py` | 脚本带 shebang（`#!/usr/bin/env python3`）且有执行权限时直接运行 |
| `chmod +x script.py` | 为脚本添加可执行权限 |
| `python3 -V` | 同 `--version` |

---

## 三、交互式解释器（REPL）

| 命令 | 说明 |
|------|------|
| `python3` | 进入交互式解释器 |
| `exit()` 或 `quit()` | 退出交互模式 |
| `help(对象)` | 查看对象的帮助文档 |
| `dir(对象)` | 查看对象的所有属性和方法 |
| `type(对象)` | 查看对象类型 |
| `import sys; sys.path` | 查看模块搜索路径 |
| `import this` | 显示 Python 之禅 |

---

## 四、pip 包管理

| 命令 | 说明 |
|------|------|
| `pip3 --version` | 查看 pip 版本 |
| `pip3 install 包名` | 安装包 |
| `pip3 install 包名==1.2.3` | 安装指定版本 |
| `pip3 install --upgrade 包名` | 升级包 |
| `pip3 uninstall 包名` | 卸载包 |
| `pip3 show 包名` | 查看包详细信息 |
| `pip3 list` | 列出已安装的所有包 |
| `pip3 list --outdated` | 列出可升级的包 |
| `pip3 freeze > requirements.txt` | 导出依赖清单 |
| `pip3 install -r requirements.txt` | 从清单批量安装依赖 |
| `pip3 search 关键词` | 搜索 PyPI 上的包 |
| `pip3 download 包名 -d ./目录` | 只下载不安装（离线备份） |
| `pip3 install -i 镜像地址 包名` | 使用指定镜像源安装 |

---

## 五、虚拟环境（venv）

| 命令 | 说明 |
|------|------|
| `python3 -m venv 环境名` | 创建虚拟环境（如 `python3 -m venv venv`） |
| `source venv/bin/activate` | 激活虚拟环境 |
| `deactivate` | 退出虚拟环境 |
| `rm -rf venv` | 删除虚拟环境（慎用） |
| `python3 -m venv --system-site-packages venv` | 创建时继承系统全局包 |

---

## 六、文件与目录操作（shell + Python 配合）

| 命令 | 说明 |
|------|------|
| `python3 -m http.server 8000` | 在当前目录启动简单 HTTP 服务器 |
| `python3 -m json.tool file.json` | 格式化 / 校验 JSON 文件 |
| `python3 -c "import hashlib; print(hashlib.md5(open('f','rb').read()).hexdigest())"` | 计算文件 MD5 |
| `cat data.txt \| python3 script.py` | 通过管道向脚本传入数据 |

---

## 七、环境变量与路径配置

| 命令 | 说明 |
|------|------|
| `export PATH=$PATH:/新的python路径` | 临时添加 Python 到 PATH |
| `echo 'export PATH=$PATH:/新的python路径' >> ~/.bashrc` | 永久添加（需 `source ~/.bashrc` 生效） |
| `export PYTHONPATH=$PYTHONPATH:/自定义模块目录` | 添加模块搜索路径 |
| `export PYTHONDONTWRITEBYTECODE=1` | 禁止生成 `.pyc` 缓存文件 |

---

## 八、进程与调试

| 命令 | 说明 |
|------|------|
| `ps aux \| grep python` | 查看正在运行的 Python 进程 |
| `kill -9 PID` | 强制结束指定 PID 的进程 |
| `nohup python3 script.py &` | 后台运行脚本（终端关闭后不中断） |
| `python3 -m pdb script.py` | 使用内置调试器 pdb 调试脚本 |
| `python3 -m cProfile script.py` | 性能分析（查看耗时函数） |
| `python3 -O script.py` | 优化模式运行（去掉 assert） |
| `python3 -W error script.py` | 将警告视为错误 |

---

## 九、常见排查命令

| 命令 | 说明 |
|------|------|
| `python3 -m pip install --user 包名` | 安装到用户目录（无 root 权限时） |
| `sudo apt install python3-pip` | Debian/Ubuntu 安装 pip |
| `sudo yum install python3-pip` | CentOS/RHEL 安装 pip |
| `python3 -m ensurepip --upgrade` | 修复 / 引导安装 pip |
| `python3 -m site` | 查看 site-packages 目录位置 |
| `pip3 config list` | 查看 pip 配置（如镜像源） |

---

## 十、实用技巧

| 技巧 | 命令 / 说明 |
|------|------|
| 快速计算 | `python3 -c "print(2**10)"` |
| 生成随机密码 | `python3 -c "import secrets; print(secrets.token_urlsafe(16))"` |
| 查看系统信息 | `python3 -c "import platform; print(platform.uname())"` |
| 批量重命名文件 | 用 Python 脚本配合 `os` / `pathlib` 模块完成 |
| 查看某模块版本 | `python3 -c "import requests; print(requests.__version__)"` |
| 历史记录搜索 | REPL 中按 `Ctrl+R` 搜索历史输入 |

---

## 十一、Conda 环境管理

### 环境与版本管理

| 命令 | 说明 |
|------|------|
| `conda --version` | 查看 conda 版本 |
| `conda create -n 环境名 python=3.11` | 创建指定 Python 版本的虚拟环境 |
| `conda create -n 环境名 --clone 旧环境名` | 克隆（复制）已有环境 |
| `conda activate 环境名` | 激活环境 |
| `conda deactivate` | 退出当前环境 |
| `conda env list` 或 `conda info --envs` | 列出所有环境（`*` 标记当前环境） |
| `conda list` | 列出当前环境已安装的包 |
| `conda list -n 环境名` | 列出指定环境的包 |
| `conda remove -n 环境名 --all` | 删除整个环境（慎用） |

### 包管理与升级

| 命令 | 说明 |
|------|------|
| `conda install 包名` | 安装包（可加 `=版本号` 指定版本） |
| `conda install -n 环境名 包名` | 向指定环境安装包 |
| `conda update 包名` | 升级指定包 |
| `conda update --all` | 升级当前环境所有包 |
| `conda update conda` | 升级 conda 自身 |
| `conda install python=3.12` | 在当前环境中切换 / 升级 Python 版本 |
| `conda remove 包名` | 卸载包 |
| `conda search 包名` | 搜索可用包及版本 |
| `conda env export > environment.yml` | 导出环境配置清单 |
| `conda env create -f environment.yml` | 从清单还原环境 |
| `conda clean --all` | 清理缓存包与索引，释放磁盘空间 |
| `conda config --add channels 镜像源` | 添加镜像源（如清华源）加速下载 |

> 提示：conda 环境内也可混用 `pip install`，pip 安装的包同样出现在 `conda list` 中，但导出时建议以 `environment.yml` 为准。

---

## 十二、pyenv 多版本管理

### 安装 Python 多版本

| 命令 | 说明 |
|------|------|
| `pyenv --version` | 查看 pyenv 版本 |
| `pyenv install --list` | 列出所有可安装的 Python 版本 |
| `pyenv install 3.12.4` | 编译安装指定版本 |
| `pyenv install -s 3.12.4` | 已存在时跳过安装（幂等安装） |
| `pyenv versions` | 列出本地已安装的所有版本（`*` 标记当前版本） |
| `pyenv version` | 查看当前生效的版本 |
| `pyenv which python` | 查看当前 python 命令的实际路径 |
| `sudo apt install build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev libffi-dev` | Debian/Ubuntu 安装编译依赖（安装前执行，避免编译失败） |

### 版本切换与设置

| 命令 | 说明 |
|------|------|
| `pyenv global 3.12.4` | 设置全局默认版本（写入 `~/.pyenv/version`） |
| `pyenv local 3.11.9` | 为当前目录设置版本（生成 `.python-version` 文件，随项目走） |
| `pyenv shell 3.10.14` | 仅为当前 shell 会话临时切换版本 |
| `pyenv shell --unset` | 取消会话级临时切换 |
| `pyenv uninstall 3.10.14` | 卸载指定版本 |
| `pyenv rehash` | 安装 / 卸载带可执行文件的包后刷新 shim（一般自动执行） |

### pyenv-virtualenv 插件（虚拟环境）

| 命令 | 说明 |
|------|------|
| `pyenv virtualenv 3.12.4 环境名` | 基于指定版本创建虚拟环境 |
| `pyenv virtualenvs` | 列出所有虚拟环境 |
| `pyenv activate 环境名` | 激活虚拟环境 |
| `pyenv deactivate` | 退出虚拟环境 |
| `pyenv virtualenv-delete 环境名` | 删除虚拟环境（慎用） |
| `pyenv local 环境名` | 进入目录自动激活该环境 |

