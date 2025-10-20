# 📚 DeepSeek Visor Agent 文档中心

欢迎来到 DeepSeek Visor Agent 的文档中心！本目录包含项目的所有文档，按类别组织。

---

## 📖 快速导航

### 🚀 新用户入门

| 文档 | 说明 | 适合人群 |
|------|------|---------|
| [README.md](../README.md) | 项目简介、快速开始 | 所有人 |
| [安装指南](installation.md) | 详细安装步骤 | 开发者 |
| [快速示例](quickstart.md) | 5分钟上手 | 开发者 |

### 💼 商业与战略

| 文档 | 说明 | 适合人群 |
|------|------|---------|
| [产品需求文档 (PRD)](business/PRD.md) | 产品定位、目标用户、功能需求 | 产品经理、投资人 |
| [战略分析](business/STRATEGIC_ANALYSIS.md) | 竞争优势、商业模式、市场分析 | 创始人、投资人 |
| [竞品对比](business/COMPETITIVE_COMPARISON.md) | vs Google Vision、AWS Textract、PaddleOCR | 决策者 |
| [开发计划](business/DEVELOPMENT_PLAN.md) | 75天详细路线图 | 项目管理 |

### 🏗️ 架构与技术

| 文档 | 说明 | 适合人群 |
|------|------|---------|
| [架构设计](architecture/ARCHITECTURE.md) | 系统架构、核心概念 | 技术人员 |
| [硬件限制分析](architecture/HARDWARE_LIMITATIONS.md) | GPU要求、原因分析 | 运维、架构师 |
| [错误分析与修复](architecture/ERROR_ANALYSIS.md) | Day 1 架构修正记录 | 开发者 |

### 🔧 开发文档

| 文档 | 说明 | 适合人群 |
|------|------|---------|
| [Day 1 完成报告](development/DAY1_REPORT.md) | 项目初始化详情 | 项目组 |
| [Day 2 完成报告](development/DAY2_REPORT.md) | 核心功能实现详情 | 项目组 |
| [Claude 协作指南](development/CLAUDE.md) | Claude Code 使用说明 | AI 辅助开发者 |

---

## 📂 文档组织结构

```
docs/
├── README.md                    # 本文件 - 文档导航中心
├── installation.md              # 安装指南
├── quickstart.md                # 快速开始
├── api_reference.md             # API 参考（待完成）
├── troubleshooting.md           # 故障排查（待完成）
│
├── business/                    # 商业与战略文档
│   ├── PRD.md                   # 产品需求文档
│   ├── STRATEGIC_ANALYSIS.md    # 战略分析
│   ├── COMPETITIVE_COMPARISON.md# 竞品对比
│   └── DEVELOPMENT_PLAN.md      # 开发计划
│
├── architecture/                # 架构与技术设计
│   ├── ARCHITECTURE.md          # 系统架构
│   ├── HARDWARE_LIMITATIONS.md  # 硬件限制分析
│   └── ERROR_ANALYSIS.md        # 错误分析与修复
│
└── development/                 # 开发过程文档
    ├── DAY1_REPORT.md           # Day 1 完成报告
    ├── DAY2_REPORT.md           # Day 2 完成报告
    └── CLAUDE.md                # Claude 协作指南
```

---

## 🎯 按场景查找文档

### 场景 1: 我想评估这个项目是否值得投资/参与

**推荐阅读顺序**:
1. [README.md](../README.md) - 了解项目概况
2. [战略分析](business/STRATEGIC_ANALYSIS.md) - 深入了解商业逻辑
3. [竞品对比](business/COMPETITIVE_COMPARISON.md) - 了解竞争优势
4. [产品需求文档](business/PRD.md) - 了解产品定位

### 场景 2: 我想在项目中使用这个工具

**推荐阅读顺序**:
1. [README.md](../README.md) - 项目简介
2. [安装指南](installation.md) - 安装步骤
3. [快速示例](quickstart.md) - 上手使用
4. [故障排查](troubleshooting.md) - 遇到问题时查阅

### 场景 3: 我想理解技术架构并贡献代码

**推荐阅读顺序**:
1. [系统架构](architecture/ARCHITECTURE.md) - 整体设计
2. [硬件限制分析](architecture/HARDWARE_LIMITATIONS.md) - 关键技术限制
3. [错误分析与修复](architecture/ERROR_ANALYSIS.md) - 学习最佳实践
4. [Claude 协作指南](development/CLAUDE.md) - 开发环境设置

### 场景 4: 我想了解项目进展

**推荐阅读顺序**:
1. [开发计划](business/DEVELOPMENT_PLAN.md) - 查看路线图
2. [Day 1 报告](development/DAY1_REPORT.md) - Day 1 完成情况
3. [Day 2 报告](development/DAY2_REPORT.md) - Day 2 完成情况

---

## 📝 文档维护规范

### 文档分类原则

| 类别 | 存放位置 | 说明 |
|------|---------|------|
| **用户文档** | `docs/` 根目录 | 面向用户的文档（安装、使用、API） |
| **商业文档** | `docs/business/` | PRD、战略分析、商业计划 |
| **技术文档** | `docs/architecture/` | 架构设计、技术决策 |
| **开发日志** | `docs/development/` | 开发过程记录、完成报告 |

### 文档命名规范

- **全大写**: 重要战略文档（PRD.md, STRATEGIC_ANALYSIS.md）
- **首字母大写**: 普通文档（Installation.md, Quickstart.md）
- **小写**: API 参考、配置文件（api_reference.md）

### 文档更新流程

1. 新增文档：在对应目录创建，更新本 README 的导航表
2. 修改文档：在文件顶部标注修改日期
3. 废弃文档：移动到 `docs/archive/`（暂未创建）

---

## 🔗 外部资源

- **项目主页**: https://github.com/JackChen-ai/deepseek-visor-agent
- **PyPI 包**: https://pypi.org/project/deepseek-visor-agent/（待发布）
- **上游项目**: https://huggingface.co/deepseek-ai/DeepSeek-OCR

---

**最后更新**: 2025-10-20
**维护者**: Claude Code + Jack
