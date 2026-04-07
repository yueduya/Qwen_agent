from src.agent import init_agent_service

def app_tui():
    """终端交互模式"""
    bot = init_agent_service()
    messages = []
    print("欢迎使用深思熟虑型投研助手，输入'退出'结束对话。\n")
    while True:
        try:
            query = input('请输入研究主题、行业、周期（如：新能源,电力,中期）：')
            if query.strip() in ['退出', 'exit', 'quit']:
                print('感谢使用，再见！')
                break
            # 简单分割
            parts = [x.strip() for x in query.split(',')]
            if len(parts) != 3:
                print('请输入格式：主题,行业,周期')
                continue
            messages.append({'role': 'user', 'content': f'研究主题:{parts[0]} 行业:{parts[1]} 周期:{parts[2]}'})
            print("正在处理...")
            response = []
            for resp in bot.run(messages):
                print('助手:', resp)
                response.append({'role': 'assistant', 'content': resp})
            messages.extend(response)
        except Exception as e:
            print(f"发生错误: {str(e)}")
            print("请重试或输入新的问题")
