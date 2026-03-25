from flask import Blueprint


bp = Blueprint('aichat', __name__)

@bp.route('/aiChat', methods=['POST'])
def ai_chat():
    '''
    调用AIChat模型
    '''
    
