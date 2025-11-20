import logging
import json
import sys
from pathlib import Path


# Корень проекта: src/logging_config.py → src → ..
BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / "data" / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "time": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "filename": record.filename,
            "lineno": record.lineno,
            "module": record.module,
            "funcName": record.funcName,
        }

        if record.exc_info:
            log_record["exc_info"] = self.formatException(record.exc_info)

        return json.dumps(log_record, ensure_ascii=False)


def get_logger(name: str) -> logging.Logger:
    """
    Создаёт/возвращает логгер для модуля `name`.
    - Пишет JSON в stdout
    - Пишет JSON в отдельный файл для каждого модуля: data/logs/<module_name>.log
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Если хендлеры уже есть — просто возвращаем (чтобы не дублировать вывод)
    if logger.handlers:
        return logger

    formatter = JsonFormatter()

    # 1) JSON в stdout (для Docker / локальной отладки)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # 2) JSON в файл, отдельный под каждый модуль
    safe_name = name.replace(".", "_")  # my_package.module → my_package_module.log
    log_file = LOGS_DIR / f"{safe_name}.log"

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
