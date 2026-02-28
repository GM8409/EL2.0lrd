import requests


resp = requests.post('http://localhost:5001/get_map_url',json={
    'image_id': 'LANDSAT/LC08/C02/T1_L2/LC08_123036_20200904',
    'vis_params': {
        "bands": ["SR_B4", "SR_B3", "SR_B2"],
        "min": 0,
        "max": 0.3,
    }
})

print(resp.text)