import os
import dashscope

# 配置 DashScope
DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY')
dashscope.api_key = DASHSCOPE_API_KEY

# LLM配置
LLM_CONFIG = {
    'model': 'qwen-turbo-2025-04-28',
    'model_server': 'dashscope',
    'timeout': 60,
    'retry_count': 3,
    'generate_cfg': {
        'top_p': 0.8,
        'temperature': 0.7,
        'max_tokens': 2000,
    }
}

# 系统提示
system_prompt = """你是深思熟虑型智能投研助手，能够分阶段完成市场感知、建模分析、推理方案生成、决策与报告。请根据用户输入的研究主题、行业焦点和时间范围，主动选择合适的工具，输出专业、系统、结构化的投研结论。"""
