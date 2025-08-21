"""
Hook di monitoraggio: Telegram alerts e heartbeat file.
"""

import time
import requests

def telegram_alert(enabled: bool, token: str, chat_id: str, text: str):
    if not enabled: return
    try:
        requests.get(f"https://api.telegram.org/bot{token}/sendMessage", params={"chat_id": chat_id, "text": text}, timeout=5)
    except Exception:
        pass

def heartbeat(enabled: bool, path: str):
    if not enabled: return
    try:
        with open(path, "w") as f:
            f.write(str(time.time()))
    except Exception:
        pass
