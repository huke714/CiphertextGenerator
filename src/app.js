/**
 * DocStream Utility - Frontend Client Controller
 * Version 3.1: Zero-Freeze Asynchronous Threading, Instant Startup Focus,
 * Full Dual-Theme Support across Gateway and Main View,
 * Live Progress Bar, and Intelligent Mode Auto-Detection.
 */

(function () {
  'use strict';

  // State
  let currentMode = 'encrypt'; // 'encrypt' or 'decrypt'
  let selectedFiles = []; // Array of { path, name, ext, size }
  let customOutputPath = '';
  let lastGeneratedPath = '';
  let isWorking = false;
  let isDropping = false;

  // Startup Key Default: '123456' SHA-256 hash
  const DEFAULT_STARTUP_HASH = '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92';
  let currentStartupHash = DEFAULT_STARTUP_HASH;

  // DOM Elements - Main Layout
  const dropZone = document.getElementById('dropZone');
  const zoneEmptyPrompt = document.getElementById('zoneEmptyPrompt');
  const fileReadyCard = document.getElementById('fileReadyCard');
  const badgeFileExt = document.getElementById('badgeFileExt');
  const labelFileName = document.getElementById('labelFileName');
  const labelFileMeta = document.getElementById('labelFileMeta');

  const batchReadyCard = document.getElementById('batchReadyCard');
  const batchCountBadge = document.getElementById('batchCountBadge');
  const batchTotalSize = document.getElementById('batchTotalSize');
  const batchListContainer = document.getElementById('batchListContainer');

  const tabEncrypt = document.getElementById('tabEncrypt');
  const tabDecrypt = document.getElementById('tabDecrypt');
  const btnExecute = document.getElementById('btnExecute');
  const btnExecuteText = document.getElementById('btnExecuteText');

  const panelTitleText = document.getElementById('panelTitleText');
  const keyInput = document.getElementById('keyInput');
  const btnGenKey = document.getElementById('btnGenKey');
  const btnPasteKey = document.getElementById('btnPasteKey');
  const btnCopyKey = document.getElementById('btnCopyKey');
  const btnExportKey = document.getElementById('btnExportKey');

  const outputPathDisplay = document.getElementById('outputPathDisplay');
  const chkAutoOpen = document.getElementById('chkAutoOpen');

  // Progress Bar DOM
  const progressContainer = document.getElementById('progressContainer');
  const progressTaskTitle = document.getElementById('progressTaskTitle');
  const progressPercentText = document.getElementById('progressPercentText');
  const progressBarFill = document.getElementById('progressBarFill');
  const progressStatusSubline = document.getElementById('progressStatusSubline');

  // Result Banner DOM
  const resultBanner = document.getElementById('resultBanner');
  const resultTitle = document.getElementById('resultTitle');
  const resultDesc = document.getElementById('resultDesc');
  const btnBackupPrompt = document.getElementById('btnBackupPrompt');
  const floatingToast = document.getElementById('floatingToast');

  // Theme & Gateway DOM
  const themeIcon = document.getElementById('themeIcon');
  const themeText = document.getElementById('themeText');
  const keyPromptModal = document.getElementById('keyPromptModal');
  const modalKeyDisplay = document.getElementById('modalKeyDisplay');
  const startupLockScreen = document.getElementById('startupLockScreen');
  const startupKeyInput = document.getElementById('startupKeyInput');
  const lockErrorMsg = document.getElementById('lockErrorMsg');
  const lockDefaultHint = document.getElementById('lockDefaultHint');

  const changeKeyModal = document.getElementById('changeKeyModal');
  const oldStartupKeyInput = document.getElementById('oldStartupKeyInput');
  const newStartupKeyInput = document.getElementById('newStartupKeyInput');
  const confirmStartupKeyInput = document.getElementById('confirmStartupKeyInput');
  const changeKeyErrorMsg = document.getElementById('changeKeyErrorMsg');

  // Helpers
  function showToast(message) {
    if (!floatingToast) return;
    floatingToast.textContent = message;
    floatingToast.classList.add('visible');
    setTimeout(() => {
      floatingToast.classList.remove('visible');
    }, 2200);
  }

  function formatBytes(bytes) {
    if (!bytes || bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  async function sha256Hex(text) {
    const enc = new TextEncoder().encode(text);
    const hashBuf = await crypto.subtle.digest('SHA-256', enc);
    const hashArr = Array.from(new Uint8Array(hashBuf));
    return hashArr.map(b => b.toString(16).padStart(2, '0')).join('');
  }

  // =========================================================================
  // 1. 系统启动安全访问网关 (支持双主题与极速自动对焦)
  // =========================================================================
  function focusStartupInput() {
    if (startupKeyInput) {
      startupKeyInput.focus();
      try { startupKeyInput.select(); } catch (e) {}
    }
  }

  function initStartupLock() {
    const localHash = localStorage.getItem('docstream_startup_lock_hash');
    if (localHash) {
      currentStartupHash = localHash;
    }

    if (currentStartupHash === DEFAULT_STARTUP_HASH) {
      if (lockDefaultHint) lockDefaultHint.style.display = 'block';
    } else {
      if (lockDefaultHint) lockDefaultHint.style.display = 'none';
    }

    focusStartupInput();
    if (startupKeyInput) {
      startupKeyInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') window.verifyStartupKey();
      });
    }

    // 多级定时器主动对焦，确保程序冷启动和激活时键盘输入无缝可用
    setTimeout(focusStartupInput, 20);
    setTimeout(focusStartupInput, 80);
    setTimeout(focusStartupInput, 200);
    setTimeout(focusStartupInput, 450);
    window.addEventListener('focus', focusStartupInput);
  }

  window.addEventListener('pywebviewready', () => {
    if (window.pywebview && window.pywebview.api && window.pywebview.api.get_startup_lock_hash) {
      window.pywebview.api.get_startup_lock_hash().then((savedHash) => {
        if (savedHash) {
          currentStartupHash = savedHash;
          localStorage.setItem('docstream_startup_lock_hash', savedHash);
          if (lockDefaultHint) {
            lockDefaultHint.style.display = (savedHash === DEFAULT_STARTUP_HASH) ? 'block' : 'none';
          }
        }
      });
    }
  });

  window.verifyStartupKey = async function () {
    const val = startupKeyInput ? startupKeyInput.value.trim() : '';
    if (!val) {
      if (lockErrorMsg) lockErrorMsg.textContent = '请输入系统访问密钥！';
      focusStartupInput();
      return;
    }

    const hashed = await sha256Hex(val);
    if (hashed === currentStartupHash) {
      if (lockErrorMsg) lockErrorMsg.textContent = '';
      if (startupLockScreen) startupLockScreen.classList.add('unlocked');
      if (startupKeyInput) startupKeyInput.value = '';
      showToast('已验证密钥，成功进入系统');
    } else {
      if (lockErrorMsg) lockErrorMsg.textContent = '❌ 访问密钥不匹配，请核对后重试';
      focusStartupInput();
    }
  };

  window.toggleStartupKeyVisibility = function () {
    if (!startupKeyInput) return;
    startupKeyInput.type = startupKeyInput.type === 'password' ? 'text' : 'password';
  };

  window.toggleInputVisibility = function (inputId) {
    const el = document.getElementById(inputId);
    if (!el) return;
    el.type = el.type === 'password' ? 'text' : 'password';
  };

  window.lockSystem = function () {
    if (startupLockScreen) {
      startupLockScreen.classList.remove('unlocked');
      if (startupKeyInput) {
        startupKeyInput.value = '';
        focusStartupInput();
      }
      if (lockErrorMsg) lockErrorMsg.textContent = '';
    }
  };

  window.openChangeKeyModal = function () {
    if (changeKeyModal) {
      if (oldStartupKeyInput) oldStartupKeyInput.value = '';
      if (newStartupKeyInput) newStartupKeyInput.value = '';
      if (confirmStartupKeyInput) confirmStartupKeyInput.value = '';
      if (changeKeyErrorMsg) changeKeyErrorMsg.textContent = '';
      changeKeyModal.classList.add('active');
      if (oldStartupKeyInput) oldStartupKeyInput.focus();
    }
  };

  window.closeChangeKeyModal = function () {
    if (changeKeyModal) changeKeyModal.classList.remove('active');
  };

  window.submitChangeStartupKey = async function () {
    const oldVal = oldStartupKeyInput ? oldStartupKeyInput.value.trim() : '';
    const newVal = newStartupKeyInput ? newStartupKeyInput.value.trim() : '';
    const confirmVal = confirmStartupKeyInput ? confirmStartupKeyInput.value.trim() : '';

    if (!oldVal) {
      if (changeKeyErrorMsg) changeKeyErrorMsg.textContent = '请输入当前原密钥！';
      return;
    }
    const oldHashed = await sha256Hex(oldVal);
    if (oldHashed !== currentStartupHash) {
      if (changeKeyErrorMsg) changeKeyErrorMsg.textContent = '❌ 原密钥错误，无法更改！';
      return;
    }

    if (!newVal || newVal.length < 4) {
      if (changeKeyErrorMsg) changeKeyErrorMsg.textContent = '新密钥长度不能少于 4 位字符！';
      return;
    }

    if (newVal !== confirmVal) {
      if (changeKeyErrorMsg) changeKeyErrorMsg.textContent = '两次输入的新密钥不一致！';
      return;
    }

    const newHashed = await sha256Hex(newVal);
    currentStartupHash = newHashed;
    localStorage.setItem('docstream_startup_lock_hash', newHashed);

    if (window.pywebview && window.pywebview.api && window.pywebview.api.save_startup_lock_hash) {
      window.pywebview.api.save_startup_lock_hash(newHashed);
    }

    if (lockDefaultHint) {
      lockDefaultHint.style.display = (newHashed === DEFAULT_STARTUP_HASH) ? 'block' : 'none';
    }

    window.closeChangeKeyModal();
    showToast('启动访问密钥已成功修改！请妥善保存。');
  };

  // =========================================================================
  // 2. 模式切换与根据文件格式自动识别
  // =========================================================================
  window.switchMode = function (mode, isAutoTriggered = false) {
    currentMode = mode;
    if (mode === 'encrypt') {
      tabEncrypt.className = 'mode-tab-item active-enc';
      tabDecrypt.className = 'mode-tab-item';
      btnExecute.className = 'btn-primary-launch mode-enc';
      if (btnGenKey) btnGenKey.style.display = 'flex';
      if (btnPasteKey) btnPasteKey.style.display = 'none';
      if (panelTitleText) panelTitleText.textContent = '安全校验凭证';
      if (keyInput) keyInput.placeholder = '输入密钥密码，或点击生成';
    } else {
      tabDecrypt.className = 'mode-tab-item active-dec';
      tabEncrypt.className = 'mode-tab-item';
      btnExecute.className = 'btn-primary-launch mode-dec';
      if (btnGenKey) btnGenKey.style.display = 'none';
      if (btnPasteKey) btnPasteKey.style.display = 'flex';
      if (panelTitleText) panelTitleText.textContent = '反向破译凭据校验';
      if (keyInput) keyInput.placeholder = '输入原校验密钥即可还原';
    }

    updateUIFileDisplay();
    if (!isAutoTriggered && resultBanner) resultBanner.style.display = 'none';
  };

  function detectAndApplyMode(files) {
    if (!files || files.length === 0) return;

    const isCipherFile = (name) => {
      const lower = name.toLowerCase();
      return lower.endsWith('.enc') || lower.endsWith('.cipher');
    };

    const hasCipher = files.some(f => isCipherFile(f.name || f.path));

    if (hasCipher) {
      if (currentMode !== 'decrypt') {
        window.switchMode('decrypt', true);
        showToast('💡 检测到转码文件，已自动切换为【逆向流解析 (解密)】模式');
      }
    } else {
      if (currentMode !== 'encrypt') {
        window.switchMode('encrypt', true);
        showToast('💡 检测到普通文档，已自动切换为【结构重编码 (加密)】模式');
      }
    }
  }

  // =========================================================================
  // 3. 多文件与单文件选择、拖拽与批量管理
  // =========================================================================
  function addFilesFromPaths(paths, isAppend = false) {
    if (!paths || paths.length === 0) return;

    if (!isAppend) {
      selectedFiles = [];
    }

    const existingPaths = new Set(selectedFiles.map(f => f.path));
    const newPaths = paths.filter(p => !existingPaths.has(p));

    if (window.pywebview && window.pywebview.api && window.pywebview.api.get_batch_file_info) {
      window.pywebview.api.get_batch_file_info(newPaths).then((infoList) => {
        if (infoList && infoList.length > 0) {
          selectedFiles.push(...infoList);
          detectAndApplyMode(selectedFiles);
          customOutputPath = '';
          updateUIFileDisplay();
        }
      });
    } else {
      newPaths.forEach(p => {
        const fn = p.split(/[\\/]/).pop();
        const ext = fn.includes('.') ? fn.split('.').pop().toUpperCase() : 'FILE';
        selectedFiles.push({ path: p, name: fn, ext: ext.slice(0, 4), size: 0 });
      });
      detectAndApplyMode(selectedFiles);
      customOutputPath = '';
      updateUIFileDisplay();
    }
  }

  window.removeFileByIndex = function (idx, e) {
    if (e) e.stopPropagation();
    selectedFiles.splice(idx, 1);
    detectAndApplyMode(selectedFiles);
    updateUIFileDisplay();
  };

  window.clearFileSelection = function (e) {
    if (e) e.stopPropagation();
    selectedFiles = [];
    customOutputPath = '';
    updateUIFileDisplay();
    if (resultBanner) resultBanner.style.display = 'none';
  };

  window.addMoreFiles = function (e) {
    if (e) e.stopPropagation();
    if (!window.pywebview) return;
    window.pywebview.api.select_files().then((paths) => {
      if (paths && paths.length > 0) {
        addFilesFromPaths(paths, true);
      }
    });
  };

  window.handleDropZoneClick = function (e) {
    if (isDropping) return;
    if (e.target.closest('.btn-remove-selection') || e.target.closest('.btn-batch-mini') || e.target.closest('.btn-item-del')) {
      return;
    }
    if (!window.pywebview) return;
    window.pywebview.api.select_files().then((paths) => {
      if (paths && paths.length > 0) {
        addFilesFromPaths(paths, false);
      }
    });
  };

  // 彻底修复 WebView2 原生文件拖拽
  if (dropZone) {
    dropZone.addEventListener('dragover', (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropZone.classList.add('dragging');
    });

    dropZone.addEventListener('dragenter', (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropZone.classList.add('dragging');
    });

    dropZone.addEventListener('dragleave', (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropZone.classList.remove('dragging');
    });

    dropZone.addEventListener('drop', (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropZone.classList.remove('dragging');

      isDropping = true;
      setTimeout(() => { isDropping = false; }, 400);

      if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files.length > 0) {
        if (window.chrome && window.chrome.webview && window.chrome.webview.postMessageWithAdditionalObjects) {
          window.chrome.webview.postMessageWithAdditionalObjects('FilesDropped', e.dataTransfer.files);
          setTimeout(() => {
            if (window.pywebview && window.pywebview.api && window.pywebview.api.get_dropped_paths) {
              window.pywebview.api.get_dropped_paths().then((paths) => {
                if (paths && paths.length > 0) {
                  addFilesFromPaths(paths, false);
                }
              });
            }
          }, 80);
        } else {
          const paths = Array.from(e.dataTransfer.files).map(f => f.path).filter(Boolean);
          if (paths.length > 0) {
            addFilesFromPaths(paths, false);
          }
        }
      }
    });
  }

  function updateUIFileDisplay() {
    if (selectedFiles.length === 0) {
      zoneEmptyPrompt.style.display = 'block';
      fileReadyCard.style.display = 'none';
      batchReadyCard.style.display = 'none';
      outputPathDisplay.textContent = '等待选择文件...';
      btnExecuteText.textContent = currentMode === 'encrypt'
        ? '点击执行结构重编码并生成对应文件'
        : '点击执行逆向流解析并还原文件';
      return;
    }

    zoneEmptyPrompt.style.display = 'none';

    if (selectedFiles.length === 1) {
      const f = selectedFiles[0];
      fileReadyCard.style.display = 'flex';
      batchReadyCard.style.display = 'none';

      badgeFileExt.textContent = f.ext || 'FILE';
      labelFileName.textContent = f.name;
      labelFileMeta.textContent = `大小: ${formatBytes(f.size)} | 路径: ${f.path}`;

      btnExecuteText.textContent = currentMode === 'encrypt'
        ? '点击执行结构重编码并生成对应文件'
        : '点击执行逆向流解析并还原文件';

      updateSuggestedOutputPath();
    } else {
      fileReadyCard.style.display = 'none';
      batchReadyCard.style.display = 'block';

      batchCountBadge.textContent = `${selectedFiles.length} 个文件`;
      const totalBytes = selectedFiles.reduce((acc, f) => acc + (f.size || 0), 0);
      batchTotalSize.textContent = `总计: ${formatBytes(totalBytes)}`;

      batchListContainer.innerHTML = '';
      selectedFiles.forEach((f, idx) => {
        const item = document.createElement('div');
        item.className = 'batch-file-item';
        item.innerHTML = `
          <div class="batch-item-left">
            <span class="file-extension-tag">${f.ext || 'FILE'}</span>
            <span class="batch-item-name" title="${f.path}">${f.name}</span>
            <span class="batch-item-size">(${formatBytes(f.size)})</span>
          </div>
          <button class="btn-item-del" onclick="removeFileByIndex(${idx}, event)" title="移除此项">✕</button>
        `;
        batchListContainer.appendChild(item);
      });

      btnExecuteText.textContent = currentMode === 'encrypt'
        ? `点击执行批量结构重编码 (共 ${selectedFiles.length} 个文件)`
        : `点击执行批量逆向流解析 (共 ${selectedFiles.length} 个文件)`;

      updateSuggestedOutputPath();
    }
  }

  function updateSuggestedOutputPath() {
    if (selectedFiles.length === 0) {
      outputPathDisplay.textContent = '等待选择文件...';
      return;
    }

    if (customOutputPath) {
      outputPathDisplay.textContent = customOutputPath;
      return;
    }

    if (selectedFiles.length === 1) {
      const f = selectedFiles[0];
      const folder = f.path.substring(0, f.path.lastIndexOf('\\') + 1);
      let outName = '';
      if (currentMode === 'encrypt') {
        outName = f.name + '.enc';
      } else {
        if (f.name.toLowerCase().endsWith('.enc')) {
          outName = f.name.slice(0, -4);
        } else if (f.name.toLowerCase().endsWith('.cipher')) {
          outName = f.name.slice(0, -7);
        } else {
          outName = 'restored_' + f.name;
        }
      }
      outputPathDisplay.textContent = folder + outName;
    } else {
      const commonFolder = selectedFiles[0].path.substring(0, selectedFiles[0].path.lastIndexOf('\\') + 1);
      outputPathDisplay.textContent = `输出至同级目录: ${commonFolder}`;
    }
  }

  window.changeOutputPath = function () {
    if (!window.pywebview) return;
    if (selectedFiles.length <= 1) {
      const defName = selectedFiles.length === 1
        ? (currentMode === 'encrypt' ? selectedFiles[0].name + '.enc' : '')
        : 'output.enc';
      window.pywebview.api.select_save_path(defName, currentMode).then((chosen) => {
        if (chosen) {
          customOutputPath = chosen;
          outputPathDisplay.textContent = chosen;
        }
      });
    } else {
      window.pywebview.api.select_folder().then((chosenFolder) => {
        if (chosenFolder) {
          customOutputPath = chosenFolder;
          outputPathDisplay.textContent = `自定义批量输出目录: ${chosenFolder}`;
        }
      });
    }
  };

  // =========================================================================
  // 4. 实时流转码进度条 (Live Progress Updates)
  // =========================================================================
  window.updateProgress = function (pct, statusText) {
    if (progressContainer) progressContainer.style.display = 'block';
    if (progressBarFill) progressBarFill.style.width = Math.min(100, Math.max(0, pct)) + '%';
    if (progressPercentText) progressPercentText.textContent = Math.round(pct) + '%';
    if (progressStatusSubline) progressStatusSubline.textContent = statusText;
    if (progressTaskTitle) progressTaskTitle.textContent = statusText;
  };

  function resetProgress() {
    if (progressContainer) progressContainer.style.display = 'none';
    if (progressBarFill) progressBarFill.style.width = '0%';
    if (progressPercentText) progressPercentText.textContent = '0%';
  }

  // =========================================================================
  // 5. 核心异步执行（多线程防假死）
  // =========================================================================
  window.executeProcess = function () {
    if (isWorking) return;
    if (selectedFiles.length === 0) {
      alert('请先拖拽或选择待处理的文件！');
      return;
    }

    const key = keyInput.value.trim();
    if (!key) {
      alert('请输入【安全校验密钥】！加解密必须使用匹配的访问凭证。');
      keyInput.focus();
      return;
    }

    const autoOpen = chkAutoOpen ? chkAutoOpen.checked : true;
    isWorking = true;
    btnExecute.disabled = true;

    window.updateProgress(5, '正在启动后台转码引擎...');

    if (selectedFiles.length === 1) {
      const singlePath = selectedFiles[0].path;
      const targetOut = customOutputPath || outputPathDisplay.textContent;
      if (window.pywebview) {
        window.pywebview.api.execute(currentMode, singlePath, targetOut, key, autoOpen);
      }
    } else {
      const paths = selectedFiles.map(f => f.path);
      const outFolder = customOutputPath || '';
      if (window.pywebview) {
        window.pywebview.api.execute_batch(currentMode, paths, outFolder, key, autoOpen);
      }
    }
  };

  // 异步任务完成全局回调（由 Python 线程安全调度，永不锁死界面）
  window.onProcessResult = function (res) {
    isWorking = false;
    btnExecute.disabled = false;

    if (res.success) {
      lastGeneratedPath = res.output_path;
      window.updateProgress(100, '处理完成！');
      setTimeout(resetProgress, 1200);

      resultBanner.className = 'result-display-panel';
      resultTitle.textContent = currentMode === 'encrypt'
        ? '✅ 结构重编码成功！'
        : '🎉 逆向流解析成功！';
      resultDesc.innerHTML = `目标文件: <b>${res.file_name}</b><br>完整路径: ${res.output_path}`;
      resultBanner.style.display = 'block';
      showToast('转码成功！');
    } else {
      resetProgress();
      resultBanner.className = 'result-display-panel error-state';
      resultTitle.textContent = '❌ 操作未完成';
      resultDesc.textContent = res.error || '校验不匹配或密文损坏';
      resultBanner.style.display = 'block';
      alert('操作失败：\n' + res.error);
    }
  };

  window.onBatchProcessResult = function (res) {
    isWorking = false;
    btnExecute.disabled = false;

    if (res.success) {
      lastGeneratedPath = res.last_out_path || res.output_folder;
      window.updateProgress(100, `批量完成！成功: ${res.succeeded} / 失败: ${res.failed}`);
      setTimeout(resetProgress, 1500);

      resultBanner.className = 'result-display-panel';
      resultTitle.textContent = `🎉 批量处理完成！(成功 ${res.succeeded} 个，失败 ${res.failed} 个)`;
      resultDesc.innerHTML = `输出目标目录: <b>${res.output_folder || '原文件同级目录'}</b>`;
      resultBanner.style.display = 'block';
      showToast(`批量${currentMode === 'encrypt' ? '重编码' : '解析'}完成！`);
    } else {
      resetProgress();
      alert('批量操作失败：\n' + res.error);
    }
  };

  window.openOutputFolder = function () {
    if (!lastGeneratedPath) {
      if (selectedFiles.length > 0) {
        lastGeneratedPath = selectedFiles[0].path;
      } else {
        showToast('暂无生成文件路径');
        return;
      }
    }
    if (window.pywebview && window.pywebview.api && window.pywebview.api.open_explorer) {
      window.pywebview.api.open_explorer(lastGeneratedPath);
    }
  };

  // =========================================================================
  // 6. 健壮剪贴板系统与密钥生成、复制、导出
  // =========================================================================

  // 健壮的三重保障剪贴板复制系统（解决 WebView2 在本地文件协议下异步剪贴板受阻问题）
  async function copyTextRobustly(text) {
    if (!text) return false;
    let copied = false;

    // 方案 1: 同步 DOM textarea + execCommand('copy')
    // 在用户原生点击交互上下文中同步触发，不受跨域与沙箱安全策略拦截
    try {
      const ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.left = '-9999px';
      ta.style.top = '-9999px';
      ta.style.opacity = '0';
      ta.setAttribute('readonly', '');
      document.body.appendChild(ta);
      ta.focus();
      ta.select();
      ta.setSelectionRange(0, text.length);
      copied = document.execCommand('copy');
      document.body.removeChild(ta);
    } catch (e) {
      copied = false;
    }

    // 方案 2: 现代浏览器 Navigator Clipboard API
    if (navigator.clipboard && navigator.clipboard.writeText) {
      try {
        await navigator.clipboard.writeText(text);
        copied = true;
      } catch (e) {}
    }

    // 方案 3: Python 原生 Windows 系统剪贴板 API（STA线程 + Win32 API + clip.exe 三重兜底）
    if (window.pywebview && window.pywebview.api && window.pywebview.api.copy_clipboard) {
      try {
        const pySuccess = await window.pywebview.api.copy_clipboard(text);
        if (pySuccess) copied = true;
      } catch (e) {}
    }

    return copied;
  }

  window.copyOutputPath = async function () {
    if (!lastGeneratedPath) {
      showToast('暂无生成路径可复制');
      return;
    }
    await copyTextRobustly(lastGeneratedPath);
    showToast('目标路径已成功复制到剪贴板！');
  };

  window.generateKey = async function () {
    const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=';
    const randArr = new Uint32Array(24);
    window.crypto.getRandomValues(randArr);
    const key = Array.from(randArr, n => chars[n % chars.length]).join('');

    keyInput.value = key;
    keyInput.type = 'text';

    // 立即执行多层剪贴板强行复制
    await copyTextRobustly(key);

    if (modalKeyDisplay) modalKeyDisplay.textContent = key;
    if (keyPromptModal) keyPromptModal.classList.add('active');
    showToast('密钥已成功生成并复制到剪贴板！');
  };

  window.closeKeyModal = function () {
    if (keyPromptModal) keyPromptModal.classList.remove('active');
  };

  window.copyModalKey = async function () {
    if (!modalKeyDisplay) return;
    const key = modalKeyDisplay.textContent.trim();
    if (!key) return;
    await copyTextRobustly(key);
    showToast('密钥已成功复制到剪贴板！');
  };

  window.copyCredentials = async function () {
    const key = keyInput.value.trim();
    if (!key) {
      alert('暂无密钥可复制！请先输入或点击生成密钥。');
      keyInput.focus();
      return;
    }
    await copyTextRobustly(key);
    showToast('密钥已成功复制到剪贴板！');
  };

  window.saveCredentials = function () {
    const key = keyInput.value.trim();
    if (!key) {
      alert('暂无密钥可导出！请先输入或生成密钥。');
      keyInput.focus();
      return;
    }
    if (window.pywebview) {
      const docName = selectedFiles.length > 0 ? selectedFiles[0].name : '文档';
      const outputTarget = lastGeneratedPath || outputPathDisplay.textContent;
      window.pywebview.api.save_credential_card(docName, key, outputTarget, '').then((res) => {
        if (res && res.saved) {
          showToast('密钥备忘卡已成功导出保存！');
        }
      });
    }
  };

  window.pasteKey = async function () {
    let text = '';
    // 优先调用 Python 原生系统剪贴板，彻底突破 WebView2 权限封锁
    if (window.pywebview && window.pywebview.api && window.pywebview.api.get_clipboard) {
      try {
        text = await window.pywebview.api.get_clipboard();
      } catch (e) {}
    }

    // 降级使用 navigator.clipboard.readText
    if (!text && navigator.clipboard && navigator.clipboard.readText) {
      try {
        text = await navigator.clipboard.readText();
      } catch (e) {}
    }

    if (text) {
      keyInput.value = text.trim();
      showToast('已从剪贴板粘贴密钥');
    } else {
      keyInput.focus();
      try {
        document.execCommand('paste');
      } catch (e) {}
    }
  };

  window.toggleKeyVisibility = function () {
    keyInput.type = keyInput.type === 'password' ? 'text' : 'password';
  };

  // =========================================================================
  // 7. 明暗双主题无缝联动（支持主界面与门禁锁屏同步）
  // =========================================================================
  function updateThemeDisplay(isLight) {
    const icon = isLight ? '🌙' : '☀️';
    const text = isLight ? '深色' : '明亮';
    if (themeIcon) themeIcon.textContent = icon;
    if (themeText) themeText.textContent = text;
    document.querySelectorAll('.lock-theme-icon').forEach(el => el.textContent = icon);
    document.querySelectorAll('.lock-theme-text').forEach(el => el.textContent = text);
  }

  window.toggleTheme = function () {
    const isLight = document.body.classList.toggle('light-theme');
    updateThemeDisplay(isLight);
    localStorage.setItem('docstream_theme', isLight ? 'light' : 'dark');
  };

  // 启动即刻渲染主题，确保锁屏初次呈现即为正确主题
  const savedTheme = localStorage.getItem('docstream_theme');
  if (savedTheme === 'light') {
    document.body.classList.add('light-theme');
    updateThemeDisplay(true);
  } else {
    updateThemeDisplay(false);
  }

  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      if (keyPromptModal && keyPromptModal.classList.contains('active')) window.closeKeyModal();
      if (changeKeyModal && changeKeyModal.classList.contains('active')) window.closeChangeKeyModal();
    }
  });

  if (keyPromptModal) {
    keyPromptModal.addEventListener('click', (e) => {
      if (e.target === keyPromptModal) window.closeKeyModal();
    });
  }
  if (changeKeyModal) {
    changeKeyModal.addEventListener('click', (e) => {
      if (e.target === changeKeyModal) window.closeChangeKeyModal();
    });
  }

  // 初始化锁屏
  initStartupLock();

})();
