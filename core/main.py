#!usr/bin/python
# -*- coding: utf-8 -*-
import sys
from pathlib import Path

from archiver import count_files_to_archive, create_arhive, create_exclusion_list
from config import create_default_config_file, get_config, isConfigExists
from logger import logger
from ssh_mounter import mount_ssh_folder, unmount_ssh_folder
from test import test, test2


def main():
    logger.info("======== Backup programm started ========")
    config_path = Path("./config/config.yml")

    if not isConfigExists(config_path):
        create_default_config_file(config_path)
        logger.info("Programm determined with status 0")
        sys.exit(0)

    config = get_config(config_path)

    local_path = Path(config.server["local_dir"])
    remote_path = Path(config.server["remote_dir"])
    username = config.server["username"]
    host = config.server["server_ip"]

    source_folder = Path(config.path)
    excluded_dirs = create_exclusion_list(source_folder, config.excluded_directories)
    target_folder = Path(config.target_folder)

    files = count_files_to_archive(source_folder, excluded_dirs)
    print(f"Total files - {files}")

    try:
        mount_ssh_folder(local_path, remote_path, username, host)
        logger.info(f"Папка успешно примонтирована в {local_path}")

        logger.info("Start zipping")
        create_arhive(source_folder, excluded_dirs, target_folder)
        logger.info("End Zipping")

        unmount_ssh_folder(local_path)
        logger.info("Папка успешно размонтирована")
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")

    logger.info("======== Finished ========")


if __name__ == "__main__":
    main()
