import requests
import os
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

# 测试POST /predict
def test_predict():
    url = 'http://localhost:5000/predict'
    image_path = r'e:\github\EL2.0\backend\temp\Xinxiang_Wheat_S2_Fused_202304-0000000000-0000000000_1920_3456.png'
    
    # 检查图片文件是否存在
    if not os.path.exists(image_path):
        logger.error(f"图片文件不存在: {image_path}")
        return
    
    # 准备文件
    files = {'file': open(image_path, 'rb')}
    
    # 发送请求
    response = requests.post(url, files=files)
    
    logger.info(f"Status Code: {response.status_code}")
    logger.info(f"Content-Type: {response.headers.get('Content-Type')}")
    
    if response.status_code == 200:
        response_data = response.json()
        logger.info(f"Response Data: {response_data}")
        
        # 验证响应内容
        assert response.status_code == 200
        assert response.headers.get('Content-Type') == 'application/json'
        assert 'message' in response_data
        assert 'img_url' in response_data
        assert 'status' in response_data
        assert response_data['status'] == 'success'
        
        # 返回预测结果图片的URL
        return response_data['img_url']
    else:
        logger.error(f"Response Text: {response.text}")
        return None

# 测试GET /predict/<filename>
def test_show_predict_result(img_url):
    if not img_url:
        logger.error("没有获取到预测结果图片的URL")
        return
    
    # 构建测试URL
    logger.info(f"测试URL: {img_url}")
    
    # 发送请求
    response = requests.get(img_url)
    
    logger.info(f"Status Code: {response.status_code}")
    logger.info(f"Content-Type: {response.headers.get('Content-Type')}")
    
    # 验证响应内容
    assert response.status_code == 200
    assert 'image' in response.headers.get('Content-Type')
    logger.info("预测结果图片展示测试成功")

if __name__ == '__main__':
    logger.info(f"{'='*20}开始测试模型预测API{'='*20}")
    img_url = test_predict()
    if img_url:
        test_show_predict_result(img_url)
    logger.info(f"{'='*20}测试完成{'='*20}")
