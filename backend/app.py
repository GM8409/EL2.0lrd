from flask import Flask,request,jsonify,send_from_directory,Response
from flask_cors import CORS
import ultralytics
import os
import json

# 添加数据集搜索和管理的导入
import sys
from pathlib import Path

project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)
from dataloader.utils.easyDataset import Dataset
from dataloader.utils.chroma_tool import DataLoader
from geesevice.AwesEE import FImage


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(BASE_DIR, 'temp')

app = Flask(__name__)
CORS(app)

model = ultralytics.YOLO(f'{BASE_DIR}/utils/model/best.pt')


@app.route('/data')
def index():
    return jsonify(
        {'message': 'Hello, Vue!'}
        )

@app.route('/temp/<path:filename>')
def serve_temp_dir(filename):
    return send_from_directory(TEMP_DIR, filename)


# 提供中国省界以及省界下二级区划的geojson文件
@app.route('/geodata/<path:filename>')
def get_geojson(filename):
    return send_from_directory(f'{os.path.dirname(BASE_DIR)}/dataloader/admini_division_src/ChinaGeodata', filename)

# 提供中国地理数据映射表
@app.route('/geodataMap')
def get_geodata_map():
    with open(f'{os.path.dirname(BASE_DIR)}/dataloader/admini_division_src/geodataUrlMap.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return jsonify(data)


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    filename = file.filename
    file.save(f'{TEMP_DIR}/{filename}')
    results = model.predict(
        source=f'{TEMP_DIR}/{filename}',
        conf = 0.5,
        save = True,
        project = TEMP_DIR,
        name = 'predict',
        exist_ok = True,
        )
    
    img_url = f'http://localhost:5000/temp/predict/{filename}'
    # 预测之后生成jpg了，但是url是png
    # 所以前端要显示jpg，要自己处理一下
    img_url = img_url.split('.')[0] + '.jpg'
    print(img_url)
    
    return jsonify(
        {'message': 'Upload success!',
        'img_url': img_url,
        'status':'success',
        }
        )

@app.route('/imgGet', methods=['POST'])
def imgGet():
    '''
    一次筛选结果接收参数
    :param data={
        'dateRange': ['2023-01-01T00:00:00Z', '2023-01-31T23:59:59Z'],
        'cloud': 50,
        'bounds': ['湖北省','武汉市'],
        'bounds_type': 'city',
        'satellite': 'LANDSAT', # 这三个参数要组合成有效id
        'category': 'TOA',
        'tier': 'T1',
    }
    
    '''
    data = request.json
    dateRange = [d.split('T')[0] for d in data['dateRange']]
    cloud = data.get('cloud', None)
    bounds_name = data.get('bounds', None)
    bounds_type = data.get('bounds_type', None)
    satellite = data.get('satellite', None)
    category = data.get('category', None)
    tier = data.get('tier', None)
    print('='*50)
    print(data)
    print('='*50)
    from dataloader.utils.usual_tools import get_bounds_json_path
    bounds_path = get_bounds_json_path(bounds_name)
    print('bounds_path:',bounds_path)
    print('='*50)
    print('dateRange:',dateRange)
    print('='*50)
    print('id:',satellite + tier + category)
    
    return jsonify(
        {'message': 'imgGet success!',
        'status':'success',
        }
        )

# 数据集搜索 API
@app.route('/datasets/search', methods=['GET'])
def search_datasets():
    '''
    搜索数据集
    参数:
        keyword: 搜索关键词
        time: 时间范围，格式为 'YYYY-MM-DD,YYYY-MM-DD'
        frequency: 频率关键词
    '''
    keyword = request.args.get('keyword', '')
    time_range = request.args.get('time', '')
    frequency = request.args.get('frequency', '')
    
    # 使用 Dataset 类进行筛选
    dataset = Dataset()
    
    # 按时间筛选
    if time_range:
        start_date, end_date = time_range.split(',')
        dataset.filter_by_time(start_date, end_date)
    
    # 按名称筛选
    if keyword:
        dataset.filter_by_name(keyword)
    
    # 按频率筛选
    if frequency:
        dataset.filter_by_frequency(frequency)
    
    # 获取筛选结果
    filtered_data = dataset.filtered_dataset.to_dict('records')
    
    return jsonify({
        'status': 'success',
        'datasets': filtered_data
    })

# 数据集详情 API
@app.route('/datasets/<dataset_id>', methods=['GET'])
def get_dataset_detail(dataset_id):
    '''
    获取数据集详情
    '''
    try:
        # 使用 Chroma 工具查询数据集元数据
        data_loader = DataLoader()
        # 这里可以根据实际情况实现元数据查询
        # 暂时返回基本信息
        return jsonify({
            'status': 'success',
            'dataset': {
                'id': dataset_id,
                'name': dataset_id.split('/')[-1],
                'source': dataset_id.split('/')[0]
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

# 影像筛选 API
@app.route('/datasets/<path:dataset_id>/filter', methods=['POST'])
def filter_images(dataset_id):
    '''
    筛选影像
    参数:
        start_date: 开始日期
        end_date: 结束日期
        bounds: 地理边界，格式为 [province, city]
        cloud: 云量阈值
    '''
    data = request.json
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    bounds = data.get('bounds')
    cloud = data.get('cloud', 100)
    
    try:
        # 使用 AwesEE 包进行筛选
        from geesevice.AwesEE import FImageCollection
        
        # 创建影像集并进行筛选
        collection = FImageCollection(dataset_id)
        collection.filter(
            start_date=start_date,
            end_date=end_date,
            bounds=bounds,
            cloud=cloud
        ).scaleAndOffset()
        
        # 获取影像 ID 列表
        image_ids = collection.get_image_ids()
        
        # 获取影像集的 HTML 表示
        html_representation = collection._repr_html_()
        
        # 获取影像集的信息
        collection_info = collection.get_info()
        
        return jsonify({
            'status': 'success',
            'bounds_filtered': collection.bounds_filtered,
            'ids': image_ids,
            'uuid': collection.get_filtered_collection(),
            'info': collection_info,
            'html': html_representation
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })


@app.route('/get_map_url', methods=['POST'])
def get_map_url():
    """
    获取影像的地图URL
    参数:
        image_id: 影像ID（单个）
        image_ids: 影像ID列表（多个）
        vis_params: 可视化参数
    """
    image_id = request.json.get('image_id')
    image_ids = request.json.get('image_ids')
    vis_params = request.json['vis_params']
    
    try:
        from geesevice.AwesEE import get_map_urls
        result = get_map_urls(image_id or image_ids, vis_params)
        return jsonify({
            'status': 'success',
            'result': result
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })


# RAG API - 流式响应
@app.route('/api/rag/stream', methods=['POST'])
def rag_query_stream():
    """处理RAG查询请求（流式响应）"""
    try:
        data = request.json
        question = data.get('question', '')
        
        if not question:
            return jsonify({
                'status': 'error',
                'message': 'Question is required'
            })
        
        # 导入RAG工具
        from dataloader.utils.rag_tool import RAGTool
        rag_tool = RAGTool()
        
        # 获取上下文
        context = rag_tool.get_answer(question)
        
        # 定义流式响应生成器
        def generate():
            # 先发送上下文信息
            yield json.dumps({"context": context, "chunk": ""}) + "\n"
            
            # 流式发送回答
            for chunk in rag_tool.stream_answer(question):
                yield json.dumps({"context": "", "chunk": chunk}) + "\n"
        
        # 返回流式响应
        return Response(generate(), mimetype='text/event-stream')
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

# 保持原有的非流式API
@app.route('/api/rag', methods=['POST'])
def rag_query():
    """处理RAG查询请求"""
    try:
        data = request.json
        question = data.get('question', '')
        
        if not question:
            return jsonify({
                'status': 'error',
                'message': 'Question is required'
            })
        
        # 导入RAG工具
        from dataloader.utils.rag_tool import RAGTool
        rag_tool = RAGTool()
        
        # 获取上下文
        context = rag_tool.get_answer(question)
        
        # 获取回答
        answer = ""
        for chunk in rag_tool.stream_answer(question):
            answer += chunk
        
        return jsonify({
            'status': 'success',
            'answer': answer,
            'context': context
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True)