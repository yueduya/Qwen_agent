import json
import re
from qwen_agent.tools.base import BaseTool, register_tool
from src.llm_utils import call_llm
from src.prompt_templates import PERCEPTION_PROMPT

@register_tool('perception')
class PerceptionTool(BaseTool):
    """
    收集并整理市场数据和信息
    """
    description = '收集并整理市场数据和信息，输入为研究主题、行业焦点、时间范围'
    parameters = [
        {'name': 'research_topic', 'type': 'string', 'description': '研究主题', 'required': True},
        {'name': 'industry_focus', 'type': 'string', 'description': '行业焦点', 'required': True},
        {'name': 'time_horizon', 'type': 'string', 'description': '时间范围', 'required': True},
    ]
    def call(self, params: str, **kwargs) -> str:
        args = json.loads(params)
        
        # 准备提示
        prompt = PERCEPTION_PROMPT.format(
            research_topic=args['research_topic'],
            industry_focus=args['industry_focus'],
            time_horizon=args['time_horizon']
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
                # 尝试提取花括号中的内容
                json_content = re.search(r'({.*})', result, re.DOTALL)
                if json_content:
                    json_result = json.loads(json_content.group(1))
                    return json.dumps(json_result, ensure_ascii=False, indent=2)
                else:
                    raise Exception("无法从LLM响应中提取有效JSON")
            except Exception as e:
                return json.dumps({
                    "market_overview": "LLM返回格式错误，无法解析市场概况",
                    "key_indicators": {"错误": "数据解析失败"},
                    "recent_news": ["LLM返回格式错误，无法解析新闻"],
                    "industry_trends": {"错误": "数据解析失败"}
                }, ensure_ascii=False, indent=2)
        except Exception as e:
            return json.dumps({
                "error": f"调用LLM时发生错误: {str(e)}",
                "market_overview": "调用失败，无法获取市场概况",
                "key_indicators": {"错误": "调用失败"},
                "recent_news": ["调用失败，无法获取新闻"],
                "industry_trends": {"错误": "调用失败"}
            }, ensure_ascii=False, indent=2)
