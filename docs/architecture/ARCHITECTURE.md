# 系统架构文档

**最后更新**: 2025-10-20
**版本**: v1.0

---

## 🏗️ 架构概览

DeepSeek Visor Agent 是一个轻量级的 Python SDK，作为 DeepSeek-OCR 和 AI Agent 框架之间的桥梁。

### 核心定位

```
┌─────────────────────────────────────────────────────────────┐
│                     AI Agent 生态                            │
│  (LangChain / LlamaIndex / Dify / Custom Agents)           │
└─────────────────────────────────────────────────────────────┘
                            ↓
           ┌────────────────────────────────┐
           │   DeepSeek Visor Agent (我们)  │
           │  - 自动设备检测                │
           │  - 模式选择                    │
           │  - 字段提取                    │
           │  - LangChain 集成              │
           └────────────────────────────────┘
                            ↓
           ┌────────────────────────────────┐
           │      DeepSeek-OCR (上游)       │
           │   HuggingFace 原始模型         │
           └────────────────────────────────┘
```

---

## 📦 模块架构

### 目录结构

```
deepseek_visor_agent/
├── __init__.py              # 对外暴露 VisionDocumentTool
├── tool.py                  # 主入口类
├── infer.py                 # 推理引擎封装
├── device_manager.py        # 设备检测与配置
├── parsers/                 # 文档解析器
│   ├── __init__.py
│   ├── base.py              # BaseParser 抽象类
│   ├── invoice.py           # 发票解析器
│   ├── contract.py          # 合同解析器
│   └── classifier.py        # 文档类型分类器
├── utils/
│   ├── error_handler.py     # 错误处理与自动降级
│   └── validators.py        # 输入验证
└── api/                     # FastAPI 托管服务（可选）
    ├── main.py
    └── schemas.py
```

---

## 🔄 数据流图

### 完整推理流程

```
用户调用
   ↓
┌─────────────────────────────────────────────────────────────┐
│ VisionDocumentTool.run(image_path, document_type="auto")    │
└─────────────────────────────────────────────────────────────┘
   ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 1: DeepSeekOCRInference.infer(image_path)              │
│   1.1 加载图片 (PIL.Image)                                   │
│   1.2 获取推理参数 (base_size, image_size, crop_mode)       │
│   1.3 调用模型 model.infer(tokenizer, image, prompt, ...)   │
│   1.4 返回 Markdown 文本                                     │
└─────────────────────────────────────────────────────────────┘
   ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 2: classify_document(markdown)                         │
│   2.1 关键词评分 (invoice/contract/resume/general)          │
│   2.2 模式匹配 (货币符号、合同条款、技能关键词)              │
│   2.3 返回文档类型                                           │
└─────────────────────────────────────────────────────────────┘
   ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 3: Parser.parse(markdown)                              │
│   3.1 InvoiceParser: 提取 total/date/vendor                 │
│   3.2 ContractParser: 提取 parties/effective_date/type      │
│   3.3 返回结构化字段                                         │
└─────────────────────────────────────────────────────────────┘
   ↓
返回给用户
{
  "markdown": "...",
  "fields": {"total": "$199.00", ...},
  "document_type": "invoice",
  "confidence": 0.95,
  "metadata": {
    "inference_mode": "base",
    "device": "cuda",
    "inference_time_ms": 1234
  }
}
```

---

## 🧩 核心模块详解

### 1. DeviceManager (设备管理器)

**职责**: 自动检测硬件环境，选择最优推理配置

**核心逻辑**:
```python
def detect_optimal_config() -> Dict:
    if torch.cuda.is_available():
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
        if gpu_memory >= 48:
            return {"device": "cuda", "inference_mode": "gundam"}
        elif gpu_memory >= 24:
            return {"device": "cuda", "inference_mode": "large"}
        elif gpu_memory >= 16:
            return {"device": "cuda", "inference_mode": "base"}
        else:
            return {"device": "cuda", "inference_mode": "small"}

    elif torch.backends.mps.is_available():
        return {"device": "mps", "inference_mode": "tiny"}

    else:
        # ⚠️ CPU 不支持（上游限制）
        return {"device": "cpu", "inference_mode": "tiny"}
```

**关键配置表**:

| 推理模式 | base_size | image_size | crop_mode | 最低 VRAM | 适用场景 |
|---------|-----------|-----------|-----------|-----------|---------|
| tiny    | 512       | 512       | False     | 4 GB      | 快速预览 |
| small   | 640       | 640       | False     | 8 GB      | 标准文档 |
| base    | 1024      | 1024      | False     | 16 GB     | 高质量 |
| large   | 1280      | 1280      | False     | 24 GB     | 复杂布局 |
| gundam  | 1024      | 640       | True      | 48 GB     | 超大文档（动态分块） |

### 2. DeepSeekOCRInference (推理引擎)

**职责**: 封装上游模型，提供统一推理接口

**关键设计**:

#### 2.1 单模型多模式架构

```python
# ✅ 正确：单一模型 ID
MODEL_ID = "deepseek-ai/DeepSeek-OCR"

# 模型只加载一次
model = AutoModel.from_pretrained(MODEL_ID, trust_remote_code=True)

# 推理时通过参数切换模式
output = model.infer(
    tokenizer, image, prompt,
    base_size=INFERENCE_MODES[mode]["base_size"],
    image_size=INFERENCE_MODES[mode]["image_size"],
    crop_mode=INFERENCE_MODES[mode]["crop_mode"]
)
```

**重要**：这是 Day 1 的关键修正。原先误以为有 5 个不同的模型文件，实际上是**1 个模型 + 5 组参数**。

#### 2.2 自动降级装饰器

```python
@auto_fallback_decorator
def infer(self, image_path, prompt, **kwargs):
    # 推理逻辑
    pass

# 装饰器会在 OOM 时自动尝试更小的模式
# gundam → large → base → small → tiny
```

### 3. Parser 系统

**职责**: 从 Markdown 中提取结构化字段

**设计模式**: 策略模式 (Strategy Pattern)

```python
# 抽象基类
class BaseParser(ABC):
    @abstractmethod
    def parse(self, markdown: str) -> Dict[str, Any]:
        pass

# 具体实现
class InvoiceParser(BaseParser):
    def parse(self, markdown: str) -> Dict:
        return {
            "total": self._extract_total(markdown),
            "date": self._extract_date(markdown),
            "vendor": self._extract_vendor(markdown)
        }

class ContractParser(BaseParser):
    def parse(self, markdown: str) -> Dict:
        return {
            "parties": self._extract_parties(markdown),
            "effective_date": self._extract_effective_date(markdown),
            "contract_type": self._extract_contract_type(markdown)
        }
```

**扩展性**: 用户可自定义 Parser

```python
# 用户自定义
class ResumeParser(BaseParser):
    def parse(self, markdown: str) -> Dict:
        return {
            "name": self._extract_name(markdown),
            "email": self._extract_email(markdown),
            "skills": self._extract_skills(markdown)
        }

# 注册到工具
tool = VisionDocumentTool()
tool.parsers["resume"] = ResumeParser()
```

### 4. VisionDocumentTool (主入口)

**职责**: 协调所有模块，提供统一 API

**核心方法**:
```python
def run(
    self,
    image_path: Union[str, Path],
    document_type: str = "auto",
    extract_fields: bool = True
) -> Dict[str, Any]:
    """
    统一入口，协调推理 → 分类 → 解析

    Returns:
        {
            "markdown": str,           # OCR 原始输出
            "fields": dict,            # 提取的结构化字段
            "document_type": str,      # 文档类型
            "confidence": float,       # 置信度
            "metadata": {...}          # 推理元数据
        }
    """
```

---

## 🔌 集成模式

### LangChain 集成

```python
from langchain.tools import tool
from deepseek_visor_agent import VisionDocumentTool

@tool
def extract_invoice(image_path: str) -> dict:
    """Extract structured data from invoice images"""
    return VisionDocumentTool().run(image_path, document_type="invoice")

# 集成到 Agent
from langchain.agents import initialize_agent
agent = initialize_agent([extract_invoice], llm, agent="zero-shot-react")
```

### LlamaIndex 集成

```python
from llama_index.tools import FunctionTool
from deepseek_visor_agent import VisionDocumentTool

def extract_document(image_path: str) -> dict:
    return VisionDocumentTool().run(image_path)

tool = FunctionTool.from_defaults(fn=extract_document)
agent = ReActAgent.from_tools([tool], llm=llm)
```

### Dify 集成（REST API）

```http
POST https://api.visor-agent.com/v1/ocr
Authorization: Bearer <API_KEY>
Content-Type: application/json

{
  "image_url": "https://example.com/invoice.jpg",
  "document_type": "auto"
}
```

---

## ⚠️ 关键技术限制

### 硬件要求

**必需**: NVIDIA GPU (CUDA 11.8+)

**原因**: DeepSeek-OCR 模型代码有硬编码的 `.cuda()` 调用（详见 [HARDWARE_LIMITATIONS.md](HARDWARE_LIMITATIONS.md)）

**证据**:
```python
# modeling_deepseekocr.py Line 917
input_ids.unsqueeze(0).cuda()  # 强制 CUDA，无视设备参数
```

**影响**:
- ❌ 不支持纯 CPU
- ❌ 不支持 AMD GPU (ROCm)
- ❓ Apple MPS 未验证（理论上也会失败）

**解决方案**:
1. 自托管：租用云端 GPU（RunPod $0.2/hr）
2. 托管 API：使用我们的托管服务

---

## 🔐 安全性设计

### 输入验证

```python
# utils/validators.py
def validate_image_path(path: Union[str, Path]) -> Path:
    """验证图片路径安全性"""
    path = Path(path).resolve()

    # 防止路径遍历攻击
    if ".." in str(path):
        raise ValueError("Invalid path: directory traversal detected")

    # 检查文件存在
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")

    # 检查文件类型
    if path.suffix.lower() not in ['.jpg', '.jpeg', '.png', '.pdf']:
        raise ValueError(f"Unsupported file type: {path.suffix}")

    return path
```

### 错误处理

```python
# 用户友好的错误消息
try:
    result = tool.run("invoice.jpg")
except torch.cuda.OutOfMemoryError:
    raise OCRError(
        "GPU out of memory. Try:\n"
        "1. Use a smaller inference mode (tiny/small)\n"
        "2. Close other GPU applications\n"
        "3. Use our hosted API"
    )
```

---

## 📊 性能优化

### 模型加载优化

```python
# 单例模式：模型只加载一次
class DeepSeekOCRInference:
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

### 批处理支持（未来）

```python
# v0.2 计划功能
def run_batch(
    self,
    image_paths: List[Union[str, Path]],
    document_type: str = "auto"
) -> List[Dict[str, Any]]:
    """批量处理图片，提升吞吐量"""
    pass
```

---

## 🧪 测试架构

### 单元测试

```python
# tests/test_parsers.py
def test_invoice_parser():
    markdown = """
    INVOICE
    Date: 2024-01-15
    Total: $199.00
    """
    parser = InvoiceParser()
    result = parser.parse(markdown)

    assert result["total"] == "$199.00"
    assert result["date"] == "2024-01-15"
```

### 集成测试

```python
# tests/test_tool.py
@pytest.mark.gpu_required
def test_invoice_extraction():
    tool = VisionDocumentTool()
    result = tool.run("tests/fixtures/invoice_sample.jpg")

    assert result["document_type"] == "invoice"
    assert "total" in result["fields"]
```

---

## 🔮 未来架构演进

### v0.2: 多模型支持

```python
# 用户可选择底层模型
tool = VisionDocumentTool(backend="paddleocr")  # 备选引擎
```

### v0.3: 插件系统

```python
# 第三方可贡献 Parser
from deepseek_visor_agent import register_parser

@register_parser("medical_report")
class MedicalReportParser(BaseParser):
    pass
```

### v0.4: 流式输出

```python
# 支持大文档流式处理
for chunk in tool.run_stream("large_document.pdf"):
    print(chunk["fields"])
```

---

## 📚 相关文档

- [硬件限制分析](HARDWARE_LIMITATIONS.md) - GPU 要求详解
- [错误分析与修复](ERROR_ANALYSIS.md) - Day 1 架构修正
- [产品需求文档](../business/PRD.md) - 产品定位
- [开发计划](../business/DEVELOPMENT_PLAN.md) - 路线图

---

**最后更新**: 2025-10-20
**维护者**: Claude Code + Jack