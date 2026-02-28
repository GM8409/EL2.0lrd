思考，
每次启动脚本都需要用鉴权一次导致脚本运行缓慢，所以考虑吧把gee相关代码独立出来作为服务启动  
避免脚本一直鉴权的同时也避免启动后端服务的时候需要同步启动这个服务，也好做职责分离  

那么这样一想，貌似gee的所有功能都可以看成一个被包装好的请求服务系统

回忆最简单和最基础的gee操作
1. 获取数据集ee.ImageCollection
imgc = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')

> 这一步可以看作是通过id创建一个类

2. 筛选
imgc = imgc.filterBounds(ee.Geometry.Point)\
    .filterDate('2023-01-01', '2023-01-31')\
    .filter(ee.Filter.lt('CLOUD_COVER', 20))

> 这一步可以看作是请求三次，或者请求一次，但是发送三个筛选信号

3. 获取信息
print(imgc.getInfo())

> 这一步可以看作是请求一次，然后从后端把imgc的信息返回过来

4. 添加到地图

Map.addLayer(imgc, {
    'bands': ['SR_B4', 'SR_B3', 'SR_B2'],
    'min': 0,
    'max': 0.3
}, 'imgc_name')

> 这一步就是拿到mapid，然后放在某个地图上

或许我可以考虑把这些方法复现一下？

复现过程中用cache缓存相关对象，然后用uuid作为key查询

那么后端需要用到哪些gee服务呢？

1. 筛选数据集

输入影像(数据集)id，边距（bounds）, 云量（cloud）, 时间范围（dateRange）等筛选条件
输出得到的imgc.getInfo()

2. 输入影像id和visparams，返回影像的mapurl