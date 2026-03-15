import {
  type GeoDataItem,
  type GeoJSONData,
  type GeoDataMap,
  getGeoDataMap,
  getGeoJSONData,
  generateGeoDataUrl
} from '@A/geodataApi';

export class GeoDataService {
  private static instance: GeoDataService;
  private provinces: GeoDataItem[] = [];
  private cities: GeoDataItem[] = [];
  private geoDataMap: GeoDataMap | null = null;
  private loaded: boolean = false;
  private isdebug: boolean;

  private constructor(debug: boolean = true) {
    this.isdebug = debug;
  }

  public static getInstance(): GeoDataService {
    if (!GeoDataService.instance) {
      GeoDataService.instance = new GeoDataService();
    }
    return GeoDataService.instance;
  }

  public async initialize(): Promise<void> {
    if (this.loaded) {
      console.log('GeoDataService already initialized');
      return;
    }

    try {
      console.log('Initializing GeoDataService...');
      await this.loadGeoDataMap();
      console.log('Geo data map loaded successfully');
      this.loadProvinces();
      console.log('Provinces loaded successfully');
      this.loadCities();
      console.log('Cities loaded successfully');
      this.loaded = true;
      console.log('GeoDataService initialized successfully');
    } catch (error) {
      console.error('Failed to initialize geo data service:', error);
      const errorMessage = error instanceof Error ? error.message : '未知错误';
      throw new Error(`地理数据服务初始化失败: ${errorMessage}`);
    }
  }

  public isInitialized(): boolean {
    return this.loaded;
  }

  public getInitializedStatus(): boolean {
    return this.loaded;
  }

  private async loadGeoDataMap(): Promise<void> {
    try {
      this.geoDataMap = await getGeoDataMap();
      if (this.isdebug) {
        console.log('Geo data map loaded successfully:', this.geoDataMap);
      }
    } catch (error) {
      console.error('Failed to load geo data map:', error);
      throw error;
    }
  }

  private loadProvinces(): void {
    if (!this.geoDataMap) return;

    const provinceNames = Object.keys(this.geoDataMap.China_provs);
    this.provinces = provinceNames.map((name, index) => ({
      id: `province_${index + 1}`,
      name,
      type: 'province' as const,
      path: `China_provs/${name}/${this.geoDataMap!.China_provs[name]!.json}`
    }));
    if (this.isdebug) {
      console.log('Provinces loaded successfully:', this.provinces);
    }
  }

  private loadCities(): void {
    if (!this.geoDataMap) return;

    let cityId = 1;
    Object.entries(this.geoDataMap.China_provs).forEach(([provinceName, provinceData]) => {
      Object.entries(provinceData.二级区划).forEach(([cityName, cityJson]) => {
        this.cities.push({
          id: `city_${cityId++}`,
          name: cityName,
          type: 'city' as const,
          path: `China_provs/${provinceName}/二级区划/${cityJson}`,
          province: provinceName
        });
      });
    });
    if (this.isdebug) {
      console.log('Cities loaded successfully:', this.cities);
    }
  }

  public search(query: string): GeoDataItem[] {
    if (!query || query.trim() === '') {
      return [];
    }

    const lowerQuery = query.toLowerCase().trim();
    const results: GeoDataItem[] = [];

    this.provinces.forEach(province => {
      if (province.name.toLowerCase().includes(lowerQuery)) {
        results.push(province);
      }
    });

    this.cities.forEach(city => {
      if (city.name.toLowerCase().includes(lowerQuery)) {
        results.push(city);
      }
    });

    const uniqueResults = this.removeDuplicates(results);
    return uniqueResults.slice(0, 10);
  }

  public async loadGeoJSONData(item: GeoDataItem): Promise<GeoJSONData> {
    try {
      const url = this.generateGeoDataUrl(item);
      const data = await getGeoJSONData(url);
      return data;
    } catch (error) {
      console.error(`Failed to load GeoJSON data for ${item.name}:`, error);
      return {
        type: 'FeatureCollection',
        features: []
      };
    }
  }

  public generateGeoDataUrl(item: GeoDataItem): string {
    return generateGeoDataUrl(item);
  }

  private removeDuplicates(items: GeoDataItem[]): GeoDataItem[] {
    const seen = new Set<string>();
    return items.filter(item => {
      const key = `${item.type}_${item.name}`;
      if (seen.has(key)) {
        return false;
      }
      seen.add(key);
      return true;
    });
  }

  public getProvinces(): GeoDataItem[] {
    return [...this.provinces];
  }

  public getCitiesByProvince(provinceName: string): GeoDataItem[] {
    return this.cities.filter(city => city.province === provinceName);
  }

  public getGeoDataItemByName(name: string): GeoDataItem | null {
    const province = this.provinces.find(p => p.name === name);
    if (province) {
      return province;
    }
    return this.cities.find(c => c.name === name) || null;
  }

  public getGeoDataMap(): GeoDataMap | null {
    return this.geoDataMap;
  }
}

export default GeoDataService.getInstance();
