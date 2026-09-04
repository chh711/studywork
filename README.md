# Qwen3 Embedding & Reranker 本地可视化原型

这是一个基于 **Flask + 本地 Qwen3 模型** 的检索能力演示原型，面向 **Embedding 向量化、Reranker 重排、简易 RAG 流程** 的本地化测试与可视化展示。

项目当前重点是：
- 跑通本地模型调用流程
- 验证召回与重排效果
- 通过可视化页面直观展示检索结果
- 为后续扩展知识库问答系统打基础

---

## 功能概览

### 1. Embedding 文本向量化
- 输入文本后生成向量
- 支持指定向量维度
- 适合用于相似度检索、召回测试等场景

### 2. Reranker 文档重排
- 输入 Query 和多条候选文档
- 自动计算文档相关性分数
- 按分数排序输出结果
- 支持 Top1 高亮和分数可视化

### 3. 简易 RAG 流程演示
- 先使用 Embedding 进行召回
- 再使用 Reranker 进行精排
- 输出最终排序结果
- 提供简易答案展示

### 4. Web 可视化界面
- 提供本地网页操作界面
- 支持 Embedding / Reranker / RAG 三个标签页
- 支持表格展示、分数条形图、结果高亮

---

## 项目结构

```text
D:\rag-embedding
├─ flask_api.py           # Flask 可视化页面与 API 服务
├─ qwen3_embedding.py     # Embedding 模型加载与编码逻辑
├─ qwen3_reranker.py      # Reranker 模型加载与重排逻辑
├─ models/                # 本地模型目录（默认不上传 GitHub）
└─ README.md
```

---

## 运行环境

当前项目在以下本地环境中运行：

- 操作系统：Windows
- Python：3.11
- 虚拟环境：Conda
- 环境名称：`qwen3-embedding-reranker`
- Web 框架：Flask
- 推理方式：本地离线加载模型

本项目使用的本地模型目录示例：

- `models/Qwen3-Embedding-0.6B`
- `models/Qwen3-Reranker-0.6B`

> 模型文件已提前下载到本地，因此系统可以离线运行，不依赖外部在线推理接口。

---

## 启动方式

在项目目录下执行：

```bash
python flask_api.py
```

启动成功后，浏览器访问：

- [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## API 接口

### `POST /embedding`
用于文本向量化。

请求示例：

```json
{
  "model_name": "Qwen3-Embedding-0.6B",
  "query_text": "你好，世界",
  "dim": 1024
}
```

### `POST /reranker`
用于候选文档重排。

请求示例：

```json
{
  "model_name": "Qwen3-Reranker-0.6B",
  "query": "中国的首都是哪里？",
  "documents": [
    "中国的首都是北京",
    "上海是中国最大的城市之一",
    "东京是日本的首都"
  ]
}
```

### `POST /rag`
用于简易 RAG 召回与重排演示。

请求示例：

```json
{
  "embedding_model_name": "Qwen3-Embedding-0.6B",
  "rerank_model_name": "Qwen3-Reranker-0.6B",
  "query": "中国的首都是哪里？",
  "documents": [
    "中国的首都是北京",
    "北京是中国的政治中心",
    "上海是中国最大的城市之一"
  ],
  "dim": 1024,
  "candidate_k": 5,
  "output_k": 3
}
```

---

## 当前实现说明

目前该项目属于 **原型验证阶段**，已完成以下能力：

- 本地 Embedding 模型加载
- 本地 Reranker 模型加载
- Embedding 检索召回
- Reranker 重排
- 简易 RAG 流程串联
- 结果页面可视化展示

当前“最终答案”模块为 **基于检索结果的简化生成逻辑**，主要用于演示流程，不等同于完整的大模型生成式问答。

---

## 后续可扩展方向

- 文档上传与知识库管理
- 引用来源展示
- 历史记录保存
- 结果导出（CSV / Excel）
- 更完整的答案生成能力
- 多知识库切换与管理

---

## 注意事项

- `models/` 目录通常较大，建议不要直接提交到 GitHub
- 首次启动或首次请求时，模型加载可能会稍慢
- 当前服务为开发调试版本，不建议直接用于生产环境

---

## 适用场景

这个原型适合用于：

- 本地检索链路验证
- Embedding / Reranker 效果演示
- RAG 原型开发
- 内部汇报与功能展示

