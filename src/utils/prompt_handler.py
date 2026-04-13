"""
加载 Prompt 文件
"""
from .path_handler import get_abs_path
from .logger_handler import logger
from .config_handler import prompts_conf


def load_prompts_conf(conf_key):
    """
    load prompts config
    :param: conf_key: config key
    :return: prompts config
    """
    try:
        prompts_path = get_abs_path(prompts_conf[conf_key])
    except KeyError as e:
        logger.error(f"{conf_key} does not exist")
        raise e

    try:
        return open(prompts_path, 'r', encoding='utf-8').read()
    except FileNotFoundError as e:
        logger.error(f"{prompts_path} does not exist")
        raise e


system_prompts = load_prompts_conf('system_prompt_path')
rag_prompts = load_prompts_conf('rag_prompt_path')
report_prompts = load_prompts_conf('report_prompt_path')

if __name__ == '__main__':
    # print(system_prompts)
    # print(rag_prompts)
    # print(report_prompts)
    pass
