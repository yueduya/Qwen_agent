import json
import re
from qwen_agent.tools.base import BaseTool, register_tool
from src.llm_utils import call_llm
from src.prompt_templates import REASONING_PROMPT

@register_tool('reasoning')
class ReasoningTool(BaseTool):
    """
    生成多个投资分析方案
    """
    description = '根据市场模型生成3个投资分析方案，输入为市场模型JSON字符串'
    parameters = [
        {'name': 'world_model', 'type': 'string', 'description': '市场模型JSON字符串', 'required': True},
        {'name': 'research_topic', 'type': 'string', 'description': '研究主题', 'required': True},
        {'name': 'industry_focus', 'type': 'string', 'description': '行业焦点', 'required': True},
        {'name': 'time_horizon', 'type': 'string', 'description': '时间范围', 'required': True},
    ]
    def call(self, params: str, **kwargs) -> str:
        args = json.loads(params)
        
        # 准备提示
        prompt = REASONING_PROMPT.format(
            research_topic=args['research_topic'],
            industry_focus=args['industry_focus'],
            time_horizon=args['time_horizon'],
            world_model=args['world_model']
        )
        
        # 调用LLM
        try:
            result = call_llm(prompt)
            # 验证结果是否为有效的JSON格式
            json_result = json.loads(result)
            return json.dumps(json_result, ensure_ascii=False, indent=2)
        except json.JSONDecodeError:
            # 如果返回结果不是有效JSON格式，尝试提取JSON部分
            try:
                import re
                json_content = re.search(r'(\[.*\])', result, re.DOTALL)
                if json_content:
                    json_result = json.loads(json_content.group(1))
                    return json.dumps(json_result, ensure_ascii=False, indent=2)
                else:
                    raise Exception("无法从LLM响应中提取有效JSON")
            except Exception as e:
                return json.dumps([
                    {
                        "plan_id": "ERROR",
                        "hypothesis": "LLM返回格式错误，无法解析",
                        "analysis_approach": "数据解析失败",
                        "expected_outcome": "数据解析失败",
                        "confidence_level": 0,
                        "pros": ["数据解析失败"],
                        "cons": ["数据解析失败"]
                    }
                ], ensure_ascii=False, indent=2)
        except Exception as e:
            return json.dumps([
                {
                    "plan_id": "ERROR",
                    "hypothesis": f"调用LLM时发生错误: {str(e)}",
                    "analysis_approach": "调用失败",
                    "expected_outcome": "调用失败",
                    "confidence_level": 0,
                    "pros": ["调用失败"],
                    "cons": ["调用失败"]
                }
            ], ensure_ascii=False, indent=2)
