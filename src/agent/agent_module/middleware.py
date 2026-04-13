"""
Agent 中间件
"""
import logging
from typing import Callable

from langchain.agents import AgentState
from langchain.agents.middleware import wrap_tool_call, dynamic_prompt, ModelRequest, before_model
from langchain_core.messages import ToolMessage
from langgraph.prebuilt.tool_node import ToolCallRequest
from langgraph.types import Command
from langgraph.runtime import Runtime

from src.utils.logger_handler import logger
from src.utils.prompt_handler import report_prompts, system_prompts


@wrap_tool_call
def monitor_tool_call(request: ToolCallRequest,
                      handler: Callable[[ToolCallRequest], ToolMessage | Command]) -> None | ToolMessage | Command:
    """
    监控工具调用
    :param request: 请求的数据
    :param handler: 执行函数
    """
    logger.info(f"call tool: {request.tool_call['name']}, args: {request.tool_call['args']}")

    try:
        res = handler(request)

        # 如果当前执行 switch_report_model 则切换为 report 模式
        request.runtime.context['switch_report_model'] = request.tool_call['name'] == 'switch_report_model'

        return res
    except Exception as e:
        logger.error(
            f"Failed to call tool: {request.tool_call['name']}, args: {request.tool_call['args']}, error: {e}")
        return None


@dynamic_prompt
def switch_report_prompt(request: ModelRequest):
    """
    切换为 report prompt
    :param request: 请求的数据
    """
    _switch_report_model = request.runtime.context['switch_report_model']
    logger.info(f"switch_report_model: {_switch_report_model}")

    return report_prompts if _switch_report_model else system_prompts


@before_model
def log_before_model(state: AgentState, runtime: Runtime):
    """
    Agent 执行过程中输出日志
    :param state: 执行过程中状态信息
    :param runtime: 执行过程中上下文信息
    """
    logger.info(f"state_len: {len(state['messages'])}")
