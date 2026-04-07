import json
import re
from qwen_agent.tools.base import BaseTool, register_tool
from src.llm_utils import call_llm
from src.prompt_templates import MODELING_PROMPT

@register_tool('modeling')
class ModelingTool(BaseTool):
    """
    构建市场内部模型，分析风险与机会
    """
    description = '根据市场数据构建内部模型，输入为市场数据JSON字符串'
    parameters = [
        {'name': 'perception_data', 'type': 'string', 'description': '市场数据JSON字符串', 'required': True},
        {'name': 'research_topic', 'type': 'string', 'description': '研究主题', 'required': True},
        {'name': 'industry_focus', 'type': 'string', 'description': '行业焦点', 'required': True},
        {'name': 'time_horizon', 'type': 'string', 'description': '时间范围', 'required': True},
    ]
    def call(self, params: str, **kwargs) -> str:
        args = json.loads(params)
        
        # 准备提示
        prompt = MODELING_PROMPT.format(
            research_topic=args['research_topic'],
            industry_focus=args['industry_focus'],
            time_horizon=args['time_horizon'],
            perception_data=args['perception_data']
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
                json_content = re.search(r'({.*})', result, re.DOTALL)
                if json_content:
                    json_result = json.loads(json_content.group(1))
                    return json.dumps(json_result, ensure_ascii=False, indent=2)
                else:
                    raise Exception("无法从LLM响应中提取有效JSON")
            except Exception as e:
                return json.dumps({
                    "market_state": "LLM返回格式错误，无法解析市场状态",
                    "economic_cycle": "数据解析失败",
                    "risk_factors": ["数据解析失败"],
                    "opportunity_areas": ["数据解析失败"],
                    "market_sentiment": "数据解析失败"
                }, ensure_ascii=False, indent=2)
        except Exception as e:
            return json.dumps({
                "error": f"调用LLM时发生错误: {str(e)}",
                "market_state": "调用失败，无法获取市场状态",
                "economic_cycle": "调用失败",
                "risk_factors": ["调用失败"],
                "opportunity_areas": ["调用失败"],
                "market_sentiment": "调用失败"
            }, ensure_ascii=False, indent=2)
