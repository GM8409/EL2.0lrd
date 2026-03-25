import pathlib
import json

PROJECT_DIR = pathlib.Path(__file__).parent
BACKEND_DIR = PROJECT_DIR / 'backend'
DATALOADER_DIR = PROJECT_DIR / 'dataloader'

DATA_DIR = DATALOADER_DIR / 'admini_division_src'
TEMP_DIR = BACKEND_DIR / 'temp'
MODEL_PATH = BACKEND_DIR / 'utils/model/best.pt'

with open(PROJECT_DIR / 'apiconfig.json', 'r', encoding='utf-8') as f:
    _API_CONFIG = json.load(f)

API_BASE_URL = _API_CONFIG['api_base_url']

SERVICE_GEEINFO = _API_CONFIG['services']['geeinfo']
SERVICE_GEODATA = _API_CONFIG['services']['geodata']
SERVICE_IMGACT = _API_CONFIG['services']['imgAct']
SERVICE_IMGCACT = _API_CONFIG['services']['imgcAct']
SERVICE_PREDICT = _API_CONFIG['services']['predict']
DEPRECATED_ROUTES = _API_CONFIG['deprecated']['routes']

if __name__ == '__main__':
    print(MODEL_PATH)
