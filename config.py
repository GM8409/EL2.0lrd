import pathlib

PROJECT_DIR = pathlib.Path(__file__).parent
BACKEND_DIR = PROJECT_DIR / 'backend'
DATALOADER_DIR = PROJECT_DIR / 'dataloader'

DATA_DIR = DATALOADER_DIR / 'admini_division_src'
TEMP_DIR = BACKEND_DIR / 'temp'
MODEL_PATH = BACKEND_DIR / 'utils/model/best.pt'



if __name__ == '__main__':
    print(MODEL_PATH)
