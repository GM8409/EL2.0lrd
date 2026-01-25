<template>
  <div class="about container mx-auto px-4 py-8">
    <h1 class="text-4xl font-bold text-slate-800 mb-8">EarthLink 平台文档</h1>
    
    <!-- 文档导航 -->
    <div class="mb-8">
      <el-menu :default-active="activeDocSection" class="el-menu-demo" mode="horizontal">
        <el-menu-item index="overview">平台概览</el-menu-item>
        <el-menu-item index="features">核心功能</el-menu-item>
        <el-menu-item index="usage">使用指南</el-menu-item>
        <el-menu-item index="architecture">技术架构</el-menu-item>
        <el-menu-item index="faq">常见问题</el-menu-item>
      </el-menu>
    </div>
    
    <!-- 平台概览 -->
    <section id="overview" class="mb-12">
      <h2 class="text-2xl font-bold text-slate-700 mb-4">平台概览</h2>
      <div class="prose max-w-none">
        <p class="mb-4">EarthLink 是一款面向遥感数据处理的可视化平台，旨在简化遥感影像的获取、处理、分析与可视化流程，为用户提供直观、高效的地理空间数据解决方案。</p>
        <p class="mb-4">平台采用模块化设计，支持多种数据源接入，内置丰富的分析工具，可满足从科研到商业应用的各种需求。</p>
        <p class="mb-4">无论您是遥感领域的专业人士，还是初次接触地理空间数据的新手，EarthLink 都能为您提供便捷的工作流程和强大的分析能力。</p>
      </div>
    </section>
    
    <!-- 核心功能 -->
    <section id="features" class="mb-12">
      <h2 class="text-2xl font-bold text-slate-700 mb-4">核心功能</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="bg-white p-6 rounded-lg shadow-sm border border-slate-200">
          <h3 class="text-xl font-semibold text-slate-700 mb-3">遥感影像获取</h3>
          <p>支持多种遥感数据源接入，包括卫星影像、无人机航拍、地面传感器等，提供统一的数据获取接口。</p>
        </div>
        <div class="bg-white p-6 rounded-lg shadow-sm border border-slate-200">
          <h3 class="text-xl font-semibold text-slate-700 mb-3">自动化处理</h3>
          <p>内置多种图像处理算法，支持自动校正、融合、分类等操作，减少人工干预，提高处理效率。</p>
        </div>
        <div class="bg-white p-6 rounded-lg shadow-sm border border-slate-200">
          <h3 class="text-xl font-semibold text-slate-700 mb-3">智能分析</h3>
          <p>集成机器学习和深度学习模型，支持地物分类、变化检测、目标识别等高级分析功能。</p>
        </div>
        <div class="bg-white p-6 rounded-lg shadow-sm border border-slate-200">
          <h3 class="text-xl font-semibold text-slate-700 mb-3">可视化输出</h3>
          <p>提供丰富的可视化工具，支持多种地图投影和渲染方式，生成高质量的地图和分析报告。</p>
        </div>
      </div>
    </section>
    
    <!-- 使用指南 -->
    <section id="usage" class="mb-12">
      <h2 class="text-2xl font-bold text-slate-700 mb-4">使用指南</h2>
      <div class="prose max-w-none">
        <h3 class="text-xl font-semibold text-slate-700 mb-3">快速开始</h3>
        <ol class="list-decimal pl-6 mb-6">
          <li class="mb-2">登录平台或注册新账号</li>
          <li class="mb-2">在左侧导航栏选择「数据获取」模块</li>
          <li class="mb-2">选择数据源类型并设置参数</li>
          <li class="mb-2">点击「获取数据」按钮开始数据下载</li>
          <li class="mb-2">数据获取完成后，可在「数据管理」中查看和管理已获取的数据集</li>
        </ol>
        
        <h3 class="text-xl font-semibold text-slate-700 mb-3">基本操作流程</h3>
        <p class="mb-4">1. <strong>数据接入</strong>：通过平台提供的接口接入遥感数据</p>
        <p class="mb-4">2. <strong>数据处理</strong>：选择合适的处理工具对数据进行预处理</p>
        <p class="mb-4">3. <strong>数据分析</strong>：应用分析模型提取有价值的信息</p>
        <p class="mb-4">4. <strong>结果可视化</strong>：将分析结果以地图、图表等形式展示</p>
        <p class="mb-4">5. <strong>导出与分享</strong>：导出分析结果或生成报告分享给他人</p>
      </div>
    </section>
    
    <!-- 技术架构 -->
    <section id="architecture" class="mb-12">
      <h2 class="text-2xl font-bold text-slate-700 mb-4">技术架构</h2>
      <div class="bg-white p-6 rounded-lg shadow-sm border border-slate-200 mb-6">
        <h3 class="text-xl font-semibold text-slate-700 mb-3">系统架构</h3>
        <div class="overflow-x-auto">
          <pre class="bg-slate-100 p-4 rounded text-sm">
+------------------------+
|      前端界面层        |
| Vue 3 + Element Plus   |
+------------------------+
|      API 接口层        |
| FastAPI                |
+------------------------+
|     核心服务层         |
| 数据处理引擎           |
| 分析算法库             |
| 可视化渲染服务         |
+------------------------+
|      数据存储层        |
| 空间数据库             |
| 文件存储系统           |
+------------------------+
          </pre>
        </div>
      </div>
      
      <div class="prose max-w-none">
        <h3 class="text-xl font-semibold text-slate-700 mb-3">技术栈</h3>
        <ul class="list-disc pl-6 mb-4">
          <li class="mb-2"><strong>前端</strong>：Vue 3, TypeScript, Element Plus, Tailwind CSS</li>
          <li class="mb-2"><strong>后端</strong>：Python, FastAPI</li>
          <li class="mb-2"><strong>数据处理</strong>：GDAL, NumPy, SciPy</li>
          <li class="mb-2"><strong>分析算法</strong>：scikit-learn, TensorFlow</li>
          <li class="mb-2"><strong>可视化</strong>：Leaflet, ECharts</li>
          <li class="mb-2"><strong>存储</strong>：PostgreSQL/PostGIS, MinIO</li>
        </ul>
      </div>
    </section>
    
    <!-- 常见问题 -->
    <section id="faq" class="mb-12">
      <h2 class="text-2xl font-bold text-slate-700 mb-4">常见问题</h2>
      <el-collapse v-model="activeFaqItems">
        <el-collapse-item title="如何获取遥感影像数据？" name="1">
          <div class="prose">
            <p>您可以通过平台的「数据获取」模块，选择相应的数据源（如卫星、无人机等），设置区域范围、时间范围等参数后，点击「获取数据」按钮开始下载。平台支持多种常用遥感数据源，包括哨兵系列、Landsat系列等。</p>
          </div>
        </el-collapse-item>
        <el-collapse-item title="平台支持哪些数据格式？" name="2">
          <div class="prose">
            <p>平台支持多种常见的遥感数据格式，包括但不限于：GeoTIFF、ENVI、HDF、NetCDF等栅格数据格式，以及Shapefile、GeoJSON等矢量数据格式。平台会自动识别并处理这些格式的数据。</p>
          </div>
        </el-collapse-item>
        <el-collapse-item title="如何提高数据处理速度？" name="3">
          <div class="prose">
            <p>您可以通过以下方式提高数据处理速度：</p>
            <ol class="list-decimal pl-6">
              <li>适当降低数据分辨率或裁剪感兴趣区域</li>
              <li>选择合适的处理算法和参数</li>
              <li>利用平台的批处理功能，在非高峰时段处理大量数据</li>
              <li>对于特别大的数据集，考虑使用平台的分布式处理能力</li>
            </ol>
          </div>
        </el-collapse-item>
        <el-collapse-item title="分析结果如何导出和分享？" name="4">
          <div class="prose">
            <p>平台支持多种导出格式，包括：</p>
            <ul class="list-disc pl-6">
              <li>栅格数据：GeoTIFF、PNG、JPEG</li>
              <li>矢量数据：Shapefile、GeoJSON、KML</li>
              <li>分析报告：PDF、HTML、Markdown</li>
            </ul>
            <p>您可以通过「导出」按钮选择相应的格式，也可以生成分享链接直接分享给他人。</p>
          </div>
        </el-collapse-item>
      </el-collapse>
    </section>
    
    <!-- 联系我们 -->
    <section class="mb-8">
      <h2 class="text-2xl font-bold text-slate-700 mb-4">联系我们</h2>
      <div class="prose max-w-none">
        <p class="mb-4">如果您在使用过程中遇到任何问题，或有任何建议和意见，欢迎通过以下方式联系我们：</p>
        <ul class="list-disc pl-6 mb-4">
          <li class="mb-2">邮箱：support@earthlink.com</li>
          <li class="mb-2">电话：400-123-4567</li>
          <li class="mb-2">在线支持：登录平台后点击右下角「在线客服」</li>
          <li class="mb-2">社区论坛：<a href="#" class="text-blue-600 hover:underline">https://forum.earthlink.com</a></li>
        </ul>
        <p class="font-semibold">我们的技术团队将在24小时内响应您的问题。</p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// 文档导航激活项
const activeDocSection = ref('overview')

// FAQ 激活项
const activeFaqItems = ref(['1'])
</script>

<style scoped>
.about {
  min-height: 100vh;
}
</style>