"""
日志管理文件
"""
from .path_handler import get_abs_path
import logging
from logging.handlers import TimedRotatingFileHandler
import os

# 日志保存目录
LOG_ROOT = get_abs_path('logs')
os.makedirs(LOG_ROOT, exist_ok=True)

# 日志格式配置
DEFAULT_LOG_FORMAT = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)-8s - %(filename)s:%(lineno)d:[%(funcName)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def get_logger(name: str = "rag_agent", level: int = logging.INFO, log_format: logging.Formatter = DEFAULT_LOG_FORMAT,
               base_log_file: str = None) -> logging.Logger:
    rag_logger = logging.getLogger(name)

    # 避免每次导入重新创建对象
    if rag_logger.handlers:
        return rag_logger

    rag_logger.setLevel(level)

    # 控制台输出
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(log_format)

    rag_logger.addHandler(console_handler)

    # 文件输出
    if base_log_file is None:
        base_log_file = os.path.join(LOG_ROOT, f"{name}.log")

    # when='MIDNIGHT' 每日零点更新
    # interval=1 以日更新
    # backupCount=30 保留 30 天日志文件
    file_handler = TimedRotatingFileHandler(base_log_file, when='MIDNIGHT', interval=1, backupCount=30,
                                            encoding='utf-8')
    file_handler.suffix = "%Y-%m-%d"
    file_handler.setLevel(level)
    file_handler.setFormatter(log_format)

    rag_logger.addHandler(file_handler)

    return rag_logger


logger = get_logger()
