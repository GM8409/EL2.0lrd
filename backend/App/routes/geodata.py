
# 本模块提供中国省界以及省界下二级区划的geojson文件，以及中国地理数据映射表

from flask import Blueprint,send_from_directory

from config import DATA_DIR

bp = Blueprint('data', __name__)

# 提供中国省界以及省界下二级区划的geojson文件
@bp.route('/geodata/<path:filename>')
def get_geojson(filename):
    return send_from_directory(f'{DATA_DIR}/ChinaGeoData', filename)

# 提供中国地理数据映射表
@bp.route('/geodataMap')
def get_geodata_map():
    return send_from_directory(DATA_DIR, 'geodataUrlMap.json')


