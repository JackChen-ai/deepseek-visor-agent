# 📚 文档导航指南

**快速链接**: [📖 文档中心](docs/README.md)

---

## 🗂️ 文档结构概览

```
deepseek-visor-agent/
├── README.md                           # 项目首页（给GitHub访客看）
├── DOCUMENTATION_GUIDE.md              # 本文件 - 文档导航指南
│
├── docs/                               # 📚 文档中心
│   ├── README.md                       # 文档导航中心（重要！）
│   │
│   ├── business/                       # 💼 商业与战略文档
│   │   ├── PRD.md                      # 产品需求文档
│   │   ├── STRATEGIC_ANALYSIS.md       # 为什么做这个项目？
│   │   ├── COMPETITIVE_COMPARISON.md   # 竞品对比速查表
│   │   └── DEVELOPMENT_PLAN.md         # 75天开发计划
│   │
│   ├── architecture/                   # 🏗️ 架构与技术文档
│   │   ├── ARCHITECTURE.md             # 系统架构详解 ⭐
│   │   ├── HARDWARE_LIMITATIONS.md     # GPU要求分析
│   │   └── ERROR_ANALYSIS.md           # Day 1 架构修正记录
│   │
│   └── development/                    # 🔧 开发过程文档
│       ├── CLAUDE.md                   # Claude Code 协作指南
│       ├── DAY1_REPORT.md              # Day 1 完成报告
│       └── DAY2_REPORT.md              # Day 2 完成报告
│
├── examples/                           # 示例代码
│   ├── langchain_example.py
│   ├── llamaindex_example.py
│   └── dify_integration.md
│
└── deepseek_visor_agent/              # 源代码
    ├── tool.py
    ├── infer.py
    └── ...
```

---

## 🎯 按角色查找文档

### 👔 决策者 / 投资人

**关心点**: 项目价值、商业模式、竞争优势

**推荐阅读**:
1. [README.md](README.md) - 项目概览（5分钟）
2. [战略分析](docs/business/STRATEGIC_ANALYSIS.md) - 深度商业分析（20分钟）
3. [竞品对比](docs/business/COMPETITIVE_COMPARISON.md) - vs Google/AWS（10分钟）
4. [PRD](docs/business/PRD.md) - 产品定位和目标（15分钟）

**核心问题解答**:
- **为什么要做？** → [战略分析](docs/business/STRATEGIC_ANALYSIS.md)
- **和竞品有何不同？** → [竞品对比](docs/business/COMPETITIVE_COMPARISON.md)
- **商业模式是什么？** → [PRD - 第六节](docs/business/PRD.md)

---

### 👨‍💻 开发者 / 贡献者

**关心点**: 如何使用、如何扩展、代码架构

**推荐阅读**:
1. [README.md](README.md) - 快速开始（5分钟）
2. [系统架构](docs/architecture/ARCHITECTURE.md) - 技术设计（30分钟）⭐
3. [硬件限制](docs/architecture/HARDWARE_LIMITATIONS.md) - GPU要求（10分钟）
4. [Claude 协作指南](docs/development/CLAUDE.md) - 开发环境（5分钟）

**核心问题解答**:
- **怎么安装使用？** → [README.md - Quick Start](README.md#-quick-start)
- **架构是怎么设计的？** → [系统架构](docs/architecture/ARCHITECTURE.md)
- **为什么需要GPU？** → [硬件限制分析](docs/architecture/HARDWARE_LIMITATIONS.md)
- **如何添加新的Parser？** → [系统架构 - Parser系统](docs/architecture/ARCHITECTURE.md)

---

### 📊 项目管理 / PM

**关心点**: 开发进度、待办任务、里程碑

**推荐阅读**:
1. [开发计划](docs/business/DEVELOPMENT_PLAN.md) - 75天路线图（15分钟）
2. [Day 1 报告](docs/development/DAY1_REPORT.md) - Day 1完成情况（5分钟）
3. [Day 2 报告](docs/development/DAY2_REPORT.md) - Day 2完成情况（5分钟）

**核心问题解答**:
- **当前进度如何？** → [开发计划 - 进度评估](docs/business/DEVELOPMENT_PLAN.md)
- **接下来做什么？** → [开发计划 - Day 3-7任务](docs/business/DEVELOPMENT_PLAN.md)
- **遇到什么阻碍？** → [Day 2 报告 - 阻碍分析](docs/development/DAY2_REPORT.md)

---

### 🎓 学习者 / 研究者

**关心点**: 学习最佳实践、理解技术决策

**推荐阅读**:
1. [错误分析与修复](docs/architecture/ERROR_ANALYSIS.md) - Day 1架构修正（15分钟）
2. [系统架构](docs/architecture/ARCHITECTURE.md) - 完整技术设计（30分钟）
3. [战略分析](docs/business/STRATEGIC_ANALYSIS.md) - 产品思维（20分钟）

**核心问题解答**:
- **为什么不是5个模型文件？** → [错误分析](docs/architecture/ERROR_ANALYSIS.md)
- **自动降级怎么实现的？** → [系统架构 - 推理引擎](docs/architecture/ARCHITECTURE.md)
- **如何做产品定位？** → [战略分析](docs/business/STRATEGIC_ANALYSIS.md)

---

## 📖 按场景查找文档

### 场景 1: 我想快速上手使用

```
1. README.md (快速开始)
2. 安装并运行第一个示例
3. examples/langchain_example.py (集成示例)
```

### 场景 2: 我想评估是否采用这个项目

```
1. README.md (了解功能)
2. docs/business/COMPETITIVE_COMPARISON.md (vs 其他方案)
3. docs/architecture/HARDWARE_LIMITATIONS.md (了解限制)
4. docs/business/PRD.md (产品定位)
```

### 场景 3: 我想贡献代码

```
1. docs/architecture/ARCHITECTURE.md (理解架构)
2. docs/development/CLAUDE.md (开发环境)
3. docs/architecture/ERROR_ANALYSIS.md (学习最佳实践)
4. CONTRIBUTING.md (贡献指南)
```

### 场景 4: 我想理解这个项目背后的思考

```
1. docs/business/STRATEGIC_ANALYSIS.md (战略分析)
2. docs/business/COMPETITIVE_COMPARISON.md (竞品对比)
3. docs/business/PRD.md (产品需求)
4. docs/architecture/ERROR_ANALYSIS.md (技术决策)
```

---

## 🔍 文档分类说明

### 📁 business/ - 商业与战略

**目标读者**: 决策者、产品经理、投资人

**特点**:
- 商业逻辑、市场分析
- 非技术人员也能理解
- 回答"为什么"的问题

**文档**:
| 文档 | 内容 | 长度 |
|------|------|------|
| PRD.md | 产品定位、目标用户、功能需求 | 140行 |
| STRATEGIC_ANALYSIS.md | 竞争优势、商业模式、市场估算 | 836行 |
| COMPETITIVE_COMPARISON.md | 场景化竞品对比 | 400行 |
| DEVELOPMENT_PLAN.md | 75天详细开发计划 | 827行 |

### 📁 architecture/ - 架构与技术

**目标读者**: 技术人员、架构师

**特点**:
- 技术设计、架构决策
- 需要技术背景理解
- 回答"怎么做"的问题

**文档**:
| 文档 | 内容 | 长度 |
|------|------|------|
| ARCHITECTURE.md ⭐ | 系统架构、模块详解、数据流 | 636行 |
| HARDWARE_LIMITATIONS.md | GPU要求、根本原因、解决方案 | 350行 |
| ERROR_ANALYSIS.md | Day 1架构修正、最佳实践 | 250行 |

### 📁 development/ - 开发过程

**目标读者**: 项目组成员、AI协作者

**特点**:
- 开发日志、完成报告
- 记录决策过程
- 回答"做了什么"的问题

**文档**:
| 文档 | 内容 | 长度 |
|------|------|------|
| CLAUDE.md | Claude Code协作指南 | 200行 |
| DAY1_REPORT.md | Day 1完成情况详细报告 | 300行 |
| DAY2_REPORT.md | Day 2完成情况详细报告 | 248行 |

---

## 💡 文档阅读建议

### ⏱️ 时间有限？优先阅读

**5分钟快速了解**:
- [README.md](README.md)

**15分钟深入了解**:
- [README.md](README.md)
- [竞品对比](docs/business/COMPETITIVE_COMPARISON.md) 

**1小时完整理解**:
- [README.md](README.md)
- [战略分析](docs/business/STRATEGIC_ANALYSIS.md)
- [系统架构](docs/architecture/ARCHITECTURE.md)

### 📚 系统学习路径

**第1天 - 产品层**:
1. README.md
2. PRD.md
3. COMPETITIVE_COMPARISON.md

**第2天 - 战略层**:
1. STRATEGIC_ANALYSIS.md
2. DEVELOPMENT_PLAN.md

**第3天 - 技术层**:
1. ARCHITECTURE.md ⭐
2. HARDWARE_LIMITATIONS.md
3. ERROR_ANALYSIS.md

---

## 🔗 快速链接

| 目的 | 链接 |
|------|------|
| **开始使用** | [README.md](README.md) |
| **文档中心** | [docs/README.md](docs/README.md) |
| **理解战略** | [战略分析](docs/business/STRATEGIC_ANALYSIS.md) |
| **理解架构** | [系统架构](docs/architecture/ARCHITECTURE.md) ⭐ |
| **查看进度** | [开发计划](docs/business/DEVELOPMENT_PLAN.md) |
| **GitHub仓库** | https://github.com/JackChen-ai/deepseek-visor-agent |

---

## 🆘 找不到想要的文档？

1. **先看**: [docs/README.md](docs/README.md) - 文档导航中心
2. **搜索**: `grep -r "关键词" docs/`
3. **提问**: [GitHub Issues](https://github.com/JackChen-ai/deepseek-visor-agent/issues)

---

**最后更新**: 2025-10-20
**维护者**: Claude Code + Jack
