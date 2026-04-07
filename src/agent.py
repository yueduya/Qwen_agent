from qwen_agent.agents import Assistant
from src.config import LLM_CONFIG, system_prompt

# 导入工具以确保它们被注册
from src.tools.perception_tool import PerceptionTool
from src.tools.modeling_tool import ModelingTool
from src.tools.reasoning_tool import ReasoningTool
from src.tools.decision_report_tool import DecisionReportTool

def init_agent_service():
    """初始化深思熟虑型投研助手"""
    bot = Assistant(
        llm=LLM_CONFIG,
        name='深思熟虑型投研助手',
        description='多阶段投研流程与结构化报告生成',
        system_message=system_prompt,
        function_list=['perception', 'modeling', 'reasoning', 'decision_report'],
    )
    print("助手初始化成功！")
    return bot
