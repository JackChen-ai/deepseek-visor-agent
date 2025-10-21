# 阿里云 GPU 实例开通指南（DeepSeek-OCR 测试）

> **目标**：租用阿里云 GPU 服务器，运行 DeepSeek-OCR 完整测试，记录性能数据
> **预计时间**：30 分钟开通 + 3 小时测试
> **预计成本**：¥6-15（测试完立即删除实例）

---

## 📋 前置准备

### 需要准备的东西
- ✅ 阿里云账号（已实名认证）
- ✅ 账户余额 ≥¥50（抢占式实例需要，测完退款）
- ✅ Mac 终端（SSH 连接用）
- ✅ 记事本（记录 IP 地址和测试结果）

### 不需要准备的东西
- ❌ 不需要本地安装 CUDA
- ❌ 不需要下载模型到本地
- ❌ 不需要占用 Mac 存储空间

---

## 🚀 第一步：创建 GPU 实例（10 分钟）

### 1.1 打开阿里云 ECS 控制台

**操作**：
```
浏览器打开：https://ecs.console.aliyun.com
```

**如果需要登录**：
- 🛑 **暂停**：使用你的阿里云账号登录
- ⏸️ 登录完成后继续

---

### 1.2 创建实例

**操作**：
1. 点击页面右上角 **蓝色按钮**："创建实例"
2. 进入购买页面

---

### 1.3 选择付费模式

**操作**：
- 付费模式：选择 **"抢占式实例"**
  - ✅ 价格便宜（正常价的 20-30%）
  - ✅ 适合短期测试
  - ⚠️ 可能被回收（测试 3-4 小时没问题）

---

### 1.4 选择地域和可用区

**操作**：
```
地域：华东2（上海）
可用区：可用区 B 或 可用区 H
```

**为什么选上海**：
- 国内访问速度快
- GPU 库存较充足

---

### 1.5 选择实例规格（重要！）

**操作**：
1. 点击 **"异构计算 GPU/FPGA"** 标签
2. 在筛选框搜索：**"gn6i"** 或 **"gn7i"**

**推荐配置**：

| 实例规格 | GPU 型号 | VRAM | vCPU | 内存 | 价格/小时 | 推荐度 |
|---------|---------|------|------|------|-----------|--------|
| **ecs.gn6i-c4g1.xlarge** | Tesla T4 | 16GB | 4核 | 15GB | ~¥1.5 | ⭐⭐⭐ 推荐 |
| **ecs.gn7i-c8g1.2xlarge** | RTX 4090 | 24GB | 8核 | 30GB | ~¥3-4 | ⭐⭐⭐⭐⭐ 最佳 |
| **ecs.gn7-c2g1.3xlarge** | A10 | 24GB | 12核 | 45GB | ~¥2.5 | ⭐⭐⭐⭐ 平衡 |

**我的建议**：
- **预算有限**：选 **T4**（¥1.5/小时，能跑 Base/Small/Tiny 模式）
- **完整测试**：选 **RTX 4090**（¥3-4/小时，能跑所有 5 种模式）

**操作**：
3. 勾选你选择的规格
4. 点击"下一步：镜像和存储"

---

### 1.6 选择镜像

**操作**：

#### 方案 A：使用深度学习镜像（推荐，省时间）
```
1. 镜像类型：选择 "镜像市场"
2. 在搜索框输入："深度学习镜像 CUDA 12.1"
3. 选择：Ubuntu 22.04 + CUDA 12.1 + PyTorch（免费镜像）
```

**优势**：CUDA 和 PyTorch 已预装，节省 20 分钟

#### 方案 B：使用纯净 Ubuntu（备选）
```
1. 镜像类型：选择 "公共镜像"
2. 操作系统：Ubuntu
3. 版本：22.04 64位
```

**需要后续手动安装 CUDA**

---

### 1.7 配置存储

**操作**：
```
系统盘：
- 类型：ESSD云盘（默认即可）
- 大小：40GB（默认）

数据盘：
- ❌ 不需要添加
```

**解释**：
- 40GB 系统盘足够（系统10GB + CUDA 8GB + 模型 6GB + 剩余16GB）
- 数据盘用不上（测试完就删）

---

### 1.8 配置网络

**操作**：
```
专有网络：默认 VPC（如果没有会自动创建）
公网IP：选择 "分配公网 IPv4 地址"
带宽计费模式：按使用流量
带宽峰值：1 Mbps（够用）
```

**为什么需要公网 IP**：
- SSH 连接需要
- 下载模型需要（模型在 HuggingFace）

---

### 1.9 配置安全组

**操作**：
```
安全组：默认安全组（自动创建）

如果需要手动配置安全组规则：
- 规则方向：入方向
- 授权策略：允许
- 协议类型：SSH(22)
- 授权对象：0.0.0.0/0（所有 IP，仅测试用）
```

**安全提示**：
- 测试完立即删除实例
- 或设置复杂 root 密码

---

### 1.10 配置登录凭证

**操作**：
```
登录凭证：选择 "密码"
用户名：root（默认）
密码：设置一个复杂密码（记住它！）
```

**示例密码格式**：
```
DeepSeek@2025!Test
（需要包含大小写字母、数字、特殊符号）
```

🛑 **重要**：把密码记在记事本里！

---

### 1.11 配置实例名称

**操作**：
```
实例名称：deepseek-ocr-test
主机名：deepseek-test
```

---

### 1.12 确认购买

**操作**：
1. 购买时长：选择 **"按小时"**
2. 购买数量：1 台
3. 勾选 **"《云服务器ECS服务条款》"**
4. 查看右侧费用预估：
   - 预估费用：¥1.5-4/小时
   - 余额冻结：~¥50（测完释放实例后退回）

5. 点击 **"确认下单"**

🛑 **暂停**：进入支付页面

---

### 1.13 支付

**操作**：
```
1. 确认金额（冻结金额，不是实际扣费）
2. 选择支付方式（余额/支付宝）
3. 点击"确认支付"
```

⏸️ **你来操作支付**

✅ 支付完成后，等待 2-3 分钟实例创建

---

### 1.14 获取公网 IP

**操作**：
```
1. 回到 ECS 控制台：https://ecs.console.aliyun.com
2. 点击左侧菜单 "实例与镜像" → "实例"
3. 找到实例名称：deepseek-ocr-test
4. 状态应该是 "运行中"（绿色）
5. 查看 "公网IP" 列，复制 IP 地址
```

**示例 IP**：
```
123.456.789.0
```

🛑 **重要**：把 IP 地址记在记事本里！

---

## 🔌 第二步：SSH 连接（5 分钟）

### 2.1 打开 Mac 终端

**操作**：
```
打开 "终端" 应用
（Launchpad → 其他 → 终端）
或按快捷键：Command + 空格，输入 "Terminal"
```

---

### 2.2 SSH 连接

**操作**：
```bash
# 替换 <IP地址> 为你刚才记录的公网 IP
ssh root@<IP地址>

# 示例：
# ssh root@123.456.789.0
```

**首次连接会提示**：
```
The authenticity of host '123.456.789.0' can't be established.
Are you sure you want to continue connecting (yes/no)?
```

**操作**：输入 `yes` 按回车

**然后提示输入密码**：
```
root@123.456.789.0's password:
```

**操作**：输入你在 1.10 设置的密码（看不到字符是正常的），按回车

---

### 2.3 验证连接成功

**成功标志**：
```
Welcome to Ubuntu 22.04.3 LTS (GNU/Linux 5.15.0-58-generic x86_64)

root@deepseek-test:~#
```

✅ 看到命令提示符，说明连接成功！

---

### 2.4 检查 GPU

**操作**：
```bash
nvidia-smi
```

**期望输出**：
```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 525.60.13    Driver Version: 525.60.13    CUDA Version: 12.1   |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
|   0  Tesla T4            Off  | 00000000:00:07.0 Off |                    0 |
+-------------------------------+----------------------+----------------------+
```

✅ 能看到 GPU 信息，说明 GPU 可用！

---

## 📦 第三步：安装依赖（10 分钟）

### 3.1 更新系统（可选）

**操作**：
```bash
apt update
```

---

### 3.2 安装 Git（如果没有）

**操作**：
```bash
git --version

# 如果没有，执行：
apt install -y git
```

---

### 3.3 克隆代码仓库

**操作**：
```bash
cd ~
git clone https://github.com/JackChen-ai/deepseek-visor-agent.git
cd deepseek-visor-agent
```

**期望输出**：
```
Cloning into 'deepseek-visor-agent'...
remote: Enumerating objects: 156, done.
...
```

---

### 3.4 安装 Python 依赖

**操作**：
```bash
pip install 'transformers==4.46.3' 'tokenizers>=0.20.0,<0.21.0' torch pillow
```

**安装时间**：5-8 分钟（会下载 PyTorch 等大型库）

**期望输出**：
```
Successfully installed transformers-4.46.3 torch-2.x.x pillow-10.x.x ...
```

---

## 🧪 第四步：运行测试（2-3 小时）

### 4.1 运行简单推理测试

**操作**：
```bash
python test_simple_inference.py
```

**首次运行会下载模型**：
```
Downloading model from huggingface.co/deepseek-ai/DeepSeek-OCR...
deepseek_ocr_model.bin: 6.2GB [00:05<00:00, 1.2GB/s]
```

**下载时间**：5-10 分钟（取决于网速）

**下载完成后开始推理**：
```
Loading model...
Running inference...
✅ Inference successful!
Output: [Markdown 文本]
Inference time: 1234 ms
```

✅ 如果看到输出，说明基本功能正常！

---

### 4.2 测试 5 种推理模式

**操作**：创建测试脚本

```bash
cat > test_all_modes.py << 'EOF'
import time
from transformers import AutoModel, AutoTokenizer
from PIL import Image
import requests
from io import BytesIO

# 下载测试图片
url = "https://raw.githubusercontent.com/deepseek-ai/DeepSeek-OCR/main/examples/invoice.jpg"
response = requests.get(url)
image = Image.open(BytesIO(response.content))

# 保存到本地
image.save("test_invoice.jpg")

# 加载模型
model_id = "deepseek-ai/DeepSeek-OCR"
model = AutoModel.from_pretrained(model_id, trust_remote_code=True).cuda()
tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)

# 测试 5 种模式
modes = [
    {"name": "Tiny", "base_size": 512, "image_size": 512, "crop_mode": False},
    {"name": "Small", "base_size": 640, "image_size": 640, "crop_mode": False},
    {"name": "Base", "base_size": 1024, "image_size": 1024, "crop_mode": False},
    {"name": "Large", "base_size": 1280, "image_size": 1280, "crop_mode": False},
    {"name": "Gundam", "base_size": 1024, "image_size": 640, "crop_mode": True},
]

results = []

for mode in modes:
    print(f"\n{'='*50}")
    print(f"Testing {mode['name']} mode...")
    print(f"{'='*50}")

    try:
        start_time = time.time()

        output = model.infer(
            tokenizer,
            prompt="<image>\nConvert to markdown.",
            image_file="test_invoice.jpg",
            base_size=mode["base_size"],
            image_size=mode["image_size"],
            crop_mode=mode["crop_mode"]
        )

        elapsed = time.time() - start_time

        result = {
            "mode": mode["name"],
            "success": True,
            "time_seconds": round(elapsed, 2),
            "output_length": len(output)
        }

        print(f"✅ {mode['name']}: {elapsed:.2f}s")
        print(f"Output preview: {output[:200]}...")

    except Exception as e:
        result = {
            "mode": mode["name"],
            "success": False,
            "error": str(e)
        }
        print(f"❌ {mode['name']} failed: {e}")

    results.append(result)

# 打印汇总
print(f"\n{'='*50}")
print("SUMMARY")
print(f"{'='*50}")
for r in results:
    if r["success"]:
        print(f"{r['mode']:10s}: {r['time_seconds']:6.2f}s ✅")
    else:
        print(f"{r['mode']:10s}: FAILED ❌")

EOF
```

**运行测试**：
```bash
python test_all_modes.py
```

**预计耗时**：
- Tiny: ~0.5-1s
- Small: ~1-2s
- Base: ~2-3s
- Large: ~4-6s（如果是 T4 可能 OOM）
- Gundam: ~8-12s（T4 肯定 OOM，RTX 4090 可以）

---

### 4.3 记录测试结果

**操作**：把终端输出复制到记事本

**需要记录的数据**：
```
GPU 型号: Tesla T4 / RTX 4090
VRAM: 16GB / 24GB

测试结果：
- Tiny 模式: 0.8s ✅
- Small 模式: 1.5s ✅
- Base 模式: 2.3s ✅
- Large 模式: OOM ❌ (T4) 或 4.5s ✅ (4090)
- Gundam 模式: OOM ❌ (T4) 或 9.2s ✅ (4090)
```

---

## 📝 第五步：更新文档（30 分钟）

### 5.1 退出 SSH 连接

**操作**：
```bash
exit
```

回到你的 Mac 终端

---

### 5.2 更新 PRD.md 性能数据

**操作**：在你的 Mac 上

```bash
cd /Users/jack/DEV/deepseek-visor-agent
```

打开 `docs/business/PRD.md`，找到性能指标部分，把"估算"/"论文数据"替换为实测值：

**示例**（根据你的实测数据调整）：
```markdown
### 性能指标（✅ GPU 实测数据 - 2025-10-21）

**测试环境**: 阿里云 Tesla T4 (16GB VRAM)

| 推理模式 | 处理时间 | 适用场景 |
|---------|---------|---------|
| Tiny | 0.8s/页 | 轻量文档 |
| Small | 1.5s/页 | 标准文档 |
| Base | 2.3s/页 | 复杂文档 |
| Large | OOM | 需要 24GB+ VRAM |
| Gundam | OOM | 需要 24GB+ VRAM |
```

---

### 5.3 更新 README.md

**操作**：更新性能基准数据

---

### 5.4 Git 提交

**操作**：
```bash
git add docs/business/PRD.md README.md
git commit -m "docs: 更新为 GPU 实测性能数据（阿里云 T4）

- 完成阿里云 Tesla T4 环境验证
- 5 种推理模式完整测试
- Tiny/Small/Base 模式验证通过
- Large/Gundam 模式需要 24GB+ VRAM

测试环境：
- GPU: Tesla T4 (16GB VRAM)
- CUDA: 12.1
- 平台: 阿里云 ecs.gn6i-c4g1.xlarge

🤖 Generated with Claude Code"

git push
```

---

## 🗑️ 第六步：释放实例（1 分钟）

### 6.1 停止实例

**操作**：
```
1. 回到阿里云 ECS 控制台
2. 找到实例 "deepseek-ocr-test"
3. 点击 "更多" → "实例状态" → "停止"
4. 确认停止
```

---

### 6.2 释放实例

**操作**：
```
1. 实例停止后（状态变为"已停止"）
2. 点击 "更多" → "实例状态" → "释放"
3. 勾选 "立即释放"
4. 点击 "确定"
```

✅ 实例删除后，冻结的余额会退回账户

---

## 💰 费用结算

**实际扣费示例**（T4 实例）：
```
开通时间: 14:00
删除时间: 17:30
实际使用: 3.5 小时
单价: ¥1.5/小时
总费用: ¥5.25

流量费: ~¥0.5（下载模型）
合计: ~¥6
```

---

## ✅ 完成检查清单

- [ ] 阿里云 GPU 实例创建成功
- [ ] SSH 连接成功
- [ ] `nvidia-smi` 显示 GPU 信息
- [ ] 代码克隆成功
- [ ] 依赖安装成功
- [ ] 模型下载成功（6.2GB）
- [ ] 5 种推理模式测试完成
- [ ] 测试结果已记录
- [ ] 文档已更新为实测数据
- [ ] Git 提交并推送
- [ ] 阿里云实例已释放
- [ ] 费用已结算

---

## 🚨 常见问题

### Q1: 抢占式实例被回收怎么办？
**A**: 重新创建一个，测试数据在本地记录不会丢失

### Q2: T4 跑 Gundam 模式 OOM 怎么办？
**A**: 正常，记录为"需要 24GB+ VRAM"即可

### Q3: 模型下载很慢怎么办？
**A**: 阿里云到 HuggingFace 速度较慢，可以考虑：
- 使用镜像源
- 或耐心等待（一次性下载，后续缓存）

### Q4: 忘记释放实例怎么办？
**A**:
- 抢占式实例最多运行 24 小时会自动回收
- 或立即登录控制台释放

---

## 📞 需要帮助？

**遇到问题随时告诉我**：
- SSH 连接失败
- 模型下载失败
- 推理报错
- 其他任何问题

**我会实时帮你解决！** 🚀

---

**准备好了就开始吧！** 🎯
