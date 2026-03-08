import pathlib

src_path = pathlib.Path(__file__).parent.parent.parent / 'dataloader' / 'admini_division_src'

def get_bounds_json_path(bounds_name:list[str]):
    '''
    认为必须输入一个列表，如果为省份，则为省名  
    如果为市名，则列表第一个为省名，第二个为城市名  
    因此如果列表长为1，则为省份，长为2，则为城市
    '''
    if len(bounds_name) == 1:
        return src_path / f'ChinaGeodata/China_provs/{bounds_name[0]}/{bounds_name[0]}.json'
    elif len(bounds_name) == 2:
        return src_path / f'ChinaGeodata/China_provs/{bounds_name[0]}/二级区划/{bounds_name[1]}.json'
    else:
        return None
    

     