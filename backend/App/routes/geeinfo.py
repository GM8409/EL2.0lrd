# 本模块提供依据爬取到的GEE数据集的信息查询接口
from flask import Blueprint, jsonify, request
import json
import pandas as pd
from dataloader.utils.geeinfo.geedataparser import DataParser


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
    keyword = request.args.get('keyword', '')
    producer = request.args.get('producer', '')
    tag = request.args.get('tag', '')
    pixel_size = request.args.get('pixel_size', None)
    pixel_comparison = request.args.get('pixel_comparison', 'eq')
    start_year = request.args.get('start_year', None)
    end_year = request.args.get('end_year', None)
    
    # 初始化DataParser
    parser = DataParser()
    
    # 按名称筛选
    if keyword:
        parser.filter_by_name(keyword)
    
    # 按生产者筛选
    if producer:
        parser.filter_by_producer(producer)
    
    # 按标签筛选
    if tag:
        parser.filter_by_tag(tag)
    
    # 按像素分辨率筛选
    if pixel_size:
        try:
            pixel_size = float(pixel_size)
            parser.filter_by_pixel_size(pixel_comparison, pixel_size)
        except ValueError:
            pass
    
    # 按时间范围筛选
    if start_year or end_year:
        try:
            start_year = int(start_year) if start_year else None
            end_year = int(end_year) if end_year else None
            parser.filter_by_time_range(start_year, end_year)
        except ValueError:
            pass
    
    # 获取筛选结果的DataFrame
    result_df = parser.get_result()
    
    # 只返回必要字段：cid, name, pixel_size_num, date_start, date_end
    result_df = result_df.reset_index(names='cid')
    result_df = result_df[['cid', 'name', 'pixel_size_num', 'date_start', 'date_end']]
    
    # 转换为字典，处理datetime格式
    result_dict = result_df.to_dict(orient='records')
    for item in result_dict:
        if isinstance(item['date_start'], pd.Timestamp):
            item['date_start'] = item['date_start'].isoformat()
        if isinstance(item['date_end'], pd.Timestamp):
            item['date_end'] = item['date_end'].isoformat()
    
    return jsonify({
        'status': 'success',
        'datasets': result_dict
    })

@bp.route('/geeinfo/details/<path:cid>')
def get_gee_dataset_details(cid):
    '''
    获取GEE数据集详情
    参数:
        cid: 数据集ID
    '''
    # 初始化DataParser
    parser = DataParser()
    
    # 按cid查询
    parser.get_by_cid(cid)
    
    # 获取基本信息
    basic_info = parser.getinfo()
    
    # 获取波段信息
    bands_info = parser.get_bands_by_cid(cid).to_dict('records')
    
    # 获取属性信息
    attrs_info = parser.get_attributes_by_cid(cid).to_dict('records')
    
    # 转换为字典
    basic_info_dict = json.loads(basic_info)
    
    return jsonify({
        'status': 'success',
        'basic_info': basic_info_dict,
        'bands_info': bands_info,
        'attrs_info': attrs_info
    })
