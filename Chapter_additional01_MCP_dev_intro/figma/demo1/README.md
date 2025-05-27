# Music App Demo

基于 Figma 设计的音乐应用前端界面实现。

## 功能特性

- 🎵 现代化音乐应用界面
- 📱 响应式设计
- 🎨 基于 Figma 设计规范
- ⚡ React 18 + 现代 CSS

## 界面组件

### 侧边栏 (Sidebar)
- 应用标题
- 主导航菜单 (Discover, Home, Browse, Radio)
- 音乐库菜单 (Playlists, Songs, Personalized picks)

### 顶部导航 (Navigation)
- 分段控制器 (Tab 切换)
- 行动按钮

### 主内容区 (MainContent)
- 播放列表大网格展示
- 专辑小网格展示
- 标题和副标题区域

## 技术栈

- React 18
- CSS3 (Flexbox, Grid)
- Inter 字体

## 安装和运行

```bash
# 安装依赖
npm install

# 启动开发服务器
npm start

# 构建生产版本
npm run build
```

## 设计规范

- 字体: Inter
- 主色调: #000000 (黑色)
- 次要色调: #454545 (灰色)
- 背景色: #ffffff (白色)
- 强调色: #f7f7f7 (浅灰)
- 圆角: 8px
- 间距: 8px, 12px, 16px, 24px, 32px

## 项目结构

```
src/
├── components/
│   ├── Sidebar.js/css
│   ├── Navigation.js/css
│   └── MainContent.js/css
├── App.js/css
├── index.js/css
└── ...
``` 