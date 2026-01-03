# 银行智能问答助手 - 前端应用

基于 React + ChatUI 构建的银行智能问答助手前端界面。

## 技术栈

- **React 18** - UI 框架
- **Vite** - 构建工具
- **ChatUI** - 阿里巴巴达摩院开源对话式 UI 组件库
- **Axios** - HTTP 客户端

## 快速开始

### 1. 安装依赖

```bash
cd frontend
npm install
```

### 2. 启动开发服务器

```bash
npm run dev
```

前端应用将在 `http://localhost:3000` 启动。

### 3. 构建生产版本

```bash
npm run build
```

构建产物将输出到 `dist` 目录。

### 4. 预览生产构建

```bash
npm run preview
```

## 功能特性

- ✅ 美观的聊天界面
- ✅ 实时消息发送和接收
- ✅ 打字动画效果
- ✅ 响应式设计，支持移动端
- ✅ 与后端 API 集成
- ✅ 错误处理和加载状态

## 项目结构

```
frontend/
├── src/
│   ├── App.jsx          # 主应用组件
│   ├── App.css          # 应用样式
│   ├── main.jsx         # 应用入口
│   └── index.css        # 全局样式
├── public/              # 静态资源
├── index.html           # HTML 模板
├── vite.config.js       # Vite 配置
└── package.json         # 项目配置
```

## 配置

### API 代理

前端通过 Vite 代理连接到后端 API。在 `vite.config.js` 中配置：

```javascript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true
    }
  }
}
```

如果需要修改后端地址，请更新 `vite.config.js` 中的 `target` 配置。

## 开发说明

### 自定义样式

可以在 `src/App.css` 中修改聊天界面的样式，包括：
- 主题颜色
- 消息气泡样式
- 输入框样式
- 动画效果

### 添加新功能

1. 消息类型：可以在 `renderMessageContent` 函数中添加新的消息类型渲染
2. 工具栏：可以在 `Chat` 组件的 `toolbar` 属性中添加工具栏按钮
3. 快捷回复：可以添加常用问题的快捷按钮

## 浏览器支持

- Chrome (最新版本)
- Firefox (最新版本)
- Safari (最新版本)
- Edge (最新版本)

## 许可证

MIT License


