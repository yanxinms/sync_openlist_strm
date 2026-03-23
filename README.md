English | 中文版

<h2 id="english">English</h2>

Convert the WebDAV/API file stream from OpenList (or AList) to local .strm files for Emby/Jellyfin. It also seamlessly downloads metadata files (NFO, JPG, ASS, SRT, etc.) directly to your local drive.

Supports synchronous incremental updates from upstream and automatically cleans up missing upstream files to prevent dead links in your media library.

⚠️ Crucial Prerequisite: OpenList Settings
To prevent Emby/Jellyfin from throwing a 401 Unauthorized error when reading the .strm direct links, you MUST disable the signature requirement in OpenList:
Go to OpenList Admin Panel -> Settings -> Global.
Turn OFF the Sign all toggle.
Ensure the target storage path (e.g., /Movies) allows guest read access or does not have a password set in "Meta".
Configuration
Open sync_openlist_strm.py with a text editor and modify the following configuration zone:

1. Path Settings (Cross-Platform)
Set your HOST, TOKEN, REMOTE_DIR, and LOCAL_DIR. Pay attention to the path format depending on your operating system:
macOS / Linux: Use standard Unix paths.
Python
LOCAL_DIR = "/Users/spore/Movies/外语电影" 
Windows: Use raw strings (add an r before the string) to avoid backslash escape errors.
Python
LOCAL_DIR = r"D:\Emby_Media\Movies"
2. Customizing Download File Types
You can customize which metadata or subtitle files should be downloaded locally instead of being converted to links. Find this line in the process_single_file function:

Python
# Add or remove extensions as needed
if item_name.lower().endswith(('.nfo', '.jpg', '.png', '.srt', '.ass', '.ext')):
Usage
Run the script directly via terminal or command prompt (Python 3 required, no third-party dependencies):

Bash
python3 sync_openlist_strm.py
Automation (Cron / Scheduled Tasks)
To keep your local library automatically synced with your cloud drive, set up a scheduled task.

For macOS / Linux (using crontab):
Open terminal and run crontab -e.
Add the following line to run the sync every 5 minutes (replace paths with your actual paths):
Bash
*/5 * * * * /usr/bin/python3 /path/to/your/sync_openlist_strm.py >/dev/null 2>&1
For Windows (using Task Scheduler):
Open Task Scheduler -> Create Basic Task.
Set the trigger to "Daily" and configure it to repeat every 5 minutes.
Set the action to "Start a program", point it to your python.exe, and add the absolute path to your sync_openlist_strm.py as an argument.
<h2 id="中文版">中文版</h2>

将 OpenList (或 AList) 的网盘文件流转换为本地 .strm 直链文件供 Emby / Jellyfin 读取，并自动将对应的媒体信息文件（NFO、JPG、ASS、SRT 等）下载到本地硬盘。

支持上游网盘的增量同步更新，并会自动反向清理上游已删除的本地失效文件（防呆防死链）。

⚠️ 避坑必看：OpenList 设置
为了防止 Emby / Jellyfin 播放时出现 401 Unauthorized 无权限报错，你必须在 OpenList 中关闭全局签名功能：
进入 OpenList 后台管理 -> 设置 -> 全局。
将 “签名所有” (Sign all) 开关关闭。
确保你挂载分享的目录没有在“元信息”中设置密码，且允许访客直接读取。
配置指南
用文本编辑器打开 sync_openlist_strm.py，修改头部的配置区：

1. 路径修改 (不同系统注意)
填入你的 HOST、TOKEN、REMOTE_DIR 和 LOCAL_DIR。请根据你的操作系统使用正确的路径格式：
macOS / Linux / 各种 NAS 系统: 使用标准的 Unix 绝对路径。
Python
LOCAL_DIR = "/Users/spore/Movies/外语电影" 
Windows: 必须在路径字符串前面加一个字母 r（代表原生字符串），防止反斜杠 \ 导致转义报错。
Python
LOCAL_DIR = r"D:\Emby_Media\Movies"
2. 修改需要下载的附属文件种类
如果你有特定格式的海报、字幕或元数据需要拉取到本地硬盘（而不是生成 strm），可以在脚本的 process_single_file 函数中找到以下代码进行修改：

Python
# 在括号里自由增删你需要的后缀名即可
if item_name.lower().endswith(('.nfo', '.jpg', '.png', '.srt', '.ass', '.ext')):
运行脚本
无需安装任何第三方依赖，直接在终端/命令行运行：

Bash
python3 sync_openlist_strm.py
自动化定时同步
建议将其加入系统的定时任务中，实现“网盘添加电影 -> 自动削刮 -> 本地秒出海报与直链”的无人值守工作流。

macOS / Linux 系统 (使用 crontab):
终端输入 crontab -e。
添加以下任务（每 5 分钟执行一次，请将路径替换为你的实际绝对路径）：
Bash
*/5 * * * * /usr/bin/python3 /path/to/your/sync_openlist_strm.py >/dev/null 2>&1
Windows 系统 (使用任务计划程序):
打开“任务计划程序” -> 创建基本任务。
触发器设置为“每天”，并在高级设置里勾选“重复任务间隔：5分钟”。
操作选择“启动程序”，程序路径选择你的 python.exe，在“添加参数”里填入你脚本的绝对路径（如 D:\script\sync_openlist_strm.py）。
