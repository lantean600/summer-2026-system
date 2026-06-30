# Operating Guide: Obsidian + Git

## 本地维护原则

这个仓库虽然有多个分类目录，但日常维护只按三个入口走：

1. `logs/daily`：当天真实发生了什么，允许粗糙。
2. `reviews/weekly`：每周判断系统是否有效。
3. `research`、`math`、`coursework`、`health`：只放整理后的正式成果。

`docs`、`templates`、`.github` 平时不要动，只有系统升级时才改。

## Obsidian 设置

在 Obsidian 中选择 `Open folder as vault`，路径选 `D:\summer-2026-system`。

已经随仓库配置好的默认项：

- Daily Notes 目录：`logs/daily`
- Daily Notes 模板：`templates/daily-log.md`
- Templates 目录：`templates`
- Backlinks：开启，用来连接论文、数学概念、实验记录

Obsidian Git 插件是可选项。如果不想折腾插件，就继续用 PowerShell 执行 `git add`、`git commit`、`git push`。

## 每天怎么用

1. 打开 Obsidian 的 Daily Note，或从 `templates/daily-log.md` 复制一份到 `logs/daily/YYYY-MM-DD.md`。
2. 打开 GitHub Project 或 Issues，看 `Today` 列。
3. 当天只承诺 1 到 3 个关键任务。
4. 临时想法先写进当天 daily log，不要一有想法就新建分类文件。
5. 当天产生的正式内容再放进对应目录：
   - 科研：`research/papers` 或 `research/experiments`
   - 数学：`math`
   - 课业：`coursework`
   - 健康与作息：先写进 daily log，周末结合 Super Productivity 汇总判断
6. 晚上更新 Issue 状态，并在 daily log 里写清楚卡点和明天第一步。
7. 晚上同步一次 Git：

```powershell
cd D:\summer-2026-system
git status
git add .
git commit -m "Daily log YYYY-MM-DD"
git push
```

## 每周怎么用

1. 周日晚上从 `templates/weekly-review.md` 复制一份到 `reviews/weekly/week-XX.md`。
2. 回看本周关闭的 Issues、提交的文件和 daily logs。
3. 把真正值得保留的内容沉淀到 `research`、`math`、`coursework`。
4. 对科研、数学、课业、健康分别写事实，不写空泛感受。
5. 下周只保留最重要的系统调整。
6. 每周只调整一次仓库结构或模板，避免每天优化系统。

## 每周导入 Super Productivity 数据

周复盘前运行：

```powershell
cd D:\summer-2026-system
python scripts/import_superproductivity.py
```

脚本会读取 Super Productivity 自动备份目录中的最新备份，并覆盖生成 `data/super-productivity/` 下的汇总文件。复盘时优先看：

- `data/super-productivity/weekly-summary.csv`
- `data/super-productivity/project-weekly-summary.csv`
- `data/super-productivity/task-detail.csv`

不要手动编辑 `data/super-productivity/` 里的 CSV；需要修正时回到 Super Productivity 修改源数据后重新运行脚本。

## 什么放进 GitHub

- 可展示产出：报告、实验记录、数学总结、代码、图表。
- 可追踪任务：Issue、Milestone、Project。
- 周期复盘：daily log、weekly review。
- 可复用模板：论文阅读、实验记录、数学总结、课程笔记。

## 什么不要塞进 GitHub

- 太碎的临时想法。
- 未整理的长篇情绪记录。
- 大体积 PDF、数据集、模型权重。
- 只对当天有用的草稿。

这些内容可以放在 Obsidian、本地草稿目录、Zotero 或 Anki 中，整理后再进入仓库。

## Issue 粒度

好的 Issue 应该能被关闭，并有验收标准。

```text
[Research] 跑通论文 A 的官方代码
[Math] 总结 SVD 和 PCA 的关系
[Course] 完成数据库第 1 章习题
[Health] 连续 7 天记录睡眠时间
```

避免这种 Issue：

```text
学习概率论
搞科研项目
调整作息
复习所有课程
```

## 产出单元

每天至少留下一个小产出：

- 一页数学总结
- 一个推导
- 一个代码 commit
- 一个实验记录
- 一个错题归因
- 一张模型结构图
- 一段论文解读
- 一个 Anki 小卡组
