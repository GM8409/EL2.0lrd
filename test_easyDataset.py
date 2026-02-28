from dataloader.utils.easyDataset import Dataset

# 测试1: 初始化Dataset实例并查看默认状态
print("测试1: 初始化Dataset实例并查看默认状态")
dataset = Dataset()
dataset.showinfo()
print()

# 测试2: 按时间筛选
print("测试2: 按时间筛选")
dataset_time = Dataset().filter_by_time('2020-01-01', '2023-12-31')
dataset_time.showinfo()
print(f"筛选后的ID列表: {dataset_time.getID()}")
print()

# 测试3: 按名称筛选
print("测试3: 按名称筛选")
dataset_name = Dataset().filter_by_name('sentinel')
dataset_name.showinfo()
print(f"筛选后的ID列表: {dataset_name.getID()}")
print()

# 测试4: 按频率筛选
print("测试4: 按频率筛选")
dataset_freq = Dataset().filter_by_frequency('5 天')
dataset_freq.showinfo()
print(f"筛选后的ID列表: {dataset_freq.getID()}")
print()

# 测试5: 链式筛选
print("测试5: 链式筛选")
dataset_chain = Dataset()\
    .filter_by_time('2020-01-01', '2023-12-31')\
    .filter_by_name('sentinel')\
    .filter_by_frequency('5 天')
dataset_chain.showinfo()
print(f"筛选后的ID列表: {dataset_chain.getID()}")
print()

# 测试6: 使用[]操作符获取单个ID
print("测试6: 使用[]操作符获取单个ID")
if len(dataset_chain.getID()) > 0:
    id_0 = dataset_chain[0]
    print(f"第一个ID: {id_0}")
print()

# 测试7: 使用[]操作符进行切片
print("测试7: 使用[]操作符进行切片")
if len(dataset_chain.getID()) > 2:
    dataset_slice = dataset_chain[0:2]
    print("切片后的数据集:")
    dataset_slice.showinfo()
    print(f"切片后的ID列表: {dataset_slice.getID()}")
print()

# 测试8: 测试边界情况
print("测试8: 测试边界情况")
dataset_empty = Dataset().filter_by_name('nonexistent_dataset')
dataset_empty.showinfo()
print(f"空数据集的ID列表: {dataset_empty.getID()}")
print()