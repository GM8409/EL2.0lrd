import requests
import uuid

def get_cache_info():
    resp = requests.get('http://localhost:5001/check_cache')
    return resp.text


class FImageCollection():
    def __init__(self, cid):
        self.cid = cid
        self.uuid = str(uuid.uuid4())
        # 先创建影像集并缓存
        self._create_imagecollection()
        self.bounds_filtered = False
        self.ids = []
        self.selected_ids = []
    
    def _create_imagecollection(self):
        """创建影像集并缓存"""
        url = f'http://localhost:5001/imagecollection/{self.uuid}'
        resp = requests.post(url, json={'cid': self.cid})
        return resp.json()
    
    def filter_Date(self, t0, t1):
        """
        专门用于 GEE 影像集的时间筛选方法
        """
        # 调用operate_cache端点进行日期筛选
        url = 'http://localhost:5001/operate'
        data = {
            'uuid': self.uuid,
            'operation': 'filter_Date',
            'params': {
                't0': t0,
                't1': t1
            }
        }
        resp = requests.post(url, json=data)
        result = resp.json()
        if result['status'] == 'success':
            return self
        else:
            raise Exception(f"筛选失败: {result}")

    def filter_Bounds(self, bounds):
        """
        支持输入 [province, city] 格式的地理边界对影像集进行筛选
        """
        # 调用operate_cache端点进行边界筛选
        url = 'http://localhost:5001/operate'
        data = {
            'uuid': self.uuid,
            'operation': 'filter_Bounds',
            'params': {
                'geometry': bounds
            }
        }
        resp = requests.post(url, json=data)
        result = resp.json()
        if result['status'] == 'success':
            self.bounds_filtered = True
            return self
        else:
            raise Exception(f"筛选失败: {result}")

    def filter(self, start_date, end_date, bounds=None, cloud=100):
        """
        筛选影像集
        参数:
            start_date: 开始日期，格式为'YYYY-MM-DD'
            end_date: 结束日期，格式为'YYYY-MM-DD'
            bounds: 地理边界，格式为 [province, city]，例如 ['江苏省', '南京市']
            cloud: 云量阈值，默认为100（不筛选云量）
        返回:
            self
        """
        url = f'http://localhost:5001/filter/{self.uuid}'
        data = {
            'cid': self.cid,
            'start_date': start_date,
            'end_date': end_date,
            'bounds': bounds,
            'cloud': cloud
        }
        resp = requests.post(url, json=data)
        result = resp.json()
        if result['status'] == 'success':
            self.bounds_filtered = result['bounds_filtered']
            return self
        else:
            raise Exception(f"筛选失败: {result}")
    
    def scaleAndOffset(self):
        """
        应用scaleAndOffset()方法到影像集
        """
        # 调用operate_cache端点应用scaleAndOffset
        url = 'http://localhost:5001/operate'
        data = {
            'uuid': self.uuid,
            'operation': 'scaleAndOffset'
        }
        resp = requests.post(url, json=data)
        result = resp.json()
        if result['status'] == 'success':
            print("成功应用scaleAndOffset()")
            return self
        else:
            raise Exception(f"应用scaleAndOffset()失败: {result}")
    
    def get_ids(self):
        """
        获取筛选出的影像 ID 列表，并存储在自身属性中。
        为了防止请求 ID 数量过多导致服务端超时或客户端崩溃，必须先调用 filter_Bounds。
        """
        if not self.bounds_filtered:
            raise RuntimeError("错误：在请求影像 ID 列表 (get_ids) 之前，必须先调用 filter_Bounds 进行空间范围筛选，以确保数据量在安全范围内。")
        
        # 调用operate_cache端点获取影像ID
        url = 'http://localhost:5001/operate'
        data = {
            'uuid': self.uuid,
            'operation': 'get_ids'
        }
        resp = requests.post(url, json=data)
        result = resp.json()
        if result['status'] == 'success' and 'result' in result:
            self.ids = result['result']
            print(f"成功获取 {len(self.ids)} 个影像 ID。")
            return self
        else:
            raise Exception(f"获取影像ID失败: {result}")
    
    def __getitem__(self, index):
        """
        支持像列表切片和根据索引取值一样选择影像 ID
        """
        if not self.ids:
            print("提示：当前 ID 列表为空，请先调用 get_ids() 获取 ID。")
            return self
            
        if isinstance(index, slice):
            self.selected_ids = self.ids[index]
        else:
            self.selected_ids = [self.ids[index]]
        return self
    
    def get_filtered_collection(self):
        """
        获取筛选后的影像集UUID
        """
        return self.uuid
    
    def get_image_ids(self):
        """
        获取筛选后影像的ID列表
        注意：必须先调用filter方法，且筛选时必须指定bounds
        """
        if not self.bounds_filtered:
            raise Exception("获取影像ID列表前必须先筛选地理边界")
        
        if not self.ids:
            self.get_ids()
        
        return self.ids
    
    def get_info(self):
        """
        获取影像集信息
        """
        # 调用operate_cache端点获取影像集信息
        url = 'http://localhost:5001/operate'
        data = {
            'uuid': self.uuid,
            'operation': 'get_info'
        }
        resp = requests.post(url, json=data)
        result = resp.json()
        if result['status'] == 'success' and 'result' in result:
            return result['result']
        else:
            raise Exception(f"获取影像集信息失败: {result}")
    
    def _repr_html_(self):
        """
        返回HTML表示，使得Jupyter Notebook能够显示FImageCollection实例
        利用后端ee.ImageCollection对象自动生成的HTML表示
        """
        # 调用operate_cache端点获取后端ee.ImageCollection对象的repr_html
        url = 'http://localhost:5001/operate'
        data = {
            'uuid': self.uuid,
            'operation': '_repr_html_'
        }
        try:
            resp = requests.post(url, json=data)
            result = resp.json()
            if result['status'] == 'success' and 'result' in result:
                return result['result']
            else:
                # 如果获取失败，返回默认的HTML表示
                return f"""
                <div style="border: 1px solid #ddd; padding: 10px; border-radius: 5px;">
                    <h3>FImageCollection实例</h3>
                    <p><strong>数据集ID:</strong> {self.cid}</p>
                    <p><strong>UUID:</strong> {self.uuid}</p>
                    <p><strong>边界筛选状态:</strong> {'已筛选' if self.bounds_filtered else '未筛选'}</p>
                    <p><strong>影像数量:</strong> {len(self.ids) if self.ids else '未获取'}</p>
                    {f"<p><strong>选中的影像数量:</strong> {len(self.selected_ids)}</p>" if self.selected_ids else ''}
                </div>
                """
        except Exception as e:
            # 如果请求失败，返回默认的HTML表示
            return f"""
            <div style="border: 1px solid #ddd; padding: 10px; border-radius: 5px;">
                <h3>FImageCollection实例</h3>
                <p><strong>数据集ID:</strong> {self.cid}</p>
                <p><strong>UUID:</strong> {self.uuid}</p>
                <p><strong>边界筛选状态:</strong> {'已筛选' if self.bounds_filtered else '未筛选'}</p>
                <p><strong>影像数量:</strong> {len(self.ids) if self.ids else '未获取'}</p>
                {f"<p><strong>选中的影像数量:</strong> {len(self.selected_ids)}</p>" if self.selected_ids else ''}
                <p><strong>错误:</strong> {str(e)}</p>
            </div>
            """


class FImage():
    def __init__(self, image_id):
        self.image_id = image_id
        self.uuid = str(uuid.uuid4())
        # 创建影像并缓存
        self._create_image()
        self.visparams = {}
    
    def _create_image(self):
        """创建影像并缓存"""
        url = f'http://localhost:5001/image/{self.uuid}'
        resp = requests.post(url, json={'cid': self.image_id})
        result = resp.json()
        if result['status'] != 'success':
            raise Exception(f"创建影像失败: {result}")
        return result
    
    def set_visparams(self, visparams):
        """
        设置可视化参数
        参数:
            visparams: 可视化参数字典，包含bands、min、max等
        返回:
            self
        """
        self.visparams = visparams
        return self
    
    def scaleAndOffset(self):
        """
        应用scaleAndOffset()方法到影像
        """
        # 调用operate_cache端点应用scaleAndOffset
        url = 'http://localhost:5001/operate'
        data = {
            'uuid': self.uuid,  # 使用uuid作为缓存键
            'operation': 'scaleAndOffset'
        }
        resp = requests.post(url, json=data)
        result = resp.json()
        if result['status'] == 'success':
            print("成功应用scaleAndOffset()")
            return self
        else:
            raise Exception(f"应用scaleAndOffset()失败: {result}")
    
    def get_map_url(self):
        """
        获取影像的地图URL
        注意：必须先设置可视化参数
        """
        if not self.visparams:
            raise Exception("错误：请先设置可视化参数 (set_visparams) 后再获取地图 URL。")
        
        # 先设置可视化参数
        url = 'http://localhost:5001/operate'
        set_params_data = {
            'uuid': self.uuid,
            'operation': 'set_visparams',
            'params': {
                'visparams': self.visparams
            }
        }
        resp = requests.post(url, json=set_params_data)
        result = resp.json()
        if result['status'] != 'success':
            raise Exception(f"设置可视化参数失败: {result}")
        
        # 然后获取地图URL
        get_url_data = {
            'uuid': self.uuid,
            'operation': 'get_map_url'
        }
        resp = requests.post(url, json=get_url_data)
        result = resp.json()
        if result['status'] == 'success' and 'result' in result:
            return result['result']
        else:
            raise Exception(f"获取地图URL失败: {result}")
    
    def get_info(self):
        """
        获取影像信息
        """
        # 调用operate_cache端点获取影像信息
        url = 'http://localhost:5001/operate'
        data = {
            'uuid': self.uuid,  # 使用uuid作为缓存键
            'operation': 'get_info'
        }
        resp = requests.post(url, json=data)
        result = resp.json()
        if result['status'] == 'success' and 'result' in result:
            return result['result']
        else:
            raise Exception(f"获取影像信息失败: {result}")
    
    def _repr_html_(self):
        """
        返回HTML表示，使得Jupyter Notebook能够显示FImage实例
        利用后端ee.Image对象自动生成的HTML表示
        """
        # 调用operate_cache端点获取后端ee.Image对象的repr_html
        url = 'http://localhost:5001/operate'
        data = {
            'uuid': self.uuid,  # 使用uuid作为缓存键
            'operation': '_repr_html_'
        }
        try:
            resp = requests.post(url, json=data)
            result = resp.json()
            if result['status'] == 'success' and 'result' in result:
                return result['result']
            else:
                # 如果获取失败，返回默认的HTML表示
                return f"""
                <div style="border: 1px solid #ddd; padding: 10px; border-radius: 5px;">
                    <h3>FImage实例</h3>
                    <p><strong>影像ID:</strong> {self.image_id}</p>
                    <p><strong>UUID:</strong> {self.uuid}</p>
                    <p><strong>可视化参数:</strong> {str(self.visparams)}</p>
                </div>
                """
        except Exception as e:
            # 如果请求失败，返回默认的HTML表示
            return f"""
            <div style="border: 1px solid #ddd; padding: 10px; border-radius: 5px;">
                <h3>FImage实例</h3>
                <p><strong>影像ID:</strong> {self.image_id}</p>
                <p><strong>UUID:</strong> {self.uuid}</p>
                <p><strong>可视化参数:</strong> {str(self.visparams)}</p>
                <p><strong>错误:</strong> {str(e)}</p>
            </div>
            """
    
def get_map_urls(image_ids, vis_params):
    """
    获取一个或多个影像的地图URL
    参数:
        image_ids: 影像ID字符串或影像ID列表
        vis_params: 可视化参数字典
    返回:
        单个地图URL字符串（当输入单个影像ID时）
        地图URL列表（当输入多个影像ID时）
    """
    
    # 直接调用后端的get_map_url端点
    url = 'http://localhost:5001/get_map_url'
    
    # 处理单个影像ID
    if isinstance(image_ids, str):
        data = {
            'image_id': image_ids,
            'vis_params': vis_params
        }
    # 处理多个影像ID
    else:
        data = {
            'image_ids': image_ids,
            'vis_params': vis_params
        }
    
    try:
        resp = requests.post(url, json=data)
        result = resp.json()
        if result['status'] == 'success' and 'result' in result:
            return result['result']
        else:
            # 如果获取失败，返回None或空列表
            return None if isinstance(image_ids, str) else []
    except Exception as e:
        print(f"获取地图URL失败: {e}")
        return None if isinstance(image_ids, str) else []

# 测试代码
if __name__ == '__main__':
    # 示例1: 链式调用示例，模拟import_ImageCollection的使用方式
    print("测试1: 链式调用示例")
    collection = FImageCollection('COPERNICUS/S2_SR_HARMONIZED')
    
    # 链式调用：筛选日期和边界
    collection.filter_Date('2020-01-01', '2020-01-31').filter_Bounds(['江苏省', '南京市'])
    
    # 获取影像ID列表
    collection.get_ids()
    print(f"获取到 {len(collection.ids)} 个影像ID")
    
    # 选择前3个影像
    collection[0:3]
    print(f"选择了 {len(collection.selected_ids)} 个影像")
    print(f"选中的影像ID: {collection.selected_ids}")
    
    # 示例2: 直接使用filter方法
    print("\n测试2: 直接使用filter方法")
    collection2 = FImageCollection('LANDSAT/LT05/C02/T1_TOA')
    # filter方法现在返回self，支持链式调用
    collection2.filter(
        start_date='2008-01-01',
        end_date='2009-01-31',
        bounds=['河南省', '开封市'],
        cloud=20
    )
    print(f"筛选后的影像集UUID: {collection2.get_filtered_collection()}")
    image_ids = collection2.get_image_ids()
    print(f"获取到 {len(image_ids)} 个影像ID")
    
    # 示例3: 链式调用，应用scaleAndOffset
    print("\n测试3: 链式调用，应用scaleAndOffset")
    collection3 = FImageCollection('COPERNICUS/S2_SR_HARMONIZED')
    # 链式调用：筛选日期、边界并应用scaleAndOffset
    collection3.filter_Date('2020-01-01', '2020-01-31').filter_Bounds(['江苏省', '南京市']).scaleAndOffset()
    collection3.get_ids()
    print(f"获取到 {len(collection3.ids)} 个影像ID")
    
    # 示例4: 测试FImage类
    print("\n测试4: 测试FImage类")
    if collection.ids:
        image_id = collection.ids[0]
        fimage = FImage(image_id)
        visparams = {
            'bands': ['SR_B4', 'SR_B3', 'SR_B2'],
            'min': 0,
            'max': 0.3
        }
        fimage.set_visparams(visparams)
        try:
            map_url = fimage.get_map_url()
            print(f"获取到地图URL: {map_url}")
        except Exception as e:
            print(f"获取地图URL失败: {e}")
    
    # 示例5: 测试get_map_urls静态方法
    print("\n测试5: 测试get_map_urls静态方法")
    if collection.ids:
        # 测试单个影像ID
        single_image_id = collection.ids[0]
        single_map_url = FImage.get_map_urls(single_image_id, visparams)
        print(f"单个影像的地图URL: {single_map_url}")
        
        # 测试多个影像ID
        if len(collection.ids) >= 3:
            multiple_image_ids = collection.ids[:3]
            multiple_map_urls = FImage.get_map_urls(multiple_image_ids, visparams)
            print(f"多个影像的地图URL数量: {len(multiple_map_urls)}")
            print(f"第一个影像的地图URL: {multiple_map_urls[0]}")


