"""
将 RAG 搜索结果和用户提问一并返回
"""
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from .vector_store_service import RagVectorStoreService
from src.utils.prompt_handler import rag_prompts
from src.model.factory import chat_model


class RagService:
    def __init__(self):
        self.vector_store_service = RagVectorStoreService()
        self.retriever = self.vector_store_service.get_retriever()
        self.rag_prompt_template = PromptTemplate.from_template(rag_prompts)
        self.chat_model = chat_model
        self.chain = self._init_chain()

    def _init_chain(self):
        return self.rag_prompt_template | self.chat_model | StrOutputParser()

    # 为 rag_prompts 中的 input，context 赋值
    def invoke(self, query: str) -> str:
        context_docs = self.retriever.invoke(query)

        # 拼接所有找到的参考资料，一起给大模型
        context = ''
        counter = 0
        for doc in context_docs:
            counter += 1
            context += f"[参考资料: {counter}], 参考资料元数据: {doc.metadata}, 参考资料: {doc.page_content}\n\n"
        # print(context)

        return self.chain.invoke({
            'input': query,
            'context': context_docs
        })


if __name__ == "__main__":
    # rag_service = RagService()
    # res = rag_service.invoke("扫地机器人保养需要注意什么")
    # print(res)
    pass