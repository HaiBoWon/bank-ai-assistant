# 银行智能问答助手

一个基于 FastAPI 和 LLM 的银行智能客服系统，支持账户、信用卡、基础业务和常见操作等各类问题的智能问答。

## 功能特性

- ✅ 账户类问题：挂失、余额查询、交易明细、冻结/解冻
- ✅ 信用卡类问题：账单查询、还款、额度提升、逾期罚息、积分兑换
- ✅ 基础业务类问题：手机银行/网银注册、转账限额、手续费、利率查询
- ✅ 常见操作类问题：密码重置、短信提醒、银行卡解绑

## 技术栈

### 后端
- **框架**: FastAPI
- **LLM服务**: OpenAI API（可选，当前使用知识库优先）
- **知识库**: JSON 结构化存储
- **Python版本**: 3.8+

### 前端
- **框架**: React 18
- **UI组件**: ChatUI（阿里巴巴达摩院）
- **构建工具**: Vite
- **HTTP客户端**: Axios

## 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+ 和 npm
- uv（推荐的 Python 包管理器，替代 pip）
- （可选）OpenAI API Key（如果使用 LLM 增强功能）

#### 安装 uv

```bash
# 使用 Homebrew（macOS）
brew install uv

# 使用 Winget（Windows）
winget install astral-sh.uv

# 使用 Pipx（跨平台）
pipx install uv

# 或直接使用 pip
pip install uv
```

### 1. 克隆项目

```bash
git clone <repository-url>
cd bank-assistant
```

### 2. 后端设置

#### 2.1 使用 uv 安装依赖并运行（推荐）

uv 是一个现代化的 Python 包管理器，比 pip 更快、更智能，同时内置了虚拟环境管理功能。

```bash
# 1. 安装依赖（uv 会自动创建并管理虚拟环境）
uv pip install -r requirements.txt

# 2. 创建 .env 文件
cat > .env << EOF
OPENAI_API_KEY=your_openai_api_key_here  # 可选，当前版本主要使用知识库
LLM_MODEL=gpt-3.5-turbo  # 可选
LLM_BASE_URL=
HTTP_PROXY=
HTTPS_PROXY=
EOF

# 3. 直接运行后端服务（使用 uv 无需手动激活虚拟环境）
uv run python -m backend.main
```

#### 2.2 传统方式（使用 pip + venv）

```bash
# 1. 创建并激活虚拟环境
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# 或 .venv\Scripts\activate  # Windows

# 2. 安装依赖
pip install -r requirements.txt

# 3. 创建 .env 文件并配置（同上）

# 4. 启动后端服务
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

后端服务将在 `http://localhost:8000` 启动。

**注意**：当前版本优先使用知识库，即使不配置 OpenAI API Key 也能正常运行。

### 3. 前端设置

#### 3.1 安装前端依赖

```bash
cd frontend
npm install
```

#### 3.2 启动前端服务

```bash
npm run dev
```

前端应用将在 `http://localhost:3000` 启动。

### 4. 访问应用

- **前端聊天界面**: http://localhost:3000
- **后端 API 文档**: http://localhost:8000/docs
- **API ReDoc 文档**: http://localhost:8000/redoc

### 5. 验证服务

#### 测试后端 API

```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"question": "如何挂失银行卡？"}'
```

#### 测试健康检查

```bash
curl http://localhost:8000/api/health
```

## 项目结构

```
bank-assistant/
├── backend/
│   ├── __init__.py
│   ├── main.py                 # FastAPI主应用
│   ├── models/                 # 数据模型
│   ├── services/               # 业务服务
│   │   ├── llm_service.py      # LLM服务
│   │   ├── knowledge_base.py   # 知识库服务
│   │   └── question_classifier.py  # 问题分类
│   ├── routers/                # API路由
│   └── data/                   # 数据文件
│       └── knowledge_base.json  # 知识库数据
├── frontend/                   # 前端应用
├── requirements.txt
├── .env
└── README.md
```

## 启动服务

### 完整启动流程

#### 方式一：使用 uv 快速启动（推荐）

**终端 1 - 启动后端：**
```bash
# 使用 uv 直接运行后端（无需激活虚拟环境）
uv run python -m backend.main
```

**终端 2 - 启动前端：**
```bash
cd frontend
npm run dev
```

#### 方式二：传统方式（使用 pip + venv）

**终端 1 - 启动后端：**
```bash
# 激活虚拟环境
source .venv/bin/activate  # macOS/Linux
# 或 .venv\Scripts\activate  # Windows

# 启动后端（支持热重载）
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

**终端 2 - 启动前端：**
```bash
cd frontend
npm run dev
```

#### 方式三：使用脚本启动（自动化）

可以创建启动脚本来自动化启动过程：

```bash
# 创建启动脚本
cat > start.sh << EOF
#!/bin/bash

# 启动后端
uv run python -m backend.main &

# 启动前端
cd frontend
npm run dev &

# 等待所有进程结束
wait
EOF

# 赋予执行权限
chmod +x start.sh

# 运行脚本
./start.sh
```

### 服务端口

- **后端 API**: http://localhost:8000
- **前端界面**: http://localhost:3000
- **API文档**: http://localhost:8000/docs

### 停止服务

- 后端：在运行后端的终端按 `Ctrl + C`
- 前端：在运行前端的终端按 `Ctrl + C`
- 脚本启动：使用 `pkill -f "python -m backend.main"` 和 `pkill -f "npm run dev"`

## 使用说明

### 前端聊天界面

1. 打开浏览器访问 http://localhost:3000
2. 在输入框中输入问题，例如：
   - "如何挂失银行卡？"
   - "怎么查余额？"
   - "信用卡怎么还款？"
3. 系统会自动匹配知识库并返回答案

### API 调用

#### 发送问题

```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"question": "如何挂失银行卡？"}'
```

#### 响应格式

```json
{
  "answer": "银行卡挂失流程：1. 立即拨打银行客服热线（如95588）进行电话挂失；2. 携带本人有效身份证件到就近银行网点办理正式挂失；3. 填写挂失申请书；4. 7个工作日后可补办新卡。",
  "category": "账户类",
  "topic": "银行卡挂失流程",
  "confidence": 0.9
}
```

## 扩展功能

- [x] Web 前端界面（ChatUI）
- [ ] 向量数据库支持（Chroma/FAISS）
- [ ] 对话历史记录
- [ ] 多轮对话上下文
- [ ] 用户反馈机制

## 许可证

MIT License

