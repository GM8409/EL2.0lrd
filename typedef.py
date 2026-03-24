from pydantic import BaseModel,Field
from typing import List, Dict, Any

class DatasetFilterParams(BaseModel):
    name: str = Field(description="数据集名称，比如landsat、sentinel2")
    start_date: str = Field(description="开始日期，格式YYYY-MM-DD")
    end_date: str = Field(description="结束日期，格式YYYY-MM-DD")
    producer: str = Field(description="数据生产者，比如usgs、esa")


class MapUrlParams(BaseModel):
    img_ids: List[str] = Field(description="影像ID列表")
    vis_params: Dict[str, Any] = Field(
        default={
            "min": 0, 
            "max": 0.3, 
            "bands": ["B4", "B3", "B2"]
                 },
        description="可视化参数"
    )
    
