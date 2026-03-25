import pandas as pd
from datetime import datetime
import re

from config import DATALOADER_DIR


LANDSAT_PATH = DATALOADER_DIR / 'utils/geeinfo/landsat_data.json'
SENTINEL_PATH = DATALOADER_DIR / 'utils/geeinfo/sentinel_data.json'
MODIS_PATH = DATALOADER_DIR / 'utils/geeinfo/modis_data.json'

bands_header_map = {
    'Name': '名',
    'Units': '单位',
    'Min': '最小值',
    'Max': '最大值',
    'Scale': '缩放',
    'Offset': '偏移',
    'Pixel Size': '像',
    'Wavelength': '波长',
    'Description': '说明',
    'Type': '类型',
}



class DataParser:
    '''
    提供一些筛选方法，这里用pandas更快
    支持链式筛选：筛选方法返回自身，连续调用优先基于临时筛选表(filtered_df)操作
    '''
    def __init__(self):
        # 初始化主数据表
        self.landsat_df = pd.read_json(LANDSAT_PATH).set_index('cid')
        self.sentinel_df = pd.read_json(SENTINEL_PATH).set_index('cid')
        self.modis_df = pd.read_json(MODIS_PATH).set_index('cid')
        self.main_df = pd.concat([self.landsat_df, self.sentinel_df, self.modis_df])
        
        # 新增：初始化临时筛选表（核心改造点1）
        self.filtered_df = None
        
        # 原有数据处理逻辑
        self._trans_tags()
        self._format_date()
        self._get_pixel_size()
        self.bands_df = self._extract_nested_table('bands_table_content')
        self.attrs_df = self._extract_nested_table('attribute_table_content')
        self._get_pixel_size_from_bands()
        self.main_df.drop(['complete_status','import_code','date_range','pixel_size',
                           'date_start_str','date_end_str'
                           ],axis=1,inplace=True)
        
    def _trans_tags(self):
        "给main_df加一个tags_str列，将tags列的列表转化为字符串"
        self.main_df['tags_str'] = self.main_df['tags'].apply(lambda x: ','.join(x) if isinstance(x,list) else x)
        return self.main_df
    
    def _format_date(self) -> datetime:
        "转换main_df的date_range列，将其转换为datetime对象"
        self.main_df[["date_start_str", "date_end_str"]] = self.main_df["date_range"].str.split("–", expand=True)
        
        # 转标准时间格式（处理Z时区后缀、小数点后的毫秒），errors="coerce"表示解析失败时设为NaN
        self.main_df["date_start"] = pd.to_datetime(
            self.main_df["date_start_str"].str.replace("Z", ""), 
            errors="coerce"
        )
        # 处理结束时间：离当前半年内设为'至今'，否则保留datetime
        now = datetime.now()
        self.main_df["date_end"] = pd.to_datetime(
            self.main_df["date_end_str"].str.split(".").str[0].str.replace("Z", ""), 
            errors="coerce"
        ).apply(lambda x: '至今' if (now - x).days < 180 else x)
    
    def _get_pixel_size(self):
        '提取像素分辨率的纯数字（如"30 meters"→30）'
        self.main_df["pixel_size_num"] = self.main_df["pixel_size"].str.extract(r"(\d+)").astype(float)
    
    def _get_pixel_size_from_bands(self):
        "如果自己的pixel_size为空，从bands_table_content中提取第一个波段的Pixel Size，如果还是没有，设为NaN"
        miss_cid_list = self.main_df[self.main_df["pixel_size_num"].isna()].index.tolist()
        if not miss_cid_list:
            return
        
        for cid in miss_cid_list:
            cid_bands = self.bands_df[self.bands_df["cid"] == cid]
            if not cid_bands.empty and "Pixel Size" in cid_bands.columns:
                band_pixel_size = cid_bands.iloc[0]["Pixel Size"]
                if isinstance(band_pixel_size, str):
                    num_match = re.search(r"\d+", band_pixel_size)
                    if num_match:
                        self.main_df.loc[cid, "pixel_size_num"] = float(num_match.group())

    def _extract_nested_table(self, nested_col_name):
        """
        私有方法：提取嵌套的波段/属性表（内部使用，不用关心）
        :param nested_col_name: 嵌套列名（"bands_table_content"或"attribute_table_content"）
        :return: 拆分后的独立表格（带cid索引）
        """ 
        nested_dfs = []
        for cid, row in self.main_df.iterrows():
            nested_data = row[nested_col_name]
            if isinstance(nested_data, list) and len(nested_data) > 1:
                headers = nested_data[0]
                # 统一表头为英文标准名
                for k,v in bands_header_map.items():
                    for i, h in enumerate(headers):
                        if h == k or v in h:
                            headers[i] = k
                data_rows = nested_data[1:]
                temp_df = pd.DataFrame(data_rows, columns=headers)
                temp_df['cid'] = cid
                nested_dfs.append(temp_df)
        return pd.concat(nested_dfs,ignore_index=True) if nested_dfs else pd.DataFrame()
    
    # -------------------------- 核心改造：筛选方法（返回自身+基于临时表筛选） --------------------------
    def _get_source_df(self):
        """私有方法：获取筛选的数据源（优先用临时筛选表，无则用主表）"""
        return self.filtered_df if self.filtered_df is not None else self.main_df
    
    def get_by_cid(self, cids:str|list[str]):
        """按cid查询主表数据（链式调用版），相当于筛选主表，将结果赋值给self.filtered_df属性
        
        :param cids: 单个cid或cid列表（支持字符串或列表）
        :return: 包含查询结果的DataFrame（空表或包含匹配行）
        
        """
        if isinstance(cids, str):
            cids = [cids]
        source_df = self._get_source_df()
        # 筛选：确保返回DataFrame（而非Series），保持结构统一
        if any(cid in source_df.index for cid in cids):
            self.filtered_df = source_df.loc[cids]  # 用[[cid]]返回DataFrame
        else:
            self.filtered_df = pd.DataFrame(columns=source_df.columns)  # 空表
        return self  # 返回自身支持链式调用
    
    def filter_by_producer(self, producer):
        """
        按生产者筛选（包含匹配+忽略大小写）（链式调用版）
        :param producer: 生产者关键词（如"USGS"/"usgs"/"nasa"）
        """
        source_df = self._get_source_df()
        
        # 处理空值+忽略大小写的包含匹配
        if isinstance(producer, str) and producer.strip():
            # 统一转小写 + 包含匹配 + 空值直接判定为不匹配（na=False）
            self.filtered_df = source_df[
                source_df["producer"]
                .str.lower()  # 字段值转小写
                .str.contains(
                    producer.strip().lower(),  # 参数转小写+去前后空格
                    case=False,  # 双重保障忽略大小写
                    na=False     # 空值直接返回False，避免报错
                )
            ]
        else:
            # 非字符串/空字符串参数：返回空表
            self.filtered_df = pd.DataFrame(columns=source_df.columns)
        
        return self

    def filter_by_tag(self, tag):
        """
        按标签筛选（忽略大小写）（链式调用版）
        :param tag: 标签关键词（如"landsat"/"LANDSAT"）
        """
        source_df = self._get_source_df()
        # 增强鲁棒性：参数和字段都转小写，同时处理空值（na=False）
        self.filtered_df = source_df[
            source_df["tags_str"].str.lower().str.contains(
                tag.lower(), 
                case=False, 
                na=False
            )
            if isinstance(tag, str)
            else pd.Series(False, index=source_df.index)
        ]
        return self
    
    def filter_by_pixel_size(self, comparison='lt', pixel_size_num=None):
        """
        按像素分辨率数字进行比较筛选（支持多类比较逻辑）（链式调用版）  
        :param comparison: 比较类型，支持：  
            'eq'  - 等于（默认）  
            'lt'  - 小于  
            'gt'  - 大于  
            'lte' - 小于等于  
            'gte' - 大于等于  
        :param pixel_size_num: 要比较的像素分辨率数值（如30、10、50）  
        :return: 自身实例，支持链式调用  
        """
        # 1. 获取筛选数据源（优先筛选表，无则主表）
        source_df = self._get_source_df()
        
        # 2. 定义支持的比较操作映射（操作符对应）
        valid_comparisons = {
            'eq': lambda x, y: x == y,
            'lt': lambda x, y: x < y,
            'gt': lambda x, y: x > y,
            'lte': lambda x, y: x <= y,
            'gte': lambda x, y: x >= y
        }
        
        # 3. 参数校验：确保比较类型有效、数值为数字
        if (comparison not in valid_comparisons) or (not isinstance(pixel_size_num, (int, float))):
            # 无效参数：返回空表（保持结构一致）
            self.filtered_df = pd.DataFrame(columns=source_df.columns)
            return self
        
        # 4. 执行筛选：排除空值 + 按指定比较逻辑筛选
        # 先过滤掉pixel_size_num为空的行，避免NaN干扰比较
        valid_pixel_df = source_df[source_df["pixel_size_num"].notna()]
        # 执行比较逻辑
        filter_cond = valid_comparisons[comparison](valid_pixel_df["pixel_size_num"], pixel_size_num)
        self.filtered_df = valid_pixel_df[filter_cond]
        
        return self
        
    def filter_by_time_range(self, start_year=None, end_year=None):
        """
        按时间范围筛选（比如筛选覆盖2023年的数据集）（链式调用版）
        start_year: 开始年份（如"2023-01-01"） 
        end_year: 结束年份（如"2023-12-31"）
        
        """
        if start_year or end_year:
            if start_year and end_year:
                if start_year > end_year:
                    raise ValueError("start_year must be less than or equal to end_year")
            
            source_df = self._get_source_df()
            filter_cond = pd.Series([True] * len(source_df), index=source_df.index)
            
            if start_year:
                # 过滤掉date_start为NaN的行
                start_date = datetime(*map(int, start_year.split('-')))
                valid_start = source_df["date_start"].notna()
                # date_start 应该 <= start_date（筛选在start_date之前开始的数据集）
                filter_cond &= valid_start & (source_df["date_start"] <= start_date)
            
            if end_year:
                # 处理date_end的混合类型（datetime/'至今'）
                end_date = datetime(*map(int, end_year.split('-')))
                now = datetime.now()
                
                # 创建一个临时的date_end用于比较，'至今'替换为当前时间
                def get_compare_date(x):
                    if x == '至今':
                        return now
                    elif isinstance(x, datetime):
                        return x
                    else:
                        return pd.NaT
                
                temp_date_end = source_df["date_end"].apply(get_compare_date)
                valid_end = temp_date_end.notna()
                
                # date_end 应该 >= end_date（筛选在end_date之后结束的数据集）
                filter_cond &= valid_end & (temp_date_end >= end_date)
            
            self.filtered_df = source_df[filter_cond]
            return self
        
        else:
            raise ValueError("start_year and end_year must be provided at least one")
        
    def filter_by_name(self, name_keyword):
        """
        按name字段筛选（包含匹配，忽略大小写）（链式调用版）
        :param name_keyword: 要匹配的名称关键词（如"Landsat 9"/"usgs"）
        """
        # 1. 获取筛选数据源（优先筛选表，无则主表）
        source_df = self._get_source_df()
        
        # 2. 筛选逻辑：忽略大小写的包含匹配，增强鲁棒性
        if isinstance(name_keyword, str) and name_keyword.strip():
            # 统一转为小写，包含匹配，空值直接判定为不匹配
            self.filtered_df = source_df[
                source_df["name"].str.lower().str.contains(
                    name_keyword.strip().lower(),
                    case=False,
                    na=False
                )
            ]
        else:
            # 非字符串/空字符串参数：返回空表
            self.filtered_df = pd.DataFrame(columns=source_df.columns)
        
        # 3. 返回自身支持链式调用
        return self

    def filter(self,
               name:list[str] | str = None,
               start_date:str = None,
               end_date:str = None,
               producer:list[str] | str = None,
               pixel_size_comparison:str = 'lt',
               pixel_size_num:float = None,
               tags:list[str] | str = None,
               **kwargs
               ):
        """
        数据集筛选方法
        name: 数据集名称列表，支持模糊匹配
        start_date: 开始日期，格式YYYY-MM-DD
        end_date: 结束日期，格式YYYY-MM-DD
        producer: 数据生产者列表
        pixel_size_comparison: 像素大小比较运算符，默认小于等于
        pixel_size_num: 像素大小
        tags: 标签列表，支持模糊匹配
        
        """
        # 这边增加鲁棒性如果传入的是date_start和date_end而没穿start_year和end_year，就把date_start和date_end赋值给start_year和end_year
        if 'date_start' in kwargs and 'date_end' in kwargs and kwargs['date_start'] and kwargs['date_end'] and start_date is None and end_date is None:
            start_date = kwargs['date_start']
            end_date = kwargs['date_end']
        
        # 加入如果是pixel_size 也考虑加入筛选
        if 'pixel_size' in kwargs and not kwargs['pixel_size_num'] and pixel_size_comparison:
            pixel_size_num = kwargs['pixel_size']
            pixel_size_comparison = kwargs['pixel_size_comparison']
            
        if name:
            if isinstance(name, list):
                for name_keyword in name:
                    self.filter_by_name(name_keyword)
            elif isinstance(name, str):
                self.filter_by_name(name)
        
        if producer:
            if isinstance(producer, list):
                for producer_keyword in producer:
                    self.filter_by_producer(producer_keyword)
            elif isinstance(producer, str):
                self.filter_by_producer(producer)
                
        if tags:
            if isinstance(tags, list):
                for tag_keyword in tags:
                    self.filter_by_tag(tag_keyword)
            elif isinstance(tags, str):
                self.filter_by_tag(tags)
        
        if pixel_size_num and pixel_size_comparison:
            self.filter_by_pixel_size(pixel_size_comparison, pixel_size_num)
            
        if start_date or end_date:
            self.filter_by_time_range(start_date, end_date)
            
        return self
    # -------------------------- 新增辅助方法 --------------------------
    def get_result(self,field:list[str] = None) -> pd.DataFrame:
        """获取当前筛选结果（返回DataFrame）"""
        filter_df = self.filtered_df if self.filtered_df is not None else self.main_df
        # 报错容差
        if field is None:
            return filter_df
        # 字段错误容差，如果输入的字段中有start_date和end_date 就自动转为date_start和date_end
        if 'start_date' in field and 'end_date' in field:
            field.remove('start_date')
            field.remove('end_date')
            field.append('date_start')
            field.append('date_end')
        
        # 如果有pixel_size 而没有pixel_size_num 就把pixel_size赋值给pixel_size_num
        if 'pixel_size' in field and 'pixel_size_num' not in field:
            field.remove('pixel_size')
            field.append('pixel_size_num')
        
        valid_fields = [f for f in field if f in filter_df.columns.tolist()]
        
        # 无有效字段返回空而不是全部
        return filter_df[valid_fields] if valid_fields else pd.DataFrame(columns=filter_df.columns)
    
    def get_filtered_ids(self) -> list[str]:
        """获取当前筛选结果的ID列表（返回列表）"""
        return self.get_result().index.tolist()
    
    def reset_filter(self):
        """重置筛选表，恢复为从主表开始筛选"""
        self.filtered_df = None
        return self  # 支持链式调用
    
    # -------------------------- 原有非筛选方法保留（调整返回逻辑） --------------------------
    def get_bands_by_cid(self, cid):
        """按cid查对应的波段信息（标准英文表头）"""
        return self.bands_df[self.bands_df["cid"] == cid]

    def get_attributes_by_cid(self, cid):
        """按cid查对应的属性信息（标准英文表头）"""
        return self.attrs_df[self.attrs_df["cid"] == cid]

    def getinfo(self,fields:list[str], orient='records', indent=2):
        """
        返回指定字段的JSON格式数据，优先基于筛选表返回
        :param fields: []
        :param orient: JSON输出格式，默认'records'（列表字典形式），可选'index'/'columns'等
        :param indent: JSON缩进，默认2（美化输出）
        :return: 格式化后的JSON字符串
        """
        # 获取数据源（优先筛选表，无则主表）
        fields = ['cid'] + fields if 'cid' not in fields else fields
        result_df = self.get_result()[fields].copy()
        
        # 6. 重置索引，将cid转为列（保留唯一标识）
        result_df = result_df.reset_index(names='cid')
        
        # 7. 转为美化的JSON（缩进2、保留中文、指定格式）
        json_result = result_df.to_json(
            orient=orient,
            indent=indent,
            force_ascii=False,  # 保证中文正常显示
            default_handler=str  # 兜底处理特殊类型，避免序列化失败
        )
        
        return json_result
