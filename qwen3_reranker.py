import logging

import torch

from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModelForSequenceClassification, AutoModel, is_torch_npu_available
from transformers.utils import is_flash_attn_2_available

import gradio as gr

logger = logging.getLogger(__name__)


class Qwen3Reranker:
    def __init__(
        self,
        model_name_or_path: str,
        max_length: int = 2048,
        instruction=None,
        use_cuda: bool = True
    ) -> None:
        self.device = torch.device("cuda" if use_cuda and torch.cuda.is_available() else "cpu")
        self.max_length=max_length
        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True, padding_side='left')
        dtype = torch.float16 if self.device.type == "cuda" else torch.float32
        model_kwargs = dict(trust_remote_code=True, torch_dtype=dtype)
        if self.device.type == "cuda" and is_flash_attn_2_available():
            model_kwargs["attn_implementation"] = "flash_attention_2"
        self.lm = AutoModelForCausalLM.from_pretrained(model_name_or_path, **model_kwargs).to(self.device).eval()
        self.token_false_id = self.tokenizer.convert_tokens_to_ids("no")
        self.token_true_id = self.tokenizer.convert_tokens_to_ids("yes")

        self.prefix = "<|im_start|>system\nJudge whether the Document meets the requirements based on the Query and the Instruct provided. Note that the answer can only be \"yes\" or \"no\".<|im_end|>\n<|im_start|>user\n"
        self.suffix = "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"

        self.prefix_tokens = self.tokenizer.encode(self.prefix, add_special_tokens=False)
        self.suffix_tokens = self.tokenizer.encode(self.suffix, add_special_tokens=False)
        self.instruction = instruction
        if self.instruction is None:
            self.instruction = "Retrieval document that can answer user's query"

    def format_instruction(self, instruction, query, doc):
        if instruction is None:
            instruction = self.instruction
        output = "<Instruct>: {instruction}\n<Query>: {query}\n<Document>: {doc}".format(instruction=instruction,query=query, doc=doc)
        return output

    def process_inputs(self, pairs):
        out = self.tokenizer(
            pairs, padding=False, truncation='longest_first',
            return_attention_mask=False, max_length=self.max_length - len(self.prefix_tokens) - len(self.suffix_tokens)
        )
        for i, ele in enumerate(out['input_ids']):
            out['input_ids'][i] = self.prefix_tokens + ele + self.suffix_tokens
        out = self.tokenizer.pad(out, padding=True, return_tensors="pt", max_length=self.max_length)
        for key in out:
            out[key] = out[key].to(self.device)
        return out

    @torch.no_grad()
    def compute_logits(self, inputs, **kwargs):

        batch_scores = self.lm(**inputs).logits[:, -1, :]
        true_vector = batch_scores[:, self.token_true_id]
        false_vector = batch_scores[:, self.token_false_id]
        batch_scores = torch.stack([false_vector, true_vector], dim=1)
        batch_scores = torch.nn.functional.log_softmax(batch_scores, dim=1)
        scores = batch_scores[:, 1].exp().tolist()
        return scores

    def compute_scores(
        self,
        pairs,
        instruction=None,
        **kwargs
    ):
        pairs = [self.format_instruction(instruction, query, doc) for query, doc in pairs]
        inputs = self.process_inputs(pairs)
        scores = self.compute_logits(inputs)
        return scores

# 将模型加载为全局变量
model_0_6B = None
model_4B = None
model_8B = None


def load_model(model_name):
    global model_0_6B, model_4B, model_8B
    if model_name == "Qwen3-Reranker-0.6B" and model_0_6B is None:
        model_0_6B = Qwen3Reranker(model_name_or_path="models/Qwen3-Reranker-0.6B")
    elif model_name == "Qwen3-Reranker-4B" and model_4B is None:
        model_4B = Qwen3Reranker(model_name_or_path="models/Qwen3-Reranker-4B")
    elif model_name == "Qwen3-Reranker-8B" and model_8B is None:
        model_8B = Qwen3Reranker(model_name_or_path="models/Qwen3-Reranker-8B")

    return {
        "Qwen3-Reranker-0.6B": model_0_6B,
        "Qwen3-Reranker-4B": model_4B,
        "Qwen3-Reranker-8B": model_8B,
    }[model_name]


def rerank_interface(model_name, query, docs_str, documents=None):
    api_flag = True

    model = load_model(model_name)

    # 将输入的文档字符串转换为列表
    if documents is None:
        api_flag = False
        documents = [doc.strip() for doc in docs_str.strip().split('\n')]

    # 构建 pairs 输入
    pairs = [(query, doc) for doc in documents]

    # 计算得分
    scores = model.compute_scores(pairs, "Given the user query, retrieval the relevant passages")

    # 排序结果
    ranked_results = sorted(
        [{"document": doc, "score": score} for (query, doc), score in zip(pairs, scores)],
        key=lambda x: x["score"],
        reverse=True
    )

    if not api_flag:
        # 返回格式化结果
        return "\n\n".join([f"文档: {item['document']}\n得分: {item['score']}" for item in ranked_results])
    else:
        return ranked_results


iface = gr.Interface(
    fn=rerank_interface,
    inputs=[
        gr.Dropdown(
            choices=["Qwen3-Reranker-0.6B", "Qwen3-Reranker-4B", "Qwen3-Reranker-8B"],
            value="Qwen3-Reranker-0.6B",
            label="选择模型"
        ),
        gr.Textbox(label="查询内容", value="中国的首都是哪里"),
        gr.Textbox(label="文档内容（每行一个文档）", value="中国的首都是北京。\n重力是一种将两个物体相互吸引的力。它赋予物理物体重量，并且是行星围绕太阳运动的原因。")

    ],
    outputs=gr.Textbox(label="Ranked Results"),
    title="Qwen3 Reranker 演示页面（FutureAI实验室）",
    description=""
)


if __name__ == '__main__':
    # 启动 Gradio 应用
    iface.launch()