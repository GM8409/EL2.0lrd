import chromadb
import pathlib
from geesevice.geeFunc.baseTool import import_ImageCollection

db_path = pathlib.Path(__file__).parent.parent / 'GEE_chroma'

CHROMADB_COLLECTION_NAME = 'RemoteSensingDatasets'
"ChromaDB的集合名"

class DataLoader:
    def __init__(self,collection_name:str = CHROMADB_COLLECTION_NAME):
        self.client = chromadb.PersistentClient(db_path)
        self.collection = self.client.get_or_create_collection(collection_name)
    
    def query_landsat(self):
        return self.collection.query(
            query_texts=["LANDSAT8"],
            n_results=40,
            
        )['metadatas']
        


class Dataset(import_ImageCollection):
    def __init__(self,cid):
        # 调用父类的__init__方法，传递dataset_id
        super().__init__(cid)
        self.client = chromadb.PersistentClient(db_path)
        self.collection = self.client.get_or_create_collection(CHROMADB_COLLECTION_NAME)
        self.cid = cid
        self.meta = self.get_meta()
        self.bands = self.meta['band_names']
        self.attributes = self.meta['attribute_names']
        self.bounds = None
        self.date_range = None

    def get_meta(self)->dict:
        """通过cid查询数据集的元数据"""
        return self.collection.query(
            query_texts=[""],
            ids=[self.cid]
        )['metadatas'][0][0]
        
