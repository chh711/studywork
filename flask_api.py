from flask import Flask, request, jsonify, render_template_string
import math
import os
from typing import List

import torch

import qwen3_embedding
import qwen3_reranker

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

app = Flask(__name__)

PAGE = """
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Qwen3 功能可视化界面</title>
  <style>
    :root {
      --bg: #0f1115;
      --panel: #1a1d24;
      --panel-2: #222633;
      --text: #e8ebf0;
      --muted: #aab2c0;
      --border: #343a4a;
      --accent: #ff6a00;
      --accent-2: #4d90fe;
      --danger: #ff5c5c;
      --ok: #35c28f;
      --code: #0b0d12;
      --top: rgba(255, 106, 0, 0.16);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: Arial, "Microsoft YaHei", sans-serif;
      background: radial-gradient(circle at top, #161a22 0, var(--bg) 60%);
      color: var(--text);
    }
    .wrap { max-width: 1500px; margin: 0 auto; padding: 28px 18px 40px; }
    h1 { text-align: center; margin: 0 0 12px; font-size: 34px; }
    .sub { text-align: center; color: var(--muted); margin-bottom: 24px; }
    .grid { display: grid; grid-template-columns: 1.05fr 1.1fr 0.75fr; gap: 18px; align-items: start; }
    .card {
      background: linear-gradient(180deg, rgba(255,255,255,.03), rgba(255,255,255,.01));
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 18px;
      box-shadow: 0 10px 30px rgba(0,0,0,.24);
    }
    .card h2 { margin: 0 0 14px; font-size: 20px; }
    .field { margin-bottom: 14px; }
    label { display: block; margin-bottom: 8px; color: var(--muted); font-size: 14px; }
    input, textarea, select {
      width: 100%;
      border: 1px solid var(--border);
      background: var(--panel-2);
      color: var(--text);
      border-radius: 10px;
      padding: 12px 14px;
      font-size: 15px;
      outline: none;
    }
    textarea { min-height: 124px; resize: vertical; }
    .row { display: grid; grid-template-columns: 1fr 130px; gap: 12px; }
    .row3 { display: grid; grid-template-columns: 1fr 1fr 120px; gap: 12px; }
    .btns { display: flex; gap: 10px; margin-top: 10px; flex-wrap: wrap; }
    button {
      border: 0;
      border-radius: 10px;
      padding: 12px 18px;
      color: white;
      font-weight: 700;
      cursor: pointer;
    }
    .primary { background: var(--accent); }
    .secondary { background: #5b6070; }
    .blue { background: var(--accent-2); }
    .result {
      margin-top: 14px;
      background: var(--code);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 14px;
      min-height: 140px;
      overflow: auto;
      word-break: break-word;
    }
    .status { font-size: 14px; margin-top: 8px; color: var(--muted); }
    .status.error { color: var(--danger); }
    .status.ok { color: var(--ok); }
    .tabs { display: flex; gap: 10px; margin-bottom: 14px; }
    .tab {
      flex: 1;
      padding: 12px;
      text-align: center;
      border-radius: 10px;
      background: #2a2f3d;
      cursor: pointer;
      user-select: none;
    }
    .tab.active { background: var(--accent); }
    .panel { display: none; }
    .panel.active { display: block; }
    .hint { color: var(--muted); font-size: 13px; margin-top: 6px; }
    .small { font-size: 12px; color: var(--muted); }
    .result-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 14px;
      color: var(--text);
    }
    .result-table th,
    .result-table td {
      border-bottom: 1px solid rgba(255,255,255,.08);
      padding: 10px 8px;
      vertical-align: top;
      text-align: left;
    }
    .result-table th { color: var(--muted); font-weight: 700; }
    .result-table tr.top1 { background: var(--top); }
    .badge {
      display: inline-block;
      padding: 3px 8px;
      border-radius: 999px;
      background: rgba(77, 144, 254, .18);
      color: #9dc0ff;
      font-size: 12px;
      margin-left: 8px;
    }
    .score {
      font-variant-numeric: tabular-nums;
      white-space: nowrap;
    }
    .empty {
      color: var(--muted);
      text-align: center;
      padding: 28px 0;
    }
    .summary {
      padding: 12px 14px;
      border: 1px solid var(--border);
      border-radius: 12px;
      background: rgba(255,255,255,.02);
      margin-bottom: 12px;
      line-height: 1.7;
    }
    .answer-box {
      padding: 14px;
      border: 1px solid rgba(53, 194, 143, .35);
      border-radius: 12px;
      background: rgba(53, 194, 143, .08);
      margin-bottom: 12px;
      line-height: 1.7;
    }
    .answer-title {
      font-size: 13px;
      color: #9be6c7;
      margin-bottom: 6px;
      font-weight: 700;
    }
    .answer-text {
      font-size: 16px;
      color: var(--text);
      font-weight: 700;
      white-space: pre-wrap;
      word-break: break-word;
    .chart-box {
      margin-top: 12px;
      padding: 12px 14px;
      border: 1px solid var(--border);
      border-radius: 12px;
      background: rgba(255,255,255,.02);
    }
    .chart-title {
      font-size: 13px;
      color: var(--muted);
      margin-bottom: 10px;
      font-weight: 700;
    }
    .chart-row {
      display: grid;
      grid-template-columns: 70px 1fr 88px;
      gap: 10px;
      align-items: center;
      margin-bottom: 10px;
    }
    .chart-label {
      font-size: 13px;
      color: var(--text);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .bar-wrap {
      height: 10px;
      border-radius: 999px;
      background: rgba(255,255,255,.08);
      overflow: hidden;
      border: 1px solid rgba(255,255,255,.06);
    }
    .bar-fill {
      height: 100%;
      border-radius: 999px;
      background: linear-gradient(90deg, #4d90fe, #35c28f);
    }
    .bar-fill.top1 {
      background: linear-gradient(90deg, #ff6a00, #ffb14a);
    }
    .chart-score {
      text-align: right;
      font-variant-numeric: tabular-nums;
      color: #dfe7f3;
      font-size: 13px;
      white-space: nowrap;
    }
    }
    pre {
      margin: 0;
      white-space: pre-wrap;
      word-break: break-word;
      font-family: Consolas, Menlo, Monaco, monospace;
      font-size: 13px;
      color: #d9e0ea;
    }
    @media (max-width: 1200px) { .grid { grid-template-columns: 1fr; } }
  </style>
</head>
<body>
  <div class="wrap">
    <h1>Qwen3 功能可视化界面</h1>
    <div class="sub">本地 Embedding / Reranker / 简易 RAG 检索流程演示</div>

    <div class="tabs">
      <div class="tab active" data-tab="embed">Embedding</div>
      <div class="tab" data-tab="rerank">Reranker</div>
      <div class="tab" data-tab="rag">RAG 流程</div>
    </div>

    <div class="grid">
      <div class="card">
        <div id="embedPanel" class="panel active">
          <h2>文本向量化</h2>
          <div class="field">
            <label>模型</label>
            <select id="embedModel">
              <option value="Qwen3-Embedding-0.6B">Qwen3-Embedding-0.6B</option>
            </select>
          </div>
          <div class="field">
            <label>输入文本</label>
            <textarea id="embedText">你好，世界</textarea>
          </div>
          <div class="row">
            <div class="field">
              <label>嵌入维度</label>
              <input id="embedDimRange" type="range" min="1" max="2048" value="1024" oninput="embedDim.value=this.value">
            </div>
            <div class="field">
              <label>&nbsp;</label>
              <input id="embedDim" type="number" min="1" max="2048" value="1024" oninput="embedDimRange.value=this.value">
            </div>
          </div>
          <div class="btns">
            <button type="button" class="secondary" id="embedClear">清空</button>
            <button type="button" class="primary" id="embedSubmit">提交</button>
          </div>
          <div id="embedStatus" class="status"></div>
          <div id="embedResult" class="result"><pre>结果会显示在这里</pre></div>
        </div>

        <div id="rerankPanel" class="panel">
          <h2>文档排序</h2>
          <div class="field">
            <label>模型</label>
            <select id="rerankModel">
              <option value="Qwen3-Reranker-0.6B">Qwen3-Reranker-0.6B</option>
            </select>
          </div>
          <div class="field">
            <label>查询</label>
            <textarea id="queryText">中国的首都是哪里？</textarea>
          </div>
          <div class="field">
            <label>候选文档</label>
            <textarea id="docsText">中国的首都是北京
北京是中国的政治中心
上海是中国最大的城市之一
广州位于中国南方
东京是日本的首都</textarea>
            <div class="hint">每一行会被当作一个候选文档</div>
          </div>
          <div class="btns">
            <button type="button" class="secondary" id="rerankClear">清空</button>
            <button type="button" class="blue" id="rerankSubmit">提交</button>
          </div>
          <div id="rerankStatus" class="status"></div>
          <div id="rerankResult" class="result"><div class="empty">结果会显示在这里</div></div>
        </div>

        <div id="ragPanel" class="panel">
          <h2>简易 RAG 流程</h2>
          <div class="field">
            <label>查询</label>
            <textarea id="ragQuery">中国的首都是哪里？</textarea>
          </div>
          <div class="field">
            <label>知识库文档</label>
            <textarea id="ragDocs">中国的首都是北京
北京是中国的政治中心
上海是中国最大的城市之一
广州位于中国南方
东京是日本的首都
深圳是中国的一座现代化城市
南京曾经是中国的古都</textarea>
            <div class="hint">先用 Embedding 做初筛，再用 Reranker 重排</div>
          </div>
          <div class="row3">
            <div class="field">
              <label>Embedding 模型</label>
              <select id="ragEmbedModel">
                <option value="Qwen3-Embedding-0.6B">Qwen3-Embedding-0.6B</option>
              </select>
            </div>
            <div class="field">
              <label>Reranker 模型</label>
              <select id="ragRerankModel">
                <option value="Qwen3-Reranker-0.6B">Qwen3-Reranker-0.6B</option>
              </select>
            </div>
            <div class="field">
              <label>候选数</label>
              <input id="ragCandidateK" type="number" min="1" max="20" value="5">
            </div>
          </div>
          <div class="row">
            <div class="field">
              <label>嵌入维度</label>
              <input id="ragDim" type="number" min="1" max="2048" value="1024">
            </div>
            <div class="field">
              <label>输出条数</label>
              <input id="ragTopK" type="number" min="1" max="20" value="5">
            </div>
          </div>
          <div class="btns">
            <button type="button" class="secondary" id="ragClear">清空</button>
            <button type="button" class="primary" id="ragSubmit">运行 RAG</button>
          </div>
          <div id="ragStatus" class="status"></div>
          <div id="ragResult" class="result"><div class="empty">结果会显示在这里</div></div>
        </div>
      </div>

      <div class="card">
        <h2>服务状态</h2>
        <div class="result" id="serviceInfo">
          <pre>/embedding 与 /reranker 接口可用
/RAG 流程会先召回再重排</pre>
        </div>
        <div class="hint">如果页面刚打开，首次请求会加载本地模型，稍等片刻即可。</div>
        <div class="hint" id="debugInfo"></div>
      </div>
    </div>
  </div>

  <script>
    const tabs = document.querySelectorAll('.tab');
    const panels = {
      embed: document.getElementById('embedPanel'),
      rerank: document.getElementById('rerankPanel'),
      rag: document.getElementById('ragPanel')
    };

    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        Object.values(panels).forEach(p => p.classList.remove('active'));
        panels[tab.dataset.tab].classList.add('active');
      });
    });

    function debug(msg, kind='') {
      const el = document.getElementById('debugInfo');
      el.textContent = msg;
      el.className = 'hint' + (kind ? ' ' + kind : '');
    }

    window.addEventListener('error', (e) => debug('页面错误：' + e.message, 'error'));
    window.addEventListener('unhandledrejection', (e) => {
      const reason = e.reason && e.reason.message ? e.reason.message : String(e.reason);
      debug('页面错误：' + reason, 'error');
    });

    function setStatus(id, msg, kind='') {
      const el = document.getElementById(id);
      el.textContent = msg;
      el.className = 'status' + (kind ? ' ' + kind : '');
    }

    function escapeHtml(text) {
      return String(text)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
    }

    function formatScore(value) {
      const n = Number(value);
      if (Number.isNaN(n)) return '-';
      return n.toFixed(6);
    }

    function splitDocs(value) {
      return value.split('\\n').map(s => s.trim()).filter(Boolean);
    }

    function renderScoreChart(items, title='分数条形图') {
      if (!items || !items.length) {
        return '<div class="empty">暂无可视化数据</div>';
      }
      const scores = items.map(item => Number(item.score ?? item.rerank_score ?? item.similarity ?? item.retrieval_score ?? 0));
      const maxScore = Math.max(...scores);
      const minScore = Math.min(...scores);
      const span = (maxScore - minScore) || 1;
      const rows = items.map((item, idx) => {
        const score = scores[idx];
        const width = Math.max(4, ((score - minScore) / span) * 100);
        const label = escapeHtml(item.document ?? '');
        const rank = item.rank ?? (idx + 1);
        const topClass = idx === 0 ? 'top1' : '';
        return `
          <div class="chart-row ${topClass}">
            <div class="chart-label">${rank}. ${label}</div>
            <div class="bar-wrap"><div class="bar-fill ${topClass}" style="width:${width.toFixed(2)}%"></div></div>
            <div class="chart-score">${formatScore(score)}</div>
          </div>`;
      }).join('');
      return `
        <div class="chart-box">
          <div class="chart-title">${escapeHtml(title)}</div>
          ${rows}
        </div>`;
    }

    function renderRankingTable(items, title='结果', scoreLabel='分数') {
      if (!items || !items.length) {
        return '<div class="empty">暂无结果</div>';
      }
      const rows = items.map((item, idx) => {
        const rank = item.rank ?? (idx + 1);
        const topClass = idx === 0 ? 'top1' : '';
        const doc = escapeHtml(item.document ?? '');
        const score = formatScore(item.score ?? item.rerank_score ?? item.similarity ?? item.retrieval_score);
        const extra = item.retrieval_score !== undefined
          ? `<div class="small">召回分：${formatScore(item.retrieval_score)}</div>`
          : '';
        return `
          <tr class="${topClass}">
            <td>${rank}${idx === 0 ? '<span class="badge">TOP 1</span>' : ''}</td>
            <td>${doc}${extra}</td>
            <td class="score">${score}</td>
          </tr>`;
      }).join('');
      const chart = renderScoreChart(items, title + '（分数可视化）');
      return `
        <div class="summary">${escapeHtml(title)}：共 ${items.length} 条结果</div>
        <table class="result-table">
          <thead>
            <tr><th style="width: 90px;">排名</th><th>文档</th><th style="width: 140px;">${escapeHtml(scoreLabel)}</th></tr>
          </thead>
          <tbody>${rows}</tbody>
        </table>
        ${chart}`;
    }

    function renderRagResult(data) {
      const retrieval = renderRankingTable(data.retrieval_results, 'Embedding 初筛结果', '相似度');
      const reranked = renderRankingTable(data.reranked_results, 'Reranker 重排结果', '重排分数');
      const topDoc = data.reranked_results && data.reranked_results.length ? data.reranked_results[0].document : '无';
      const answer = escapeHtml(data.final_answer || '未生成答案');
      const confidence = data.answer_confidence !== undefined ? formatScore(data.answer_confidence) : '-';
      const summary = `
        <div class="summary">
          <div><b>查询：</b>${escapeHtml(data.query || '')}</div>
          <div><b>候选数：</b>${data.candidate_count ?? 0} &nbsp; <b>输出数：</b>${data.output_count ?? 0}</div>
          <div><b>最终 Top1：</b>${escapeHtml(topDoc)}</div>
        </div>`;
      const answerBox = `
        <div class="answer-box">
          <div class="answer-title">最终答案</div>
          <div class="answer-text">${answer}</div>
          <div class="small" style="margin-top:8px;">参考置信分：${confidence}</div>
        </div>`;
      return summary + answerBox + '<div style="display:grid;grid-template-columns:1fr;gap:14px;">' + retrieval + reranked + '</div>';
    }
    function clearEmbed() {
      document.getElementById('embedText').value = '';
      document.getElementById('embedResult').innerHTML = '<div class="empty">结果会显示在这里</div>';
      setStatus('embedStatus', '');
    }

    function clearRerank() {
      document.getElementById('queryText').value = '';
      document.getElementById('docsText').value = '';
      document.getElementById('rerankResult').innerHTML = '<div class="empty">结果会显示在这里</div>';
      setStatus('rerankStatus', '');
    }

    function clearRag() {
      document.getElementById('ragQuery').value = '';
      document.getElementById('ragDocs').value = '';
      document.getElementById('ragResult').innerHTML = '<div class="empty">结果会显示在这里</div>';
      setStatus('ragStatus', '');
    }

    async function runEmbedding() {
      const payload = {
        model_name: document.getElementById('embedModel').value,
        query_text: document.getElementById('embedText').value,
        dim: Number(document.getElementById('embedDim').value)
      };
      setStatus('embedStatus', '请求中...');
      try {
        const res = await fetch('/embedding', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || '请求失败');
        document.getElementById('embedResult').innerHTML = '<pre>' + escapeHtml(JSON.stringify(data.embedding, null, 2)) + '</pre>';
        setStatus('embedStatus', '成功', 'ok');
      } catch (e) {
        document.getElementById('embedResult').innerHTML = '<pre>' + escapeHtml(String(e)) + '</pre>';
        setStatus('embedStatus', '错误：' + e.message, 'error');
      }
    }

    async function runRerank() {
      const docs = splitDocs(document.getElementById('docsText').value);
      const payload = {
        model_name: document.getElementById('rerankModel').value,
        query: document.getElementById('queryText').value,
        documents: docs
      };
      setStatus('rerankStatus', '请求中...');
      try {
        const res = await fetch('/reranker', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || '请求失败');
        document.getElementById('rerankResult').innerHTML = renderRankingTable(data.ranked_results, 'Reranker 结果', '重排分数');
        setStatus('rerankStatus', '成功', 'ok');
      } catch (e) {
        document.getElementById('rerankResult').innerHTML = '<pre>' + escapeHtml(String(e)) + '</pre>';
        setStatus('rerankStatus', '错误：' + e.message, 'error');
      }
    }

    async function runRag() {
      const docs = splitDocs(document.getElementById('ragDocs').value);
      const payload = {
        embedding_model_name: document.getElementById('ragEmbedModel').value,
        rerank_model_name: document.getElementById('ragRerankModel').value,
        query: document.getElementById('ragQuery').value,
        documents: docs,
        dim: Number(document.getElementById('ragDim').value),
        candidate_k: Number(document.getElementById('ragCandidateK').value),
        output_k: Number(document.getElementById('ragTopK').value)
      };
      setStatus('ragStatus', '请求中...');
      try {
        const res = await fetch('/rag', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || '请求失败');
        document.getElementById('ragResult').innerHTML = renderRagResult(data);
        setStatus('ragStatus', '成功', 'ok');
      } catch (e) {
        document.getElementById('ragResult').innerHTML = '<pre>' + escapeHtml(String(e)) + '</pre>';
        setStatus('ragStatus', '错误：' + e.message, 'error');
      }
    }

    document.getElementById('embedClear').addEventListener('click', clearEmbed);
    document.getElementById('embedSubmit').addEventListener('click', runEmbedding);
    document.getElementById('rerankClear').addEventListener('click', clearRerank);
    document.getElementById('rerankSubmit').addEventListener('click', runRerank);
    document.getElementById('ragClear').addEventListener('click', clearRag);
    document.getElementById('ragSubmit').addEventListener('click', runRag);
  </script>
</body>
</html>
"""


def get_json_body():
    return request.get_json(silent=True) or {}


def normalize_documents(documents) -> List[str]:
    if documents is None:
        return []
    if isinstance(documents, str):
        source = documents.splitlines()
    else:
        source = documents
    cleaned = []
    for item in source:
        text = str(item).strip()
        if text:
            cleaned.append(text)
    return cleaned


def json_error(message: str, status: int = 400):
    return jsonify({"error": message}), status


def generate_answer(query: str, ranked_results: List[dict]):
    if not ranked_results:
        return {
            "final_answer": "未找到相关文档，暂时无法生成答案。",
            "answer_confidence": None,
            "answer_evidence": []
        }

    top_items = ranked_results[:3]
    top_doc = str(top_items[0].get('document', '')).strip()
    if not top_doc:
        top_doc = '未找到可用内容'

    if not top_doc.endswith(('。', '！', '？', '.', '!', '?')):
        top_doc = top_doc + '。'

    answer = f"根据检索结果，建议答案是：{top_doc}"
    evidence = []
    for item in top_items:
        evidence.append({
            'rank': item.get('rank'),
            'document': item.get('document'),
            'score': item.get('score'),
        })

    return {
        'final_answer': answer,
        'answer_confidence': float(top_items[0].get('score', 0.0) or 0.0),
        'answer_evidence': evidence,
    }
def rerank_documents(model_name: str, query: str, documents: List[str], metadata: List[dict] | None = None):
    model = qwen3_reranker.load_model(model_name)
    pairs = [(query, doc) for doc in documents]
    scores = model.compute_scores(pairs, "Given the user query, retrieval the relevant passages")
    ranked = []
    for idx, (doc, score) in enumerate(zip(documents, scores)):
        item = {
            "index": idx,
            "document": doc,
            "score": float(score),
        }
        if metadata and idx < len(metadata):
            source = metadata[idx]
            item["retrieval_score"] = source.get("score")
            item["retrieval_rank"] = source.get("rank")
            item["source_index"] = source.get("index")
        ranked.append(item)
    ranked.sort(key=lambda item: item["score"], reverse=True)
    for rank, item in enumerate(ranked, start=1):
        item["rank"] = rank
        item["is_top"] = rank == 1
    return ranked


def retrieve_by_embedding(model_name: str, query: str, documents: List[str], dim: int = 1024, candidate_k: int = 5):
    model = qwen3_embedding.load_model(model_name)
    query_vec = model.encode(query, is_query=True, dim=dim)[0]
    doc_vecs = model.encode(documents, is_query=False, dim=dim)
    scores = torch.mv(doc_vecs, query_vec)
    top_k = min(max(int(candidate_k), 1), len(documents))
    values, indices = torch.topk(scores, k=top_k)
    results = []
    for rank, (idx, score) in enumerate(zip(indices.tolist(), values.tolist()), start=1):
        results.append({
            "index": idx,
            "document": documents[idx],
            "score": float(score),
            "rank": rank,
        })
    return results


@app.route('/')
def home():
    return render_template_string(PAGE)


@app.route('/embedding', methods=['POST'])
def get_embedding():
    data = get_json_body()
    model_name = data.get('model_name')
    query_text = data.get('query_text')
    dim = data.get('dim')
    if not model_name or query_text is None or dim is None:
        return json_error('参数缺失')

    try:
        dim = int(dim)
        embedding = qwen3_embedding.encode_query(model_name, query_text, dim)
        return jsonify({'embedding': embedding})
    except Exception as e:
        return json_error(str(e), 500)


@app.route('/reranker', methods=['POST'])
def rerank():
    data = get_json_body()
    model_name = data.get('model_name')
    query = data.get('query')
    documents = normalize_documents(data.get('documents'))

    if not model_name or query is None or not documents:
        return json_error('参数缺失')

    try:
        ranked_results = rerank_documents(model_name, query, documents)
        return jsonify({'ranked_results': ranked_results})
    except Exception as e:
        return json_error(str(e), 500)


@app.route('/rag', methods=['POST'])
def rag():
    data = get_json_body()
    embedding_model_name = data.get('embedding_model_name')
    rerank_model_name = data.get('rerank_model_name')
    query = data.get('query')
    documents = normalize_documents(data.get('documents'))
    dim = data.get('dim', 1024)
    candidate_k = data.get('candidate_k', 5)
    output_k = data.get('output_k', candidate_k)

    if not embedding_model_name or not rerank_model_name or query is None or not documents:
        return json_error('参数缺失')

    try:
        dim = int(dim)
        candidate_k = int(candidate_k)
        output_k = int(output_k)
        candidate_results = retrieve_by_embedding(embedding_model_name, query, documents, dim=dim, candidate_k=candidate_k)
        candidate_docs = [item['document'] for item in candidate_results]
        reranked_results = rerank_documents(rerank_model_name, query, candidate_docs, metadata=candidate_results)
        answer_pack = generate_answer(query, reranked_results)

        final_results = []
        for item in reranked_results[: max(1, output_k)]:
            final_results.append({
                'index': item.get('source_index', item['index']),
                'document': item['document'],
                'score': item['score'],
                'rank': item['rank'],
                'is_top': item['is_top'],
                'retrieval_score': item.get('retrieval_score', None),
                'retrieval_rank': item.get('retrieval_rank', None),
            })

        return jsonify({
            'query': query,
            'candidate_count': len(candidate_results),
            'output_count': len(final_results),
            'retrieval_results': candidate_results,
            'reranked_results': final_results,
            'final_answer': answer_pack['final_answer'],
            'answer_confidence': answer_pack['answer_confidence'],
            'answer_evidence': answer_pack['answer_evidence'],
        })
    except Exception as e:
        return json_error(str(e), 500)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

