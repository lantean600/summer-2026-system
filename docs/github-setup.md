# GitHub Setup

这个仓库适合用 GitHub Issues、Milestones 和 Projects 管理暑期进度。

## Labels

建议在 GitHub 上创建这些标签：

| Label | 用途 |
| --- | --- |
| `area: research` | 科研主线 |
| `area: math` | 数学支撑 |
| `area: coursework` | 课业保底 |
| `area: health` | 作息健康 |
| `type: task` | 普通任务 |
| `type: review` | 复盘 |
| `type: note` | 总结或笔记 |
| `status: blocked` | 卡住，需要处理 |
| `priority: high` | 本周高优先级 |

## Milestones

建议按周建立 Milestones：

```text
Week 01 - 系统搭建与科研选题
Week 02 - 读论文与画结构图
Week 03 - 环境配置与 baseline
Week 04 - 代码理解与小实验
Week 05 - 项目整理与报告初稿
Week 06 - 第二轮改进或新项目
Week 07 - 数学与课业补强
Week 08 - 汇总展示
```

## Project Board

列保持简单：

```text
Backlog -> This Week -> Today -> Doing -> Done -> Archived
```

不要把个人学习系统做成复杂 Scrum。看板只服务一件事：让你知道今天推进什么、本周关闭什么。

## 可选 gh 命令

如果已登录 GitHub CLI，可以在仓库根目录执行：

```powershell
gh repo create summer-2026-system --private --source . --remote origin --push
```

如果想公开展示成果，把 `--private` 改成 `--public`。
