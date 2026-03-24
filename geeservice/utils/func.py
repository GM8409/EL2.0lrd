from ..rpc import exec_code,eval_code
from pydantic import BaseModel,Field
from typing import List,Dict,Any,Optional,Union

class ParamsFilterImgId(BaseModel):
    """筛选图像id参数（保留，仅适配新装饰器）"""
    cid: str = Field(description="目标图像数据集id", example="LANDSAT/LT05/C02/T1_L2")
    bounds: List[str] = Field(description="[省份名,城市名(可选)]", example=["湖北省", "武汉市"])
    start_date: str = Field(description="开始日期yyyy-MM-dd", example="2008-01-01")
    end_date: str = Field(description="结束日期yyyy-MM-dd", example="2009-12-31")


def fliter_img_id(cid:str,bounds:list[str,],start_date:str,end_date:str)->list[str]:
    exec_code(f'from geeservice.geeFunc.baseTool import import_FeatureCollection as FC,import_ImageCollection as IC')        
    resp = eval_code(f'IC("{cid}").filter_Bounds(FC({str(bounds)})).filter_Date("{start_date}","{end_date}").get_ids()')
    if resp['code'] == 200:
        return resp['result']
    else:
        raise Exception(f'筛选图像id失败：{resp["msg"]}')


class VisParams(BaseModel):
    """GEE影像可视化参数模型（符合Google官方规范）"""
    # 核心必填字段
    bands: List[str] = Field(
        description="要显示的波段列表，如RGB真彩色填['B4','B3','B2']（基于影像数据集的波段名称填写）",
        examples=[["B4", "B3", "B2"]]
    )
    # 核心可选字段（控制影像拉伸显示）
    min: Optional[Union[float, List[float]]] = Field(
        default=None,
        description="拉伸最小值，单值所有波段共用，列表则对应每个波段",
        examples=[0.0, [0.0, 0.0, 0.0]]
    )
    max: Optional[Union[float, List[float]]] = Field(
        default=None,
        description="拉伸最大值，单值所有波段共用，列表则对应每个波段",
        examples=[0.3, [0.3, 0.3, 0.3]]
    )
    # 扩展可选字段
    palette: Optional[List[str]] = Field(
        default=None,
        description="单波段影像的颜色调色板（十六进制颜色值列表）",
        examples=[["000000", "FF0000", "FFFF00"]]
    )
    opacity: Optional[float] = Field(
        default=None,
        ge=0.0,  # 限制最小值0
        le=1.0,  # 限制最大值1
        description="影像透明度，取值范围0-1（1为不透明）",
        examples=[1.0]
    )
    gamma: Optional[Union[float, List[float]]] = Field(
        default=None,
        description="伽马校正值，调整影像亮度",
        examples=[1.0]
    )

    class Config:
        # 允许传入GEE的其他小众参数（兼容扩展性）
        extra = "allow"


class ParamsGetMapUrl(BaseModel):
    img_ids: List[str] | str = Field(description="单个影像id或影像ID列表")
    vis_params: VisParams = Field(description="可视化参数")



def get_map_urls(img_ids: str | list ,vis_params: VisParams) -> str:
    exec_code(f'from geeservice.geeFunc.baseTool import get_map_urls')
    if isinstance(img_ids, str):
        return eval_code(f'get_map_urls("{img_ids}",{vis_params.model_dump()})')    
    elif isinstance(img_ids, list):
        return eval_code(f'get_map_urls({img_ids},{vis_params.model_dump()})')    
