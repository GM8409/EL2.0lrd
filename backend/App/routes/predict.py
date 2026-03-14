# 本模块提供模型预测接口
from flask import Blueprint,jsonify,request,send_from_directory
from ultralytics import YOLO
from config import MODEL_PATH, TEMP_DIR


bp = Blueprint('predict', __name__)

model = YOLO(MODEL_PATH)

@bp.route('/predict', methods=['POST'])
def predict():
    '''
    模型预测接口
    接收参数：file（待预测的图片文件）
    返回参数：message（上传成功消息）、img_url（预测结果图片的url）、status（状态码）
    '''
    file = request.files.get('file')
    filename = file.filename
    file.save(f'{TEMP_DIR}/{filename}')
    model.predict(
        source=f'{TEMP_DIR}/{filename}',
        conf = 0.5,
        save = True,
        project = TEMP_DIR,
        name = 'predict',
        exist_ok = True,
        )
    
    img_url = f'http://localhost:5000/predict/{filename}'
    # 预测之后生成jpg了，但是url是png
    # 所以前端要显示jpg，要自己处理一下
    img_url = img_url.split('.')[0] + '.jpg'
    print(img_url)
    
    return jsonify(
        {'message': 'Upload success!',
        'img_url': img_url,
        'status':'success',
        })

@bp.route('/predict/<filename>')
def show_predict_result(filename):
    return send_from_directory(f'{TEMP_DIR}/predict', filename)




