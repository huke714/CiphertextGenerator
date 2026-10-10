# 文档格式与流转码助手 (DocStream Utility / CiphertextGenerator)

<p align="center">
  <img src="assets/doc_icon.ico" width="80" height="80" alt="DocStream Helper Logo">
</p>

<p align="center">
  <strong>专有流混淆架构 · 极简校验单密钥体系 · 多文件批量秒转 · 动态流进度监控 · 文件格式智能识别 · 启动安全门禁网关</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Windows%2010%2F11-0078D6?style=flat-square&logo=windows" alt="Platform">
  <img src="https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/UI-WebView2%20%2B%20HTML5%20Crisp-0ea5e9?style=flat-square" alt="UI">
  <img src="https://img.shields.io/badge/Architecture-Asynchronous%20Multi--threading-10b981?style=flat-square" alt="Threading">
  <img src="https://img.shields.io/badge/Release-v3.2%20Standalone-f59e0b?style=flat-square" alt="Release">
  <img src="https://img.shields.io/badge/License-MIT-gray?style=flat-square" alt="License">
</p>

---

## 📖 项目简介 (Overview)

**文档格式与流转码助手 (DocStream Utility)** 是一款深度定制的高性能文档数据流重编码与反向解析还原桌面端工具。

系统从**界面呈现、交互术语、日志输出、导出备忘卡**等所有可见维度进行了全方位的**伪装设计 (Camouflage Deception)**，对外表现为“专有二进制数据流格式转码工具”，底层采用强安全级流式置换与认证验签引擎，实现**高强度安全防护同时不暴露任何具体加密算法细节**。

---

## 💎 核心技术特性 (Key Features)

### 1. 🔐 系统启动安全访问网关 (Startup Lock Gateway)
- **开机门禁锁屏**：首次启动程序时强制呈现系统级访问安全网关，输入正确的系统口令方可进入工作台。
- **初始默认访问口令**：`123456`（进入主界面后支持随时在右上角修改并持久化加密保存）。
- **离座即时锁屏**：右上角提供一键 `【🔒 锁屏】` 功能，临时离开电脑时可瞬间锁定主界面。
- **全端明暗双主题联动**：网关锁屏与主界面无缝支持 **☀️ 明亮模式 (Light)** 与 **🌙 深色冰川模式 (Dark)**，自动记忆首选项。

### 2. ⚡ 极简单一密钥体系 (Single-Key Architecture)
- **单一访问凭证**：摒弃传统多参数记忆负担，用户只需掌握一个唯一校验密钥（Key）。
- **随机高熵生成**：支持一键 `【⚡ 生成密钥】`，自动生成 24 位高熵随机安全口令。
- **三重系统级剪贴板写入保障**：
  1. DOM 同步上下文强行复制 (`execCommand`)，彻底解决本地 `file:///` 协议下异步剪贴板受阻问题；
  2. 现代 Navigator Clipboard API 并行写入；
  3. Windows 系统底层 .NET WinForms STA 线程与 Win32 原生 API 穿透写入；
  生成密钥即 100% 写入 Windows 系统剪贴板。
- **备忘卡一键导出**：支持将当前文件的关联凭证一键导出为标准备忘卡文本。

### 3. 🎯 按照文件格式智能自动识别 (Intelligent Auto-Detection)
- **零手动模式切换**：
  - 当拖入或选中的文件包含 `.enc` / `.cipher` 时，系统**自动毫秒级切换为【逆向流解析 (解密)】模式**；
  - 当拖入或选中的为普通源文档（如 `.docx`、`.pdf`、`.xlsx`、`.txt`、`.zip` 等）时，系统**自动切换为【结构重编码 (加密)】模式**；
- 配备轻量 Toast 动态提示，兼顾全自动化与极简操作体验。

### 4. 📦 多文件批量上传与队列并发转码 (Batch Processing)
- **批量拖拽多选**：支持一次性拖入或多选数十个任意格式的文件。
- **清单化展示与管理**：自动呈现已选清单卡片，实时统计总文件数与总文件体积，支持单项移除或一键清空。
- **一键批量执行**：点击批量执行，多线程后台流水线自动化连续作业。

### 5. 📊 实时动态流转码进度条 (Live Progress Bar)
- **毫秒级进度联动**：处理大文件或批量队列时，实时展示百分比动态进度（0% ~ 100%）。
- **细粒度子状态指引**：实时清晰反馈当前处理步长与文件名（例如：`正在结构重编码 [2/5]: 财务预算表.xlsx`）。
- **自动归位重置**：任务完成后智能呈现成功卡片，并自动收起进度条。

### 6. 🚀 零卡顿异步多线程架构 (Zero-Freeze Responsiveness)
- 前端与 Python 后台采用基于守护工作线程（Daemon Worker Thread）的完全解耦架构。
- 彻底解决 WinForms UI 线程与 WebView2 消息泵死锁造成的程序“未响应 (Not Responding)”假死缺陷，全局 60FPS 丝滑流畅。
- 采用 WebView2 持久化用户缓存策略，程序冷热启动秒级响应并即时聚焦输入。

### 7. 🛡️ 专有数据流伪装隐蔽 (Camouflage Identity)
| 实际安全能力 | 界面隐蔽表述 | 实际技术原理 |
| :--- | :--- | :--- |
| **文档高强度加密** | **🔄 结构重编码 (加密)** | 专有动态二进制数据流混淆与认证验签封装 |
| **文档反向解密** | **↩️ 逆向流解析 (解密)** | 流完整性校验与专有逆向映射恢复 |
| **安全主密钥** | **安全校验密钥 (Key)** | 256 位高熵主密钥凭据 |
| **生成密文格式** | **`.enc` 二进制流包** | 自研 `DOCSTREAM::V3` 专有封包头 |

---

## 📂 项目工程目录 (Repository Structure)

```text
CiphertextGenerator/
├── dist/                          # 最终发布的免安装绿色独立可执行程序
│   ├── 文档格式转换助手.exe          # 伪装中文版 (双击即用，18.8 MB)
│   └── DocStreamHelper.exe        # 隐蔽英文版 (双击即用，18.8 MB)
├── src/                           # 核心源码与解耦前端
│   ├── index.html                 # 页面骨架：多文件清单、进度条、双主题锁屏网关与设置弹窗
│   ├── style.css                  # 页面表现：Apple/Vercel 级清爽双主题样式系统
│   ├── app.js                     # 页面交互：三重剪贴板写入、拖拽监听、即时自动识别
│   ├── doc_stream_app.py          # 容器宿主：WebView2 渲染窗体、STA 剪贴板、多线程异步桥接
│   ├── crypto_engine.py           # 核心内核：专有数据流转码引擎 (无任何算法泄露)
│   └── main.py                    # 程序主入口
├── assets/                        # 资源文件夹
│   └── doc_icon.ico               # 官方风格伪装桌面图标
├── build_exe.py                   # PyInstaller 一键编译独立 EXE 脚本
├── requirements.txt               # Python 运行依赖清单
├── run.py                         # 根目录快速启动调试脚本
├── .gitignore                     # Git 忽略配置
└── README.md                      # 本文档
```

---

## 🛠️ 环境准备与快速运行 (Quick Start)

### 方式一：直接运行已编译可执行程序（免环境）
进入 `dist/` 目录，直接双击运行：
- **`dist/文档格式转换助手.exe`** (中文版)
- **`dist/DocStreamHelper.exe`** (英文版)

### 方式二：从源码运行

#### 1. 克隆代码仓库
```bash
git clone https://github.com/huke714/CiphertextGenerator.git
cd CiphertextGenerator
```

#### 2. 安装 Python 环境依赖
推荐使用 Python 3.9 ~ 3.12：
```bash
pip install -r requirements.txt
```

#### 3. 启动应用
```bash
python run.py
# 或直接运行
python src/main.py
```

---

## 📦 独立 EXE 重新编译打包 (Build Standalone EXE)

本项目内置完全自动化的打包脚本 [`build_exe.py`](build_exe.py)，会自动打包前端 HTML/CSS/JS、图标及全部依赖：

```bash
python build_exe.py
```

执行完毕后，将在 `dist/` 目录下生成全新的单文件可执行程序：
- `dist/DocStreamHelper.exe` (18.8 MB)
- `dist/文档格式转换助手.exe` (18.8 MB)

---

## 🔒 首次使用操作指引

1. **进入系统**：双击启动程序，在系统访问网关输入初始默认访问密钥 `123456`，点击 `【🔓 验证并进入系统】`；
2. **修改访问密钥（可选）**：进入后点击右上角 `【🔐 启动密钥】`，输入原密钥 `123456` 并设置您专属的新口令；
3. **加密转码文件**：
   - 拖拽任意 Word、PDF、Excel、TXT 等文件到界面（支持多选）；
   - 点击 `【⚡ 生成密钥】`（密钥将自动复制到剪贴板）；
   - 点击 `【⚡ 点击执行结构重编码】`，稍候即可在原文件同级目录下获得 `.enc` 文件；
4. **解密还原文件**：
   - 拖拽一个或多个 `.enc` 文件至程序，系统自动切换为【逆向流解析】模式；
   - 粘贴对应的密钥，点击 `【🔓 点击执行逆向流解析】`，系统将毫秒级完整还原原文件。

---

## 📄 开源许可证 (License)

本项目采用 [MIT License](LICENSE) 开源协议。
仅供个人数据保护与安全学习交流使用，请勿用于非法用途。
