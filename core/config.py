import os
from dataclasses import dataclass
from pathlib import Path
from typing import List

import yaml
from logger import logger


@dataclass
class DurationConfig:
    """Конфигурация времени"""

    day_week: str
    month: str
    day: str
    hour: str
    minute: str


@dataclass
class ServerConfig:
    """Конфигурация сервера"""

    server_ip: str
    username: str
    password: str
    remote_dir: str
    local_dir: str


@dataclass
class Config:
    """Главная конфигурационная структура"""

    path: str
    target_folder: str
    excluded_directories: List[str]
    log_path: str
    duration: DurationConfig
    server: ServerConfig


def get_config(path: Path) -> Config:
    logger.info("Getting config file")
    try:
        with open(path, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
            return Config(**config)
    except FileNotFoundError:
        logger.error("Config file not found")


def isConfigExists(path: Path) -> bool:
    if path.exists():
        logger.info(f"Config file already exists at {path}")
        return True
    logger.warning("Config file doesn't exist")
    logger.warning(f"Config file would be created at {path}")

    return False


def create_default_config_file(path: Path):
    example_config = """# Example main config
path: /var/www
target_folder: /mnt/backups/
duration:
  day_week: 1
  month: 1
  day: "*"
  hour: 12
  minute: 00
excluded_directories:
  - dir_1/target
  - dir_2/
  - dir_3/project/.git/
server:
  server_ip: "72.16.0.1"
  username: "username"
  password: "password"
  remote_dir: "/backup/72-16-0-1"
  local_dir: "/mnt/backups"
log_path: "./status.log"
"""
    try:
        os.makedirs(path.parent, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            f.write(example_config)
        logger.info(f"Example config file created at {path}")
        logger.warning(
            "Now you can change the log file path. Also default config file created. You can find it at - "
            + str(path)
        )
    except OSError as e:
        logger.error(f"Failed to create directories and file: {str(e)}")
        return None
