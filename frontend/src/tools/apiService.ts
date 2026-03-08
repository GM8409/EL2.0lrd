import axios from "axios";
import config from '@/config';



// 地理数据 API 路径
const API_GEO_URL = 'api/geodata/';

// 地理数据映射表 API 路径
const API_GEODATA_MAP_URL = 'api/geodataMap';



export const pathmap = {
    all_prov_path: API_GEO_URL + 'China_provs_all.geojson',
};

// 获取 GeoJSON 数据
export const getGeojson = async (path: string) => {
    console.log('开始加载 GeoJSON 数据:', path);
    try {
        const response = await axios.get(path);
        console.log('GeoJSON 数据加载成功');
        return response.data;
    } catch (error) {
        console.error('Error loading GeoJSON:', error);
        return null;
    }
};

// 获取地理数据映射表
export const getGeoDataMap = async () => {
    console.log('开始加载地理数据映射表');
    try {
        const response = await axios.get(API_GEODATA_MAP_URL);
        console.log('地理数据映射表加载成功');
        return response.data;
    } catch (error) {
        console.error('Failed to load geo data map:', error);
        throw error;
    }
};

// 获取指定路径的 GeoJSON 数据
export const getGeoJSONData = async (path: string) => {
    console.log('开始加载指定路径的 GeoJSON 数据:', path);
    try {
        const response = await axios.get(path);
        console.log('指定路径的 GeoJSON 数据加载成功');
        return response.data;
    } catch (error) {
        console.error('Failed to load GeoJSON data:', error);
        throw error;
    }
};

// 生成地理数据 URL
export const generateGeoDataUrl = (item: any) => {
    return API_GEO_URL + item.path;
};


// 从本地localstorage获取选中的数据集
export const getSelectedDataset = () => {
    console.log('开始从本地存储获取选中的数据集');
    const data = localStorage.getItem(config.SELECTED_DATASET_KEY);
    const result = data ? JSON.parse(data) : null;
    console.log('从本地存储获取选中的数据集完成:', result ? '成功' : '未找到');
    return result;
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

// 从localStorage获取数据并发送到后端进行筛选
export const filterImagesFromStorage = async () => {
    console.log('开始从本地存储获取数据并发送到后端进行筛选');
    const selectedDataset = getSelectedDataset();
    const step2Data = getStep2FormData();
    
    if (!selectedDataset || !step2Data) {
        console.error('本地存储中未找到数据');
        throw new Error('No data found in localStorage');
    }
    
    const { start_date, end_date, bounds, cloud } = step2Data;
    console.log('开始调用筛选接口');
    const result = await filterImages(selectedDataset.id, {
        start_date,
        end_date,
        bounds,
        cloud
    });
    console.log('筛选结果:', result);
    console.log('从本地存储获取数据并发送到后端进行筛选完成');
    return result;
    
};

// 搜索数据集
export const searchDatasets = async (params: {
    keyword?: string;
    time?: string;
    frequency?: string;
}) => {
    console.log('开始搜索数据集:', params);
    try {
        const response = await axios.get('api/datasets/search', {
            params
        });
        console.log('数据集搜索完成');
        return response.data;
    } catch (error) {
        console.error('Failed to search datasets:', error);
        throw error;
    }
};

// 获取数据集详情
export const getDatasetDetail = async (datasetId: string) => {
    console.log('开始获取数据集详情:', datasetId);
    try {
        const response = await axios.get(`api/datasets/${datasetId}`);
        console.log('数据集详情获取完成');
        return response.data;
    } catch (error) {
        console.error('Failed to get dataset detail:', error);
        throw error;
    }
};

// 筛选影像
export const filterImages = async (datasetId: string, params: {
    start_date: string;
    end_date: string;
    bounds?: string[];
    cloud?: number;
}) => {
    console.log('开始筛选影像:', datasetId, params);
    try {
        const response = await axios.post(`api/datasets/${encodeURIComponent(datasetId)}/filter`, params);
        console.log('影像筛选结果:', response.data);
        return response.data;
    } catch (error) {
        console.error('Failed to filter images:', error);
        throw error;
    }
};

// 获取影像地图URL
export const getMapUrls = async (imageIds: string | string[], visParams: any) => {
    console.log('开始获取影像地图URL:', imageIds, visParams);
    try {
        const response = await axios.post('api/get_map_url', {
            image_id: typeof imageIds === 'string' ? imageIds : undefined,
            image_ids: typeof imageIds === 'string' ? undefined : imageIds,
            vis_params: visParams
        });
        console.log('地图URL获取结果:', response.data);
        return response.data;
    } catch (error) {
        console.error('Failed to get map urls:', error);
        throw error;
    }
};

// 从本地获取visparams和imageIds并发送到后端获取地图URL
export const getMapUrlsFromStorage = async () => {
    console.log('开始从本地获取visparams和imageIds并发送到后端获取地图URL');
    try {
        const visParams = getVisualParams();
        if (!visParams) {
            console.error('本地存储中未找到可视化参数');
            throw new Error('No visualization parameters found in localStorage');
        }
        
        const basic = visParams.basic;
        if (!basic) {
            console.error('本地存储中未找到基本可视化参数');
            throw new Error('No basic visualization parameters found in localStorage');
        }
        
        const { selectedImages, bands, max, min } = basic;
        if (!selectedImages || selectedImages.length === 0) {
            console.error('本地存储中未找到选中的影像');
            throw new Error('No selected images found in localStorage');
        }
        
        // 只使用basic中的max、min和bands三个属性
        const simplifiedVisParams = {
            bands,
            max,
            min
        };
        
        const response = await axios.post('api/get_map_url', {
            image_ids: selectedImages,
            vis_params: simplifiedVisParams
        });
        console.log('地图URL获取结果:', response.data);
        return response.data;
    } catch (error) {
        console.error('Failed to get map urls from storage:', error);
        throw error;
    }
};


declare global {
    interface Window {
        searchDatasets: (params: any) => Promise<any>;
        getDatasetDetail: (datasetId: string) => Promise<any>;
        filterImages: (datasetId: string, params: any) => Promise<any>;
        getSelectedDataset: () => any;
        getFilterResult: () => any;
        getStep1FormData: () => any;
        getStep2FormData: () => any;
        getVisualParams: () => any;
        filterImagesFromStorage: () => Promise<any>;
        getMapUrls: (imageIds: string | string[], visParams: any) => Promise<any>;
        getMapUrlsFromStorage: () => Promise<any>;
    }
}

window.searchDatasets = searchDatasets;
window.getDatasetDetail = getDatasetDetail;
window.filterImages = filterImages;
window.getSelectedDataset = getSelectedDataset;
window.getFilterResult = getFilterResult;
window.getStep1FormData = getStep1FormData;
window.getStep2FormData = getStep2FormData;
window.getVisualParams = getVisualParams;
window.filterImagesFromStorage = filterImagesFromStorage;
window.getMapUrls = getMapUrls;
window.getMapUrlsFromStorage = getMapUrlsFromStorage;
