"""
ReAct 框架下的 Agent
"""
from langchain.agents import create_agent

from src.model.factory import chat_model
from src.utils.prompt_handler import system_prompts
from .agent_module.agent_tools import rag_invoke, get_location, get_weather, get_current_month, get_user_id, \
    get_external_data, switch_report_model
from .agent_module.middleware import monitor_tool_call, switch_report_prompt, log_before_model


class ReactAgent:
    def __init__(self):
        self.agent = create_agent(
            model=chat_model,
            tools=[rag_invoke, get_location, get_weather, get_current_month, get_user_id, get_external_data,
                   switch_report_model],
            system_prompt=system_prompts,
            middleware=[monitor_tool_call, switch_report_prompt, log_before_model]
        )

    def stream(self, query: str):
        messages = [{"role": "user", "content": query}]
        input_ = {"messages": messages}

        is_first_out = True
        # 初始化自定义变量
        for chunk in self.agent.stream(input=input_, stream_mode='values', context={'switch_report_model': False}):
            if is_first_out:
                is_first_out = False
                continue

            latest_msg = chunk['messages'][-1]
            if latest_msg.content:
                yield latest_msg.content.strip() + '\n\n'


if __name__ == "__main__":
    react_agent = ReactAgent()

    input_ = "扫地机器人在我所在的地区气温下，有效的保养方式是什么？"
    for chunk in react_agent.stream(input_):
        print(chunk, end='')
