# Dify 本地部署说明

## 一、部署前准备

请先确保本机已安装：

- Docker Desktop
- Docker Compose

建议资源：

- CPU：2 核及以上
- 内存：4 GB 及以上

## 二、启动步骤

### 1. 进入 Docker 目录

```powershell
cd docker
```

### 2. 复制环境模板

```powershell
Copy-Item .env.example .env
```

### 3. 修改 `.env`

你可以按自己的需要配置：

- 数据库
- Redis
- 存储
- 模型 API Key
- 站点地址和端口

> 注意：
>
> - `docker/.env.example` 可以提交到 GitHub
> - `docker/.env` 不要提交到 GitHub

### 4. 启动容器

```powershell
docker compose up -d
```

### 5. 访问安装页

打开浏览器访问：

- http://localhost/install

## 三、常用排查命令

### 查看容器状态

```powershell
docker compose ps
```

### 查看日志

```powershell
docker compose logs -f
```

### 查看某个服务日志

```powershell
docker compose logs -f api
```

### 停止服务

```powershell
docker compose down
```

## 四、上传仓库建议

建议保留：

- 源代码
- `docker/.env.example`
- `docker/envs/*.env.example`
- 部署文档

建议不要提交：

- `docker/.env`
- 数据卷
- 缓存目录
- 临时日志
- 真实密钥与账号信息

## 五、常见问题

### 1. 页面打不开

优先检查：

- Docker 是否启动
- 容器是否全部正常运行
- 端口是否冲突
- Nginx / Web / API 服务是否异常

### 2. 模型无法调用

优先检查：

- API Key 是否填写正确
- 模型供应商是否已在 Dify 中配置
- Base URL 是否正确
- 网络是否可访问对应模型服务

### 3. 修改配置后不生效

可以尝试：

```powershell
docker compose down
docker compose up -d
```

## 六、补充

如果你后续要把这个仓库作为自己的公开项目，建议再补充：

- 项目简介
- 使用截图
- 你的功能改动说明
- 工作流示例
- 常见问题 FAQ
