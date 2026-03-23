import os
import json
import urllib.request
import urllib.parse
import concurrent.futures
import shutil

# ================= 配置区 =================
# 你的 OpenList 地址，结尾不要加斜杠
HOST = " "
# 管理员 Token (在 OpenList 后台 -> 设置 -> 其他 中获取)
TOKEN = " "
# 网盘里的源目录
REMOTE_DIR = " "
# 本地读取的目录
LOCAL_DIR = " "
# ==========================================
# 运行线程数
MAX_WORKERS = 10
# ==========================================

# 🚀 新增：用于记录网盘真实存在的“预期文件清单”
EXPECTED_FILES = set()

def get_files(path):
    url = f"{HOST}/api/fs/list"
    req = urllib.request.Request(url, method="POST")
    req.add_header("Authorization", TOKEN)
    req.add_header("Content-Type", "application/json")
    data = json.dumps({"path": path, "password": "", "page": 1, "per_page": 0, "refresh": False}).encode('utf-8')
    
    try:
        with urllib.request.urlopen(req, data=data) as res:
            return json.loads(res.read().decode('utf-8'))['data']['content']
    except Exception as e:
        print(f"❌ 获取目录失败 {path}: {e}")
        return []

def download_file(remote_path, local_path):
    url = f"{HOST}/api/fs/get"
    req = urllib.request.Request(url, method="POST")
    req.add_header("Authorization", TOKEN)
    req.add_header("Content-Type", "application/json")
    data = json.dumps({"path": remote_path, "password": ""}).encode('utf-8')
    
    try:
        with urllib.request.urlopen(req, data=data) as res:
            response = json.loads(res.read().decode('utf-8'))
            
        if response['code'] == 200:
            raw_url = response['data']['raw_url']
            dl_req = urllib.request.Request(raw_url)
            dl_req.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
            
            with urllib.request.urlopen(dl_req) as dl_res, open(local_path, 'wb') as f:
                f.write(dl_res.read())
            print(f"⬇️ 下载成功: {local_path}")
    except Exception as e:
        print(f"❌ 下载失败 {remote_path}: {e}")

def process_single_file(item_name, remote_item_path, local_item_path):
    try:
        # 如果是附属文件
        if item_name.lower().endswith(('.nfo', '.jpg', '.png', '.srt', '.ass', '.ext')):
            # 记录到预期清单中
            EXPECTED_FILES.add(local_item_path)
            # 增量下载：本地没有才下载
            if not os.path.exists(local_item_path):
                download_file(remote_item_path, local_item_path)
        
        # 如果是视频文件
        elif item_name.lower().endswith(('.mp4', '.mkv', '.ts', '.iso', '.avi', '.rmvb', '.flv')):
            strm_path = os.path.splitext(local_item_path)[0] + '.strm'
            # 记录到预期清单中
            EXPECTED_FILES.add(strm_path)
            # 增量生成：本地没有才生成
            if not os.path.exists(strm_path):
                encoded_path = urllib.parse.quote(remote_item_path)
                strm_content = f"{HOST}/d{encoded_path}"
                
                with open(strm_path, 'w', encoding='utf-8') as f:
                    f.write(strm_content)
                print(f"✅ 生成 STRM: {strm_path}")
    except Exception as e:
        print(f"❌ 处理文件出错 {remote_item_path}: {e}")

def process_dir(current_remote_path, executor):
    items = get_files(current_remote_path)
    if not items:
        return

    for item in items:
        item_name = item['name']
        remote_item_path = f"{current_remote_path}/{item_name}"
        
        rel_path = os.path.relpath(remote_item_path, REMOTE_DIR)
        local_item_path = os.path.join(LOCAL_DIR, rel_path)
        
        if item['is_dir']:
            os.makedirs(local_item_path, exist_ok=True)
            process_dir(remote_item_path, executor)
        else:
            executor.submit(process_single_file, item_name, remote_item_path, local_item_path)

def cleanup_local_files():
    """反向扫描本地目录，清理不在网盘里的孤儿文件和空文件夹"""
    print("\n🧹 步骤 2: 开始清理本地失效文件...")
    
    # topdown=False 保证我们是从最深层的子文件夹开始扫描
    for root, dirs, files in os.walk(LOCAL_DIR, topdown=False):
        for name in files:
            local_file_path = os.path.join(root, name)
            # 如果本地文件不在预期清单里，说明网盘里已经删了，咔嚓掉！
            if local_file_path not in EXPECTED_FILES:
                try:
                    os.remove(local_file_path)
                    print(f"🗑️ 删除失效文件: {local_file_path}")
                except Exception as e:
                    print(f"⚠️ 删除失败 {local_file_path}: {e}")
        
        # 顺手清理掉因为删除文件而变成空壳的文件夹
        if not os.listdir(root):
            try:
                os.rmdir(root)
                print(f"📁 删除空目录: {root}")
            except Exception:
                pass

if __name__ == "__main__":
    print(f"🚀 步骤 1: 开始多线程拉取和比对... (并发数: {MAX_WORKERS})")
    os.makedirs(LOCAL_DIR, exist_ok=True)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        process_dir(REMOTE_DIR, executor)
        
    # 等所有线程拉取完毕后，执行本地清理
    cleanup_local_files()
    
    print("🎉 同步与清理全部完成！媒体库已是最新状态。")