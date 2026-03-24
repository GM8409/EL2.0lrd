from pydantic import BaseModel, Field


class DatasetFields(BaseModel):
    """数据集字段"""
    index_url: str = Field(description="数据集索引URL")
    name: str = Field(description="数据集名称")
    producer: str = Field(description="数据生产者")
    revisit_interval: str = Field(description="重访间隔")
    tags: list[str] = Field(description="标签列表")
    description: str = Field(description="数据集描述")
    bands_table_content: str = Field(description="波段表格内容")
    attribute_table_content: str = Field(description="属性表格内容")
    terms: str = Field(description="使用条款")
    tags_str: str = Field(description="标签字符串")
    date_start: str = Field(description="开始日期")
    date_end: str = Field(description="结束日期")
    pixel_size_num: float = Field(description="像素大小")