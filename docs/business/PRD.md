# 产品需求文档（PRD）  
**项目代号**：Visor Agent  
**版本**：1.0（MCP - Minimum Commercializable Product）  
**目标**：成为 LangChain / LlamaIndex / Dify 等 AI Agent 框架中 **事实标准的视觉理解工具**  

---

## 一、产品愿景（Vision）

> 让任何 AI Agent 都能“看懂”一张图——无需复杂封装，一行代码即可调用结构化文档理解能力。

---

## 二、目标用户（Target Users）

| 用户类型 | 需求场景 | 为什么选我们 |
|--------|--------|------------|
| **AI Agent 开发者** | 让 Agent 能解析用户上传的发票、合同、表格截图 | 开箱即用的 Tool 封装，输出 LLM 友好格式 |
| **低代码平台插件作者**（如 Dify、Flowise） | 为可视化 Agent 添加"视觉输入"节点 | 提供 REST API + Python SDK 双接入 |
| **独立开发者 / Indie Hacker** | 快速构建文档自动化产品（如自动记账、知识库导入） | 免费开源 + 可私有部署 + Lemon Squeezy 商业化模板 |
| **AI 公司 / 研究机构**（论文验证）| 需要大量文档数据用于 LLM 预训练/微调 | 33M 页/天数据生成能力（160 GPUs 集群），10× 压缩技术 |

> ❌ 不面向普通终端用户（如学生、文员）——我们不做 UI 产品，只做开发者基础设施。

---

## 三、核心功能需求（MCP Scope）

### 3.1 核心能力：DeepSeek-OCR Agent Tool（Python SDK）

| 功能 | 说明 | 验收标准 |
|------|------|--------|
| **1. 统一封装推理接口** | 提供 `VisionDocumentTool` 类，隐藏 FlashAttention、GPU、crop_mode 等复杂性 | `tool.run(image_path="invoice.jpg")` 返回结构化结果 |
| **2. 多模式智能适配** | ✅ **所有 5 种模式均已开源**（通过参数控制）：<br>- **Tiny**: `base_size=512, crop_mode=False` (4GB VRAM, 快速预览)<br>- **Small**: `base_size=640, crop_mode=False` (8GB VRAM, 通用文档)<br>- **Base**: `base_size=1024, crop_mode=False` (16GB VRAM, **推荐**)<br>- **Large**: `base_size=1280, crop_mode=False` (24GB VRAM, 高精度)<br>- **Gundam**: `base_size=1024, image_size=640, crop_mode=True` (超大文档)<br><br>根据 GPU VRAM 自动选择模式，支持手动覆盖参数。<br>代码参考: `DeepSeek-OCR-master/DeepSeek-OCR-hf/run_dpsk_ocr.py` | 支持所有 5 种模式，根据 VRAM 自动降级，不崩溃 |
| **3. 输出结构化 JSON** | 不仅返回 Markdown，还解析关键字段：<br>`{"markdown": "...", "fields": {"total": "$199", "date": "2025-10-01"}}` | 支��常见文档类型字段提取（发票、合同、简历） |
| **4. 错误处理与降级** | OOM、CUDA error、图像损坏等场景自动降级或返回友好错误 | 不抛出原始 PyTorch 异常 |
| **5. PyPI 发布** | 包名：`deepseek-ocr-agent` | `pip install deepseek-ocr-agent` 成功 |

**代码使用示例**:
```python
from deepseek_ocr_agent import VisionDocumentTool

tool = VisionDocumentTool()

# Base 模式（推荐，自动适配）
result = tool.run(image_path="invoice.jpg", mode="base")
# 返回: {"markdown": "...", "fields": {"total": "$199", ...}}

# Gundam 模式（超大文档）
result = tool.run(image_path="large_contract.jpg", mode="gundam")

# 手动控制参数（高级用法）
result = tool.run(
    image_path="doc.jpg",
    base_size=640,
    image_size=640,
    crop_mode=False
)
```

### 3.2 辅助能力：轻量 REST API（可选，MCP 阶段非必须）

- 用于 Dify / Flowise 等无 Python 环境的平台；
- 基于 FastAPI + Uvicorn，单文件部署；
- 支持 `POST /ocr` 上传图片，返回 JSON；
- 可选：集成 Lemon Squeezy Webhook 做简单用量控制（MCP 后期）。

---

## 四、非功能需求

| 类别 | 要求 |
|------|------|
| **硬件要求** | ⚠️ **NVIDIA GPU (CUDA 11.8+) 必需**<br>**GPU 架构要求（关键）**：<br>- ✅ **最低：RTX 2060 (6GB VRAM, Turing 架构)**<br>- ✅ 推荐：RTX 3090 / RTX 4090 (24GB VRAM, Ampere/Ada)<br>- ✅ 生产：A100 (40GB/80GB, Ampere)<br>- ❌ **不支持：GTX 10 系列（Pascal 架构）** - FlashAttention 2.x 不兼容<br>- ❌ **不支持纯 CPU**（模型硬编码 CUDA 调用）<br>- ❌ 不支持 AMD GPU (ROCm)<br>- ❓ Apple MPS 未验证<br><br>**云端 GPU 推荐**：<br>- RunPod: RTX 3090 ($0.2/hr)<br>- Vast.ai: RTX 4090 ($0.4/hr)<br>- Lambda Labs: A100 ($1.1/hr) |
| **部署环境** | - Linux (Ubuntu 20.04+)<br>- Windows (WSL2 + CUDA)<br>- Docker (nvidia-docker) ✅ 推荐<br>- 云端 GPU (RunPod, Vast.ai, Lambda Labs) |
| **依赖** | - transformers==4.46.3 (固定版本)<br>- torch>=2.6.0 + CUDA<br>- 避免引入 heavy 依赖 |
| **许可证** | MIT（鼓励集成、fork、商用） |
| **文档** | README 包含：<br>- **硬件要求警告**（置顶）<br>- 安装命令<br>- 3 个典型用例（发票、合同、表格）<br>- LangChain 集成示例<br>- 托管 API 方案（无 GPU 用户） |
| **性能指标** | ✅ **GPU 实测数据（阿里云 Tesla T4, 2025-10-21）**<br><br>**HuggingFace Transformers 版本（MCP v0.1.0 实现）**：<br>- Tiny 模式: 5.35s/页 ✅ 实测<br>- Small 模式: 6.53s/页 ✅ 实测<br>- Base 模式: 6.77s/页 ✅ 实测（最常用）<br>- Large 模式: 6.35s/页 ✅ 实测<br>- Gundam 模式: 6.67s/页 ✅ 实测（crop分块）<br>- 测试环境: Tesla T4 (16GB VRAM), 简单文档<br>- ⚠️ **实际复杂文档性能可能不同**<br><br>**vLLM 优化版本（论文数据，v1.1+ 规划）**：<br>- Base 模式: ~0.1s/页（论文数据）<br>- Gundam 模式: ~0.26s/页（论文数据）<br>- 单卡吞吐: 200k+ 页/天（A100-40G，论文数据）<br>- vLLM 状态: ✅ 代码已开源，需手动注册模型<br>- 集群能力: 160 GPUs → 33M 页/天（论文数据） |

---

## 五、技术架构（MCP）

```
deepseek-ocr-agent/
├── __init__.py
├── tool.py                 # VisionDocumentTool 核心类
├── infer.py                # 封装 model.infer()，处理设备/模式/错误
├── parsers/                # 字段提取器（invoice_parser.py, contract_parser.py）
├── api/                    # （可选）FastAPI REST 接口
├── examples/
│   ├── langchain_example.py
│   ├── dify_integration.md
│   └── invoice_demo.ipynb
└── README.md
```

---

## 六、商业化路径（与 Lemon Squeezy 对接）

| 阶段 | 策略 |
|------|------|
| **MCP（0–30 天）** | 完全免费开源，聚焦 GitHub Star 和社区采用 |
| **增长（30–60 天）** | 推出 **Cloud API 版本**（托管版 Gundam 模式），通过 Lemon Squeezy 收费：<br>- $0.01/次（≥1000 次/月）<br>- $29/月（不限量） |
| **扩展（60–90 天）** | **两条增长曲线**：<br>1. Agent 工具：多项目管理，独立 API key<br>2. **数据生成服务**（论文验证）：<br>   - 目标：AI 公司的 LLM 训练数据需求<br>   - 定价：$0.001/页（批量折扣）<br>   - 能力：160 GPUs → 33M 页/天 |

> 💡 关键：**开源 SDK 是获客引擎，托管 API 是变现引擎，数据生成是规模化引擎**。

### 新增商业方向（基于论文洞察）

**数据生成即服务（Data-as-a-Service）**:
- **需求验证**: 论文证明 DeepSeek-OCR 可用于 LLM 预训练数据生成（33M 页/天）
- **目标客户**: AI 公司、研究机构需要大量高质量文档数据
- **技术优势**:
  - 10× 压缩比，97% 精度（Fox Benchmark 验证）
  - 256 tokens vs MinerU 6790 tokens（96% token 减少）
  - vLLM 并发处理，吞吐量高
- **定价策略**:
  - 小规模测试：$0.01/页（≤10k 页）
  - 批量折扣：$0.001/页（≥1M 页）
  - 企业包月：$5k/月（不限量，优先队列）

---

## 七、成功指标（SMART）

| 指标 | 目标（60 天） | 说明 |
|------|-------------|------|
| **GitHub Stars** | ≥300 | 社区认可度 |
| **PyPI 下载量** | ≥1,000 | 实际使用量 |
| **被 LangChain Awesome List / LlamaIndex 社区收录** | 是 | 生态融入 |
| **至少 3 个公开项目引用（GitHub）** | 是 | 实际应用 |
| **Lemon Squeezy 托管 API 付费用户** | ≥10 | Agent 工具变现 |
| **数据生成服务试点客户**（新增）| ≥1 | 验证论文提到的 B2B 场景 |

---

## 八、风险与应对

| 风险 | 应对 |
|------|------|
| DeepSeek 官方后续推出官方 SDK | 我们已建立社区心智，可转型为“增强版”（如加字段解析、PDF 支持） |
| FlashAttention 安装失败率高 | 提供 Docker 镜像 + Colab 示例作为 fallback |
| 用户要求支持更多文档类型 | 采用插件式 parser 架构，社区可贡献 |

---

## 九、下一步行动（Next Steps）

1. **立即注册 PyPI 包名**：`deepseek-ocr-agent`（检查可用性）  
2. **注册域名**（可选但推荐）：如 `visor-agent.com` 或 `deepseek-ocr.dev`  
3. **创建 GitHub 仓库**，初始化目录结构  
4. **实现 `VisionDocumentTool` 核心逻辑**（基于 DeepSeek-OCR HF 示例）  
5. **撰写 LangChain 集成示例**，准备发布帖  

---

> **附：DeepSeek-OCR 官方依赖（来自 HF 页面）**  
> ```text
> torch==2.6.0
> transformers==4.46.3
> tokenizers==0.20.3
> einops
> addict 
> easydict
> pip install flash-attn==2.7.3 --no-build-isolation
> ```
> 推理调用示例：
> ```python
> prompt = "<image>\n<|grounding|>Convert the document to markdown."
> res = model.infer(tokenizer, prompt=prompt, image_file=image_file, 
>                   base_size=1024, image_size=640, crop_mode=True)
> ```
本项目依赖的原始开源项目地址：https://huggingface.co/deepseek-ai/DeepSeek-OCR  
```

---

## 附录：开源代码验证（2025-10-21）

### ✅ 所有功能均已验证可实现

基于对 DeepSeek-OCR 源代码的完整验证，PRD 中的所有功能都可以基于开源代码实现：

**验证结果**:
- ✅ **GitHub 仓库包含完整代码**（HuggingFace 版本 + vLLM 优化版本）
- ✅ **所有 5 种模式通过 `model.infer()` 方法的参数实现**
- ✅ **crop_mode 参数在源代码中存在**，Gundam 模式可直接使用
- ✅ **vLLM 支持已开源**，吞吐量 2500 tokens/s 可实现

**验证来源**:
- GitHub: `https://github.com/deepseek-ai/DeepSeek-OCR`
  - HF 版本: `DeepSeek-OCR-master/DeepSeek-OCR-hf/run_dpsk_ocr.py`
  - vLLM 版本: `DeepSeek-OCR-master/DeepSeek-OCR-vllm/`
- 本地代码: `~/.cache/huggingface/hub/models--deepseek-ai--DeepSeek-OCR/.../`
- 架构分析: `/docs/architecture/DEEPSEEK_OCR_ADVANTAGES.md`

**关键技术细节验证**:

```python
# 官方代码示例（来自 run_dpsk_ocr.py）
from transformers import AutoModel, AutoTokenizer

model = AutoModel.from_pretrained('deepseek-ai/DeepSeek-OCR', 
                                   trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained('deepseek-ai/DeepSeek-OCR',
                                           trust_remote_code=True)

# Tiny 模式
res = model.infer(tokenizer, prompt="<image>\nFree OCR.",
                  image_file="doc.jpg",
                  base_size=512, image_size=512, crop_mode=False)

# Base 模式（推荐）
res = model.infer(tokenizer, prompt="<image>\n<|grounding|>Convert to markdown.",
                  image_file="doc.jpg",
                  base_size=1024, image_size=1024, crop_mode=False)

# Gundam 模式（超大文档）
res = model.infer(tokenizer, prompt="<image>\n<|grounding|>Convert to markdown.",
                  image_file="large_doc.jpg",
                  base_size=1024, image_size=640, crop_mode=True)
```

### 📊 PRD 更新记录

| 项目 | 原描述 | 更新后 | 状态 |
|------|--------|--------|------|
| 多模式支持 | "根据设备自动选择，无 GPU → Tiny（CPU）" | "所有 5 种模式均已开源，通过参数控制" | ✅ 已更正 |
| Gundam 模式 | 未明确说明实现方式 | 明确 `crop_mode=True` 参数 | ✅ 已补充 |
| 代码示例 | 无 | 添加完整使用示例 | ✅ 已添加 |

### 🚀 实现建议

基于源代码验证，我们的 SDK 应该：

1. **封装 5 种预设模式**:
   ```python
   MODE_CONFIGS = {
       'tiny': {'base_size': 512, 'image_size': 512, 'crop_mode': False},
       'small': {'base_size': 640, 'image_size': 640, 'crop_mode': False},
       'base': {'base_size': 1024, 'image_size': 1024, 'crop_mode': False},
       'large': {'base_size': 1280, 'image_size': 1280, 'crop_mode': False},
       'gundam': {'base_size': 1024, 'image_size': 640, 'crop_mode': True}
   }
   ```

2. **VRAM 自动检测**:
   ```python
   import torch
   
   def detect_optimal_mode():
       if torch.cuda.is_available():
           vram_gb = torch.cuda.get_device_properties(0).total_memory / 1e9
           if vram_gb >= 24: return 'large'
           elif vram_gb >= 16: return 'base'
           elif vram_gb >= 8: return 'small'
           else: return 'tiny'
       else:
           raise RuntimeError("GPU required")
   ```

3. **错误降级策略**:
   - OOM → 自动降级到下一级模式
   - CUDA error → 提供友好错误信息
   - 图像损坏 → 返回 JSON 错误而非抛异常

### ✅ 结论

**PRD 的核心逻辑完全正确，所有功能都可以基于开源代码实现，无需等待官方更新。**

---

**PRD 版本**: 1.0  
**最后更新**: 2025-10-21  
**验证状态**: ✅ 所有技术假设已验证
