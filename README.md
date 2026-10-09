姓名：左伟明
专业：微电子科学与工程
一、个人简介

- 个人简介 PDF：
- 个人网站：
- 网站源码：
- 二、通用素养

 1. Git 分支与合并

- 分支：从主线上分出来的一条独立开发线，可以在不影响主线的同时修改代码。
- 合并：把某个分支的修改整合到当前分支，例如把 `dev` 分支合并到 `main`。

 2. 命令行说明

| 命令 | 用途 |
|------|------|
| `cd` | 切换目录，例如 `cd Desktop` |
| `ls` | 列出当前目录下的文件 |
| `mkdir` | 创建新目录，例如 `mkdir project` |
| `git init` | 初始化本地仓库 |
| `git add .` | 添加所有修改到暂存区 |
| `git commit -m "说明"` | 提交一次版本 |
| `git push` | 推送到 GitHub |
| `git pull` | 拉取远程更新 |
| `git branch` | 查看分支 |
| `git checkout` | 切换分支 |
| `git merge` | 合并分支 |
| `git log` | 查看提交历史 |
| `git status` | 查看当前状态 |

 3. LICENSE

本项目使用 MIT License。  
选择原因：MIT 许可证非常宽松，允许他人自由使用、修改、分发代码，只需保留版权声明和许可声明。适合教学和开源项目。
4. GitHub 两步验证

已开启 GitHub 两步验证（2FA）。  
开启路径：GitHub → Settings → Password and authentication → Two-factor authentication。
5. AI 给过但我查证后认为是错误的信息

> AI 曾说：“PySpice 只要 pip install PySpice 就能直接运行。”  
> 我查证后发现：Windows 下还必须安装 ngspice.dll，否则会报 OSError: cannot load library ... ngspice.dll。  
> 查证过程：先看报错信息，再去 PySpice 官方文档和 GitHub Issues 搜索，最后运行 pyspice-post-installation --install-ngspice-dll 或手动下载 DLL 才解决。  
> 结论：AI 给的安装步骤不完整，必须结合官方文档和实际报错验证。
6. 防“纯粘贴”承诺——AI 生成代码关键逻辑解释

1.贪吃蛇自动寻路为什么能避开死路？
AI 生成的代码用了 BFS（广度优先搜索）计算蛇头到食物的最短路径。在决定走哪一步之前，程序会模拟：如果按这条路径走，蛇头会不会撞墙、撞到自己？只有安全时才走。如果找不到安全路径，就选择一个能最大化剩余活动空间的移动，避免把自己困死。

2. 评分函数怎么想？
贪吃蛇 AI 的评分函数通常考虑：离食物更近、保留更多空格、避免贴墙、避免蛇身过长导致空间不足。每一步比较几个候选方向的得分，选最高分的方向走。这就是它能连续吃 15 个食物不死的核心。


