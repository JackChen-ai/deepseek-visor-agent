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
| **低代码平台插件作者**（如 Dify、Flowise） | 为可视化 Agent 添加“视觉输入”节点 | 提供 REST API + Python SDK 双接入 |
| **独立开发者 / Indie Hacker** | 快速构建文档自动化产品（如自动记账、知识库导入） | 免费开源 + 可私有部署 + Lemon Squeezy 商业化模板 |

> ❌ 不面向普通终端用户（如学生、文员）——我们不做 UI 产品，只做开发者基础设施。

---

## 三、核心功能需求（MCP Scope）

### 3.1 核心能力：DeepSeek-OCR Agent Tool（Python SDK）

| 功能 | 说明 | 验收标准 |
|------|------|--------|
| **1. 统一封装推理接口** | 提供 `VisionDocumentTool` 类，隐藏 FlashAttention、GPU、crop_mode 等复杂性 | `tool.run(image_path="invoice.jpg")` 返回结构化结果 |
| **2. 多模式自动适配** | 根据设备自动选择推理模式：<br>- 无 GPU → Tiny 模式（CPU）<br>- 有 GPU 且内存 >16GB → Gundam 模式<br>- 否则 → Base 模式 | 自动 fallback，不崩溃 |
| **3. 输出结构化 JSON** | 不仅返回 Markdown，还解析关键字段：<br>`{"markdown": "...", "fields": {"total": "$199", "date": "2025-10-01"}}` | 支持常见文档类型字段提取（发票、合同、简历） |
| **4. 错误处理与降级** | OOM、CUDA error、图像损坏等场景自动降级或返回友好错误 | 不抛出原始 PyTorch 异常 |
| **5. PyPI 发布** | 包名：`deepseek-ocr-agent` | `pip install deepseek-ocr-agent` 成功 |

### 3.2 辅助能力：轻量 REST API（可选，MCP 阶段非必须）

- 用于 Dify / Flowise 等无 Python 环境的平台；
- 基于 FastAPI + Uvicorn，单文件部署；
- 支持 `POST /ocr` 上传图片，返回 JSON；
- 可选：集成 Lemon Squeezy Webhook 做简单用量控制（MCP 后期）。

---

## 四、非功能需求

| 类别 | 要求 |
|------|------|
| **部署** | 支持 Mac（M 系列）、Linux、Windows（WSL）；GPU/CPU 自动检测 |
| **依赖** | 尽量复用 `transformers` + `flash-attn`，避免引入 heavy 依赖 |
| **许可证** | MIT（鼓励集成、fork、商用） |
| **文档** | README 包含：<br>- 安装命令<br>- 3 个典型用例（发票、合同、论文）<br>- LangChain 集成示例 |
| **性能** | Gundam 模式处理 A4 扫描件 ≤8s（RTX 4090）；Tiny 模式 ≤2s（M2） |

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
| **扩展（60–90 天）** | 支持多项目管理，为不同客户分配独立 API key |

> 💡 关键：**开源 SDK 是获客引擎，托管 API 是变现引擎**。

---

## 七、成功指标（SMART）

| 指标 | 目标（60 天） |
|------|-------------|
| GitHub Stars | ≥300 |
| PyPI 下载量 | ≥1,000 |
| 被 LangChain Awesome List / LlamaIndex 社区收录 | 是 |
| 至少 3 个公开项目引用（GitHub） | 是 |
| Lemon Squeezy 托管 API 付费用户 | ≥10 |

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

