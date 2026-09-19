"""
Logger abstraído - funciona em desktop, mobile, backend.
No mobile, envia para Crashlytics. No desktop, para file.
"""
import logging
import os
from typing import Optional

class AppLogger:
    def __init__(self, name: str = "LotofacilPro", level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        if not self.logger.handlers:
            # Console handler sempre
            console = logging.StreamHandler()
            console.setLevel(level)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            console.setFormatter(formatter)
            self.logger.addHandler(console)
            
            # File handler se possível (desktop)
            try:
                os.makedirs("storage/logs", exist_ok=True)
                file_handler = logging.FileHandler("storage/logs/system.log", encoding="utf-8")
                file_handler.setLevel(level)
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)
            except Exception:
                pass  # Mobile não tem permissão, ignora

    def info(self, msg: str):
        self.logger.info(msg)

    def warning(self, msg: str):
        self.logger.warning(msg)

    def error(self, msg: str, exc: Optional[Exception] = None):
        if exc:
            self.logger.error(f"{msg}: {exc}", exc_info=True)
        else:
            self.logger.error(msg)

    def debug(self, msg: str):
        self.logger.debug(msg)

# Singleton
logger = AppLogger()
