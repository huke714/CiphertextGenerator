"""
Build script to compile the Deceptive HTML5 Document Stream Transformer into a standalone EXE.
Bundles decoupled index.html, style.css, and app.js.
"""

import os
import sys
import shutil
import subprocess

def build():
    print("=== 开始打包 [文档格式转换助手 (DocStreamHelper)] 独立 EXE ===")

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    SRC_DIR = os.path.join(ROOT_DIR, "src")
    ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
    DIST_DIR = os.path.join(ROOT_DIR, "dist")
    BUILD_DIR = os.path.join(ROOT_DIR, "build")

    entry_script = os.path.join(SRC_DIR, "main.py")
    icon_path = os.path.join(ASSETS_DIR, "doc_icon.ico")
    index_html = os.path.join(SRC_DIR, "index.html")
    style_css = os.path.join(SRC_DIR, "style.css")
    app_js = os.path.join(SRC_DIR, "app.js")

    exe_internal_name = "DocStreamHelper"

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconsole",
        "--onefile",
        f"--name={exe_internal_name}",
        f"--icon={icon_path}",
        f"--add-data={index_html};.",
        f"--add-data={style_css};.",
        f"--add-data={app_js};.",
        f"--add-data={index_html};src",
        f"--add-data={style_css};src",
        f"--add-data={app_js};src",
        f"--paths={SRC_DIR}",
        "--collect-all=cryptography",
        "--collect-all=webview",
        "--collect-all=clr_loader",
        "--collect-all=pythonnet",
        "--clean",
        entry_script
    ]

    print("执行打包命令...")
    res = subprocess.run(cmd, cwd=ROOT_DIR, check=False)

    if res.returncode == 0:
        src_exe = os.path.join(DIST_DIR, f"{exe_internal_name}.exe")
        camouflaged_cn_exe = os.path.join(DIST_DIR, "文档格式转换助手.exe")

        if os.path.exists(src_exe):
            shutil.copy2(src_exe, camouflaged_cn_exe)

        # Clean intermediate build cache and spec files
        shutil.rmtree(BUILD_DIR, ignore_errors=True)
        spec_file = os.path.join(ROOT_DIR, f"{exe_internal_name}.spec")
        if os.path.exists(spec_file):
            os.remove(spec_file)

        print("\n=======================================================")
        print(" [成功] 具有迷惑性的独立 EXE 打包完成！")
        print(f" 英文隐蔽文件名: {src_exe}")
        print(f" 中文伪装文件名: {camouflaged_cn_exe}")
        if os.path.exists(src_exe):
            size_mb = os.path.getsize(src_exe) / (1024 * 1024)
            print(f" 程序文件大小: {size_mb:.2f} MB")
        print("=======================================================")
    else:
        print("\n[错误] 打包失败，退出码:", res.returncode)

if __name__ == "__main__":
    build()
