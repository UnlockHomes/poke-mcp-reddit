# 🚂 Railway 部署指南

## 📋 部署步骤

### 1. 准备代码

确保你的仓库包含以下文件：
- ✅ `http_server.py` - HTTP 服务器包装器
- ✅ `pyproject.toml` - 已更新依赖（包含 fastapi 和 uvicorn）
- ✅ `requirements.txt` - 依赖列表（可选，Railway 会自动检测）
- ✅ `railway.json` - Railway 配置（可选）

### 2. 在 Railway 创建项目

1. 访问 https://railway.app/
2. 用 GitHub 登录
3. 点击 **"New Project"**
4. 选择 **"Deploy from GitHub repo"**
5. 选择你的仓库：`UnlockHomes/poke-mcp-reddit`

### 3. 配置服务

Railway 会自动检测到 Python 项目，但需要确认以下配置：

#### 环境变量
- **无需配置**（Reddit MCP 使用公共 API）

#### 启动命令
Railway 会自动检测，但确保是：
```
python http_server.py
```

#### 端口
Railway 会自动设置 `PORT` 环境变量，`http_server.py` 会自动读取。

### 4. 部署

1. Railway 会自动开始构建和部署
2. 等待部署完成（通常 2-5 分钟）
3. 点击服务，查看 **"Settings"** → **"Networking"**
4. 生成一个公共域名（格式：`your-project.up.railway.app`）

### 5. 测试部署

#### 健康检查
```bash
curl https://your-project.up.railway.app/health
```

预期响应：
```json
{"status": "healthy"}
```

#### 测试 MCP 端点
```bash
curl https://your-project.up.railway.app/mcp \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list"
  }'
```

### 6. 在 Poke 中配置

1. 打开 Poke 应用
2. 进入 **Settings** → **Connections**
3. 点击 **Add MCP Server**
4. 填写：
   - **Name**: Reddit MCP
   - **URL**: `https://your-project.up.railway.app/mcp`
   - **Type**: HTTP/HTTPS
5. 保存并测试

---

## 🔧 故障排查

### 问题 1: 构建失败

**症状**: Railway 构建失败

**可能原因**:
- 依赖安装失败
- Python 版本不匹配

**解决方案**:
1. 查看 Railway 构建日志
2. 确认 `pyproject.toml` 中的依赖正确
3. 确认 Python 版本 >= 3.11

### 问题 2: 服务启动失败

**症状**: 部署成功但服务无法启动

**可能原因**:
- 启动命令错误
- 端口配置问题

**解决方案**:
1. 检查启动命令：`python http_server.py`
2. 确认 `http_server.py` 文件存在
3. 查看 Railway 日志

### 问题 3: MCP 端点返回错误

**症状**: `/mcp` 端点返回错误

**可能原因**:
- JSON-RPC 格式错误
- 工具调用失败

**解决方案**:
1. 检查请求格式是否符合 JSON-RPC 2.0
2. 查看 Railway 日志了解详细错误
3. 测试 `/health` 端点确认服务运行正常

### 问题 4: Poke 无法连接

**症状**: Poke 显示连接失败

**可能原因**:
- URL 格式错误
- CORS 问题
- SSL 证书问题

**解决方案**:
1. 确认 URL 格式：`https://your-project.up.railway.app/mcp`
2. 确认 Railway 服务状态为 "Active"
3. 在浏览器测试 URL 是否可访问

---

## 📊 Railway 配置说明

### railway.json（可选）

```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python http_server.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### 环境变量

Railway 会自动设置：
- `PORT` - 服务端口（`http_server.py` 会自动读取）

---

## 💰 Railway 免费额度

Railway 提供：
- **$5/月** 免费额度
- 足够运行这个 MCP 服务器
- 超出后按使用量付费

---

## ✅ 部署检查清单

- [ ] 代码已推送到 GitHub
- [ ] Railway 项目已创建
- [ ] 服务已部署并运行
- [ ] `/health` 端点返回正常
- [ ] `/mcp` 端点可以访问
- [ ] Poke 中已配置并测试

---

## 🎉 完成！

部署成功后，你的 Poke 就可以使用 Reddit MCP 了！

测试命令（在 Poke 中）：
```
"帮我看看 Reddit r/Python 版块的热门帖子"
```

