# 🚀 Cloudflare Workers 完整部署指南

## 📋 部署前准备

### 1. 环境要求
```bash
# 检查 Node.js 版本 (需要 >= 16.0.0)
node --version

# 检查 npm 版本
npm --version
```

### 2. 安装依赖
```bash
# 安装 Wrangler CLI
npm install -g wrangler

# 验证安装
wrangler --version
```

### 3. Cloudflare 账号准备
- 注册 [Cloudflare 账号](https://dash.cloudflare.com/sign-up)
- 获取 API Token（可选，用于自动化）

## 🔧 项目配置检查

### 1. 验证项目结构
```
augment2api-proxy/
├── src/
│   ├── worker-multiuser.js     ✅ 主Worker文件
│   └── utils/                  ✅ 工具函数
├── schema-extended.sql         ✅ 数据库结构
├── deploy-multiuser.sh         ✅ 部署脚本
├── wrangler.toml              ✅ Cloudflare配置
└── package.json               ✅ 项目配置
```

### 2. 配置文件状态
- ✅ `wrangler.toml` - 已优化，数据库ID将自动配置
- ✅ `schema-extended.sql` - 完整的多用户数据库结构
- ✅ `deploy-multiuser.sh` - 自动化部署脚本

## 🚀 一键部署流程

### 方法1: 使用自动化脚本（推荐）

```bash
# 1. 登录 Cloudflare
wrangler login

# 2. 开发环境部署
chmod +x deploy-multiuser.sh
./deploy-multiuser.sh dev

# 3. 生产环境部署
./deploy-multiuser.sh production
```

### 方法2: 手动部署步骤

```bash
# 1. 登录 Cloudflare
wrangler login

# 2. 创建 D1 数据库
wrangler d1 create augment2api-multiuser

# 3. 记录数据库ID并更新 wrangler.toml
# 将输出的 database_id 复制到 wrangler.toml 中

# 4. 初始化数据库结构
wrangler d1 execute augment2api-multiuser --file=schema-extended.sql

# 5. 部署 Worker
wrangler deploy

# 6. 生产环境部署
wrangler deploy --env production
```

## 📊 部署后验证

### 1. 健康检查
```bash
# 检查服务状态
curl https://your-worker.workers.dev/health

# 预期响应
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00.000Z",
  "version": "v1.0.0"
}
```

### 2. 管理面板访问
- 访问: `https://your-worker.workers.dev`
- 默认管理员: `admin / admin123`

### 3. API端点测试
```bash
# 获取模型列表
curl https://your-worker.workers.dev/v1/models

# 管理员登录
curl -X POST https://your-worker.workers.dev/api/admin/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

## 🔒 安全配置

### 1. 更新默认密码
```bash
# 在 wrangler.toml 中更新
[vars]
ADMIN_PASSWORD = "your-strong-password"
```

### 2. 环境变量配置
```toml
[vars]
ENVIRONMENT = "production"
DEFAULT_TOKEN_QUOTA = "3"
MAX_TOKEN_QUOTA = "10"
SESSION_EXPIRE_HOURS = "24"
RATE_LIMIT_PER_HOUR = "1000"
```

## 🌐 自定义域名（可选）

### 1. 添加域名到 Cloudflare
- 在 Cloudflare 控制台添加域名
- 更新 DNS 服务器

### 2. 绑定到 Worker
```bash
# 在 Cloudflare 控制台中：
# Workers & Pages → 选择你的 Worker → Triggers → Custom Domains
```

## 📈 监控和日志

### 1. 查看实时日志
```bash
wrangler tail
```

### 2. 数据库操作
```bash
# 查看用户列表
wrangler d1 execute augment2api-multiuser --command="SELECT * FROM users LIMIT 10"

# 查看Token状态
wrangler d1 execute augment2api-multiuser --command="SELECT * FROM tokens"
```

## 🔧 故障排除

### 常见问题

1. **Error 1101 - Worker threw exception**
   - 检查数据库是否正确绑定
   - 验证 `wrangler.toml` 中的 `database_id`

2. **Database not found**
   - 确保数据库已创建: `wrangler d1 list`
   - 重新运行: `wrangler d1 create augment2api-multiuser`

3. **Permission denied**
   - 重新登录: `wrangler logout && wrangler login`
   - 检查 Cloudflare 账号权限

### 调试命令
```bash
# 检查 Wrangler 状态
wrangler whoami

# 列出所有数据库
wrangler d1 list

# 检查 Worker 状态
wrangler status
```

## 📚 下一步

部署成功后：
1. 访问管理面板创建用户
2. 添加 Augment Token 到系统
3. 为用户分配 Token 配额
4. 配置客户端使用新的 API 端点

## 🎯 API 使用示例

```python
import openai

# 配置客户端
client = openai.OpenAI(
    base_url="https://your-worker.workers.dev/v1",
    api_key="user-personal-token"
)

# 发送请求
response = client.chat.completions.create(
    model="claude-3.7-chat",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

---

🎉 **恭喜！您的 Augment2Api 多用户代理系统已成功部署到 Cloudflare Workers！**
