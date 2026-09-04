# Qwen3 Embedding & Reranker 本地可视化原型

这是一个基于 Flask 的本地可视化原型，集成了：

- Embedding 文本向量化
- Reranker 文档重排
- 简易 RAG 检索流程
- Web 可视化展示

## 运行方式

```bash
python flask_api.py
```

然后在浏览器打开：

- http://127.0.0.1:5000

## 说明

- 模型文件默认放在 `models/` 下
- `models/` 目录较大，不建议提交到 GitHub
