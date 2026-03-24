import sys
import os
from typing import List, Dict, Any

# ----------------------
# 1. 环境配置 + 导入你的真实业务模块
# ----------------------
sys.path.append('E:\github\EL2.0')


from geeservice.AwesEE import FImageCollection, get_map_urls
from geeservice.geeFunc.satellite_ids import *
from dataloader.utils.geeinfo.geedataparser import DataParser

# ----------------------
# 2. LangChain 1.x 核心库导入
# ----------------------
from langchain.agents import create_agent, AgentState
from langchain.tools import tool
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain.messages import AIMessage, HumanMessage, ToolMessage
from pydantic import BaseModel, Field, field_validator

# ----------------------
# 3. 初始化 LLM
# ----------------------
MODEL_NAME = "qwen-plus-2025-09-11"
llm = ChatTongyi(model_name=MODEL_NAME)

# ----------------------
# 4. 定义 Pydantic 模型
# ----------------------
class DatasetFilterParams(BaseModel):
    name: str = Field(description="数据集名称，比如landsat、sentinel2")
    start_date: str = Field(description="开始日期，格式YYYY-MM-DD")
    end_date: str = Field(description="结束日期，格式YYYY-MM-DD")
    producer: str = Field(description="数据生产者，比如usgs、esa")

    @field_validator("start_date", "end_date")
    def check_date_format(cls, v):
        from datetime import datetime
        try:
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            raise ValueError(f"日期格式错误，必须是YYYY-MM-DD，当前值：{v}")

class DatasetDescriptionParams(BaseModel):
    imgc_id: str = Field(description="数据集ID，格式如 LANDSAT/LT05/C02/T1_TOA")

class ImageFilterParams(BaseModel):
    imgc: str = Field(description="影像数据集ID，格式如 LANDSAT/LT05/C02/T1_TOA")
    bounds: List[str] = Field(description="地理范围[省份, 城市]")
    start_date: str = Field(description="开始日期")
    end_date: str = Field(description="结束日期")

class MapUrlParams(BaseModel):
    img_ids: List[str] = Field(description="影像ID列表")
    vis_params: Dict[str, Any] = Field(
        default={"min": 0, "max": 0.3, "bands": ["B4", "B3", "B2"]},
        description="可视化参数"
    )

# ----------------------
# 5. 【彻底修复】工具定义
# ----------------------
@tool(args_schema=DatasetFilterParams)
def filter_dataset(name: str, start_date: str, end_date: str, producer: str) -> str:
    """筛选符合条件的影像数据集，返回ID列表"""
    dataset = DataParser()
    dataset.filter(name=name, start_date=start_date, end_date=end_date, producer=producer)
    df = dataset.get_result()
    imgc_ids = df.index.tolist()
    return f"符合条件的数据集ID列表：{imgc_ids}"

@tool(args_schema=DatasetDescriptionParams)
def get_dataset_description(imgc_id: str) -> str:
    """ 根据数据集ID（如 LANDSAT/LT05/C02/T1_TOA）获取详细描述"""
    dataset = DataParser()
    try:
        return f"数据集 {imgc_id} 的详细描述：{dataset.get_by_cid(imgc_id).get_result()['description']}"
    except Exception as e:
        return f"查询数据集描述失败：{str(e)}"

@tool(args_schema=ImageFilterParams)
def filter_image_ids(imgc: str, bounds: List[str], start_date: str, end_date: str) -> Dict[str, Any]:
    """【修复2】结构化返回：既返回总数，又返回完整ID列表，Agent能拿到"""
    params = {
        "imgc": imgc,
        "filter": {
            "bounds": bounds,
            "start_date": start_date,
            "end_date": end_date
        }
    }
    img_ids = FImageCollection(params['imgc'])\
        .filter(**params['filter'])\
        .get_image_ids()
    
    # 【修复3】结构化返回，Agent 可以解析
    result = {
        "total_count": len(img_ids),
        "all_ids": img_ids,  # 【关键】返回完整 ID 列表
        "display_ids": img_ids[:10]  # 只展示前10个
    }
    
    if len(img_ids) > 10:
        return f"""
        查询结果：
        - 总影像数：{result['total_count']}（超过10个）
        - 展示的ID（前10个）：{result['display_ids']}
        - 完整ID列表：{result['all_ids']}
        提示：你可以直接使用完整ID列表中的任意ID，如需生成地图链接，建议优先使用前10个以节省Token。
        """
    else:
        return f"""
        查询结果：
        - 总影像数：{result['total_count']}
        - 完整ID列表：{result['all_ids']}
        """

@tool(args_schema=MapUrlParams)
def get_map_urls_tool(img_ids: List[str], vis_params: Dict[str, Any]) -> List[str]:
    """生成地图链接，默认只生成前3个"""
    limited_ids = img_ids[:3]
    return get_map_urls(limited_ids, vis_params)

# ----------------------
# 6. 创建 Agent
# ----------------------
tools = [filter_dataset, 
         get_dataset_description, 
         filter_image_ids, 
         get_map_urls_tool]

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="""
    你是专业的遥感影像查询助手。
    执行步骤：
    1. 调用 filter_dataset 筛选数据集ID；
    2. 如果需要了解数据集详情，调用 get_dataset_description（传入完整的数据集ID，格式如 LANDSAT/LT05/C02/T1_TOA）；
    3. 调用 filter_image_ids 筛选影像ID；
    4. 从返回的完整ID列表中选择，调用 get_map_urls_tool 生成地图链接。
    注意：
    - filter_image_ids 会返回结构化的结果，包含 total_count（总数）、all_ids（完整ID列表）、display_ids（前10个）；
    - 你可以直接使用 all_ids 中的任意ID；
    - 数据集ID格式是 LANDSAT/LT05/C02/T1_TOA（斜杠分隔），不是下划线。
    """,
    state_schema=AgentState
)

# ----------------------
# 7. 测试运行
# ----------------------
if __name__ == "__main__":
    user_input = "帮我找2008年到2009年湖北省武汉市的landsat影像，生产者是usgs，先看看数据集详情，再生成地图链接"
    
    print("="*80)
    print(f"👤 用户输入：{user_input}")
    print("="*80)
    print("\n🤖 Agent 执行过程：")
    print("-"*80)
    
    # 极简 Token 统计
    total_prompt_tokens = 0
    total_completion_tokens = 0
    total_tokens = 0
    
    final_chunk = None
    for chunk in agent.stream(
        {"messages": [{"role": "user", "content": user_input}]},
        stream_mode="values"
    ):
        final_chunk = chunk
        latest_message = chunk["messages"][-1]
        
        # Token 统计
        if isinstance(latest_message, AIMessage):
            if hasattr(latest_message, 'response_metadata'):
                metadata = latest_message.response_metadata
                if 'token_usage' in metadata:
                    usage = metadata['token_usage']
                    total_prompt_tokens += usage.get('input_tokens', 0)
                    total_completion_tokens += usage.get('output_tokens', 0)
                    total_tokens += usage.get('total_tokens', 0)
        
        # 打印执行过程
        if isinstance(latest_message, HumanMessage):
            continue
        elif isinstance(latest_message, AIMessage):
            if latest_message.content:
                print(f"\n💭 {latest_message.content}")
            if latest_message.tool_calls:
                print(f"\n🔧 调用工具：{[tc['name'] for tc in latest_message.tool_calls]}")
                for tc in latest_message.tool_calls:
                    print(f"   参数：{tc['args']}")
        elif isinstance(latest_message, ToolMessage):
            print(f"\n✅ 工具返回：")
            print(latest_message.content)
            
        print("-"*80)
    
    # 打印最终结果
    if final_chunk:
        print("\n" + "="*80)
        print("🎉 最终结果：")
        print("="*80)
        print(final_chunk["messages"][-1].content)
    
    # 打印 Token 统计
    print("\n" + "="*80)
    print("📊 Token 使用统计")
    print("="*80)
    print(f"   输入 Token:  {total_prompt_tokens}")
    print(f"   输出 Token:  {total_completion_tokens}")
    print(f"   总 Token:    {total_tokens}")
    print("="*80)