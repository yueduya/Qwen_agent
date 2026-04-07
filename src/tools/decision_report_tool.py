import json
import re
from qwen_agent.tools.base import BaseTool, register_tool
from src.llm_utils import call_llm
from src.prompt_templates import DECISION_PROMPT, REPORT_PROMPT

@register_tool('decision_report')
class DecisionReportTool(BaseTool):
    """
    选择最优方案并生成研究报告
    """
    description = '根据候选方案和市场模型，选择最优方案并生成研究报告，输入为方案列表和市场模型JSON字符串'
    parameters = [
        {'name': 'reasoning_plans', 'type': 'string', 'description': '方案列表JSON字符串', 'required': True},
        {'name': 'world_model', 'type': 'string', 'description': '市场模型JSON字符串', 'required': True},
        {'name': 'perception_data', 'type': 'string', 'description': '感知数据JSON字符串', 'required': True},
        {'name': 'research_topic', 'type': 'string', 'description': '研究主题', 'required': True},
        {'name': 'industry_focus', 'type': 'string', 'description': '行业焦点', 'required': True},
        {'name': 'time_horizon', 'type': 'string', 'description': '时间范围', 'required': True},
    ]
    def call(self, params: str, **kwargs) -> str:
        args = json.loads(params)
        
        # 第一步：先生成决策
        decision_prompt = DECISION_PROMPT.format(
            research_topic=args['research_topic'],
            industry_focus=args['industry_focus'],
            time_horizon=args['time_horizon'],
            world_model=args['world_model'],
            reasoning_plans=args['reasoning_plans']
        )
        
        try:
            decision_result = call_llm(decision_prompt)
            # 尝试解析JSON
            try:
                decision_json = json.loads(decision_result)
            except json.JSONDecodeError:
                # 尝试提取JSON部分
                import re
                json_content = re.search(r'({.*})', decision_result, re.DOTALL)
                if json_content:
                    decision_json = json.loads(json_content.group(1))
                else:
                    raise Exception("无法从LLM响应中提取有效决策JSON")
            
            # 第二步：生成完整报告
            report_prompt = REPORT_PROMPT.format(
                research_topic=args['research_topic'],
                industry_focus=args['industry_focus'],
                time_horizon=args['time_horizon'],
                perception_data=args['perception_data'],
                world_model=args['world_model'],
                selected_plan=json.dumps(decision_json, ensure_ascii=False)
            )
            
            report_result = call_llm(report_prompt)
            
            # 返回包含决策和报告的结果
            final_result = {
                "decision": decision_json,
                "report": report_result
            }
            
            return json.dumps(final_result, ensure_ascii=False, indent=2)
            
        except Exception as e:
            return json.dumps({
                "error": f"决策与报告生成失败: {str(e)}",
                "decision": {
                    "selected_plan_id": "ERROR",
                    "investment_thesis": "处理失败",
                    "supporting_evidence": ["处理失败"],
                    "risk_assessment": "处理失败",
                    "recommendation": "处理失败",
                    "timeframe": "处理失败"
                },
                "report": f"报告生成失败，原因: {str(e)}"
            }, ensure_ascii=False, indent=2)
