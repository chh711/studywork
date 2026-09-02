# 我的 Dify 仓库说明

本文件用于补充说明当前仓库的使用方式，避免直接改动官方 README 的主体内容。

## 1. 仓库用途

本仓库基于 Dify 官方开源代码整理，主要用于：

- 本地 Docker 部署
- Dify 功能体验与测试
- 二次开发与个性化配置
- 工作流 / 应用 / 知识库相关实验

## 2. 快速启动

### 2.1 进入 Docker 目录

```powershell
cd docker
```

### 2.2 复制环境变量模板

```powershell
Copy-Item .env.example .env
```

### 2.3 按需修改 `.env`

至少应检查以下内容：

- 端口配置
- 数据库连接配置
- Redis 配置
- 对象存储配置
- 模型供应商 API Key

> 注意：`docker/.env` 仅用于本地运行，不要提交到 GitHub。

### 2.4 启动容器

```powershell
docker compose up -d
```

### 2.5 打开初始化页面

浏览器访问：

- http://localhost/install

## 3. 常用 Docker 命令

### 查看容器状态

```powershell
docker compose ps
```

### 查看日志

```powershell
docker compose logs -f
```

### 停止服务

```powershell
docker compose down
```

### 重启服务

```powershell
docker compose restart
```

## 4. 上传 GitHub 时的注意事项

建议不要上传以下内容：

- `docker/.env`
- 各类真实 API Key
- 数据库密码
- 本地缓存、卷数据、日志
- 个人 IDE 临时文件

当前仓库已通过 `.gitignore` 排除了常见本地运行文件。

## 5. 如果启动异常，优先检查

- Docker Desktop 是否正常运行
- 端口是否被占用
- `.env` 是否漏填关键变量
- `docker compose logs -f` 是否有报错
- 模型供应商配置是否正确

## 6. 相关说明

- 官方项目说明：`README.md`
- 本地部署补充：`docs/DEPLOYMENT_CN.md`
