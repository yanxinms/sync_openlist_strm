# sync_openlist_strm

[English](#english) | [中文版](#中文版)

---

<h2 id="english">English</h2>

Convert the WebDAV/API file stream from OpenList (or AList) to local `.strm` files for Emby/Jellyfin. It also seamlessly downloads metadata files (NFO, JPG, ASS, SRT, etc.) directly to your local drive.

Supports synchronous incremental updates from upstream and automatically cleans up missing upstream files to prevent dead links in your media library.

### ⚠️ Crucial Prerequisite: OpenList Settings
To prevent Emby/Jellyfin from throwing a `401 Unauthorized` error when reading the `.strm` direct links, you **MUST** disable the signature requirement in OpenList:
1. Go to OpenList Admin Panel -> **Settings** -> **Global**.
2. Turn **OFF** the **Sign all** toggle.
3. Ensure the target storage path (e.g., `/Movies`) allows guest read access or does not have a password set in "Meta".

### Configuration

Open `sync_openlist_strm.py` with a text editor and modify the following configuration zone:

#### 1. Path Settings (Cross-Platform)
Set your `HOST`, `TOKEN`, `REMOTE_DIR`, and `LOCAL_DIR`. Pay attention to the path format depending on your operating system:

* **macOS / Linux:** Use standard Unix paths.
    ```python
    LOCAL_DIR = "/Users/spore/Movies/外语电影" 
    ```
* **Windows:** Use raw strings (add an `r` before the string) to avoid backslash escape errors.
    ```python
    LOCAL_DIR = r"D:\Emby_Media\Movies"
    ```

#### 2. Customizing Download File Types
You can customize which metadata or subtitle files should be downloaded locally instead of being converted to links. Find this line in the `process_single_file` function:
```python
# Add or remove extensions as needed
if item_name.lower().endswith(('.nfo', '.jpg', '.png', '.srt', '.ass', '.ext')):
