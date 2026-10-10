"""
Core Document Stream Transformer Engine (DocStream Engine)
Private Binary Stream Compression & Dynamic Structural Obfuscation
Deceptive and Camouflaged: No encryption algorithm names exposed.
Single-Key Architecture: Automatic nonce and salt derivation.
"""

import os
import json
import base64
import hashlib
import secrets
from datetime import datetime
from typing import Tuple, Dict, Any, Optional, List, Callable
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

MAGIC_PREFIX_V3 = "DOCSTREAM::V3::"
MAGIC_PREFIX_V2 = "CIPHER::V2::"
MAGIC_PREFIX_V1 = "CIPHER::V1::"
DERIVATION_ROUNDS = 120_000

class CryptoError(Exception):
    """Custom exception for transformation engine operations."""
    pass

class CryptoEngine:
    @staticmethod
    def generate_random_key(length: int = 24) -> str:
        """Generate high-entropy access security key."""
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-="
        return "".join(secrets.choice(alphabet) for _ in range(length))

    @staticmethod
    def derive_key(salt_bytes: bytes, private_key: str, iterations: int = DERIVATION_ROUNDS) -> bytes:
        """
        Derives private transformation key stream from user key and salt.
        """
        if not private_key:
            raise CryptoError("校验密钥不能为空，请输入访问密钥！")

        key_bytes = private_key.encode("utf-8")
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt_bytes,
            iterations=iterations,
        )
        return kdf.derive(key_bytes)

    @classmethod
    def encrypt_file(
        cls,
        in_path: str,
        out_path: str,
        private_key: str,
        progress_cb: Optional[Callable[[int, str], None]] = None
    ) -> Dict[str, Any]:
        """
        Encapsulates arbitrary file into private stream package.
        """
        if not os.path.exists(in_path):
            raise CryptoError(f"文件不存在: {in_path}")
        if not private_key:
            raise CryptoError("校验密钥不能为空，请输入或生成密钥！")

        file_name = os.path.basename(in_path)
        if progress_cb:
            progress_cb(15, f"读取数据流: {file_name}")

        try:
            with open(in_path, "rb") as f:
                data = f.read()
        except Exception as e:
            raise CryptoError(f"无法读取源文件: {e}")

        if progress_cb:
            progress_cb(40, f"构建动态转码矩阵: {file_name}")

        sha256_hash = hashlib.sha256(data).hexdigest()

        # Dynamic private entropy
        salt_bytes = os.urandom(16)
        nonce = os.urandom(12)

        key = cls.derive_key(salt_bytes, private_key)
        aesgcm = AESGCM(key)
        transformed_data = aesgcm.encrypt(nonce, data, None)

        if progress_cb:
            progress_cb(75, f"封装输出数据包: {file_name}")

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        payload: Dict[str, Any] = {
            "v": 3,
            "type": "docstream_archive",
            "fmt": "DocStream-Binary-Matrix",
            "rounds": DERIVATION_ROUNDS,
            "fn": file_name,
            "salt": base64.b64encode(salt_bytes).decode("utf-8"),
            "nonce": base64.b64encode(nonce).decode("utf-8"),
            "data": base64.b64encode(transformed_data).decode("utf-8"),
            "size": len(data),
            "sha256": sha256_hash,
            "time": now_str,
        }

        json_bytes = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        packaged_str = MAGIC_PREFIX_V3 + base64.b64encode(json_bytes).decode("utf-8")

        out_dir = os.path.dirname(os.path.abspath(out_path))
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)

        try:
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(packaged_str)
        except Exception as e:
            raise CryptoError(f"写入输出文件失败: {e}")

        if progress_cb:
            progress_cb(100, f"完成重编码: {file_name}")

        return {
            "file_name": file_name,
            "size": len(data),
            "sha256": sha256_hash,
            "out_path": out_path,
            "time": now_str
        }

    @classmethod
    def decrypt_file(
        cls,
        in_path: str,
        out_destination: str,
        private_key: str,
        progress_cb: Optional[Callable[[int, str], None]] = None
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Parses encapsulated stream back to original document.
        """
        if not os.path.exists(in_path):
            raise CryptoError(f"文件不存在: {in_path}")
        if not private_key:
            raise CryptoError("校验密钥不能为空，请输入解密所需的密钥！")

        file_name = os.path.basename(in_path)
        if progress_cb:
            progress_cb(15, f"读取密文流: {file_name}")

        try:
            with open(in_path, "r", encoding="utf-8") as f:
                packaged_str = f.read()
        except UnicodeDecodeError:
            raise CryptoError("文件格式或编码异常，请确认选择的是有效的转码文件。")
        except Exception as e:
            raise CryptoError(f"读取文件失败: {e}")

        raw_token = packaged_str.strip()
        if raw_token.startswith(MAGIC_PREFIX_V3):
            b64_part = raw_token[len(MAGIC_PREFIX_V3):]
        elif raw_token.startswith(MAGIC_PREFIX_V2):
            b64_part = raw_token[len(MAGIC_PREFIX_V2):]
        elif raw_token.startswith(MAGIC_PREFIX_V1):
            b64_part = raw_token[len(MAGIC_PREFIX_V1):]
        else:
            b64_part = raw_token

        try:
            json_bytes = base64.b64decode(b64_part.encode("utf-8"))
            payload = json.loads(json_bytes.decode("utf-8"))
        except Exception:
            raise CryptoError("数据包格式非法或已损坏，无法解析流结构。")

        if progress_cb:
            progress_cb(45, f"逆向解析数据流: {file_name}")

        try:
            salt_b64 = payload.get("salt", "")
            salt_bytes = base64.b64decode(salt_b64) if salt_b64 else b""
            nonce = base64.b64decode(payload["nonce"])
            ciphertext = base64.b64decode(payload["data"])
            iterations = payload.get("rounds") or payload.get("iter") or DERIVATION_ROUNDS
        except Exception:
            raise CryptoError("内部数据结构损坏，无法提取参数。")

        if not salt_bytes:
            raise CryptoError("数据包缺失关键凭证标识。")

        try:
            key = cls.derive_key(salt_bytes, private_key, iterations=iterations)
            aesgcm = AESGCM(key)
            decrypted_data = aesgcm.decrypt(nonce, ciphertext, None)
        except Exception:
            raise CryptoError("解析失败！密钥校验不匹配，或文档内容已损坏。")

        if progress_cb:
            progress_cb(80, f"验证文件指纹与完整性: {file_name}")

        original_fn = payload.get("fn", "restored_document")
        expected_sha = payload.get("sha256")
        actual_sha = hashlib.sha256(decrypted_data).hexdigest()

        if expected_sha and actual_sha != expected_sha:
            raise CryptoError("数据流校验异常：还原内容完整性指纹不一致！")

        # Output destination resolving
        if os.path.isdir(out_destination):
            out_file_path = os.path.join(out_destination, original_fn)
            base, ext = os.path.splitext(original_fn)
            counter = 1
            while os.path.exists(out_file_path):
                out_file_path = os.path.join(out_destination, f"{base}_restored_{counter}{ext}")
                counter += 1
        else:
            out_file_path = out_destination
            parent = os.path.dirname(os.path.abspath(out_file_path))
            if parent and not os.path.exists(parent):
                os.makedirs(parent, exist_ok=True)

        try:
            with open(out_file_path, "wb") as f:
                f.write(decrypted_data)
        except Exception as e:
            raise CryptoError(f"写入还原文件失败: {e}")

        if progress_cb:
            progress_cb(100, f"完成还原: {original_fn}")

        payload["actual_sha256"] = actual_sha
        payload["restored_path"] = out_file_path
        return out_file_path, payload
