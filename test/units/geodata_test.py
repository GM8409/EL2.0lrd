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
def truncate_string(s, max_length=100):
    if len(s) > max_length:
        return s[:max_length] + '...'
    return s

# 测试GET /geodata/<path:filename>
def test_get_geojson():
    url = 'http://localhost:5000/geodata/China_provs/北京市/北京市.json'
    response = requests.get(url)
    
    logger.info(f"Status Code: {response.status_code}")
    logger.info(f"Content-Type: {response.headers.get('Content-Type')}")
    
    if response.status_code == 200:
        response_data = response.json()
        # 转换为字符串并截断
        data_str = json.dumps(response_data, ensure_ascii=False)
        truncated_data = truncate_string(data_str)
        logger.info(f"Response Data: {truncated_data}")
        
        assert response.status_code == 200
        assert response.headers.get('Content-Type') == 'application/json'
        assert 'type' in response.json()
        assert 'features' in response.json()
    else:
        logger.error(f"Response Text: {truncate_string(response.text)}")

# 测试GET /geodataMap
def test_get_geodata_map():
    url = 'http://localhost:5000/geodataMap'
    response = requests.get(url)
    
    logger.info(f"Status Code: {response.status_code}")
    logger.info(f"Content-Type: {response.headers.get('Content-Type')}")
    
    if response.status_code == 200:
        response_data = response.json()
        # 转换为字符串并截断
        data_str = json.dumps(response_data, ensure_ascii=False)
        truncated_data = truncate_string(data_str)
        logger.info(f"Response Data: {truncated_data}")
        
        assert response.status_code == 200
        assert response.headers.get('Content-Type') == 'application/json'
        assert isinstance(response.json(), dict)
    else:
        logger.error(f"Response Text: {truncate_string(response.text)}")

if __name__ == '__main__':
    logger.info(f"{'='*20}开始测试地理数据API{'='*20}")
    test_get_geojson()
    test_get_geodata_map()
    logger.info(f"{'='*20}测试完成{'='*20}")