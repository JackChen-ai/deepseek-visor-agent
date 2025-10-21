# 🚀 Visor Agent 项目开发计划 v2.0（融合版 - 75 天）

> **目标定位**：成为 AI Agent 生态的标准视觉理解工具
> **核心价值**：开箱即用 + LLM 友好输出 + 自动降级策略
> **商业模式**：开源 SDK 获客 → 托管 API 变现

---

## 📋 项目资产

| 资产类型 | 推荐名称 | 备选方案 | 状态 |
|---------|---------|---------|------|
| **PyPI 包名** | `deepseek-visor-agent` | ~~`deepseek-ocr-agent`~~ | ✅ 已验证可用 |
| **GitHub 仓库** | `deepseek-visor-agent` | - | ✅ 本地已创建 |
| **域名** | `visor-agent.com` | `deepseek-ocr.dev` | ⏳ 待注册 |
| **品牌定位** | "Standard Vision Tool for AI Agents" | - | ✅ 已确定 |

**注意**：项目统一使用 `deepseek-visor-agent` 命名（PyPI 用连字符，Python 包用下划线 `deepseek_visor_agent`）

---

## 📅 第 1 周（Day 1-7）：奠基与验证

### 本周目标
✅ 能在本地调用 DeepSeek-OCR 并输出结构化 Markdown

### 任务清单

| 任务 | 交付物 | 验收标准 | 技术要点 | 状态 |
|------|--------|---------|---------|------|
| **1.1 注册项目资产** | - GitHub 仓库（public）<br>- PyPI 包名预留<br>- 域名注册 | `pip search deepseek-visor-agent` 无冲突 | 使用 `twine` 上传占位包（v0.0.1） | ✅ 部分完成 |
| **1.2 环境验证** | - 本地成功运行 HF 示例<br>- 测试 Tiny/Small/Base/Large/Gundam 5 种推理模式 | 能处理发票/合同/表格图像 | 测试设备：RTX 4090 + M2 Mac | ⏳ 待完成 |
| **1.3 初始化项目结构** | 完整目录树（见下方） | `pytest --collect-only` 通过 | 包含占位符文件 | ✅ 已完成 |
| **1.4 依赖管理** | `requirements.txt` + `requirements-dev.txt` | `pip install -r requirements.txt` 成功 | 可选依赖用 `extras_require` | ✅ 已完成 |
| **1.5 设备检测模块** | `device_manager.py` | 通过单元测试 | 检测 CUDA/MPS/CPU + 内存估算 | ✅ 已完成 |


**Day 1-2 完成情况（2025-10-20）** ✅ **超预期完成**

### ✅ 基础设施（Day 1）
- PyPI 包名验证：`deepseek-visor-agent` 可用
- 本地 Git 仓库初始化
- 完整项目结构（31 个文件，~2600 行代码）
- 核心模块框架：device_manager, infer, tool, parsers
- 配置文件：pyproject.toml, requirements.txt, setup.py, .gitignore, LICENSE
- 示例文件：LangChain, LlamaIndex, Dify 集成指南
- 测试框架：单元测试模板 + GitHub Actions CI/CD
- 首次 Git 提交

### ✅ GitHub 集成（Day 2）
- 远程仓库创建：https://github.com/JackChen-ai/deepseek-visor-agent
- 成功推送 12 次提交
- 所有核心代码已同步

### ✅ 依赖与版本兼容（Day 2 - 关键突破）
- **解决 transformers 版本问题**：必须使用 4.46.3
  - ❌ 4.51.x/4.57.x：LlamaFlashAttention2 导入错误
  - ✅ 4.46.3：经过验证可用
- 模型下载：6.2 GB DeepSeek-OCR 已缓存至 `~/.cache/huggingface/`
- 所有依赖安装成功

### ✅ 推理引擎修复（Day 2）
- 修复模型加载：`AutoModelForCausalLM` → `AutoModel`（符合官方API）
- 添加 `output_path` 参数（tempfile.TemporaryDirectory）
- 正确的设备/dtype 处理（CUDA: bfloat16, MPS: float32）
- 推理参数正确传递：base_size, image_size, crop_mode

### ✅ Parser 完整实现（Day 2）
- **InvoiceParser**：多货币支持（$,€,£,¥）、多日期格式、智能vendor提取
- **ContractParser**：合同方识别、生效日期、类型分类、期限和管辖法律提取
- **Classifier 增强**：加权评分、模式匹配、置信度阈值

### ✅ 测试与文档（Day 2）
- `test_simple_inference.py` 验证脚本
- `DAY2_COMPLETION_REPORT.md` 完整报告（248行）
- `CLAUDE.md` 版本兼容性说明
- `requirements.txt` 固定关键版本

### 🚨 **重大发现：硬件限制分析（Day 2）**

**问题**: 在 M1 Mac 上测试时发现 DeepSeek-OCR 模型内部有**硬编码的 `.cuda()` 调用**

**证据**:
```python
# modeling_deepseekocr.py Line 917
input_ids.unsqueeze(0).cuda(),  # 无视设备参数，强制 CUDA
```

**影响**:
- ❌ **纯 CPU 不支持**（即使指定 device="cpu"）
- ❌ AMD GPU (ROCm) 不支持
- ❓ Apple MPS 未验证（理论上也会失败）
- ✅ NVIDIA GPU (CUDA) 完全支持

**根本原因**: DeepSeek-OCR 是研究项目，未做设备抽象层，面向拥有 NVIDIA GPU 的用户

**我们的应对策略** ✅:
1. **接受限制**：这是上游模型的设计，不是我们的 bug
2. **明确文档**：在 README/PRD 置顶说明 GPU 要求
3. **商业化机会**：托管 API 反而成为核心变现产品（解决无 GPU 用户需求）
4. **目标用户匹配**：AI Agent 开发者通常有 GPU 访问（云端或本地）

**详细分析文档**: 见 [CRITICAL_LIMITATION_ANALYSIS.md](CRITICAL_LIMITATION_ANALYSIS.md)

### ✅ **P0 文档更新（Day 3 - 2025-10-21）** - 已完成

**关键外部反馈**: 发现 GTX 1080 Ti 兼容性错误（Pascal 架构不支持 FlashAttention 2.x）

**紧急修复完成**:
- [x] 更新 PRD.md 硬件要求：最低 GPU 从 GTX 1080 Ti 改为 RTX 2060 (Turing+) ✅
- [x] 更新 PRD.md 性能指标：区分 Transformers (估算) vs vLLM (论文数据) ✅
- [x] 更新 README.md: 添加 GPU Requirements 警告部分（置顶） ✅
- [x] 创建 GPU_COMPATIBILITY.md：详细兼容性表格、云端GPU指南、故障排查 ✅

**技术核心发现**:
- ✅ FlashAttention 2.x 要求 compute capability 7.5+ (Turing/Ampere/Ada)
- ❌ Pascal 架构 (GTX 10 系列) 是 sm_60/61，不支持
- ✅ 最低要求: RTX 2060 (sm_75, 6GB VRAM)
- ✅ vLLM 状态: 代码已开源，需手动注册模型（非原生支持）

### ⏳ **待完成任务（Day 3-7 调整后优先级）**

**P0 - 获取 GPU 环境验证** ⚠️ **阻塞任务**
- [ ] 租用 RunPod GPU 实例（RTX 3090, $0.2/hr）
- [ ] 运行 `test_simple_inference.py` 完整测试
- [ ] 验证 5 种推理模式（tiny/small/base/large/gundam）
- [ ] 记录性能基准数据（A4 扫描件处理时间）
- [ ] 测试自动降级机制（模拟 OOM）
- [ ] 更新所有文档中的性能数据为实测值（移除"估算"/"论文数据"标注）
- **预算**: $10（可完成所有验证）
- **时间**: 1-2 天

**P1 - 文档完善**（P0 完成后）
- [x] 更新 README.md 添加硬件要求警告（置顶）✅
- [ ] 补充安装步骤（CUDA 检查）
- [ ] 添加 3 个快速示例
- [ ] 添加"无 GPU？使用托管 API"指引

**P2 - 测试扩充**（可在无 GPU 环境完成）
- [ ] 添加 Parser 单元测试（纯字符串解析，不需要推理）
- [ ] 添加 Classifier 测试用例
- [ ] 添加 DeviceManager 测试

**P3 - PyPI 占位包**（Week 2）
- [ ] `python -m build`
- [ ] `twine upload dist/*`
- [ ] 发布 v0.0.1（标注 "Pre-release - GPU required"）

---

### 📊 **进度评估：超前约 5 天** 🎉

| 原计划 | 实际完成 | 评价 |
|--------|---------|------|
| Day 1-2: 项目初始化 | ✅ 100% | 符合预期 |
| Day 3-5: 环境验证 | 🟡 70% (缺 GPU 测试) | 受硬件限制 |
| Day 8-14: Parser 实现 | ✅ 100% | 🚀 超前 7 天 |
| Day 15-21: 文档 | 🟡 80% | 🚀 超前 10 天 |

**关键成就**:
1. ✅ 版本兼容问题 2 天内解决（原计划可能需要 1 周）
2. ✅ Parser 实现完整度高（非占位代码，可直接使用）
3. ✅ 发现并分析硬件限制（避免后续返工）

**唯一缺口**: GPU 推理验证（非代码问题，是环境限制）

---

### 🎯 **当前阻塞 & 解决方案**

#### 阻塞 1: Mac M1 无法运行推理测试

**原因**: DeepSeek-OCR 模型硬编码 CUDA 调用

**影响范围**:
- ❌ 无法验证实际推理效果
- ❌ 无法测试 5 种推理模式
- ❌ 无法获取性能基准数据

**解决方案** ✅:
```bash
# 方案 1: 云端 GPU（推荐）
# 注册 RunPod/Vast.ai，租用 RTX 3090
# 成本：$0.2/hr × 4hr = $0.8

# 方案 2: Colab Pro（备选）
# $10/月，包含 T4/V100 GPU
# 适合持续开发

# 方案 3: 本地 eGPU（不推荐）
# 成本高（$500+），仅为此项目不划算
```

**推荐**: RunPod，原因：
- 按需计费，无月费
- RTX 3090 性能强劲
- SSH 访问，可直接运行 pytest

#### 阻塞 2: 无法发布 PyPI（缺少实际验证）

**影响**: 无法确保用户安装后能正常运行

**解决方案**: 分阶段发布
- Week 1: 发布 v0.0.1-pre（标注 "Pre-release, GPU validation pending"）
- Week 2: GPU 验证后发布 v0.1.0（稳定版）


### 项目结构（完整版）

```
deepseek-ocr-agent/
├── deepseek_ocr_agent/
│   ├── __init__.py
│   ├── tool.py              # VisionDocumentTool 核心类
│   ├── infer.py             # 推理引擎封装
│   ├── device_manager.py    # GPU/CPU 自动检测
│   ├── parsers/
│   │   ├── __init__.py
│   │   ├── base.py          # BaseParser 抽象类
│   │   ├── invoice.py       # 发票解析器
│   │   ├── contract.py      # 合同解析器
│   │   └── classifier.py    # 文档类型识别
│   ├── api/                 # FastAPI（可选）
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── schemas.py
│   └── utils/
│       ├── error_handler.py # 异常处理 + 自动降级
│       └── validators.py
├── examples/
│   ├── langchain_example.py
│   ├── llamaindex_example.py
│   ├── dify_integration.md
│   └── notebooks/
│       └── invoice_demo.ipynb
├── tests/
│   ├── test_device_manager.py
│   ├── test_tool.py
│   ├── test_parsers.py
│   ├── benchmark.py
│   └── fixtures/
│       ├── invoice_sample.jpg
│       ├── contract.pdf
│       └── resume.png
├── docs/
│   ├── installation.md
│   ├── quickstart.md
│   ├── api_reference.md
│   └── troubleshooting.md
├── .github/
│   └── workflows/
│       ├── test.yml
│       └── publish.yml
├── setup.py
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
├── LICENSE (MIT)
└── README.md
```

### 核心代码框架

#### 1.5.1 设备检测模块（device_manager.py）

```python
import torch
import psutil
from typing import Dict

class DeviceManager:
    """自动检测最优设备配置"""

    @staticmethod
    def detect_optimal_config() -> Dict[str, any]:
        """
        返回：{
            "device": "cuda" | "mps" | "cpu",
            "inference_mode": "gundam" | "large" | "base" | "small" | "tiny",
            "use_flash_attn": bool,
            "max_memory_gb": float
        }
        """
        config = {
            "device": "cpu",
            "inference_mode": "tiny",
            "use_flash_attn": False,
            "max_memory_gb": 0
        }

        # 1. 检测 CUDA
        if torch.cuda.is_available():
            config["device"] = "cuda"
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
            config["max_memory_gb"] = gpu_memory

            # 根据显存选择推理模式
            if gpu_memory >= 48:
                config["inference_mode"] = "gundam"
            elif gpu_memory >= 24:
                config["inference_mode"] = "base"
            else:
                config["inference_mode"] = "tiny"

            # 检查 FlashAttention
            try:
                import flash_attn
                config["use_flash_attn"] = True
            except ImportError:
                pass

        # 2. 检测 Apple Silicon MPS
        elif torch.backends.mps.is_available():
            config["device"] = "mps"
            config["inference_mode"] = "tiny"  # M2 建议用 Tiny 模式
            config["max_memory_gb"] = psutil.virtual_memory().available / 1e9

        # 3. CPU 模式
        else:
            config["max_memory_gb"] = psutil.virtual_memory().available / 1e9

        return config
```

---

## 📅 第 2-3 周（Day 8-21）：核心功能开发

### 本周目标
✅ 外部开发者 `pip install` 后，3 行代码让 LangChain Agent 看懂发票

### 任务清单

| 任务 | 交付物 | 验收标准 | 技术要点 |
|------|--------|---------|---------|
| **2.1 推理引擎封装** | `infer.py` | 能自动处理 GPU/CPU + 模式选择 | 封装 HF 的 `model.infer()` |
| **2.2 错误处理策略** | `utils/error_handler.py` | OOM 自动降级：Gundam→Base→Tiny | 使用装饰器模式 |
| **2.3 Tool 类实现** | `tool.py` | 统一 API：`tool.run("invoice.jpg")` | 支持 path/bytes/URL 输入 |
| **2.4 Invoice Parser** | `parsers/invoice.py` | 提取 total/date/vendor | 正则 + 启发式规则 |
| **2.5 文档类型识别** | `parsers/classifier.py` | 自动识别发票/合同/简历 | 基于关键词匹配 |
| **2.6 单元测试** | `tests/test_*.py` | pytest 覆盖率 ≥70% | 使用 fixtures 准备测试图像 |
| **2.7 LangChain 集成** | `examples/langchain_example.py` | 3 行代码让 Agent 识别发票 | 使用 `@tool` 装饰器 |
| **2.8 PyPI v0.1 发布** | `pip install deepseek-ocr-agent==0.1.0` | 安装成功率 >95% | 使用 `build` + `twine` |

### 核心代码框架

#### 2.1 推理引擎（infer.py）

```python
from typing import Dict, Union
from pathlib import Path
import time
import torch
from .device_manager import DeviceManager
from .utils.error_handler import auto_fallback_decorator

class DeepSeekOCRInference:
    def __init__(self, inference_mode="auto", device="auto"):
        """
        Args:
            inference_mode: "auto" | "gundam" | "large" | "base" | "small" | "tiny"
            device: "auto" | "cuda" | "mps" | "cpu"
        """
        self.config = DeviceManager.detect_optimal_config()

        if inference_mode != "auto":
            self.config["inference_mode"] = inference_mode
        if device != "auto":
            self.config["device"] = device

        self.model = self._load_model()
        self.tokenizer = self._load_tokenizer()

    def _load_model(self):
        """加载 DeepSeek-OCR 模型（单一模型 ID）"""
        from transformers import AutoModelForCausalLM

        # DeepSeek-OCR has only ONE model
        model_id = "deepseek-ai/DeepSeek-OCR"

        # 加载参数
        load_kwargs = {
            "trust_remote_code": True,
            "torch_dtype": torch.bfloat16 if self.config["device"] != "cpu" else torch.float32,
        }

        if self.config["use_flash_attn"]:
            load_kwargs["attn_implementation"] = "flash_attention_2"

        return AutoModelForCausalLM.from_pretrained(model_id, **load_kwargs).to(self.config["device"])

    def _load_tokenizer(self):
        """加载 Tokenizer"""
        from transformers import AutoTokenizer
        model_id = "deepseek-ai/DeepSeek-OCR"
        return AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)

    @auto_fallback_decorator
    def infer(
        self,
        image_path: Union[str, Path],
        prompt: str = "<image>\n<|grounding|>Convert the document to markdown.",
        **kwargs
    ) -> Dict[str, any]:
        """
        推理接口

        返回：{
            "markdown": str,
            "raw_output": str,
            "metadata": {
                "inference_mode": str,
                "device": str,
                "inference_time_ms": int
            }
        }
        """
        start_time = time.time()

        # 1. 图像预处理
        from PIL import Image
        image = Image.open(image_path).convert("RGB")

        # 2. 调用模型
        output = self.model.infer(
            self.tokenizer,
            image,
            prompt,
            **kwargs
        )

        # 3. 输出标准化
        inference_time = int((time.time() - start_time) * 1000)

        return {
            "markdown": output,
            "raw_output": output,
            "metadata": {
                "inference_mode": self.config["inference_mode"],
                "device": self.config["device"],
                "inference_time_ms": inference_time
            }
        }
```

#### 2.2 错误处理装饰器（utils/error_handler.py）

```python
from functools import wraps
import logging

logger = logging.getLogger(__name__)

class OCRError(Exception):
    """基础异常类"""
    pass

class OOMError(OCRError):
    """内存不足"""
    pass

class InferenceModeError(OCRError):
    """推理模式错误"""
    pass

def auto_fallback_decorator(func):
    """自动降级装饰器：Gundam → Large → Base → Small → Tiny → 报错"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        modes = ["gundam", "large", "base", "small", "tiny"]
        current_mode = self.config["inference_mode"]

        # 从当前模式开始尝试
        start_idx = modes.index(current_mode) if current_mode in modes else 0

        for mode in modes[start_idx:]:
            try:
                if mode != current_mode:
                    logger.warning(f"Falling back to {mode} mode...")
                    # Only change inference_mode, don't reload model
                    self.config["inference_mode"] = mode

                return func(self, *args, **kwargs)

            except (RuntimeError, torch.cuda.OutOfMemoryError) as e:
                logger.error(f"{mode} mode failed: {e}")
                torch.cuda.empty_cache()  # 清空显存
                continue

        raise OCRError("All inference modes failed. Try using CPU mode or smaller images.")

    return wrapper
```

#### 2.3 Tool 类（tool.py）

```python
from typing import Dict, Union, Optional
from pathlib import Path
from .infer import DeepSeekOCRInference
from .parsers.classifier import classify_document
from .parsers import InvoiceParser, ContractParser

class VisionDocumentTool:
    """统一工具接口，兼容 LangChain/LlamaIndex"""

    def __init__(self, inference_mode="auto", device="auto"):
        self.engine = DeepSeekOCRInference(inference_mode, device)
        self.parsers = {
            "invoice": InvoiceParser(),
            "contract": ContractParser(),
        }

    def run(
        self,
        image_path: Union[str, Path],
        document_type: str = "auto",
        extract_fields: bool = True
    ) -> Dict[str, any]:
        """
        主入口

        Args:
            image_path: 图片路径
            document_type: "auto" | "invoice" | "contract" | "resume"
            extract_fields: 是否提取结构化字段

        Returns:
            {
                "markdown": str,
                "fields": dict,
                "confidence": float,
                "document_type": str
            }
        """
        # 1. OCR 推理
        result = self.engine.infer(image_path)
        markdown = result["markdown"]

        # 2. 文档类型识别
        if document_type == "auto":
            document_type = classify_document(markdown)

        # 3. 字段提取
        fields = {}
        confidence = 1.0

        if extract_fields and document_type in self.parsers:
            parser = self.parsers[document_type]
            fields = parser.parse(markdown)
            confidence = parser.get_confidence()

        return {
            "markdown": markdown,
            "fields": fields,
            "confidence": confidence,
            "document_type": document_type,
            "metadata": result["metadata"]
        }
```

#### 2.7 LangChain 集成示例（examples/langchain_example.py）

```python
from langchain.tools import tool
from deepseek_ocr_agent import VisionDocumentTool

# 初始化工具
ocr_tool = VisionDocumentTool()

@tool
def extract_invoice_data(image_path: str) -> dict:
    """从发票图片中提取金额、日期、供应商等信息"""
    return ocr_tool.run(image_path, document_type="invoice")

# 集成到 Agent
from langchain.agents import initialize_agent, AgentType
from langchain.llms import OpenAI

tools = [extract_invoice_data]
agent = initialize_agent(
    tools,
    OpenAI(temperature=0),
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

# 使用
response = agent.run("从这张发票提取总金额：invoice.jpg")
print(response)
```

---

## 📅 第 4 周（Day 22-28）：测试与质量保障

### 本周目标
✅ pytest 覆盖率 ≥80%，无 critical bug

### 任务清单

| 任务 | 交付物 | 验收标准 |
|------|--------|---------|
| **3.1 完善单元测试** | 覆盖所有核心模块 | pytest 通过，覆盖率 ≥80% |
| **3.2 集成测试** | LangChain + LlamaIndex | 能成功调用并返回结果 |
| **3.3 性能基准测试** | `tests/benchmark.py` | Gundam模式+4090 ≤8s, Tiny模式+M2 ≤2s |
| **3.4 错误场景测试** | 测试 OOM、推理失败 | 自动降级成功 |
| **3.5 文档完善** | README + 安装指南 | 新用户能独立完成安装 |

### 测试用例示例

```python
# tests/test_tool.py
import pytest
from deepseek_ocr_agent import VisionDocumentTool

def test_invoice_extraction():
    """测试发票字段提取"""
    tool = VisionDocumentTool()
    result = tool.run("tests/fixtures/invoice_sample.jpg")

    assert result["document_type"] == "invoice"
    assert result["fields"]["total"] == "$199.00"
    assert result["fields"]["date"] == "2024-01-15"
    assert result["confidence"] > 0.8

def test_auto_fallback():
    """测试自动降级机制"""
    tool = VisionDocumentTool(inference_mode="gundam")
    # 模拟 OOM（使用巨大图片）
    result = tool.run("tests/fixtures/large_image.jpg")
    assert result["metadata"]["inference_mode"] in ["large", "base", "small", "tiny"]

def test_cpu_mode():
    """测试 CPU 模式"""
    tool = VisionDocumentTool(device="cpu")
    result = tool.run("tests/fixtures/contract.pdf")
    assert result["markdown"] is not None
    assert result["metadata"]["device"] == "cpu"
```

---

## 📅 第 5 周（Day 29-35）：社区冷启动

### 本周目标
✅ GitHub Stars ≥50，至少 5 个外部项目引用

### 任务清单

| 任务 | 交付物 | 渠道 | 话术示例 |
|------|--------|------|---------|
| **4.1 完善 README** | 安装指南 + 3 个用例 | GitHub | 突出"Agent-ready"定位 |
| **4.2 社区发布** | 发帖 + Demo | Reddit, Discord, Indie Hackers | "I made DeepSeek-OCR work as a LangChain Tool" |
| **4.3 Hugging Face Spaces** | 在线 Demo | HF Spaces | 上传 invoice_demo 笔记本 |
| **4.4 提交 PR** | 收录到官方列表 | LangChain Awesome, LlamaIndex Hub | - |
| **4.5 博客文章** | 技术博客 | Medium, Dev.to | "Building an Agent-Ready OCR Tool" |

### README 模板

```markdown
# DeepSeek OCR Agent

> Standard vision tool for AI agents - Convert documents to structured data in 3 lines of code

## ⚡ Quick Start

```python
from deepseek_ocr_agent import VisionDocumentTool

tool = VisionDocumentTool()
result = tool.run("invoice.jpg")
print(result["fields"]["total"])  # $199.00
```

## 🎯 Features

- ✅ **Agent-Ready**: Works with LangChain, LlamaIndex, Dify
- ✅ **Auto Fallback**: Gundam → Base → Tiny (OOM safe)
- ✅ **Multi-Device**: CUDA, Apple MPS, CPU
- ✅ **Structured Output**: Extract fields automatically

## 📦 Installation

```bash
pip install deepseek-ocr-agent

# Optional: For RTX GPUs
pip install deepseek-ocr-agent[flash-attn]
```

## 🔗 Integrations

### LangChain
```python
from langchain.tools import tool

@tool
def extract_invoice(image_path: str) -> dict:
    """Extract invoice data"""
    return VisionDocumentTool().run(image_path)
```

### Dify
See [integration guide](docs/dify_integration.md)

## ⚡ Performance

| Inference Mode | Device | Time (A4 scan) |
|-------|--------|----------------|
| Gundam | RTX 4090 | 6.2s |
| Base | RTX 3090 | 12s |
| Tiny | M2 Mac | 1.8s |

## 📚 Documentation

- [Installation Guide](docs/installation.md)
- [API Reference](docs/api_reference.md)
- [Troubleshooting](docs/troubleshooting.md)

## 🛣️ Roadmap

- [x] v0.1: Invoice + Contract parsers
- [ ] v0.2: PDF support
- [ ] v0.3: Multi-language support
- [ ] v0.4: Hosted API

## 📄 License

MIT
```

### 社区推广渠道清单

| 渠道 | 目标受众 | 发布时机 | KPI |
|------|---------|---------|-----|
| **r/MachineLearning** | ML 研究者 | Week 5 Day 1 | 50+ upvotes |
| **r/LangChain** | Agent 开发者 | Week 5 Day 2 | 20+ upvotes |
| **LangChain Discord** | Agent 开发者 | Week 5 Day 3 | 10+ 回复 |
| **Indie Hackers** | 独立开发者 | Week 5 Day 4 | 5+ 评论 |
| **Hacker News** | 技术创业者 | Week 5 Day 5 | 首页（可选）|
| **Product Hunt** | 产品爱好者 | Week 6 | 50+ upvotes |

---

## 📅 第 6 周（Day 36-42）：商业化准备

### 本周目标
✅ 托管 API 上线，至少 3 个付费用户

### 任务清单

| 任务 | 交付物 | 技术栈 | 成本 |
|------|--------|--------|------|
| **5.1 搭建托管 API** | FastAPI + vLLM | Render / Fly.io | $0（免费额度）|
| **5.2 集成支付** | Lemon Squeezy Store | LS Webhook | $0 开通费 |
| **5.3 API Key 管理** | KV 存储 + 用量统计 | Upstash Redis / D1 | $0（免费额度）|
| **5.4 定价方案** | Free + Pro + Enterprise | - | - |
| **5.5 商业版文档** | API 调用指南 + SLA | GitHub Wiki | - |

### 定价方案

| 套餐 | 价格 | 额度 | 目标用户 |
|------|------|------|---------|
| **Free** | $0 | 100次/月 | 试用 + 开源项目 |
| **Pro** | $29/月 | 不限量 | 小团队 + 独立开发者 |
| **Enterprise** | 定制 | 不限量 + 私有部署 | 企业客户 |

### API 实现（api/main.py）

```python
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from deepseek_ocr_agent import VisionDocumentTool
import redis

app = FastAPI()
tool = VisionDocumentTool()
redis_client = redis.from_url("redis://localhost:6379")

class OCRRequest(BaseModel):
    image_url: str
    document_type: str = "auto"

@app.post("/v1/ocr")
async def ocr_endpoint(
    request: OCRRequest,
    authorization: str = Header(None)
):
    # 1. 验证 API Key
    api_key = authorization.replace("Bearer ", "")
    user_id = redis_client.get(f"apikey:{api_key}")

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid API key")

    # 2. 检查用量
    usage = redis_client.get(f"usage:{user_id}:month") or 0
    if int(usage) >= 100:  # Free tier limit
        raise HTTPException(status_code=429, detail="Quota exceeded")

    # 3. 执行 OCR
    result = tool.run(request.image_url, document_type=request.document_type)

    # 4. 记录用量
    redis_client.incr(f"usage:{user_id}:month")

    return result
```

---

## 📅 第 7-9 周（Day 43-63）：迭代与优化

### 任务清单

| 任务 | 交付物 | 优先级 |
|------|--------|--------|
| **6.1 收集用户反馈** | GitHub Issues + Discord | P0 |
| **6.2 修复高频 bug** | FlashAttention 安装问题 | P0 |
| **6.3 新增 Parser** | Resume Parser, PDF 表格 | P1 |
| **6.4 性能优化** | crop_mode 优化大图处理 | P1 |
| **6.5 多语言支持** | 中文/日文/韩文 | P2 |
| **6.6 发布 v0.2.0** | Bug fixes + 1-2 new features | P0 |

---

## 📅 第 10-11 周（Day 64-75）：扩展与护城河

### 任务清单

| 任务 | 交付物 | 说明 |
|------|--------|------|
| **7.1 支持 PDF 输入** | 集成 `pdf2image` | 用户可直接上传 PDF |
| **7.2 插件式架构** | 开放 `parsers/` 目录 | 鼓励社区贡献 |
| **7.3 申请官方收录** | LangChain Awesome List | 获取官方背书 |
| **7.4 Lemon Squeezy 多项目** | 创建多个 Store | `visor-invoice`, `visor-contract` |
| **7.5 复盘与 V2 规划** | 基于数据决定方向 | 聚焦高 ROI 功能 |

---

## 📊 关键里程碑（KPIs）

| 时间节点 | 核心指标 | 验收标准 | 当前状态 |
|---------|---------|---------|---------|
| **Day 1** | 项目初始化完成 | 代码仓库 + 核心模块框架 | ✅ 已完成（2025-10-20） |
| **Day 7** | 环境验证完成 | 本地成功运行 3 种模式 | ⏳ 进行中 |
| **Day 21** | PyPI v0.1 发布 | `pip install` 成功率 >95% | ⏳ 待开始 |
| **Day 28** | 测试覆盖率 ≥80% | pytest 通过，无 critical bug | ⏳ 待开始 |
| **Day 35** | GitHub Stars ≥50 | 社区初步认可 | ⏳ 待开始 |
| **Day 42** | 托管 API 上线 | 至少 3 个付费用户 | ⏳ 待开始 |
| **Day 63** | Stars ≥150 | PyPI 下载 ≥1,000 | ⏳ 待开始 |
| **Day 75** | 商业化验证 | 付费用户 ≥10，MRR ≥$100 | ⏳ 待开始 |

---

## 🛡️ 风险管理矩阵

| 风险 | 概率 | 影响 | 应对措施 | 责任人 |
|------|------|------|---------|--------|
| **FlashAttention 安装失败** | 高 | 高 | 提供 CPU-only 版本 + Docker 镜像 | 后端工程师 |
| **DeepSeek 官方推 SDK** | 中 | 高 | 差异化：Parser + LangChain 深度集成 | 产品经理 |
| **GPU 内存不足** | 中 | 中 | 自动降级 + crop_mode 优化 | 后端工程师 |
| **用户留存低** | 中 | 高 | 快速迭代 + 社区运营 | 产品经理 |
| **支付集成复杂** | 低 | 中 | 使用 Lemon Squeezy（无需公司） | DevOps |

---

## 🔧 技术栈建议（极简原则）

| 模块 | 推荐方案 | 备选方案 | 成本 |
|------|---------|---------|------|
| **Python 打包** | `setuptools` + `pyproject.toml` | Poetry | $0 |
| **API 托管** | Render / Fly.io | Railway | $0（免费额度）|
| **GPU 推理** | 自有 GPU | RunPod ($0.2/hr) | 按需 |
| **支付网关** | Lemon Squeezy | Stripe | 5% 手续费 |
| **KV 存储** | Upstash Redis | Vercel KV | $0（免费额度）|
| **文档托管** | GitHub Wiki | Vercel + MDX | $0 |
| **CI/CD** | GitHub Actions | - | $0 |

---

## 👥 团队分工建议（Solo 可选）

| 角色 | 职责 | 工作量占比 | 技能要求 |
|------|------|-----------|---------|
| **后端工程师** | 推理引擎 + Parser + API | 50% | Python, PyTorch |
| **DevOps** | Docker + CI/CD + 部署 | 20% | Linux, Docker |
| **文档工程师** | README + 示例 + 博客 | 15% | 技术写作 |
| **产品经理** | 社区运营 + 商业化 | 15% | 运营, 数据分析 |

**Solo 开发者建议**：优先完成后端 + 文档，商业化延后至 Week 7。

---

## ⏱️ 每日/每周节奏建议

### 每日节奏
- **工作时长**：1-2 小时（高效开发）
- **核心原则**：每天至少���成 1 个任务清单项
- **提交频率**：每日至少 1 次 commit

### 每周节奏
- **周五发布**：v0.1.1, v0.1.2... 快速迭代
- **周日回顾**：复盘本周进度 + 调整下周计划
- **双周互动**：在社区回复 issue、发布更新

### 时间管理建议
```
Week 1-2: 80% 开发 + 20% 文档
Week 3-4: 70% 开发 + 30% 测试
Week 5-6: 50% 开发 + 50% 运营
Week 7+:  40% 开发 + 60% 商业化
```

---

## 📅 下一步行动（立即执行）

### ~~今天完成（Day 1 - 2025-10-20）~~ ✅ 已完成
- [x] 检查 PyPI 包名可用性：`deepseek-visor-agent` ✅ 可用
- [x] 初始化项目结构：完整目录树 + 31 个文件 ✅
- [x] 实现 `device_manager.py` 核心逻辑 ✅
- [x] 实现 `infer.py` 推理引擎框架 ✅
- [x] 实现 `tool.py` VisionDocumentTool ✅
- [x] 创建 parsers 模块（invoice, contract, classifier）✅
- [x] 配置文件完成（pyproject.toml, requirements.txt）✅
- [x] 示例文件（LangChain, LlamaIndex, Dify）✅
- [x] 测试框架 + GitHub Actions ✅
- [x] 撰写 README.md 初版 ✅
- [x] Git 仓库初始化 + 首次提交 ✅

### 明天/本周完成（Day 2-7）
- [ ] **创建 GitHub 远程仓库**：`https://github.com/你的用户名/deepseek-visor-agent`
- [ ] **推送到 GitHub**：`git remote add origin <url> && git push -u origin main`
- [ ] **环境验证**：
  - [ ] 安装依赖：`pip install -r requirements.txt`
  - [ ] 下载 DeepSeek-OCR 模型（HuggingFace 自动下载）
  - [ ] 运行简单推理测试
  - [ ] 验证设备检测功能
- [ ] **运行测试**：`pytest tests/ -v`
- [ ] **上传占位包到 PyPI**：`python -m build && twine upload dist/*`

### 下周计划（Day 8-14）
- [ ] 完善推理引擎的实际推理调用逻辑（使用正确的 inference_mode 参数）
- [ ] 测试自动降级装饰器（模拟 OOM）
- [ ] 完善 Invoice Parser 的正则表达式
- [ ] 添加测试 fixture 图片
- [ ] 编写更多集成示例

---

## 📈 成功标准（75 天后）

### 技术指标
- ✅ PyPI 稳定版本 ≥v0.2.0
- ✅ 测试覆盖率 ≥80%
- ✅ 推理速度：Gundam+4090 ≤8s

### 社区指标
- ✅ GitHub Stars ≥200
- ✅ PyPI 总下载量 ≥2,000
- ✅ 至少 1 个主流框架官方推荐

### 商业指标
- ✅ 托管 API 上线并稳定运行
- ✅ 付费用户 ≥10
- ✅ MRR（月经常性收入）≥$100

---

## 🎯 核心原则（贯穿全程）

1. **MVP 优先**：先做能跑的最小版本，再优化
2. **快速迭代**：每周至少 1 个版本发布
3. **用户导向**：根据 GitHub Issues 调整优先级
4. **商业验证**：Week 6 即启动付费，快速验证需求
5. **开源获客**：免费 SDK 吸引用户，托管 API 变现

---

**祝项目顺利！有问题随时在 GitHub Issues 讨论。** 🚀
