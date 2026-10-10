"""
Deceptive Document Stream Transformer Application (DocStreamHelper)
Proprietary Stream Matrix Transformation & Single-Key Architecture
Zero algorithm exposure. 
Asynchronous multithreading engine for 60FPS responsive UI (Never 'Not Responding').
Persistent WebView2 profile cache for instantaneous startup.
"""

import os
import sys
import json
import time
import subprocess
import threading
from datetime import datetime
import webview
from typing import Dict, Any, Optional, List

# Enable WebView2 Drag and Drop listener state
try:
    from webview.dom import _dnd_state
    _dnd_state['num_listeners'] = 999
except Exception:
    pass

# Ensure src/ is in sys.path
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from crypto_engine import CryptoEngine, CryptoError

def get_resource_path(relative_path: str) -> str:
    """Get absolute path to resource, works for dev and for PyInstaller."""
    if hasattr(sys, "_MEIPASS"):
        p1 = os.path.join(sys._MEIPASS, relative_path)
        if os.path.exists(p1):
            return p1
        p2 = os.path.join(sys._MEIPASS, "src", relative_path)
        if os.path.exists(p2):
            return p2

    cand1 = os.path.join(SRC_DIR, relative_path)
    if os.path.exists(cand1):
        return cand1
    cand2 = os.path.join(os.path.dirname(SRC_DIR), "assets", relative_path)
    if os.path.exists(cand2):
        return cand2
    cand3 = os.path.join(os.path.dirname(SRC_DIR), relative_path)
    if os.path.exists(cand3):
        return cand3
    return os.path.join(os.path.abspath("."), relative_path)

def open_in_explorer(target_path: str):
    """Accurately highlight the file or open folder in Windows Explorer."""
    if not target_path:
        return
    norm_path = os.path.normpath(target_path)
    if os.path.exists(norm_path):
        if os.path.isfile(norm_path):
            try:
                subprocess.Popen(f'explorer /select,"{norm_path}"', shell=True)
                return
            except Exception:
                pass
        try:
            folder = norm_path if os.path.isdir(norm_path) else os.path.dirname(norm_path)
            os.startfile(folder)
            return
        except Exception:
            pass
    # If target doesn't exist, try parent folder
    parent = os.path.dirname(norm_path)
    if os.path.exists(parent):
        try:
            os.startfile(parent)
        except Exception:
            pass

def set_windows_clipboard(text: str) -> bool:
    """Native Windows clipboard copy via WinForms STA thread with multi-layer fallback."""
    if not text:
        return False
    # Layer 1: WinForms STA thread
    try:
        import clr
        clr.AddReference('System.Windows.Forms')
        import System.Windows.Forms as WinForms
        from System.Threading import ThreadStart, ApartmentState, Thread

        success_flag = [False]
        def copy_action():
            for _ in range(5):
                try:
                    WinForms.Clipboard.SetText(text)
                    success_flag[0] = True
                    break
                except Exception:
                    time.sleep(0.02)

        th = Thread(ThreadStart(copy_action))
        th.SetApartmentState(ApartmentState.STA)
        th.Start()
        th.Join(600)
        if success_flag[0]:
            return True
    except Exception:
        pass

    # Layer 2: ctypes 64-bit safe Win32 API
    try:
        import ctypes
        from ctypes import wintypes
        user32 = ctypes.windll.user32
        kernel32 = ctypes.windll.kernel32

        user32.OpenClipboard.argtypes = [wintypes.HWND]
        user32.OpenClipboard.restype = wintypes.BOOL
        user32.EmptyClipboard.restype = wintypes.BOOL
        user32.SetClipboardData.argtypes = [wintypes.UINT, wintypes.HANDLE]
        user32.SetClipboardData.restype = wintypes.HANDLE
        user32.CloseClipboard.restype = wintypes.BOOL

        kernel32.GlobalAlloc.argtypes = [wintypes.UINT, ctypes.c_size_t]
        kernel32.GlobalAlloc.restype = wintypes.HGLOBAL
        kernel32.GlobalLock.argtypes = [wintypes.HGLOBAL]
        kernel32.GlobalLock.restype = ctypes.c_void_p
        kernel32.GlobalUnlock.argtypes = [wintypes.HGLOBAL]
        kernel32.GlobalUnlock.restype = wintypes.BOOL

        data = text.encode("utf-16-le") + b"\x00\x00"
        for _ in range(5):
            if user32.OpenClipboard(None):
                user32.EmptyClipboard()
                h_glob = kernel32.GlobalAlloc(0x0002, len(data))
                if h_glob:
                    p_glob = kernel32.GlobalLock(h_glob)
                    if p_glob:
                        ctypes.memmove(p_glob, data, len(data))
                        kernel32.GlobalUnlock(h_glob)
                        user32.SetClipboardData(13, h_glob) # CF_UNICODETEXT
                user32.CloseClipboard()
                return True
            time.sleep(0.02)
    except Exception:
        pass

    # Layer 3: Subprocess clip.exe fallback
    try:
        p = subprocess.Popen(["clip"], stdin=subprocess.PIPE, shell=True)
        p.communicate(input=text.encode("gbk", errors="ignore"), timeout=2)
        return True
    except Exception:
        pass

    return False

def get_windows_clipboard() -> str:
    """Native Windows clipboard retrieval with multi-layer fallback."""
    # Layer 1: WinForms STA thread
    try:
        import clr
        clr.AddReference('System.Windows.Forms')
        import System.Windows.Forms as WinForms
        from System.Threading import ThreadStart, ApartmentState, Thread

        res = [""]
        def get_action():
            try:
                if WinForms.Clipboard.ContainsText():
                    res[0] = WinForms.Clipboard.GetText()
            except Exception:
                pass

        th = Thread(ThreadStart(get_action))
        th.SetApartmentState(ApartmentState.STA)
        th.Start()
        th.Join(600)
        if res[0]:
            return res[0]
    except Exception:
        pass

    # Layer 2: Win32 API ctypes
    try:
        import ctypes
        from ctypes import wintypes
        user32 = ctypes.windll.user32
        kernel32 = ctypes.windll.kernel32

        user32.OpenClipboard.argtypes = [wintypes.HWND]
        user32.OpenClipboard.restype = wintypes.BOOL
        user32.GetClipboardData.argtypes = [wintypes.UINT]
        user32.GetClipboardData.restype = wintypes.HANDLE
        user32.CloseClipboard.restype = wintypes.BOOL
        kernel32.GlobalLock.argtypes = [wintypes.HGLOBAL]
        kernel32.GlobalLock.restype = ctypes.c_void_p
        kernel32.GlobalUnlock.argtypes = [wintypes.HGLOBAL]
        kernel32.GlobalUnlock.restype = wintypes.BOOL

        if user32.OpenClipboard(None):
            h_data = user32.GetClipboardData(13) # CF_UNICODETEXT
            if h_data:
                p_data = kernel32.GlobalLock(h_data)
                if p_data:
                    text = ctypes.wstring_at(p_data)
                    kernel32.GlobalUnlock(h_data)
                    user32.CloseClipboard()
                    return text
            user32.CloseClipboard()
    except Exception:
        pass

    # Layer 3: PowerShell fallback
    try:
        out = subprocess.check_output(["powershell", "-NoProfile", "-Command", "Get-Clipboard"], timeout=2, text=True)
        return out.strip()
    except Exception:
        pass

    return ""

def get_app_config_path() -> str:
    """Get persistent configuration file path in user APPDATA."""
    app_data = os.environ.get("APPDATA") or os.path.expanduser("~")
    cfg_dir = os.path.join(app_data, "DocStreamHelper")
    os.makedirs(cfg_dir, exist_ok=True)
    return os.path.join(cfg_dir, "config.json")

class BridgeApi:
    def __init__(self):
        self.window = None

    def set_window(self, window):
        self.window = window

    def get_startup_lock_hash(self) -> str:
        """Retrieve stored startup key hash from config."""
        try:
            cfg_path = get_app_config_path()
            if os.path.exists(cfg_path):
                with open(cfg_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("startup_lock_hash", "")
        except Exception:
            pass
        return ""

    def save_startup_lock_hash(self, hash_val: str) -> bool:
        """Store startup key hash to config."""
        try:
            cfg_path = get_app_config_path()
            data = {}
            if os.path.exists(cfg_path):
                try:
                    with open(cfg_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                except Exception:
                    data = {}
            data["startup_lock_hash"] = hash_val
            with open(cfg_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False

    def select_files(self) -> List[str]:
        """Open native file dialog with multiple selection support."""
        if not self.window:
            return []
        res = self.window.create_file_dialog(
            dialog_type=webview.OPEN_DIALOG,
            allow_multiple=True
        )
        if res:
            return [os.path.normpath(p) for p in res]
        return []

    def select_file(self) -> str:
        """Open native file dialog to select a single document."""
        files = self.select_files()
        return files[0] if files else ""

    def select_folder(self) -> str:
        """Open native folder dialog."""
        if not self.window:
            return ""
        res = self.window.create_file_dialog(
            dialog_type=webview.FOLDER_DIALOG
        )
        if res and len(res) > 0:
            return os.path.normpath(res[0])
        return ""

    def select_save_path(self, default_name: str, mode: str) -> str:
        """Open native save file dialog to choose output destination."""
        if not self.window:
            return ""
        res = self.window.create_file_dialog(
            dialog_type=webview.SAVE_DIALOG,
            save_filename=default_name or "output"
        )
        if res:
            if isinstance(res, (list, tuple)) and len(res) > 0:
                return os.path.normpath(res[0])
            return os.path.normpath(str(res))
        return ""

    def get_dropped_paths(self) -> List[str]:
        """Retrieve dropped file paths captured by WebView2."""
        try:
            from webview.dom import _dnd_state
            paths = [os.path.normpath(item[1]) for item in _dnd_state.get('paths', [])]
            _dnd_state['paths'] = []
            return paths
        except Exception:
            return []

    def get_batch_file_info(self, file_paths: List[str]) -> List[Dict[str, Any]]:
        """Retrieve file metadata for a list of file paths."""
        results = []
        for p in file_paths:
            if p and os.path.exists(p):
                norm_p = os.path.normpath(p)
                fn = os.path.basename(norm_p)
                ext = fn.split('.')[-1].upper() if '.' in fn else 'FILE'
                results.append({
                    "path": norm_p,
                    "name": fn,
                    "ext": ext[:5],
                    "size": os.path.getsize(norm_p)
                })
        return results

    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """Fetch single file metadata size."""
        if file_path and os.path.exists(file_path):
            return {"size": os.path.getsize(file_path)}
        return {"size": 0}

    def generate_key(self) -> str:
        """Generate high-strength access token/key."""
        return CryptoEngine.generate_random_key(24)

    def execute(self, mode: str, in_path: str, out_path: str, key: str, auto_open: bool) -> Dict[str, Any]:
        """
        Asynchronous single-file processing on worker thread.
        Never blocks the WinForms UI message pump.
        """
        def worker():
            try:
                if not in_path or not os.path.exists(in_path):
                    err_res = {"success": False, "error": "待处理的源文件不存在或路径无效！"}
                    if self.window:
                        self.window.evaluate_js(f"window.onProcessResult({json.dumps(err_res)})")
                    return

                if not key:
                    err_res = {"success": False, "error": "安全校验密钥（Key）不能为空！"}
                    if self.window:
                        self.window.evaluate_js(f"window.onProcessResult({json.dumps(err_res)})")
                    return

                norm_in = os.path.normpath(in_path)
                norm_out = os.path.normpath(out_path)

                def progress_cb(pct: int, msg: str):
                    if self.window:
                        clean_msg = msg.replace("'", "\\'")
                        self.window.evaluate_js(f"window.updateProgress({pct}, '{clean_msg}')")

                if mode == "encrypt":
                    res = CryptoEngine.encrypt_file(
                        in_path=norm_in,
                        out_path=norm_out,
                        private_key=key,
                        progress_cb=progress_cb
                    )
                    if auto_open:
                        threading.Thread(target=open_in_explorer, args=(norm_out,), daemon=True).start()

                    final_res = {
                        "success": True,
                        "output_path": norm_out,
                        "file_name": os.path.basename(norm_out),
                        "sha256": res.get("sha256", ""),
                        "size": res.get("size", 0)
                    }
                else:
                    restored_path, payload = CryptoEngine.decrypt_file(
                        in_path=norm_in,
                        out_destination=norm_out,
                        private_key=key,
                        progress_cb=progress_cb
                    )
                    if auto_open:
                        threading.Thread(target=open_in_explorer, args=(restored_path,), daemon=True).start()

                    final_res = {
                        "success": True,
                        "output_path": restored_path,
                        "file_name": os.path.basename(restored_path),
                        "sha256": payload.get("actual_sha256", ""),
                        "size": payload.get("size", 0)
                    }

                if self.window:
                    self.window.evaluate_js(f"window.onProcessResult({json.dumps(final_res)})")

            except Exception as e:
                err_res = {"success": False, "error": str(e)}
                if self.window:
                    self.window.evaluate_js(f"window.onProcessResult({json.dumps(err_res)})")

        threading.Thread(target=worker, daemon=True).start()
        return {"started": True}

    def execute_batch(self, mode: str, file_paths: List[str], custom_out_dir: str, key: str, auto_open: bool) -> Dict[str, Any]:
        """
        Asynchronous batch processing on worker thread.
        Maintains 60FPS UI smoothness and eliminates any 'Not Responding' freezes.
        """
        def worker():
            try:
                if not file_paths:
                    err_res = {"success": False, "error": "请先选择需要批量处理的文件列表！"}
                    if self.window:
                        self.window.evaluate_js(f"window.onBatchProcessResult({json.dumps(err_res)})")
                    return

                if not key:
                    err_res = {"success": False, "error": "安全校验密钥（Key）不能为空！"}
                    if self.window:
                        self.window.evaluate_js(f"window.onBatchProcessResult({json.dumps(err_res)})")
                    return

                total = len(file_paths)
                succeeded = 0
                failed = 0
                results = []
                last_out_path = ""
                action_name = "结构重编码" if mode == "encrypt" else "逆向流解析"

                for idx, in_path in enumerate(file_paths):
                    fn = os.path.basename(in_path)
                    overall_pct = int((idx / total) * 100)
                    if self.window:
                        self.window.evaluate_js(f"window.updateProgress({overall_pct}, '正在{action_name} [{idx+1}/{total}]: {fn}')")

                    try:
                        if custom_out_dir and os.path.exists(custom_out_dir):
                            folder = custom_out_dir
                        else:
                            folder = os.path.dirname(in_path)

                        if mode == "encrypt":
                            target_out = os.path.join(folder, fn + ".enc")
                            res = CryptoEngine.encrypt_file(in_path, target_out, key)
                            succeeded += 1
                            last_out_path = target_out
                            results.append({"name": fn, "status": "success", "out": target_out})
                        else:
                            restored_path, _ = CryptoEngine.decrypt_file(in_path, folder, key)
                            succeeded += 1
                            last_out_path = restored_path
                            results.append({"name": fn, "status": "success", "out": restored_path})

                    except Exception as e:
                        failed += 1
                        results.append({"name": fn, "status": "error", "error": str(e)})

                final_result = {
                    "success": True,
                    "total": total,
                    "succeeded": succeeded,
                    "failed": failed,
                    "results": results,
                    "last_out_path": last_out_path,
                    "output_folder": os.path.dirname(last_out_path) if last_out_path else ""
                }

                if auto_open and last_out_path:
                    threading.Thread(target=open_in_explorer, args=(last_out_path,), daemon=True).start()

                if self.window:
                    self.window.evaluate_js(f"window.onBatchProcessResult({json.dumps(final_result)})")

            except Exception as e:
                err_res = {"success": False, "error": str(e)}
                if self.window:
                    self.window.evaluate_js(f"window.onBatchProcessResult({json.dumps(err_res)})")

        threading.Thread(target=worker, daemon=True).start()
        return {"started": True}

    def copy_credentials(self, key: str, doc_name: str) -> bool:
        """Copy formatted credential memo to clipboard."""
        memo = (
            f"【文档安全校验密钥备忘】\n"
            f"关联文档: {doc_name or '未指定'}\n"
            f"校验密钥 (Key): {key}\n"
            f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"⚠️ 重要提示：反向破译时仅需输入该唯一密钥即可还原，请妥善保管！"
        )
        return self.copy_clipboard(memo)

    def save_credential_card(self, doc_name: str, key: str, output_path: str, sha256: str) -> Dict[str, Any]:
        """Save a formatted credential card file (.txt) to local disk without exposing algorithms."""
        if not self.window:
            return {"saved": False}

        base_name = os.path.basename(doc_name) if doc_name else "文档"
        default_file = f"安全密钥备忘卡_{base_name}.txt"

        save_target = self.window.create_file_dialog(
            dialog_type=webview.SAVE_DIALOG,
            save_filename=default_file
        )

        if not save_target:
            return {"saved": False}

        dest_path = save_target[0] if isinstance(save_target, (list, tuple)) else str(save_target)
        dest_path = os.path.normpath(dest_path)

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        card_content = (
            "======================================================================\n"
            "                 【文档格式流转与安全校验密钥备忘卡】\n"
            "======================================================================\n\n"
            f"关联源文档: {base_name}\n"
            f"输出路径: {output_path or '同级目录'}\n"
            f"密钥生成时间: {now_str}\n\n"
            "----------------------- [ 唯一反向破译凭证 ] -----------------------\n"
            f"安全校验密钥 (Security Key): {key}\n"
            "--------------------------------------------------------------------\n\n"
            "----------------------- [ 关键指引说明 ] -----------------------\n"
            "1. 逆向解析还原该文档时，仅需输入上述【唯一安全校验密钥】。\n"
            "2. 本系统采用专有二进制流混淆重编码与动态认证验签技术。\n"
            "   若遗失该密钥，任何计算集群均无法反向还原数据。\n"
            "3. 建议将本密钥妥善保存在安全的离线介质或专业密码管理器中。\n"
            "======================================================================\n"
        )

        try:
            with open(dest_path, "w", encoding="utf-8") as f:
                f.write(card_content)
            return {"saved": True, "path": dest_path}
        except Exception as e:
            return {"saved": False, "error": str(e)}

    def open_explorer(self, file_path: str):
        """Open folder and highlight file."""
        open_in_explorer(file_path)

    def copy_clipboard(self, text: str) -> bool:
        """Copy text to Windows clipboard reliably."""
        return set_windows_clipboard(text)

    def get_clipboard(self) -> str:
        """Retrieve text from Windows clipboard reliably."""
        return get_windows_clipboard()

def main():
    html_file = get_resource_path("index.html")
    if not os.path.exists(html_file):
        html_file = get_resource_path("src/index.html")

    api = BridgeApi()
    
    # Camouflage deceptive window title
    window_title = "文档格式与流转码助手 v3.0 (DocStream Utility)"

    app_data = os.environ.get("APPDATA") or os.path.expanduser("~")
    cache_dir = os.path.join(app_data, "DocStreamHelper", "cache")
    os.makedirs(cache_dir, exist_ok=True)

    window = webview.create_window(
        title=window_title,
        url=html_file,
        js_api=api,
        width=660,
        height=780,
        resizable=True,
        min_size=(580, 680)
    )
    api.set_window(window)

    def on_window_loaded():
        # Bring immediate keyboard focus to webview
        def set_focus():
            try:
                time.sleep(0.05)
                import webview.platforms.winforms as wf
                for inst in wf.BrowserView.instances.values():
                    if hasattr(inst, 'webview'):
                        inst.webview.Focus()
            except Exception:
                pass
        threading.Thread(target=set_focus, daemon=True).start()

    window.events.loaded += on_window_loaded

    # Use private_mode=False and persistent storage_path for instant warm boot
    webview.start(debug=False, private_mode=False, storage_path=cache_dir)

if __name__ == "__main__":
    main()
