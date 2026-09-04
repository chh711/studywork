from typing import List, Union
import torch
import torch.nn.functional as F

from torch import Tensor
from transformers import AutoTokenizer, AutoModel
from transformers.utils import is_flash_attn_2_available

import gradio as gr

class Qwen3Embedding():
    def __init__(self, model_name_or_path, instruction=None, use_fp16: bool = True, use_cuda: bool = True,
                 max_length=8192):
        if instruction is None:
            instruction = 'Given a web search query, retrieve relevant passages that answer the query'
        self.instruction = instruction
        self.device = torch.device("cuda" if use_cuda and torch.cuda.is_available() else "cpu")
        dtype = torch.float16 if self.device.type == "cuda" else torch.float32
        model_kwargs = dict(trust_remote_code=True, torch_dtype=dtype)
        if self.device.type == "cuda" and is_flash_attn_2_available():
            model_kwargs["attn_implementation"] = "flash_attention_2"
        self.model = AutoModel.from_pretrained(model_name_or_path, **model_kwargs).to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True, padding_side='left')
        self.max_length = max_length

    def last_token_pool(self, last_hidden_states: Tensor,
                        attention_mask: Tensor) -> Tensor:
        left_padding = (attention_mask[:, -1].sum() == attention_mask.shape[0])
        if left_padding:
            return last_hidden_states[:, -1]
        else:
            sequence_lengths = attention_mask.sum(dim=1) - 1
            batch_size = last_hidden_states.shape[0]
        return last_hidden_states[torch.arange(batch_size, device=last_hidden_states.device), sequence_lengths]

    def get_detailed_instruct(self, task_description: str, query: str) -> str:
        if task_description is None:
            task_description = self.instruction
        return f'Instruct: {task_description}\nQuery:{query}'

    def encode(self, sentences: Union[List[str], str], is_query: bool = False, instruction=None, dim: int = -1):
        if isinstance(sentences, str):
            sentences = [sentences]
        if is_query:
            sentences = [self.get_detailed_instruct(instruction, sent) for sent in sentences]
        inputs = self.tokenizer(sentences, padding=True, truncation=True, max_length=self.max_length, return_tensors='pt')
        inputs = inputs.to(self.device)
        with torch.no_grad():
            model_outputs = self.model(**inputs)
            output = self.last_token_pool(model_outputs.last_hidden_state, inputs['attention_mask'])
            if dim != -1:
                output = output[:, :dim]
            output = F.normalize(output, p=2, dim=1)
        return output


# 将模型加载为全局变量
model_0_6B = None
model_4B = None
model_8B = None


def load_model(model_name):
    global model_0_6B, model_4B, model_8B
    if model_name == "Qwen3-Embedding-0.6B" and model_0_6B is None:
        model_0_6B = Qwen3Embedding("models/Qwen3-Embedding-0.6B")
    elif model_name == "Qwen3-Embedding-4B" and model_4B is None:
        model_4B = Qwen3Embedding("models/Qwen3-Embedding-4B")
    elif model_name == "Qwen3-Embedding-8B" and model_8B is None:
        model_8B = Qwen3Embedding("models/Qwen3-Embedding-8B")

    return {
        "Qwen3-Embedding-0.6B": model_0_6B,
        "Qwen3-Embedding-4B": model_4B,
        "Qwen3-Embedding-8B": model_8B,
    }[model_name]


def encode_query(model_name, query_text, dim=1024):
    """
    编码输入的查询文本。

    参数:
        query_text (str): 用户输入的查询文本。
        model_name (str): 选择的模型名称。
        dim (int): 输出向量的维度。

    返回:
        numpy.ndarray: 归一化后的嵌入向量（JSON 可序列化）。
    """
    model = load_model(model_name)
    output = model.encode(query_text, is_query=True, dim=dim)
    return output.cpu().numpy().tolist()  # 转换为 JSON 可序列化的列表格式

# 创建 Gradio 接口
iface = gr.Interface(
    fn=encode_query,
    inputs=[
        gr.Dropdown(choices=["Qwen3-Embedding-0.6B", "Qwen3-Embedding-4B", "Qwen3-Embedding-8B"], value="Qwen3-Embedding-0.6B", label="选择模型"),
        gr.Textbox(lines=2, placeholder="在这里输入文本", label="输入文本"),  # 输入框
        gr.Slider(minimum=1, maximum=2048, step=1, value=1024, label="嵌入维度")  # 维度选择滑块
    ],
    outputs=gr.JSON(label="Embedding 结果"),  # 输出格式为 JSON
    title="Qwen3 Embedding 演示页面（FutureAI实验室）",  # 页面标题
    description=""  # 描述信息
)

# 启动 Gradio 服务
if __name__ == "__main__":
    iface.launch()