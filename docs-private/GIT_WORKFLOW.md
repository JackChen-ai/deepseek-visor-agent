# Git 双仓库工作流程指南

**创建日期**: 2025-10-21
**维护者**: Jack Chen

---

## 📋 仓库配置概览

### 🔐 私有仓库 (完整历史 + 所有文件)
- **名称**: deepseek-visor-agent-private
- **URL**: https://github.com/JackChen-ai/deepseek-visor-agent-private
- **可见性**: Private
- **内容**:
  - ✅ 完整 Git 提交历史（所有开发记录）
  - ✅ 所有源代码
  - ✅ `docs-private/` 私有文档（商业计划、开发日志等）
  - ✅ 测试脚本（test_inference.py, test_simple_inference.py）
- **用途**: 个人备份、完整开发历史查看

### 🌍 公开仓库 (干净历史 + 仅公开文件)
- **名称**: deepseek-visor-agent
- **URL**: https://github.com/JackChen-ai/deepseek-visor-agent
- **可见性**: Public
- **内容**:
  - ✅ 仅 1 个初始提交（无历史记录）
  - ✅ 33 个公开文件（源代码、文档、测试）
  - ❌ 不包含 `docs-private/`
  - ❌ 不包含临时测试脚本
- **用途**: 开源发布、用户使用、成为行业标准工具

---

## 🌲 本地分支说明

### `main` 分支
- **用途**: 日常开发分支
- **跟踪远程**: `private/main`
- **推送目标**: 私有仓库
- **包含内容**: 所有文件 + 完整历史

### `public-clean` 分支
- **用途**: 公开发布分支
- **跟踪远程**: `origin/main`
- **推送目标**: 公开仓库
- **包含内容**: 仅公开文件 + 无历史记录

---

## 🔄 常用操作命令

### 查看当前配置

```bash
# 查看当前分支
git branch

# 查看所有远程仓库
git remote -v

# 查看当前分支跟踪关系
git branch -vv
```

**预期输出**:
```
  main         [private/main] ...
* public-clean [origin/main] ...

origin   https://github.com/JackChen-ai/deepseek-visor-agent.git (公开)
private  https://github.com/JackChen-ai/deepseek-visor-agent-private.git (私有)
```

---

## 📝 日常开发工作流

### 场景 1: 日常开发（私有仓库）

```bash
# 1. 确保在 main 分支
git checkout main

# 2. 编写代码、修改文档...

# 3. 提交更改
git add .
git commit -m "feat: 添加新功能"

# 4. 推送到私有仓库
git push private main
```

**⚠️ 注意**:
- 在 `main` 分支开发
- 只推送到 `private` 远程
- **永远不要** `git push origin main`（会推送到公开仓库）

---

### 场景 2: 发布到公开仓库（更新公开版本）

```bash
# 1. 确保 main 分支的更改已提交并推送到私有仓库
git checkout main
git push private main

# 2. 切换到 public-clean 分支
git checkout public-clean

# 3. 将 main 分支的更改合并过来（但不提交）
git merge main --no-commit --no-ff

# 4. 排除私有文档（如果有的话）
git reset HEAD docs-private/ 2>/dev/null || true
git checkout -- docs-private/ 2>/dev/null || true

# 5. 检查待提交的更改
git status

# 6. 提交更改
git commit -m "feat: 添加新功能"

# 7. 推送到公开仓库
git push origin public-clean:main
```

**⚠️ 注意**:
- 在 `public-clean` 分支操作
- 合并时使用 `--no-commit` 防止自动提交私有内容
- 推送前务必检查 `git status` 确保没有私有文件

---

### 场景 3: 仅更新私有文档（不发布）

```bash
# 1. 在 main 分支修改私有文档
git checkout main
# 编辑 docs-private/ 中的文件...

# 2. 提交并推送到私有仓库
git add docs-private/
git commit -m "docs: 更新商业计划"
git push private main

# 不需要推送到公开仓库！
```

---

## 🚨 防止推送错误的检查清单

### 推送前必查项目

#### 推送到私有仓库时:
```bash
# ✅ 确认当前分支是 main
git branch --show-current
# 应显示: main

# ✅ 确认推送目标是 private
# 使用: git push private main
```

#### 推送到公开仓库时:
```bash
# ✅ 确认当前分支是 public-clean
git branch --show-current
# 应显示: public-clean

# ✅ 确认没有私有文件
git status | grep docs-private
# 应无输出

# ✅ 确认推送目标是 origin
# 使用: git push origin public-clean:main
```

---

## ⚙️ Git 配置建议

### 设置推送保护

```bash
# 防止误推送 main 分支到公开仓库
git config --local branch.main.remote private
git config --local branch.main.pushRemote private

# 防止误推送 public-clean 到私有仓库
git config --local branch.public-clean.remote origin
git config --local branch.public-clean.pushRemote origin
```

配置后：
- 在 `main` 分支执行 `git push` 会自动推送到 `private`
- 在 `public-clean` 分支执行 `git push` 会自动推送到 `origin`

---

## 🔧 故障排查

### 问题 1: 不小心推送了私有内容到公开仓库

**解决方案**:
```bash
# 1. 立即切换到 public-clean 分支
git checkout public-clean

# 2. 强制重置到初始提交
git reset --hard eaaaf7d  # 初始提交的 hash

# 3. 强制推送覆盖公开仓库
git push --force origin public-clean:main

# 4. 在 GitHub 检查是否已恢复
```

---

### 问题 2: 忘记当前在哪个分支

**解决方案**:
```bash
# 查看当前分支（带高亮显示）
git branch

# 查看更详细信息
git status

# 查看当前分支跟踪的远程
git branch -vv
```

---

### 问题 3: 合并时引入了私有文件

**解决方案**:
```bash
# 在 public-clean 分支
git checkout public-clean

# 取消暂存私有文件
git reset HEAD docs-private/
git reset HEAD test_inference.py
git reset HEAD test_simple_inference.py

# 恢复这些文件（从 .gitignore）
git checkout -- docs-private/
rm -f test_inference.py test_simple_inference.py

# 重新提交
git commit -m "你的提交信息"
```

---

## 📊 快速参考表

| 操作 | 分支 | 命令 | 推送目标 |
|------|------|------|---------|
| **日常开发** | `main` | `git push private main` | 私有仓库 |
| **发布公开版本** | `public-clean` | `git push origin public-clean:main` | 公开仓库 |
| **更新私有文档** | `main` | `git push private main` | 私有仓库 |
| **查看配置** | 任意 | `git remote -v` | - |
| **切换分支** | - | `git checkout main/public-clean` | - |

---

## 🎯 最佳实践

1. ✅ **永远在 main 分支开发** - 保持工作流一致
2. ✅ **定期推送到私有仓库** - 避免丢失代码
3. ✅ **发布前仔细检查** - 确保无私有内容
4. ✅ **使用明确的远程名称** - `git push private main` 而非 `git push`
5. ✅ **保持这份文档更新** - 记录特殊操作

---

## 📞 紧急联系

如果遇到无法解决的 Git 问题：
- **备份**: `/Users/jack/DEV/deepseek-visor-agent-backup`
- **恢复方法**: 删除当前目录，复制备份，重新配置远程仓库

---

**最后更新**: 2025-10-21
**下次审查**: 首次公开发布后 1 周
