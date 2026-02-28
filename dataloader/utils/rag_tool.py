from typing import Any
from langchain_community.chat_models.tongyi import ChatTongyi 
from langchain_core.prompts import ChatPromptTemplate
from langchain_chroma import Chroma 
import chromadb 
from langchain_core.output_parsers import StrOutputParser 
from langchain_core.tools import tool 
import os 
from pathlib import Path
import json

# 设置API密钥
os.environ["DASHSCOPE_API_KEY"]="sk-3314f171aebc47b4b8f7e691a600223b"

# 使用绝对路径
CHROMADB_PATH = str(Path(__file__).parent.parent / 'GEE_chroma')
CHROMADB_COLLECTION_NAME_QWEN = 'RemoteSensingDatasets'

# 原始函数实现
def _get_search_keywords(question: str) -> str:
    """
    根据用户问题生成推荐的检索关键词
    
    Args:
        question: 用户的问题
    
    Returns:
        推荐的检索关键词，多个关键词用逗号分隔
    """
    # 简单的关键词提取逻辑
    # 实际应用中可以使用更复杂的NLP技术
    keywords = []
    
    # 常见的遥感数据集名称
    datasets = ['landsat', 'sentinel', 'modis', 'aster', 'worldview', 'quickbird']
    
    # 常见的遥感数据属性
    attributes = ['resolution', 'band', 'spectral', 'temporal', 'spatial', 'coverage']
    
    # 常见的应用场景
    applications = ['vegetation', 'land cover', 'urban', 'water', 'forest', 'agriculture']
    
    # 提取关键词
    question_lower = question.lower()
    
    # 检查数据集名称
    for dataset in datasets:
        if dataset in question_lower:
            keywords.append(dataset)
    
    # 检查属性
    for attribute in attributes:
        if attribute in question_lower:
            keywords.append(attribute)
    
    # 检查应用场景
    for application in applications:
        if application in question_lower:
            keywords.append(application)
    
    # 如果没有提取到关键词，返回问题中的主要名词
    if not keywords:
        # 简单的名词提取
        import re
        nouns = re.findall(r'\b[a-zA-Z]+\b', question_lower)
        # 过滤常见虚词
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'with', 'by'}
        keywords = [word for word in nouns if word not in stop_words][:5]
    
    return ','.join(keywords)

@tool
def get_search_keywords(question: str) -> str:
    """
    根据用户问题生成推荐的检索关键词
    
    Args:
        question: 用户的问题
    
    Returns:
        推荐的检索关键词，多个关键词用逗号分隔
    """
    return _get_search_keywords(question)

class RAGTool:
    def __init__(self):
        # 初始化ChromaDB客户端
        print(f"Initializing ChromaDB with path: {CHROMADB_PATH}")
        self.client = chromadb.PersistentClient(path=CHROMADB_PATH)
        
        # 检查collection是否存在
        collections = self.client.list_collections()
        print(f"Available collections: {[col.name for col in collections]}")
        
        # 初始化向量存储
        self.vectorstore = Chroma(
            client=self.client,
            collection_name=CHROMADB_COLLECTION_NAME_QWEN,
        )
        
        # 检查collection中的文档数量
        collection = self.client.get_collection(CHROMADB_COLLECTION_NAME_QWEN)
        print(f"Collection {CHROMADB_COLLECTION_NAME_QWEN} has {collection.count()} documents")
        
        # 创建检索器
        self.retriever = self.vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 10})
        
        # 初始化LLM
        self.llm = ChatTongyi(
            model_name='qwen-plus-2025-12-01',
        )
        
        # 定义系统提示词
        self.system_prompt = """你是专业的 GEE 遥感数据助手。
        
你的工作流程：
1. 首先分析用户问题，确定是否需要提取关键词
2. 如果需要提取关键词，可以从用户问题中提取相关的检索关键词
3. 使用提取的关键词在数据库中搜索相关的数据集信息
4. 基于检索结果和你的外部知识回答用户问题

回答要求：
1. 基础信息：精准列出匹配的 GEE 影像集 ID（cid）、数据集名称（name）、核心用途（tags）、像素大小（pixel_size）、覆盖时间（date_range）、重访周期（revisit_interval）、生产者（producer）；
2. 进阶信息：
   - 如果用户询问波段详情，请从【补充信息】的 `band_table_detail` 里提取（这是一个 JSON 字符串，请解析后提取波段名、中文名称、核心用途等关键信息）；
   - 如果用户询问属性详情，请从【补充信息】的 `attribute_table_detail` 里提取（这是一个 JSON 字符串，请解析后提取关键信息）；
   - 如果用户询问原始页面链接，请从【补充信息】的 `index_url` 里提取；
   - 如果用户询问导入代码，请从【补充信息】的 `import_code` 里提取；
3. 如果检索不到相关信息，使用外部知识回答问题，并说明未查询到符合要求的 GEE 数据；
4. 格式清晰，分点说明，不要有冗余内容；
5. 使用Markdown格式回答，包括标题、列表等元素，使回答更加清晰易读。"""
    
    def format_docs(self, docs):
        """把检索到的文档内容 + IndexData 结构的 Metadata 拼成完整上下文"""
        context_parts = []
        for idx, doc in enumerate(docs):
            # 提取 IndexData 结构的 Metadata
            meta = doc.metadata
            part = f"""
        --- 匹配结果 {idx+1} ---
        【文档内容（用于语义检索）】
        {doc.page_content}

        【补充信息（Metadata，用于提取详情）】
        - GEE ID（cid）：{meta.get('cid', '无')}
        - 数据集名称（name）：{meta.get('name', '无')}
        - 覆盖时间（date_range）：{meta.get('date_range', '无')}
        - 生产者（producer）：{meta.get('producer', '无')}
        - 导入代码（import_code）：{meta.get('import_code', '无')}
        - 重访周期（revisit_interval）：{meta.get('revisit_interval', '无')}
        - 标签（tags）：{meta.get('tags', '无')}
        - 描述（description）：{meta.get('description', '无')}
        - 像素大小（pixel_size）：{meta.get('pixel_size', '无')}
        - 所有波段名（band_names）：{meta.get('band_names', '无')}
        - 完整波段表详情（band_table_detail，JSON格式）：{meta.get('band_table_detail', '无')}
        - 所有属性名（attribute_names）：{meta.get('attribute_names', '无')}
        - 完整属性表详情（attribute_table_detail，JSON格式）：{meta.get('attribute_table_detail', '无')}
        - 使用条款（terms）：{meta.get('terms', '无')}
            """.strip()
            context_parts.append(part)
        return "\n\n".join(context_parts)
    
    def get_answer(self, question):
        """获取问题的回答和上下文"""
        try:
            # 先获取上下文（用于前端显示）
            docs = self.retriever.invoke(question)
            context = self.format_docs(docs)
            
            return context
        except Exception as e:
            return ""
    
    def stream_answer(self, question):
        """流式生成回答，让LLM自己决定是否提取关键词和搜索"""
        try:
            # 第一步：让LLM分析问题，决定是否需要搜索以及提取什么关键词
            decision_prompt = ChatPromptTemplate.from_messages([
                ("system", """你是一个专业的问题分析助手。请分析用户的问题，决定是否需要在数据库中搜索相关信息。

如果需要搜索，请以JSON格式输出，包含以下字段：
- "need_search": true
- "search_keywords": 搜索关键词（字符串，多个关键词用逗号分隔）

如果不需要搜索，请以JSON格式输出：
- "need_search": false

只输出JSON，不要有其他内容。"""),
                ("human", "{question}")
            ])
            
            decision_chain = decision_prompt | self.llm | StrOutputParser()
            decision_result = decision_chain.invoke({"question": question})
            
            print(f"Decision result: {decision_result}")
            
            # 解析决策结果
            try:
                decision = json.loads(decision_result)
            except json.JSONDecodeError:
                # 如果解析失败，默认需要搜索，使用原问题作为关键词
                decision = {"need_search": True, "search_keywords": question}
            
            context = ""
            if decision.get("need_search", True):
                search_keywords = decision.get("search_keywords", question)
                print(f"Searching with keywords: {search_keywords}")
                
                # 搜索数据库
                docs = self.retriever.invoke(search_keywords)
                context = self.format_docs(docs)
                print(f"Retrieved {len(docs)} documents")
            
            # 第二步：基于上下文生成回答
            answer_prompt = ChatPromptTemplate.from_messages([
                ("system", self.system_prompt),
                ("human", "用户问题：{question}\n\n检索到的上下文信息：\n{context}\n\n请基于以上信息回答用户的问题。")
            ])
            
            answer_chain = answer_prompt | self.llm | StrOutputParser()
            
            # 流式输出
            for chunk in answer_chain.stream({"question": question, "context": context}):
                yield chunk
                
        except Exception as e:
            yield f"Error: {str(e)}"

# 测试代码
if __name__ == '__main__':
    rag_tool = RAGTool()
    # 测试基础问题
    question = "能做植被检测的30米分辨率的landsat遥感数据集有哪些？"
    # 测试get_answer方法（返回context）
    context = rag_tool.get_answer(question)
    print("Context:")
    print(context)
    
    # 测试agent回答
    print("\nAnswer:")
    for chunk in rag_tool.stream_answer(question):
        print(chunk, end="", flush=True)
    print()
