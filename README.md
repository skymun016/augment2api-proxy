# 🌐 Augment2Api Cloudflare 多用户代理

> **无服务器 • 全球分布 • 零维护 • 多用户管理**

基于 Cloudflare Workers + D1 数据库的 Augment2Api 多用户统一代理服务，完全无服务器部署。

[![Deploy to Cloudflare Workers](https://deploy.workers.cloudflare.com/button)](https://deploy.workers.cloudflare.com/?url=https://github.com/amesky/augment2api-proxy)

## ✨ 特性

- 🚀 **无服务器架构**: 基于 Cloudflare Workers，无需管理服务器
- 🌍 **全球分布**: Cloudflare 全球 CDN 网络，低延迟访问
- 💰 **成本极低**: 免费额度通常足够个人和小团队使用
- 🔒 **企业级安全**: DDoS 防护、自动 SSL、访问控制
- ⚡ **高性能**: 边缘计算，毫秒级响应
- 🔧 **零维护**: 自动扩展，无需运维

## 🎯 核心功能

### 多用户Token池管理
- 🏢 **企业级多用户系统**：支持用户注册、Token分配、配额管理
- 🔄 **智能负载均衡**：自动选择最优Token，故障转移
- 📊 **使用统计监控**：详细的用户使用统计和分析
- 🔒 **权限管理**：细粒度的用户权限和Token访问控制

### 统一代理模式
- 客户端使用统一的域名和个人token
- 系统内部管理多个真实 Augment token
- 自动负载均衡和故障转移
- 支持 OpenAI 兼容和 Augment 原生接口

### Web 管理界面
- 🎛️ **管理员面板**：Token池管理、用户管理、系统配置
- 👥 **用户管理**：用户注册、配额分配、使用监控
- 📈 **实时监控**：Token状态、使用统计、性能指标
- 🔐 **安全认证**：管理员和用户双重认证体系

## 🚀 快速部署

### 方法1: GitHub一键部署（推荐）

1. **Fork本仓库**到您的GitHub账号
2. **登录Cloudflare控制台**
3. **进入Workers & Pages** → **Create application** → **Pages** → **Connect to Git**
4. **选择您fork的仓库**
5. **配置构建设置**：
   ```
   Framework preset: None
   Build command: npm install
   Build output directory: /
   Root directory: /
   ```
6. **点击Deploy**

### 方法2: 自动化脚本部署

1. **Fork 此仓库**
2. **在 Cloudflare 中连接 GitHub**
   - 登录 [Cloudflare Dashboard](https://dash.cloudflare.com/)
   - 进入 "Workers & Pages"
   - 点击 "Create application"
   - 选择 "Pages" → "Connect to Git"
   - 选择此仓库

3. **配置构建设置**
   - Framework preset: `None`
   - Build command: `npm install`
   - Build output directory: `/`

4. **设置环境变量**
   ```
   UNIFIED_TOKEN=your-unified-token-here
   ACCESS_PWD=your-admin-password
   ```

```bash
# 登录 Cloudflare
npx wrangler login

# 一键部署（开发环境）
chmod +x deploy-multiuser.sh
./deploy-multiuser.sh dev

# 生产环境部署
./deploy-multiuser.sh production
```

### 方法3: 手动部署

```bash
# 克隆仓库
git clone https://github.com/amesky/augment2api-proxy.git
cd augment2api-proxy

# 安装依赖
npm install

# 登录 Cloudflare
npx wrangler login

# 创建 D1 数据库
npx wrangler d1 create augment2api-multiuser

# 更新 wrangler.toml 中的 database_id

# 初始化数据库
npx wrangler d1 execute augment2api-multiuser --file=./schema-extended.sql

# 部署
npx wrangler deploy
```

## 📖 使用指南

### 1. 配置管理

部署完成后：
1. 访问您的 Worker 域名
2. 使用管理密码登录
3. 添加真实的 Augment token

### 2. 客户端使用

```python
# Python 示例
import openai

client = openai.OpenAI(
    base_url="https://your-worker.workers.dev/v1",
    api_key="your-unified-token"
)

response = client.chat.completions.create(
    model="claude-3.7-chat",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

```javascript
// JavaScript 示例
import OpenAI from 'openai';

const openai = new OpenAI({
  baseURL: 'https://your-worker.workers.dev/v1',
  apiKey: 'your-unified-token',
});

const response = await openai.chat.completions.create({
  model: 'claude-3.7-chat',
  messages: [{ role: 'user', content: 'Hello!' }],
});
```

### 3. 支持的接口

- `GET /v1/models` - 模型列表
- `POST /v1/chat/completions` - OpenAI 兼容聊天接口
- `POST /chat-stream` - Augment 原生流式接口
- `GET /` - Web 管理界面

## 🔧 配置说明

### 环境变量

| 变量名 | 说明 | 必需 | 示例 |
|--------|------|------|------|
| `UNIFIED_TOKEN` | 客户端使用的统一认证token | ✅ | `your-unified-token` |
| `ACCESS_PWD` | 管理界面登录密码 | ✅ | `admin-password` |

### 自定义域名

1. 在 Cloudflare 中添加您的域名
2. 在 Worker 设置中绑定自定义域名
3. 更新客户端配置使用新域名

## 💰 成本估算

### Cloudflare 免费额度
- **Workers**: 100,000 请求/天
- **D1 数据库**: 5GB 存储 + 25M 行读取/天
- **自定义域名**: 免费

### 实际成本
- **个人使用**: 完全免费
- **小团队**: 通常免费
- **大规模使用**: $5-20/月

## 🛡️ 安全特性

- ✅ Cloudflare 企业级 DDoS 防护
- ✅ 自动 SSL/TLS 加密
- ✅ Token 安全存储
- ✅ 访问日志记录
- ✅ 管理员认证保护

## 🔍 监控管理

### 查看日志
```bash
npx wrangler tail
```

### 数据库操作
```bash
# 查看所有 token
npx wrangler d1 execute augment2api-db --command "SELECT * FROM tokens"

# 添加 token
npx wrangler d1 execute augment2api-db --command "INSERT INTO tokens (token, tenant_url, remark) VALUES ('your-token', 'https://xxx.augmentcode.com/', 'test')"
```

## 🚀 高级功能

### 多环境部署
- 支持 staging 和 production 环境
- 独立的配置和数据库
- 安全的发布流程

### 性能优化
- 边缘缓存
- 智能路由
- 自动故障转移

### 扩展功能
- 使用统计
- 访问控制
- 自定义限流

## 🆘 故障排除

### 常见问题

1. **部署失败**
   - 检查环境变量配置
   - 验证 Cloudflare 账户权限

2. **数据库连接失败**
   - 确认 database_id 正确
   - 重新初始化数据库

3. **域名访问问题**
   - 检查 DNS 解析
   - 验证域名绑定

### 获取帮助

- 📚 [详细文档](./docs/)
- 🐛 [提交 Issue](https://github.com/skymun016/augment2apicloudflare/issues)
- 💬 [讨论区](https://github.com/skymun016/augment2apicloudflare/discussions)

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

基于 [Augment2Api](https://github.com/linqiu919/augment2api) 项目开发

---

**🌟 如果这个项目对您有帮助，请给个 Star！**
