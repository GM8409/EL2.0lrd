import axios from 'axios';
import config from '@/config';

export interface GeoDataItem {
  id: string;
  name: string;
  type: 'province' | 'city';
  path: string;
  province?: string;
}

export interface GeoJSONData {
  type: string;
  features: any[];
}

export interface GeoDataMap {
  China_provs: {
    [provinceName: string]: {
      json: string;
      二级区划: {
        [cityName: string]: string;
      };
    };
  };
}

export const getGeoDataMap = async (): Promise<GeoDataMap> => {
  console.log('开始加载地理数据映射表');
  try {
    const response = await axios.get(config.API_GEODATA_MAP_URL);
    console.log('地理数据映射表加载成功');
    return response.data;
  } catch (error) {
    console.error('Failed to load geo data map:', error);
    throw error;
  }
};

export const getGeoJSONData = async (path: string): Promise<GeoJSONData> => {
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

export const generateGeoDataUrl = (item: GeoDataItem): string => {
  return config.API_GEO_URL + item.path;
};

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

export const pathmap = config.pathmap;
