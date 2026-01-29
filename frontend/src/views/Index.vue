<template>
  <div class="index-container">
    <!-- 顶部英雄区域 -->
    <section class="hero-banner">
      <div class="hero-overlay"></div>
      <div class="hero-content">
        <h1 class="hero-title">🌍 欢迎使用 EarthLink</h1>
        <p class="hero-subtitle">遥感影像处理的终极解决方案</p>
        <p class="hero-description">
          无需代码，快速完成遥感影像获取、处理、分析与可视化
        </p>
        <div class="hero-buttons">
          <button class="btn btn-primary">
            <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
            </svg>
            快速开始
          </button>
          <button class="btn btn-secondary">
            <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            了解更多
          </button>
        </div>
      </div>
    </section>

    <!-- 主容器 -->
    <div class="content-container">
      <!-- 功能特性区域 -->
      <section class="features-section">
        <div class="section-header">
          <h2 class="section-title">✨ 核心功能</h2>
          <p class="section-subtitle">强大功能，助力您的遥感分析</p>
        </div>
        
        <div class="features-grid">
          <div class="feature-item">
            <div class="feature-icon">🛰️</div>
            <h3>遥感影像获取</h3>
            <p>支持多种数据源，包括卫星影像、无人机航拍、地面传感器等</p>
          </div>
          <div class="feature-item">
            <div class="feature-icon">⚙️</div>
            <h3>自动化处理</h3>
            <p>内置多种算法，支持自动校正、融合、分类等操作</p>
          </div>
          <div class="feature-item">
            <div class="feature-icon">🤖</div>
            <h3>智能分析</h3>
            <p>集成机器学习模型，支持分类、变化检测、目标识别</p>
          </div>
          <div class="feature-item">
            <div class="feature-icon">📊</div>
            <h3>可视化输出</h3>
            <p>丰富的地图工具，生成高质量的地图和分析报告</p>
          </div>
          <div class="feature-item">
            <div class="feature-icon">⚡</div>
            <h3>高效处理</h3>
            <p>云计算架构，快速处理海量遥感数据</p>
          </div>
          <div class="feature-item">
            <div class="feature-icon">🔧</div>
            <h3>易于使用</h3>
            <p>无需编程，拖拽式工作流设计，人人可用</p>
          </div>
        </div>
      </section>

      <!-- 技术优势 -->
      <section class="advantages-section">
        <div class="advantages-content">
          <div class="advantages-text">
            <h2 class="section-title">🚀 技术优势</h2>
            <p class="section-subtitle">专业的技术方案，卓越的用户体验</p>
            <ul class="advantages-list">
              <li>✅ 云计算架构，高效并行处理</li>
              <li>✅ 专业算法库，覆盖多种应用</li>
              <li>✅ 直观的可视化界面</li>
              <li>✅ 灵活的工作流设计</li>
              <li>✅ 完整的数据管理体系</li>
              <li>✅ 强大的可视化能力</li>
            </ul>
          </div>
          <div class="advantages-visual">
            <div class="tech-card">
              <h4>前端技术</h4>
              <p>Vue 3 • TypeScript • Element Plus</p>
            </div>
            <div class="tech-card">
              <h4>后端技术</h4>
              <p>Python • FastAPI • PostgreSQL</p>
            </div>
            <div class="tech-card">
              <h4>数据处理</h4>
              <p>GDAL • NumPy • SciPy</p>
            </div>
            <div class="tech-card">
              <h4>智能分析</h4>
              <p>TensorFlow • scikit-learn</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 应用场景 -->
      <section class="applications-section">
        <div class="section-header">
          <h2 class="section-title">🎯 应用场景</h2>
          <p class="section-subtitle">广泛应用于各个领域</p>
        </div>
        
        <div class="applications-grid">
          <div class="app-card">
            <div class="app-icon">🌱</div>
            <h3>农业管理</h3>
            <p>监测作物生长情况，评估产量预报，优化农业管理</p>
          </div>
          <div class="app-card">
            <div class="app-icon">🌳</div>
            <h3>环境监测</h3>
            <p>森林覆盖监测，水质污染检测，生态环境保护</p>
          </div>
          <div class="app-card">
            <div class="app-icon">🏙️</div>
            <h3>城市规划</h3>
            <p>城市扩展分析，土地利用规划，基础设施监测</p>
          </div>
          <div class="app-card">
            <div class="app-icon">⚠️</div>
            <h3>灾害管理</h3>
            <p>洪水监测预警，地震灾害评估，灾后重建评价</p>
          </div>
          <div class="app-card">
            <div class="app-icon">🔍</div>
            <h3>资源调查</h3>
            <p>矿产资源勘查，地质灾害评估，自然资源管理</p>
          </div>
          <div class="app-card">
            <div class="app-icon">📡</div>
            <h3>科学研究</h3>
            <p>气候变化研究，地表形态分析，科学数据挖掘</p>
          </div>
        </div>
      </section>

      <!-- 平台特点 -->
      <section class="highlights-section">
        <div class="section-header">
          <h2 class="section-title">⭐ 为什么选择 EarthLink</h2>
          <p class="section-subtitle">业界领先的解决方案</p>
        </div>
        
        <div class="highlights-grid">
          <div class="highlight-box">
            <h3>🎨 可视化设计</h3>
            <p>直观的界面设计，让复杂的分析变得简单易用</p>
          </div>
          <div class="highlight-box">
            <h3>⚡ 性能卓越</h3>
            <p>高效的算法优化，快速处理大规模数据</p>
          </div>
          <div class="highlight-box">
            <h3>🔒 安全可靠</h3>
            <p>企业级安全保障，确保数据隐私与系统稳定</p>
          </div>
          <div class="highlight-box">
            <h3>🤝 专业支持</h3>
            <p>完善的技术支持和详细的文档指导</p>
          </div>
          <div class="highlight-box">
            <h3>🌐 开放协作</h3>
            <p>支持多种数据格式，易于集成与扩展</p>
          </div>
          <div class="highlight-box">
            <h3>💡 持续创新</h3>
            <p>不断更新功能，引入最新技术与算法</p>
          </div>
        </div>
      </section>

      <!-- 快速开始 -->
      <section class="quickstart-section">
        <div class="section-header">
          <h2 class="section-title">🚀 快速开始</h2>
          <p class="section-subtitle">三步开启您的遥感分析之旅</p>
        </div>
        
        <div class="steps-container">
          <div class="step-box">
            <div class="step-number">1</div>
            <h3>注册账号</h3>
            <p>点击快速开始，注册您的账号，获得平台访问权限</p>
          </div>
          <div class="step-arrow">→</div>
          <div class="step-box">
            <div class="step-number">2</div>
            <h3>导入数据</h3>
            <p>选择数据源，设置参数，一键导入遥感影像</p>
          </div>
          <div class="step-arrow">→</div>
          <div class="step-box">
            <div class="step-number">3</div>
            <h3>开始分析</h3>
            <p>使用工作流工具，进行数据处理和分析</p>
          </div>
        </div>
      </section>

      <!-- 推荐语 -->
      <section class="testimonials-section">
        <div class="section-header">
          <h2 class="section-title">💬 用户评价</h2>
        </div>
        
        <div class="testimonials-grid">
          <div class="testimonial-card">
            <div class="stars">⭐⭐⭐⭐⭐</div>
            <p>"EarthLink 让遥感数据分析变得前所未有的简单，大大提高了我们的工作效率。"</p>
            <p class="author">—— 某科研机构负责人</p>
          </div>
          <div class="testimonial-card">
            <div class="stars">⭐⭐⭐⭐⭐</div>
            <p>"无需编程即可完成复杂分析，这正是我们一直寻找的解决方案。"</p>
            <p class="author">—— 某农业公司技术总监</p>
          </div>
          <div class="testimonial-card">
            <div class="stars">⭐⭐⭐⭐⭐</div>
            <p>"专业的技术团队，完善的功能，强烈推荐给所有需要遥感分析的团队。"</p>
            <p class="author">—— 某地方政府规划部门</p>
          </div>
        </div>
      </section>

      <!-- 底部 CTA -->
      <section class="cta-section">
        <h2>准备好开始了吗？</h2>
        <p>加入数千个使用 EarthLink 的组织，开启遥感数据分析之旅</p>
        <button class="btn btn-primary btn-lg">立即开始免费试用</button>
      </section>
    </div>
  </div>
</template><script setup>
import { ref } from 'vue'

const scrollPosition = ref(0)
</script>

<style scoped>
.index-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

/* ========== 英雄区域 ========== */
.hero-banner {
  position: relative;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 100px 32px;
  text-align: center;
  overflow: hidden;
  min-height: 600px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 20% 80%, rgba(255, 255, 255, 0.15) 0%, transparent 50%),
              radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
  z-index: 0;
}

.hero-content {
  position: relative;
  z-index: 1;
  max-width: 600px;
  animation: fadeInUp 0.8s ease-out;
}

.hero-title {
  font-size: 52px;
  font-weight: bold;
  margin-bottom: 16px;
  animation: slideDown 0.8s ease-out;
}

.hero-subtitle {
  font-size: 24px;
  margin-bottom: 12px;
  opacity: 0.95;
  animation: slideDown 0.8s ease-out 0.1s both;
}

.hero-description {
  font-size: 16px;
  margin-bottom: 36px;
  opacity: 0.85;
  animation: slideDown 0.8s ease-out 0.2s both;
}

.hero-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
  animation: slideUp 0.8s ease-out 0.3s both;
}

/* 按钮样式 */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 32px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
}

.btn-icon {
  width: 20px;
  height: 20px;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 30px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.5);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.3);
  border-color: white;
}

.btn-lg {
  padding: 16px 48px;
  font-size: 18px;
}

/* ========== 内容容器 ========== */
.content-container {
  max-width: 1400px;
  margin: -60px auto 0;
  padding: 0 32px;
  position: relative;
  z-index: 10;
}

/* ========== 区段通用 ========== */
.features-section,
.advantages-section,
.applications-section,
.highlights-section,
.quickstart-section,
.testimonials-section {
  background: white;
  padding: 60px 48px;
  margin-bottom: 32px;
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.05);
  animation: fadeInUp 0.6s ease-out;
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

/* ========== 功能特性 ========== */
.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
}

.feature-item {
  padding: 32px 24px;
  border: 1px solid #e8e8e8;
  border-radius: 12px;
  text-align: center;
  transition: all 0.3s ease;
  background: white;
}

.feature-item:hover {
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

.feature-item h3 {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 12px;
}

.feature-item p {
  color: #666;
  line-height: 1.6;
  font-size: 14px;
}

/* ========== 技术优势 ========== */
.advantages-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 48px;
  align-items: center;
}

.advantages-text {
  flex: 1;
}

.advantages-list {
  list-style: none;
  padding: 0;
}

.advantages-list li {
  padding: 12px 0;
  color: #666;
  font-size: 15px;
  line-height: 1.8;
}

.advantages-visual {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.tech-card {
  background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 100%);
  padding: 24px;
  border-radius: 12px;
  border: 1px solid rgba(102, 126, 234, 0.1);
  text-align: center;
  transition: all 0.3s ease;
}

.tech-card:hover {
  border-color: #667eea;
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.12);
  transform: translateY(-4px);
}

.tech-card h4 {
  color: #667eea;
  font-weight: bold;
  margin-bottom: 8px;
}

.tech-card p {
  color: #666;
  font-size: 13px;
}

/* ========== 应用场景 ========== */
.applications-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
}

.app-card {
  background: linear-gradient(135deg, #f8f9fa 0%, #f0f2f5 100%);
  padding: 32px 24px;
  border-radius: 12px;
  text-align: center;
  border: 1px solid #e8e8e8;
  transition: all 0.3s ease;
}

.app-card:hover {
  background: white;
  border-color: #667eea;
  box-shadow: 0 12px 32px rgba(102, 126, 234, 0.15);
  transform: translateY(-8px);
}

.app-icon {
  font-size: 48px;
  margin-bottom: 16px;
  display: inline-block;
  animation: bounce 2s infinite;
}

.app-card h3 {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 12px;
}

.app-card p {
  color: #666;
  font-size: 14px;
  line-height: 1.6;
}

/* ========== 平台特点 ========== */
.highlights-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
}

.highlight-box {
  padding: 32px 24px;
  background: linear-gradient(135deg, #f8f9fa 0%, #f5f7fa 100%);
  border: 1px solid rgba(102, 126, 234, 0.1);
  border-radius: 12px;
  text-align: center;
  transition: all 0.3s ease;
}

.highlight-box:hover {
  border-color: #667eea;
  background: white;
  box-shadow: 0 12px 32px rgba(102, 126, 234, 0.12);
  transform: translateY(-4px);
}

.highlight-box h3 {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 12px;
}

.highlight-box p {
  color: #666;
  font-size: 14px;
  line-height: 1.6;
}

/* ========== 快速开始 ========== */
.steps-container {
  display: flex;
  align-items: center;
  gap: 24px;
  justify-content: center;
  flex-wrap: wrap;
  padding: 24px;
}

.step-box {
  flex: 0 1 200px;
  padding: 32px 24px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 100%);
  border: 2px solid #667eea;
  border-radius: 12px;
  text-align: center;
  transition: all 0.3s ease;
}

.step-box:hover {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(102, 126, 234, 0.25);
}

.step-box:hover .step-number {
  background: white;
  color: #667eea;
  transform: scale(1.1);
}

.step-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 50%;
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 16px;
  transition: all 0.3s ease;
}

.step-box h3 {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 12px;
}

.step-box p {
  font-size: 14px;
  line-height: 1.6;
}

.step-arrow {
  font-size: 32px;
  color: #667eea;
  font-weight: bold;
}

/* ========== 用户评价 ========== */
.testimonials-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
}

.testimonial-card {
  padding: 32px;
  background: white;
  border: 1px solid #e8e8e8;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.testimonial-card:hover {
  border-color: #667eea;
  box-shadow: 0 12px 32px rgba(102, 126, 234, 0.12);
  transform: translateY(-4px);
}

.stars {
  font-size: 18px;
  margin-bottom: 12px;
}

.testimonial-card p {
  color: #666;
  line-height: 1.8;
  margin-bottom: 12px;
  font-size: 14px;
}

.author {
  color: #999;
  font-style: italic;
  font-size: 13px;
}

/* ========== CTA 区域 ========== */
.cta-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 60px 48px;
  text-align: center;
  border-radius: 16px;
  margin-bottom: 0;
}

.cta-section h2 {
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 12px;
}

.cta-section p {
  font-size: 16px;
  margin-bottom: 32px;
  opacity: 0.95;
}

/* ========== 动画 ========== */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes fadeInUp {
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
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
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

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

/* ========== 响应式设计 ========== */
@media (max-width: 1024px) {
  .hero-banner {
    padding: 80px 24px;
    min-height: 500px;
  }

  .hero-title {
    font-size: 40px;
  }

  .hero-subtitle {
    font-size: 20px;
  }

  .content-container {
    padding: 0 24px;
  }

  .features-section,
  .advantages-section,
  .applications-section,
  .highlights-section,
  .quickstart-section,
  .testimonials-section {
    padding: 40px 32px;
  }

  .advantages-content {
    grid-template-columns: 1fr;
    gap: 32px;
  }

  .advantages-visual {
    grid-template-columns: 1fr;
  }

  .section-title {
    font-size: 28px;
  }
}

@media (max-width: 768px) {
  .hero-banner {
    padding: 60px 16px;
    min-height: 400px;
  }

  .hero-title {
    font-size: 32px;
  }

  .hero-subtitle {
    font-size: 18px;
  }

  .hero-description {
    font-size: 14px;
  }

  .content-container {
    padding: 0 16px;
  }

  .features-section,
  .advantages-section,
  .applications-section,
  .highlights-section,
  .quickstart-section,
  .testimonials-section {
    padding: 32px 24px;
    margin-bottom: 20px;
    border-radius: 12px;
  }

  .section-title {
    font-size: 24px;
  }

  .section-subtitle {
    font-size: 14px;
  }

  .features-grid,
  .applications-grid,
  .highlights-grid,
  .testimonials-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .steps-container {
    gap: 12px;
  }

  .step-box {
    flex: 0 1 150px;
    padding: 20px 16px;
  }

  .step-arrow {
    transform: rotate(90deg);
    margin: 0;
  }

  .feature-item,
  .app-card,
  .highlight-box,
  .tech-card {
    padding: 24px 16px;
  }

  .feature-icon,
  .app-icon {
    font-size: 36px;
  }

  .cta-section {
    padding: 40px 24px;
  }

  .cta-section h2 {
    font-size: 24px;
  }

  .cta-section p {
    font-size: 14px;
  }
}

@media (max-width: 480px) {
  .hero-banner {
    padding: 40px 12px;
    min-height: 350px;
  }

  .hero-title {
    font-size: 24px;
  }

  .hero-subtitle {
    font-size: 16px;
  }

  .hero-description {
    font-size: 13px;
  }

  .hero-buttons {
    gap: 12px;
  }

  .btn {
    padding: 10px 20px;
    font-size: 14px;
  }

  .content-container {
    margin-top: -40px;
    padding: 0 12px;
  }

  .features-section,
  .advantages-section,
  .applications-section,
  .highlights-section,
  .quickstart-section,
  .testimonials-section,
  .cta-section {
    padding: 24px 16px;
    margin-bottom: 16px;
  }

  .section-header {
    margin-bottom: 32px;
  }

  .section-title {
    font-size: 20px;
  }

  .section-subtitle {
    font-size: 13px;
  }

  .feature-item,
  .app-card,
  .highlight-box,
  .step-box,
  .tech-card {
    padding: 20px 12px;
  }

  .feature-icon,
  .app-icon {
    font-size: 32px;
  }

  .step-number {
    width: 40px;
    height: 40px;
    font-size: 20px;
  }

  .cta-section h2 {
    font-size: 20px;
  }

  .cta-section p {
    font-size: 13px;
    margin-bottom: 20px;
  }

  .btn-lg {
    padding: 12px 32px;
    font-size: 16px;
  }
}
</style>