# DeepSeek-OCR 硬件限制深度分析

**文档创建时间**: 2025-10-20
**分析者**: Claude
**验证设备**: MacBook M1 (无CUDA)

---

## 🚨 核心发现：DeepSeek-OCR 不支持纯 CPU 推理

### 证据链

#### 1. 官方模型代码硬编码 `.cuda()` 调用

**位置**: `~/.cache/huggingface/modules/transformers_modules/deepseek-ai/DeepSeek-OCR/*/modeling_deepseekocr.py`

```python
# Line 917-919 (infer 函数中)
input_ids.unsqueeze(0).cuda(),
images=[(images_crop.cuda(), images_ori.cuda())],
images_seq_mask = images_seq_mask.unsqueeze(0).cuda(),

# Line 935-937
input_ids.unsqueeze(0).cuda(),
images=[(images_crop.cuda(), images_ori.cuda())],
images_seq_mask = images_seq_mask.unsqueeze(0).cuda(),

# Line 950
outputs = tokenizer.decode(output_ids[0, input_ids.unsqueeze(0).cuda().shape[1]:])
```

**共计发现 10 处硬编码 `.cuda()` 调用**，遍布整个推理流程。

#### 2. 实际测试错误信息

```
Traceback (most recent call last):
  File "modeling_deepseekocr.py", line 917, in infer
    input_ids.unsqueeze(0).cuda(),
  File "torch/cuda/__init__.py", line 403, in _lazy_init
    raise AssertionError("Torch not compiled with CUDA enabled")
AssertionError: Torch not compiled with CUDA enabled
```

#### 3. 即使指定 `device="cpu"` 也无效

我们的 `device_manager.py` 正确检测了设备，但模型内部代码**忽略了设备参数**，直接调用 `.cuda()`。

---

## 📊 支持的硬件环境

| 设备类型 | 是否支持 | 备注 |
|---------|---------|------|
| **NVIDIA GPU (CUDA)** | ✅ 完全支持 | 推荐，最佳性能 |
| **Apple Silicon (MPS)** | ❓ 未验证 | 理论上应该失败（有 `.cuda()` 调用） |
| **纯 CPU** | ❌ 不支持 | 模型代码硬编码 CUDA |
| **AMD GPU (ROCm)** | ❌ 不支持 | 模型硬编码 `.cuda()` |