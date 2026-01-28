<template>
  <div id="map-container" class="h-full w-full"></div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

let map = null;
const mapContainer = ref(null);

const initMap = () => {
  const container = document.getElementById('map-container');
  if (!container) {
    console.error('Map container not found');
    return;
  }

  try {
    // 初始化地图
    map = L.map('map-container', {
      center: [34.3416, 108.9398], // 西安坐标
      zoom: 5,
    });

    // 尝试使用中国地图服务商插件
    if (typeof L.tileLayer.chinaProvider === 'function') {
      console.log('Using Chinese TMS Providers');
      // 添加底图图层
      const baseLayers = {
        '高德地图': L.tileLayer.chinaProvider('GaoDe.Normal.Map', {
          maxZoom: 18,
          minZoom: 3
        }),
        '高德卫星': L.tileLayer.chinaProvider('GaoDe.Satellite.Map', {
          maxZoom: 18,
          minZoom: 3
        }),
        'Google地图': L.tileLayer.chinaProvider('Google.Normal.Map', {
          maxZoom: 18,
          minZoom: 3
        }),
        'Google卫星': L.tileLayer.chinaProvider('Google.Satellite.Map', {
          maxZoom: 18,
          minZoom: 3
        })
      };

      // 添加默认图层
      baseLayers['高德地图'].addTo(map);

      // 添加图层控制
      L.control.layers(baseLayers).addTo(map);
    } else {
      console.warn('Chinese TMS Providers not available, using OpenStreetMap instead');
      // 使用OpenStreetMap作为备选
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(map);
    }
    // 安全添加全屏控件
    if (typeof L.control.fullscreen === 'function') {
      L.control.fullscreen().addTo(map);
    } else {
      console.warn('Fullscreen control not available');
    }
    // 添加绘制控件
    if (typeof L.Draw !== 'undefined') {
      const drawControl = new L.Control.Draw({
        draw: {
          polygon: true,
          polyline: false,
          rectangle: true,
          circle: false,
          marker: false
        },
        edit: {
          featureGroup: new L.FeatureGroup(),
          remove: true
        }
      });
      map.addControl(drawControl);

      // 监听绘制完成事件
      map.on('draw:created', function(e) {
        const layer = e.layer;
        // 可以在这里处理绘制的几何图形
        console.log('绘制完成:', layer.toGeoJSON());
      });
    }
    
    

    console.log('Map initialized successfully');
  } catch (error) {
    console.error('Error initializing map:', error);
  }
};

onMounted(() => {
  initMap();

  // 加载中国地图服务商插件
  const chinaProviderScript = document.createElement('script');
  chinaProviderScript.src = '/src/assets/leaflet.ChineseTmsProviders.js';
  document.body.appendChild(chinaProviderScript);

  // 动态加载Leaflet Draw插件
  const drawScript = document.createElement('script');
  drawScript.src = 'https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.2/leaflet.draw.js';
  document.body.appendChild(drawScript);

  const drawCss = document.createElement('link');
  drawCss.href = 'https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.2/leaflet.draw.css';
  drawCss.rel = 'stylesheet';
  document.head.appendChild(drawCss);

  // 动态加载Fullscreen插件
  const fullscreenScript = document.createElement('script');
  fullscreenScript.src = 'https://cdn.jsdelivr.net/npm/leaflet.fullscreen@3.0.0/Control.FullScreen.min.js';
  document.body.appendChild(fullscreenScript);

  const fullscreenCss = document.createElement('link');
  fullscreenCss.href = 'https://cdn.jsdelivr.net/npm/leaflet.fullscreen@3.0.0/Control.FullScreen.css';
  fullscreenCss.rel = 'stylesheet';
  document.head.appendChild(fullscreenCss);
});


onUnmounted(() => {
  if (map) {
    map.remove();
    map = null;
  }
});
</script>
