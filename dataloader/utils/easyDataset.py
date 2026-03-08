import pandas
from datetime import datetime
from pathlib import Path

PROJECT_PATH = Path(__file__).parent.parent.parent
BASIC_INFO_PATH = PROJECT_PATH / 'dataloader' / 'basic_info.json'

class Dataset:
    def __init__(self,dataset_info:str=BASIC_INFO_PATH):
        self.dataset_info = self._loadinfo(dataset_info)
        self.filtered_dataset = self.dataset_info[self.dataset_info['status'] == 'able']
        self.start_dt = None
        self.end_dt = None
        
    def _loadinfo(self, info_path:str) -> pandas.DataFrame:
        '''
        读取初始信息用于数据集类的初始化
        '''
        initial_info = pandas.read_json(info_path)
        # 把时间转化为可比较的时间格式
        time_format = r'%Y-%m-%d'
        
        def parse_start(x):
            try:
                return datetime.strptime(x.split('–')[0].split('T')[0], time_format)
            except:
                return datetime.min

        def parse_end(x):
            try:
                return datetime.strptime(x.split('–')[1].split('T')[0], time_format)
            except:
                return datetime.max

        def format_time_range(x):
            '''
            格式化时间范围，将时区格式转换为 {最早时间}-{最晚时间} 的形式，
            如果最晚时间与当前时间差不超过一年，最晚时间显示为 "至今"
            '''
            if not x:
                return ''
            
            parts = x.split('–')
            if len(parts) != 2:
                return x
            
            earliest = parts[0].split('T')[0]
            latest = parts[1].split('T')[0]
            
            now = datetime.now()
            latest_date = datetime.strptime(latest, time_format)
            one_year_ago = datetime(now.year - 1, now.month, now.day)
            
            if latest_date >= one_year_ago:
                return f"{earliest} - 至今"
            else:
                return f"{earliest} - {latest}"

        initial_info['数据集开始时间'] = initial_info['数据集可用时间'].apply(parse_start)
        initial_info['数据集结束时间'] = initial_info['数据集可用时间'].apply(parse_end)
        initial_info['数据集可用时间'] = initial_info['数据集可用时间'].apply(format_time_range)
        
        # 初始化状态列，默认全为 'able'
        initial_info['status'] = 'able'
        return initial_info
    
    def filter_by_time(self, t0: str, t1: str = '-') -> 'Dataset':
        '''
        筛选出在时间范围内的数据集。用户输入格式为 YYYY-MM-DD
        修改自身 status 列而返回 self，支持链式调用
        '''
        time_format = r'%Y-%m-%d'
        self.start_dt = datetime.strptime(t0, time_format)
        if t1 == '-':
            self.end_dt = datetime.now()
        else:
            self.end_dt = datetime.strptime(t1, time_format)
            
        # 仅对当前为 'able' 的行进行筛选
        mask = (self.dataset_info['status'] == 'able') & \
               ~((self.dataset_info['数据集开始时间'] <= self.start_dt) & 
                 (self.dataset_info['数据集结束时间'] >= self.end_dt))
        
        self.dataset_info.loc[mask, 'status'] = 'disable'
        self.filtered_dataset = self.dataset_info[self.dataset_info['status'] == 'able']
        return self

    def filter_by_name(self, keyword: str) -> 'Dataset':
        '''
        实现按数据集名称筛选的功能，输入名称如 landsat, sentinel 等
        修改自身 status 列而返回 self，支持链式调用
        '''
        # 仅对当前为 'able' 的行进行筛选
        mask = (self.dataset_info['status'] == 'able') & \
               ~(self.dataset_info['name'].str.contains(keyword, case=False, na=False))
        
        self.dataset_info.loc[mask, 'status'] = 'disable'
        self.filtered_dataset = self.dataset_info[self.dataset_info['status'] == 'able']
        return self

    def filter_by_frequency(self, keyword: str) -> 'Dataset':
        '''
        实现按频率筛选的功能。如果没有值或不包含关键字，则设为 disable
        返回 self 支持链式调用
        '''
        # 1. 处理空值情况：如果“频率”列为空，直接设为 disable
        self.dataset_info.loc[
            (self.dataset_info['status'] == 'able') & 
            (self.dataset_info['频率'].isna() | (self.dataset_info['频率'] == '')), 
            'status'
        ] = 'disable'

        # 2. 模糊匹配关键字
        mask = (self.dataset_info['status'] == 'able') & \
               ~(self.dataset_info['频率'].str.contains(keyword, case=False, na=False))
        
        self.dataset_info.loc[mask, 'status'] = 'disable'
        self.filtered_dataset = self.dataset_info[self.dataset_info['status'] == 'able']
        return self

    def getID(self) -> list:
        '''
        获取当前筛选出的数据集 ID 列表
        '''
        return list(self.filtered_dataset['id'].astype(str))

    def __getitem__(self, index):
        '''
        支持像列表切片和根据索引取值一样选择数据集
        '''
        if isinstance(index, slice):
            # 切片操作，返回新的Dataset实例
            new_dataset = Dataset()
            new_dataset.dataset_info = self.dataset_info.copy()
            new_dataset.filtered_dataset = self.filtered_dataset.iloc[index]
            new_dataset.start_dt = self.start_dt
            new_dataset.end_dt = self.end_dt
            return new_dataset
        else:
            # 单个索引，返回对应的ID
            if 0 <= index < len(self.filtered_dataset):
                return str(self.filtered_dataset.iloc[index]['id'])
            else:
                raise IndexError(f"Index {index} out of range for current filtered datasets (total: {len(self.filtered_dataset)})")
    
    def showinfo(self):
        print(f"当前筛选出的有效数据集数量: {len(self.filtered_dataset)} / 总数: {len(self.dataset_info)}")
        if not self.filtered_dataset.empty:
            print("有效数据集详情:")
            print(self.filtered_dataset[['id', 'name', '频率', '数据集可用时间']])
        else:
            print("未找到匹配的数据集。")
        return self
        