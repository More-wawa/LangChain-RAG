"""
向量存储服务
"""
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.utils.config_handler import chroma_conf
from src.utils.logger_handler import logger
from src.utils.file_handler import get_file_md5_hex, is_repeat_md5_hex, save_md5_hex, list_allowed_type_in_dir, \
    load_documents
from src.model.factory import embedding_model


class RagVectorStoreService:
    def __init__(self):
        # 向量数据库
        self.vector_store = Chroma(
            collection_name=chroma_conf["collection_name"],
            embedding_function=embedding_model,
            persist_directory=chroma_conf["persist_directory"],
        )
        # 分词器
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_conf["chunk_size"],
            chunk_overlap=chroma_conf["chunk_overlap"],
            separators=chroma_conf["separators"],
            length_function=len,
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={'k': chroma_conf['k']})

    def load_document(self):
        if allowed_files_path := list_allowed_type_in_dir(chroma_conf['data_path'],
                                                          tuple(chroma_conf['allowed_types'])):
            # 遍历文件夹中所有指定格式文件，并使用 md5 去除重复上传的文件后，加载进向量数据库
            for file_path in allowed_files_path:
                # 获取当前文件唯一编码
                md5_hex = get_file_md5_hex(file_path)

                # md5 读取失败
                if md5_hex is None:
                    logger.warning(f"Failed to calculate MD5 for {file_path}")
                    continue

                # 重复上传，跳过该文件
                if is_repeat_md5_hex(md5_hex):
                    continue

                # 上传文件至向量数据库
                try:
                    docs: list[Document] = load_documents(file_path=file_path)
                    # 当前文件无效
                    if docs is None:
                        logger.warning(f"{file_path} has no documents")
                        continue

                    # 文本分割后才能将一段文件映射成向量
                    split_docs = self.splitter.split_documents(docs)
                    if split_docs is None:
                        logger.warning(f"{file_path} has no documents after splitting")
                        continue

                    # 在向量库中新增内容
                    self.vector_store.add_documents(split_docs)

                    # 将该文件标记为已上传
                    save_md5_hex(md5_hex)
                except Exception as e:
                    logger.error(f"{file_path} has an error: {e}")


if __name__ == "__main__":
    # rvs = RagVectorStoreService()
    # rvs.load_document()
    #
    # retriever = rvs.get_retriever()
    #
    # res = retriever.invoke('扫地')
    # for r in res:
    #     print(r.page_content)
    #     print('*' * 100)
    pass
