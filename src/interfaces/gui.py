from src.agent import init_agent_service
from qwen_agent.gui import WebUI

def app_gui():
    """Web 图形界面模式"""
    try:
        print("正在启动 Web 界面...")
        bot = init_agent_service()
        chatbot_config = {
            'prompt.suggestions': [
                '新能源,电力,中期',
                '高端制造,机械,长期',
                '数字经济,互联网,短期',
            ],
            'input.placeholder': '请输入研究主题、行业、周期（如：新能源,电力,中期）'
        }
        print("Web 界面准备就绪，正在启动服务...")
        WebUI(
            bot,
            chatbot_config=chatbot_config
        ).run()
    except Exception as e:
        print(f"启动 Web 界面失败: {str(e)}")
        print("请检查网络连接和 API Key 配置")
