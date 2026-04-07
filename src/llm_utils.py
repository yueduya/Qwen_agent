from dashscope import Generation

def call_llm(prompt: str) -> str:
    """调用DashScope的LLM进行推理"""
    response = Generation.call(
        model='qwen-turbo-2025-04-28',
        prompt=prompt,
        result_format='message',
        temperature=0.7,
        top_p=0.8,
        max_tokens=2000,
    )
    
    if response.status_code == 200:
        return response.output.choices[0].message.content
    else:
        raise Exception(f"调用LLM失败: {response.message}")
