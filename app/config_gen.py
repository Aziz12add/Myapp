import uuid
from typing import Any


def gen_vless_config(secret: str, ip: str, port: int = 443, path: str = "/ws") -> dict[str, Any]:
    """تولید کانفیگ VLESS به صورت دیکشنری + لینک"""
    user_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, secret))  # UUID پایدار بر اساس secret

    config = {
        "outbounds": [
            {
                "protocol": "vless",
                "settings": {
                    "vnext": [
                        {
                            "address": ip,
                            "port": port,
                            "users": [
                                {
                                    "id": user_id,
                                    "encryption": "none",
                                    "flow": ""
                                }
                            ]
                        }
                    ]
                },
                "streamSettings": {
                    "network": "ws",
                    "security": "tls",
                    "tlsSettings": {
                        "serverName": ip,
                        "allowInsecure": False
                    },
                    "wsSettings": {
                        "path": path
                    }
                }
            }
        ]
    }

    # لینک آماده برای کپی
    link = f"vless://{user_id}@{ip}:{port}?encryption=none&security=tls&type=ws&path={path}#Myapp"

    return {
        "config": config,
        "link": link
    }


def gen_trojan_config(secret: str, ip: str, port: int = 443) -> dict[str, Any]:
    """تولید کانفیگ Trojan"""
    link = f"trojan://{secret}@{ip}:{port}?security=tls#Myapp"

    return {
        "config": {
            "password": secret,
            "address": ip,
            "port": port
        },
        "link": link
    }


def gen_vmess_config(secret: str, ip: str, port: int = 443, path: str = "/ws") -> dict[str, Any]:
    """تولید کانفیگ ساده VMess"""
    import base64
    import json

    user_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, secret))

    vmess_obj = {
        "v": "2",
        "ps": "Myapp",
        "add": ip,
        "port": port,
        "id": user_id,
        "aid": 0,
        "net": "ws",
        "type": "none",
        "host": "",
        "path": path,
        "tls": "tls"
    }

    link = "vmess://" + base64.b64encode(json.dumps(vmess_obj).encode()).decode()

    return {
        "config": vmess_obj,
        "link": link
    }


def generate_config(protocol: str, secret: str, ip: str) -> dict[str, Any]:
    """تابع کمکی برای انتخاب پروتکل"""
    if protocol == "vless":
        return gen_vless_config(secret, ip)
    elif protocol == "trojan":
        return gen_trojan_config(secret, ip)
    elif protocol == "vmess":
        return gen_vmess_config(secret, ip)
    else:
        raise ValueError(f"پروتکل پشتیبانی نشده: {protocol}")
