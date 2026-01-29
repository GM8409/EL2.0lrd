<template>
  <div class="about-container">
    <!-- 顶部英雄区域 -->
    <section class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">🌍 EarthLink 平台</h1>
        <p class="hero-subtitle">遥感影像处理的终极解决方案</p>
        <p class="hero-description">强大、灵活、高效的地理空间数据分析平台</p>
      </div>
    </section>

    <!-- 导航菜单 -->
    <nav class="sticky-nav">
      <div class="nav-container">
        <div class="nav-menu">
          <a 
            v-for="item in navItems" 
            :key="item.id"
            :href="`#${item.id}`"
            class="nav-item"
            :class="{ active: activeDocSection === item.id }"
            @click="scrollToSection(item.id)"
          >
            {{ item.label }}
          </a>
        </div>
      </div>
    </nav>

    <!-- 主容器 -->
    <div class="content-wrapper">
      <!-- 平台概览 -->
      <section id="overview" class="content-section">
        <div class="section-header">
          <h2 class="section-title">📊 平台概览</h2>
          <p class="section-subtitle">了解 EarthLink 的核心优势</p>
        </div>
        <div class="overview-grid">
          <div class="overview-card">
            <p>EarthLink 是一款面向遥感数据处理的可视化平台，旨在简化遥感影像的获取、处理、分析与可视化流程，为用户提供直观、高效的地理空间数据解决方案。</p>
          </div>
          <div class="overview-card">
            <p>平台采用模块化设计，支持多种数据源接入，内置丰富的分析工具，可满足从科研到商业应用的各种需求。</p>
          </div>
          <div class="overview-card">
            <p>无论您是遥感领域的专业人士，还是初次接触地理空间数据的新手，EarthLink 都能为您提供便捷的工作流程和强大的分析能力。</p>
          </div>
        </div>
      </section>
      
      <!-- 核心功能 -->
      <section id="features" class="content-section">
        <div class="section-header">
          <h2 class="section-title">⚡ 核心功能</h2>
          <p class="section-subtitle">强大的功能模块，满足各种需求</p>
        </div>
        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">🛰️</div>
            <h3 class="feature-title">遥感影像获取</h3>
            <p class="feature-description">支持多种遥感数据源接入，包括卫星影像、无人机航拍、地面传感器等，提供统一的数据获取接口。</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">⚙️</div>
            <h3 class="feature-title">自动化处理</h3>
            <p class="feature-description">内置多种图像处理算法，支持自动校正、融合、分类等操作，减少人工干预，提高处理效率。</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <h3 class="feature-title">智能分析</h3>
            <p class="feature-description">集成机器学习和深度学习模型，支持地物分类、变化检测、目标识别等高级分析功能。</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">📈</div>
            <h3 class="feature-title">可视化输出</h3>
            <p class="feature-description">提供丰富的可视化工具，支持多种地图投影和渲染方式，生成高质量的地图和分析报告。</p>
          </div>
        </div>
      </section>
      
      <!-- 使用指南 -->
      <section id="usage" class="content-section">
        <div class="section-header">
          <h2 class="section-title">📖 使用指南</h2>
          <p class="section-subtitle">快速上手，轻松开始</p>
        </div>
        
        <div class="guide-container">
          <div class="guide-section">
            <h3 class="guide-heading">🚀 快速开始</h3>
            <ol class="guide-list">
              <li>登录平台或注册新账号</li>
              <li>在左侧导航栏选择「数据获取」模块</li>
              <li>选择数据源类型并设置参数</li>
              <li>点击「获取数据」按钮开始数据下载</li>
              <li>数据获取完成后，可在「数据管理」中查看和管理已获取的数据集</li>
            </ol>
          </div>
          
          <div class="guide-section">
            <h3 class="guide-heading">🔄 基本操作流程</h3>
            <div class="workflow-diagram">
              <div class="workflow-step">
                <span class="step-num">1</span>
                <span class="step-name">数据接入</span>
              </div>
              <div class="workflow-arrow">→</div>
              <div class="workflow-step">
                <span class="step-num">2</span>
                <span class="step-name">数据处理</span>
              </div>
              <div class="workflow-arrow">→</div>
              <div class="workflow-step">
                <span class="step-num">3</span>
                <span class="step-name">数据分析</span>
              </div>
              <div class="workflow-arrow">→</div>
              <div class="workflow-step">
                <span class="step-num">4</span>
                <span class="step-name">结果可视化</span>
              </div>
              <div class="workflow-arrow">→</div>
              <div class="workflow-step">
                <span class="step-num">5</span>
                <span class="step-name">导出分享</span>
              </div>
            </div>
          </div>
        </div>
      </section>
      
      <!-- 技术架构 -->
      <section id="architecture" class="content-section">
        <div class="section-header">
          <h2 class="section-title">🏗️ 技术架构</h2>
          <p class="section-subtitle">专业的技术方案</p>
        </div>
        
        <div class="architecture-container">
          <div class="architecture-diagram">
            <div class="arch-layer">
              <div class="arch-label">前端界面层</div>
              <p>Vue 3 + TypeScript + Element Plus</p>
            </div>
            <div class="arch-arrow">⬇️</div>
            <div class="arch-layer">
              <div class="arch-label">API 接口层</div>
              <p>FastAPI + Python</p>
            </div>
            <div class="arch-arrow">⬇️</div>
            <div class="arch-layer">
              <div class="arch-label">核心服务层</div>
              <p>数据处理 | 分析算法 | 可视化渲染</p>
            </div>
            <div class="arch-arrow">⬇️</div>
            <div class="arch-layer">
              <div class="arch-label">数据存储层</div>
              <p>PostgreSQL/PostGIS | MinIO</p>
            </div>
          </div>
        </div>

        <div class="tech-stack">
          <h3 class="stack-title">📚 技术栈</h3>
          <div class="stack-grid">
            <div class="stack-item">
              <span class="stack-label">前端</span>
              <span class="stack-value">Vue 3 • TypeScript • Element Plus • Tailwind CSS</span>
            </div>
            <div class="stack-item">
              <span class="stack-label">后端</span>
              <span class="stack-value">Python • FastAPI</span>
            </div>
            <div class="stack-item">
              <span class="stack-label">数据处理</span>
              <span class="stack-value">GDAL • NumPy • SciPy</span>
            </div>
            <div class="stack-item">
              <span class="stack-label">分析算法</span>
              <span class="stack-value">scikit-learn • TensorFlow</span>
            </div>
            <div class="stack-item">
              <span class="stack-label">可视化</span>
              <span class="stack-value">Leaflet • ECharts</span>
            </div>
            <div class="stack-item">
              <span class="stack-label">存储</span>
              <span class="stack-value">PostgreSQL/PostGIS • MinIO</span>
            </div>
          </div>
        </div>
      </section>
      
      <!-- 常见问题 -->
      <section id="faq" class="content-section">
        <div class="section-header">
          <h2 class="section-title">❓ 常见问题</h2>
          <p class="section-subtitle">快速找到您关心的问题答案</p>
        </div>
        <div class="faq-container">
          <div 
            v-for="(item, index) in faqItems" 
            :key="index"
            class="faq-item"
            :class="{ expanded: expandedFaq === index }"
            @click="expandedFaq = expandedFaq === index ? -1 : index"
          >
            <div class="faq-question">
              <span class="faq-icon">{{ expandedFaq === index ? '▼' : '▶' }}</span>
              <span class="faq-text">{{ item.question }}</span>
            </div>
            <div v-if="expandedFaq === index" class="faq-answer">
              {{ item.answer }}
            </div>
          </div>
        </div>
      </section>
      
      <!-- 联系我们 -->
      <section id="contact" class="content-section">
        <div class="section-header">
          <h2 class="section-title">📧 联系我们</h2>
          <p class="section-subtitle">我们随时准备为您服务</p>
        </div>
        <div class="contact-grid">
          <div class="contact-card">
            <div class="contact-icon">✉️</div>
            <h3>邮箱</h3>
            <p>114514@163.com</p>
          </div>
          <div class="contact-card">
            <div class="contact-icon">📞</div>
            <h3>电话</h3>
            <p>13999999999</p>
          </div>
          <div class="contact-card">
            <div class="contact-icon">💬</div>
            <h3>在线客服</h3>
            <p>登录平台后点击右下角</p>
          </div>
          <div class="contact-card">
            <div class="contact-icon">🌐</div>
            <h3>社区论坛</h3>
            <p>暂无</p>
          </div>
        </div>
        <p class="contact-note">💡 我们的技术团队将在 24 小时内响应您的问题</p>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// 导航项目
const navItems = [
  { id: 'overview', label: '📊 平台概览' },
  { id: 'features', label: '⚡ 核心功能' },
  { id: 'usage', label: '📖 使用指南' },
  { id: 'architecture', label: '🏗️ 技术架构' },
  { id: 'faq', label: '❓ 常见问题' },
  { id: 'contact', label: '📧 联系我们' }
]

// 文档导航激活项
const activeDocSection = ref('overview')

// FAQ 展开项
const expandedFaq = ref(0)

// 平滑滚动到指定栏目
const scrollToSection = (sectionId) => {
  activeDocSection.value = sectionId
  const element = document.getElementById(sectionId)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

// FAQ 数据
const faqItems = [
  {
    question: '如何获取遥感影像数据？',
    answer: '您可以通过平台的「数据获取」模块，选择相应的数据源（如卫星、无人机等），设置区域范围、时间范围等参数后，点击「获取数据」按钮开始下载。平台支持多种常用遥感数据源，包括哨兵系列、Landsat系列等。'
  },
  {
    question: '平台支持哪些数据格式？',
    answer: '平台支持多种常见的遥感数据格式，包括但不限于：GeoTIFF、ENVI、HDF、NetCDF等栅格数据格式，以及Shapefile、GeoJSON等矢量数据格式。平台会自动识别并处理这些格式的数据。'
  },
  {
    question: '如何提高数据处理速度？',
    answer: '您可以通过以下方式提高数据处理速度：1. 适当降低数据分辨率或裁剪感兴趣区域 2. 选择合适的处理算法和参数 3. 利用平台的批处理功能，在非高峰时段处理大量数据 4. 对于特别大的数据集，考虑使用平台的分布式处理能力'
  },
  {
    question: '分析结果如何导出和分享？',
    answer: '平台支持多种导出格式：栅格数据（GeoTIFF、PNG、JPEG）、矢量数据（Shapefile、GeoJSON、KML）、分析报告（PDF、HTML、Markdown）。您可以通过「导出」按钮选择相应的格式，也可以生成分享链接直接分享给他人。'
  }
]
</script>

<style scoped>
.about-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

/* ========== 英雄区域 ========== */
.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 80px 32px;
  text-align: center;
  animation: fadeIn 0.8s ease-out;
}

.hero-title {
  font-size: 48px;
  font-weight: bold;
  margin-bottom: 12px;
  animation: slideDown 0.8s ease-out;
}

.hero-subtitle {
  font-size: 24px;
  margin-bottom: 8px;
  opacity: 0.95;
  animation: slideDown 0.8s ease-out 0.1s both;
}

.hero-description {
  font-size: 16px;
  opacity: 0.85;
  animation: slideDown 0.8s ease-out 0.2s both;
}

/* ========== 导航栏 ========== */
.sticky-nav {
  position: fixed;
  top: 70px;
  left: 0;
  right: 0;
  background: white;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  z-index: 100;
  padding: 0;
}

.nav-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 32px;
}

.nav-menu {
  display: flex;
  gap: 0;
  flex-wrap: wrap;
}

.nav-item {
  padding: 16px 20px;
  color: #666;
  text-decoration: none;
  font-weight: 500;
  font-size: 14px;
  transition: all 0.3s ease;
  border-bottom: 3px solid transparent;
  cursor: pointer;
}

.nav-item:hover {
  color: #667eea;
  background: #f5f7fa;
}

.nav-item.active {
  color: #667eea;
  border-bottom-color: #667eea;
}

/* ========== 内容包装 ========== */
.content-wrapper {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 32px;
}

/* ========== 内容区域通用 ========== */
.content-section {
  background: white;
  padding: 60px 48px;
  margin-bottom: 32px;
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.05);
  animation: slideUp 0.6s ease-out;
}

.section-header {
  text-align: center;
  margin-bottom: 48px;
}

.section-title {
  font-size: 32px;
  font-weight: bold;
  color: #333;
  margin-bottom: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.section-subtitle {
  font-size: 16px;
  color: #999;
}

/* ========== 概览卡片 ========== */
.overview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
}

.overview-card {
  background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 100%);
  padding: 32px;
  border-radius: 12px;
  border: 1px solid rgba(102, 126, 234, 0.1);
  line-height: 1.8;
  color: #555;
  transition: all 0.3s ease;
  cursor: pointer;
}

.overview-card:hover {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(102, 126, 234, 0.25);
}

/* ========== 功能卡片 ========== */
.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
}

.feature-card {
  background: white;
  padding: 32px 24px;
  border-radius: 12px;
  border: 1px solid #e8e8e8;
  text-align: center;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.feature-card:hover {
  border-color: #667eea;
  box-shadow: 0 12px 32px rgba(102, 126, 234, 0.15);
  transform: translateY(-8px);
}

.feature-icon {
  font-size: 48px;
  margin-bottom: 16px;
  display: inline-block;
  animation: bounce 2s infinite;
}

.feature-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 12px;
}

.feature-description {
  color: #666;
  line-height: 1.6;
  font-size: 14px;
}

/* ========== 使用指南 ========== */
.guide-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 32px;
}

.guide-section {
  background: #f8f9fa;
  padding: 32px;
  border-radius: 12px;
  border-left: 4px solid #667eea;
}

.guide-heading {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
}

.guide-list {
  list-style: none;
  padding: 0;
  counter-reset: step-counter;
}

.guide-list li {
  counter-increment: step-counter;
  margin-bottom: 14px;
  padding-left: 32px;
  position: relative;
  color: #666;
  line-height: 1.6;
}

.guide-list li::before {
  content: counter(step-counter);
  position: absolute;
  left: 0;
  top: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 12px;
}

/* 工作流图 */
.workflow-diagram {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 24px;
  overflow-x: auto;
  padding: 12px 0;
}

.workflow-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  min-width: 100px;
  padding: 16px 12px;
  background: white;
  border: 2px solid #667eea;
  border-radius: 8px;
  text-align: center;
}

.step-num {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 14px;
}

.step-name {
  font-size: 12px;
  font-weight: 600;
  color: #333;
}

.workflow-arrow {
  font-size: 20px;
  color: #667eea;
  font-weight: bold;
}

/* ========== 技术架构 ========== */
.architecture-container {
  background: #f8f9fa;
  padding: 32px;
  border-radius: 12px;
  margin-bottom: 32px;
}

.architecture-diagram {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.arch-layer {
  background: white;
  padding: 20px;
  border-radius: 8px;
  border-left: 4px solid #667eea;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.arch-label {
  font-weight: bold;
  color: #667eea;
  font-size: 14px;
  margin-bottom: 8px;
}

.arch-layer p {
  color: #666;
  margin: 0;
  font-size: 13px;
}

.arch-arrow {
  text-align: center;
  color: #667eea;
  font-size: 20px;
  margin: 8px 0;
}

/* 技术栈 */
.tech-stack {
  background: #f8f9fa;
  padding: 32px;
  border-radius: 12px;
}

.stack-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 24px;
}

.stack-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 16px;
}

.stack-item {
  background: white;
  padding: 18px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  border: 1px solid #e8e8e8;
}

.stack-label {
  font-weight: bold;
  color: #667eea;
  font-size: 13px;
}

.stack-value {
  color: #666;
  font-size: 13px;
  line-height: 1.5;
}

/* ========== FAQ ========== */
.faq-container {
  display: grid;
  gap: 12px;
}

.faq-item {
  background: #f8f9fa;
  border: 1px solid #e8e8e8;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
}

.faq-item:hover {
  border-color: #667eea;
  background: white;
}

.faq-item.expanded {
  background: white;
  border-color: #667eea;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.1);
}

.faq-question {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  font-weight: 600;
  color: #333;
  user-select: none;
}

.faq-icon {
  color: #667eea;
  font-weight: bold;
  transition: transform 0.3s ease;
}

.faq-item.expanded .faq-icon {
  color: #667eea;
}

.faq-text {
  flex: 1;
}

.faq-answer {
  padding: 0 20px 16px 48px;
  color: #666;
  line-height: 1.8;
  animation: slideDown 0.3s ease-out;
}

/* ========== 联系我们 ========== */
.contact-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.contact-card {
  background: white;
  padding: 32px 24px;
  border-radius: 12px;
  text-align: center;
  border: 1px solid #e8e8e8;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.contact-card:hover {
  border-color: #667eea;
  box-shadow: 0 12px 32px rgba(102, 126, 234, 0.15);
  transform: translateY(-8px);
}

.contact-icon {
  font-size: 48px;
  margin-bottom: 16px;
  display: inline-block;
  animation: bounce 2s infinite;
}

.contact-card h3 {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
}

.contact-card p {
  color: #666;
  font-size: 14px;
  margin: 0;
}

.contact-note {
  text-align: center;
  color: #667eea;
  font-weight: 600;
  padding: 16px;
  background: rgba(102, 126, 234, 0.05);
  border-radius: 8px;
  border: 1px solid rgba(102, 126, 234, 0.1);
}

/* ========== 动画 ========== */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-8px);
  }
}

/* ========== 响应式设计 ========== */
@media (max-width: 1024px) {
  .hero-section {
    padding: 60px 24px;
  }

  .hero-title {
    font-size: 36px;
  }

  .hero-subtitle {
    font-size: 20px;
  }

  .content-section {
    padding: 40px 32px;
    margin-bottom: 24px;
  }

  .section-title {
    font-size: 28px;
  }

  .guide-container {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .about-container {
    background: linear-gradient(135deg, #f5f7fa 0%, #e0e7ff 100%);
  }

  .hero-section {
    padding: 48px 16px;
  }

  .hero-title {
    font-size: 28px;
  }

  .hero-subtitle {
    font-size: 18px;
  }

  .nav-container {
    padding: 0 16px;
  }

  .nav-item {
    padding: 12px 16px;
    font-size: 13px;
  }

  .content-wrapper {
    padding: 0 16px;
  }

  .content-section {
    padding: 32px 24px;
    margin-bottom: 16px;
  }

  .section-header {
    margin-bottom: 32px;
  }

  .section-title {
    font-size: 24px;
  }

  .section-subtitle {
    font-size: 14px;
  }

  .overview-grid,
  .features-grid,
  .contact-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .workflow-diagram {
    flex-direction: column;
    gap: 8px;
  }

  .workflow-arrow {
    transform: rotate(90deg);
    margin: 0;
  }

  .stack-grid {
    grid-template-columns: 1fr;
  }

  .faq-answer {
    padding-left: 36px;
  }
}

@media (max-width: 480px) {
  .hero-section {
    padding: 32px 12px;
  }

  .hero-title {
    font-size: 22px;
  }

  .hero-subtitle {
    font-size: 16px;
  }

  .hero-description {
    font-size: 14px;
  }

  .nav-menu {
    overflow-x: auto;
    scroll-behavior: smooth;
  }

  .nav-item {
    padding: 12px 12px;
    font-size: 12px;
    white-space: nowrap;
  }

  .content-section {
    padding: 24px 16px;
    border-radius: 12px;
  }

  .section-title {
    font-size: 20px;
  }

  .section-subtitle {
    font-size: 13px;
  }

  .section-header {
    margin-bottom: 24px;
  }

  .feature-card {
    padding: 20px 16px;
  }

  .feature-icon {
    font-size: 36px;
  }

  .guide-list li {
    padding-left: 28px;
  }

  .guide-list li::before {
    width: 22px;
    height: 22px;
    font-size: 11px;
  }
}
</style>