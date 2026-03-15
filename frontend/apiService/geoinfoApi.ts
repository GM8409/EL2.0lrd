import axios from 'axios';
import config from '@/config';

export interface SearchData {
  cid: string;
  name: string;
  pixel_size_num: number | null;
  date_start: string;
  date_end: string | '至今';
}

export interface SearchDatasetsParams {
  keyword?: string;
  producer?: string;
  tag?: string;
  pixel_size?: string;
  pixel_comparison?: string;
  start_year?: string;
  end_year?: string;
}

export interface SearchDatasetsResponse {
  status: string;
  datasets: SearchData[];
}

export interface BandInfo {
  [key: string]: any;
}

export interface AttributeInfo {
  [key: string]: any;
}

export interface DatasetDetailResponse {
  status: string;
  basic_info: any;
  bands_info: BandInfo[];
  attrs_info: AttributeInfo[];
}

export const searchDatasets = async (params: SearchDatasetsParams): Promise<SearchDatasetsResponse> => {
  console.log('开始搜索数据集:', params);
  try {
    const response = await axios.get(config.API_DATASETS_SEARCH, { params });
    console.log('数据集搜索完成');
    console.log('数据集搜索结果:', response.data);
    return response.data;
  } catch (error) {
    console.error('Failed to search datasets:', error);
    throw error;
  }
};

export const getDatasetDetail = async (datasetId: string): Promise<DatasetDetailResponse> => {
  console.log('开始获取数据集详情:', datasetId);
  try {
    const response = await axios.get(`${config.API_DATASETS_DETAIL}${datasetId}`);
    console.log('数据集详情获取完成');
    return response.data;
  } catch (error) {
    console.error('Failed to get dataset detail:', error);
    throw error;
  }
};
