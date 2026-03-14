import config from '@/config';

// 从本地localstorage获取选中的数据集
export const getSelectedDataset = () => {
    console.log('开始从本地存储获取选中的数据集');
    const data = localStorage.getItem(config.SELECTED_DATASET_KEY);
    const result = data ? JSON.parse(data) : null;
    console.log('从本地存储获取选中的数据集完成:', result ? '成功' : '未找到');
    return result;
};

// 从本地localstorage获取搜索结果
export const getSearchResult = () => {
    console.log('开始从本地存储获取搜索结果');
    const data = localStorage.getItem(config.SEARCH_RESULT_KEY);
    const result = data ? JSON.parse(data) : null;
    console.log('从本地存储获取搜索结果完成:', result ? '成功' : '未找到');
    return result;
};

// 保存搜索结果到本地localstorage
export const saveSearchResult = (data: any) => {
    console.log('开始保存搜索结果到本地存储');
    localStorage.setItem(config.SEARCH_RESULT_KEY, JSON.stringify(data));
    console.log('搜索结果保存完成');
};

// 删除搜索结果
export const removeSearchResult = () => {
    console.log('开始删除搜索结果');
    localStorage.removeItem(config.SEARCH_RESULT_KEY);
    console.log('搜索结果删除完成');
};

// 从本地localstorage获取筛选结果
export const getFilterResult = () => {
    console.log('开始从本地存储获取筛选结果');
    const data = localStorage.getItem(config.FILTER_RESULT_KEY);
    const result = data ? JSON.parse(data) : null;
    console.log('从本地存储获取筛选结果完成:', result ? '成功' : '未找到');
    return result;
};

// 从本地localstorage获取Step1表单数据
export const getStep1FormData = () => {
    console.log('开始从本地存储获取Step1表单数据');
    const data = localStorage.getItem(config.STEP1_FORM_DATA_KEY);
    const result = data ? JSON.parse(data) : null;
    console.log('从本地存储获取Step1表单数据完成:', result ? '成功' : '未找到');
    return result;
};

// 从本地localstorage获取Step2表单数据
export const getStep2FormData = () => {
    console.log('开始从本地存储获取Step2表单数据');
    const data = localStorage.getItem(config.STEP2_FORM_DATA_KEY);
    const result = data ? JSON.parse(data) : null;
    console.log('从本地存储获取Step2表单数据完成:', result ? '成功' : '未找到');
    return result;
};

// 保存Step1表单数据到本地localstorage
export const saveStep1FormData = (data: any) => {
    localStorage.setItem(config.STEP1_FORM_DATA_KEY, JSON.stringify(data));
};

// 保存Step2表单数据到本地localstorage
export const saveStep2FormData = (data: any) => {
    localStorage.setItem(config.STEP2_FORM_DATA_KEY, JSON.stringify(data));
};

// 从本地localstorage获取可视化参数
export const getVisualParams = () => {
    console.log('开始从本地存储获取可视化参数');
    const data = localStorage.getItem(config.VISUAL_PARAMS_KEY);
    const result = data ? JSON.parse(data) : null;
    console.log('从本地存储获取可视化参数完成:', result ? '成功' : '未找到');
    return result;
};

// 保存可视化参数到本地localstorage
export const saveVisualParams = (data: any) => {
    console.log('开始保存可视化参数到本地存储');
    localStorage.setItem(config.VISUAL_PARAMS_KEY, JSON.stringify(data));
    console.log('可视化参数保存完成');
};

// 删除选中的数据集
export const removeSelectedDataset = () => {
    console.log('开始删除选中的数据集');
    localStorage.removeItem(config.SELECTED_DATASET_KEY);
    console.log('选中的数据集删除完成');
};

// 删除筛选结果
export const removeFilterResult = () => {
    console.log('开始删除筛选结果');
    localStorage.removeItem(config.FILTER_RESULT_KEY);
    console.log('筛选结果删除完成');
};

// 删除Step1表单数据
export const removeStep1FormData = () => {
    console.log('开始删除Step1表单数据');
    localStorage.removeItem(config.STEP1_FORM_DATA_KEY);
    console.log('Step1表单数据删除完成');
};

// 删除Step2表单数据
export const removeStep2FormData = () => {
    console.log('开始删除Step2表单数据');
    localStorage.removeItem(config.STEP2_FORM_DATA_KEY);
    console.log('Step2表单数据删除完成');
};

// 删除可视化参数
export const removeVisualParams = () => {
    console.log('开始删除可视化参数');
    localStorage.removeItem(config.VISUAL_PARAMS_KEY);
    console.log('可视化参数删除完成');
};

// 清除所有Step2相关的数据
export const clearStep2Data = () => {
    console.log('开始清除Step2相关的数据');
    removeFilterResult();
    removeStep2FormData();
    console.log('Step2相关的数据清除完成');
};

// 清除所有VisualParams相关的数据
export const clearVisualParamsData = () => {
    console.log('开始清除VisualParams相关的数据');
    removeVisualParams();
    console.log('VisualParams相关的数据清除完成');
};

// 清除所有数据（除了Step1）
export const clearAllExceptStep1 = () => {
    console.log('开始清除除Step1外的所有数据');
    clearStep2Data();
    clearVisualParamsData();
    console.log('除Step1外的所有数据清除完成');
};