import requests
import json
import logging

# 配置logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# 截断字符串函数
def truncate_string(s, max_length=200):
    if len(s) > max_length:
        return s[:max_length] + '...'
    return s

# 测试GET /geeinfo/search - 测试不同查询参数组合
def test_search_gee_datasets():
    # 测试用例1: 按名称和生产者搜索
    logger.info("测试用例1: 按名称和生产者搜索")
    url = 'http://localhost:5000/geeinfo/search'
    params = {
        'keyword': 'landsat',
        'producer': 'USGS'
    }
    response = requests.get(url, params=params)
    
    logger.info(f"Status Code: {response.status_code}")
    logger.info(f"Content-Type: {response.headers.get('Content-Type')}")
    
    if response.status_code == 200:
        response_data = response.json()
        logger.info(f"响应状态: {response_data['status']}")
        logger.info(f"数据集数量: {len(response_data['datasets'])}")
        
        # 展示前2个数据集的详细信息
        if len(response_data['datasets']) > 0:
            for i, dataset in enumerate(response_data['datasets'][:2]):
                logger.info(f"\n数据集 {i+1}:")
                logger.info(f"  CID: {dataset.get('cid')}")
                logger.info(f"  名称: {dataset.get('name')}")
                logger.info(f"  开始日期: {dataset.get('date_start')}")
                logger.info(f"  结束日期: {dataset.get('date_end')}")
                logger.info(f"  像素大小: {dataset.get('pixel_size_num')}")
        
        assert response.status_code == 200
        assert response.headers.get('Content-Type') == 'application/json'
        assert 'status' in response_data
        assert 'datasets' in response_data
        assert response_data['status'] == 'success'
        
        # 验证返回的数据集只包含必要字段
        if len(response_data['datasets']) > 0:
            first_dataset = response_data['datasets'][0]
            assert 'cid' in first_dataset
            assert 'name' in first_dataset
            assert 'pixel_size_num' in first_dataset
            assert 'date_start' in first_dataset
            assert 'date_end' in first_dataset
            # 确保没有返回不必要的字段
            assert 'producer' not in first_dataset
            assert 'tags' not in first_dataset
    else:
        logger.error(f"Response Text: {truncate_string(response.text)}")
    
    # 测试用例2: 按像素分辨率搜索
    logger.info("\n测试用例2: 按像素分辨率搜索")
    params = {
        'pixel_size': 30,
        'pixel_comparison': 'eq'
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        response_data = response.json()
        logger.info(f"响应状态: {response_data['status']}")
        logger.info(f"数据集数量: {len(response_data['datasets'])}")
    
    # 测试用例3: 按时间范围搜索
    logger.info("\n测试用例3: 按时间范围搜索")
    params = {
        'start_year': 2000,
        'end_year': 2010
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        response_data = response.json()
        logger.info(f"响应状态: {response_data['status']}")
        logger.info(f"数据集数量: {len(response_data['datasets'])}")

# 测试GET /geeinfo/details/<path:cid>
def test_get_gee_dataset_details():
    # 测试一个具体的数据集ID
    cid = 'LANDSAT/LT05/C02/T1_TOA'
    url = f'http://localhost:5000/geeinfo/details/{cid}'
    response = requests.get(url)
    
    logger.info(f"\n测试用例4: 获取数据集详情 - ID: {cid}")
    logger.info(f"Status Code: {response.status_code}")
    logger.info(f"Content-Type: {response.headers.get('Content-Type')}")
    
    if response.status_code == 200:
        response_data = response.json()
        logger.info(f"响应状态: {response_data['status']}")
        
        # 展示基本信息
        logger.info("\n基本信息:")
        if response_data['basic_info']:
            basic_info = response_data['basic_info'][0] if isinstance(response_data['basic_info'], list) else response_data['basic_info']
            for key, value in basic_info.items():
                logger.info(f"  {key}: {truncate_string(str(value))}")
        
        # 展示波段信息
        logger.info("\n波段信息:")
        if response_data['bands_info']:
            logger.info(f"  波段数量: {len(response_data['bands_info'])}")
            for i, band in enumerate(response_data['bands_info'][:3]):  # 只展示前3个波段
                logger.info(f"  波段 {i+1}:")
                for key, value in band.items():
                    logger.info(f"    {key}: {truncate_string(str(value))}")
        
        # 展示属性信息
        logger.info("\n属性信息:")
        if response_data['attrs_info']:
            logger.info(f"  属性数量: {len(response_data['attrs_info'])}")
            for i, attr in enumerate(response_data['attrs_info'][:3]):  # 只展示前3个属性
                logger.info(f"  属性 {i+1}:")
                for key, value in attr.items():
                    logger.info(f"    {key}: {truncate_string(str(value))}")
        
        assert response.status_code == 200
        assert response.headers.get('Content-Type') == 'application/json'
        assert 'status' in response_data
        assert 'basic_info' in response_data
        assert 'bands_info' in response_data
        assert 'attrs_info' in response_data
        assert response_data['status'] == 'success'
    else:
        logger.error(f"Response Text: {truncate_string(response.text)}")

if __name__ == '__main__':
    logger.info(f"{'='*20}开始测试GEE数据集信息API{'='*20}")
    test_search_gee_datasets()
    test_get_gee_dataset_details()
    logger.info(f"{'='*20}测试完成{'='*20}")
