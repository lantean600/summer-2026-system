# Summer 2026 System

这是一个用于管理 2026 暑期学习、科研和复盘的个人工作仓库。它不是普通笔记本，而是暑期主控台：记录目标、拆解任务、沉淀产出、复盘进度，并把可展示成果持续保存到 GitHub。

## 核心原则

- 科研项目是主线：暑假结束时要有可展示产物，而不是只有学习时长。
- 数学学习是基础设施：围绕机器学习、科研阅读和实验理解，补齐线性代数、概率论和优化。
- 课业学习是保底系统：提前处理高风险课程，避免开学后压力集中爆发。
- 作息健康是系统约束：睡眠、运动和复盘不能只依赖临时意志力。
- 每天至少留下一个可检查产出：总结、推导、实验记录、代码提交、论文解读、错题归因都可以。

## 日常只看三个入口

1. 今天写什么：[logs/daily](logs/daily)
2. 本周怎么判断：[reviews/weekly](reviews/weekly)
3. 正式成果放哪里：[research](research)、[math](math)、[coursework](coursework)、[health](health)

平时不要在所有目录里来回翻找。先写 daily log，周末再整理成正式成果。

## 仓库结构

```text
.
|-- .github/ISSUE_TEMPLATE/       # GitHub Issue 表单
|-- .obsidian/                    # Obsidian 仓库配置
|-- docs/                         # 系统说明、路线图、GitHub 设置
|-- templates/                    # 日志、复盘、论文、实验、数学、课程模板
|-- logs/daily/                   # 每日记录
|-- reviews/weekly/               # 每周复盘
|-- research/
|   |-- papers/                   # 论文阅读
|   `-- experiments/              # 实验记录
|-- math/                         # 线代、概率、优化等数学总结
|-- coursework/                   # 课程学习与题目整理
|-- health/                       # 作息、运动、身体状态记录
|-- data/
|   `-- super-productivity/       # Super Productivity 导出的汇总数据
|-- scripts/                      # 自动化脚本
|-- assets/                       # 图片、结构图、展示材料
|-- sync.ps1                      # 导入数据、提交并推送
`-- sync.cmd                      # PowerShell 执行策略受限时的备用入口
```

## 每日最小闭环

1. 在 GitHub Issue 或当天计划里确认今天推进的 1 到 3 个任务。
2. 写一份 `logs/daily/YYYY-MM-DD.md`。
3. 至少产生一个可检查产出。
4. 晚上记录卡点、实际进展和明天第一步。
5. 同步到 GitHub。

推荐用 Obsidian 打开整个 `D:\summer-2026-system` 文件夹：

- Daily Notes 目录：`logs/daily`
- Daily Notes 模板：`templates/daily-log.md`
- Templates 目录：`templates`

## 每周最小闭环

1. 关闭或更新本周 Milestone。
2. 写一份 `reviews/weekly/week-XX.md`。
3. 统计科研、数学、课业、健康四条线的真实进展。
4. 把值得保留的内容沉淀到 `research`、`math` 或 `coursework`。
5. 只调整下周系统中真正影响执行的一处问题。

## 同步与发布

常规同步：

```powershell
cd D:\summer-2026-system
.\sync.ps1
```

自定义提交说明：

```powershell
.\sync.ps1 -Message "Daily log 2026-06-30"
```

只提交当前改动，不导入 Super Productivity 数据：

```powershell
.\sync.ps1 -SkipImport
```

预演同步流程，不实际提交或推送：

```powershell
.\sync.ps1 -DryRun
```

如果 PowerShell 执行策略拦截，使用备用入口：

```powershell
.\sync.cmd
```

## Super Productivity 数据

`sync.ps1` 默认会先运行：

```powershell
python -B scripts/import_superproductivity.py
```

导入脚本会读取 Super Productivity 最新备份，并覆盖生成 `data/super-productivity/` 下的汇总文件：

- `task-detail.csv`：任务明细
- `daily-summary.csv`：按天汇总
- `weekly-summary.csv`：按周汇总
- `project-weekly-summary.csv`：按项目和周汇总
- `latest-import.json`：最近一次导入元信息

不要手动维护这些 CSV。需要修正数据时，回到 Super Productivity 修改源数据后重新运行导入。

## GitHub 工作方式

建议用 GitHub Issues、Milestones 和 Project Board 管理进度。

推荐看板列：

```text
Backlog -> This Week -> Today -> Doing -> Done -> Archived
```

Issue 粒度应该能被关闭，并带有验收标准。示例：

```text
[Research] 跑通论文 A 的官方代码
[Math] 总结 SVD 和 PCA 的关系
[Course] 完成数据库第 1 章习题
[Health] 连续 7 天记录睡眠时间
```

避免创建这种无法验收的 Issue：

```text
学习概率论
搞科研项目
调整作息
复习所有课程
```

## 暑期可验收成果

- 科研项目：完成一个中等规模论文复现或小型改进项目，包含可运行代码、实验记录、结果解释和技术报告。
- 数学主线：形成一套服务机器学习理解的线性代数、概率论、优化笔记。
- 作息健康：连续记录睡眠、运动、学习块和复盘，形成可观察的数据。

## 推荐工具分工

- GitHub：任务、阶段、产出、复盘、版本控制。
- Obsidian：本地 Markdown、daily log、反向链接、阶段性整理。
- Super Productivity：任务计时、项目统计、周复盘数据来源。
- Calendar / Google Tasks：起床、学习块、运动、睡前关机等时间约束。
- Zotero：论文 PDF、引用和批注。
- Anki：术语、公式、定理条件、论文核心概念等长期记忆。

不要第一天就把所有自动化搭完。先让每日记录、Issue 推进和周复盘连续跑两周。
