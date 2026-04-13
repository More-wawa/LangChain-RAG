"""
Agent 工具
"""
import os.path
import random

from langchain_core.tools import tool

from src.utils.path_handler import get_abs_path
from src.utils.logger_handler import logger
from src.utils.config_handler import agent_conf
from src.rag.rag_service import RagService

rag_service = RagService()
external_dict = {}


@tool
def rag_invoke(query: str) -> str:
    """
    从向量数据库中检索资料并总结，得到最终总结后结果，以字符串返回
    :param query: query
    :return: summarized result
    """
    return rag_service.invoke(query)


@tool
def get_location() -> str:
    """
    获取用户当前所在城市名称，以字符串返回
    :return: city name
    """
    return random.choice(agent_conf['cities'])


@tool
def get_weather(city: str) -> str:
    """
    获取指定城市的天气信息，以字符串返回
    :param city: city name
    :return: the weather condition of the city
    """
    return f"{city}： 今日多云转晴，微风，无雨"


@tool
def get_current_month() -> str:
    """
    获取当前月份，以字符串返回
    :return: month
    """
    return random.choice(agent_conf['months'])


@tool
def get_user_id() -> str:
    """
    获取当前用户 ID, 以字符串返回
    :return: user ID
    """
    return random.choice(agent_conf['user_ids'])


# 初始化 external 知识库，保存进 dict 中
def _init_external_dict():
    external_data_abs_path = get_abs_path(agent_conf['external_data_path'])

    # ensure file is exist
    if not os.path.exists(external_data_abs_path):
        logger.warning(f"{external_data_abs_path} is not exist")
        raise FileNotFoundError(f"{external_data_abs_path} is not exist")

    # read external data, and initialize external_dict
    with open(external_data_abs_path, 'r', encoding='utf-8') as fr:
        # 跳过表头
        for line in fr.readlines()[1:]:
            line_data: list[str] = line.strip().split(',')

            user_id: str = line_data[0].replace('"', '')
            feature: str = line_data[1].replace('"', '')
            efficiency: str = line_data[2].replace('"', '')
            consumables: str = line_data[3].replace('"', '')
            comparisons: str = line_data[4].replace('"', '')
            month: str = line_data[5].replace('"', '')

            if user_id not in external_dict:
                external_dict[user_id] = {}

            external_dict[user_id][month] = {
                "特征": feature,
                "效率": efficiency,
                "耗材": consumables,
                "对比": comparisons,
            }


@tool
def get_external_data(user_id: str, month: str) -> str:
    """
    根据 user_id, month 信息，查询知识库并返回信息，以字符串返回
    :param user_id: user ID
    :param month: current month
    :return: result of query
    """
    # 初始化 external_dict
    if not external_dict:
        _init_external_dict()

    try:
        return external_dict[user_id][month]
    except KeyError:
        logger.warning(f"Failed to search user ID: {user_id}, month: {month}")
        return ""


@tool
def switch_report_model():
    """无入参，无返回值，调用会 switch_report_model 会触发中间件切换为 report 模式，用于最终生成一份报告给用户"""
    return "switch_report_model"
