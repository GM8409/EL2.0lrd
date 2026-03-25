# 本模块提供依据爬取到的GEE数据集的信息查询接口
from flask import Blueprint, jsonify, request

from dataloader.utils.geeinfo \
    import filter_dataset,get_detail

bp = Blueprint('geeinfo', __name__)

@bp.route('/geeinfo/search')
def search_gee_datasets():
    '''
    搜索GEE数据集
    参数:
        keyword: 搜索关键词（匹配name字段）
        producer: 生产者关键词
        tag: 标签关键词
        pixel_size: 像素分辨率
        pixel_comparison: 像素分辨率比较类型（eq/lt/gt/lte/gte）
        start_year: 开始年份
        end_year: 结束年份
    '''
    # 获取请求参数
    args = request.args    
    result_ids = filter_dataset(args)
    details = get_detail(result_ids,[
        'name',
        'date_start',
        'date_end',
        'pixel_size_num',
    ])
    result = [
        {
            'cid': result_ids.ids[i],
            'name': d['name'],
            'date_start': d['date_start'],
            'date_end': d['date_end'],
            'pixel_size_num': d['pixel_size_num'],
        }
        for i,d in enumerate(details)
    ]
    return jsonify({
        'status': 'success',
        'datasets': result
    })

