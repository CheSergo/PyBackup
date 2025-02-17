import subprocess

from logger import logger


def mount_ssh_folder(local_path, remote_path, username, host):
    """
    Монтирует удаленную папку через SSH
    """
    # Создаем локальную директорию если она не существует
    logger.info("Creating a local directory at local path")
    try:
        mkdir_command = f"mkdir -p {local_path}"
        subprocess.call(mkdir_command, shell=True)

        # Монтируем удаленную папку
        logger.info("Mouning remote directory at remote path")
        mount_command = f"sshfs -o allow_other -o IdentityFile=~/.ssh/id_rsa {username}@{host}:{remote_path} {local_path}"
        subprocess.call(mount_command, shell=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Ошибка при выполнении команды: {e}")
    except Exception as e:
        logger.error(f"Произошла ошибка: {str(e)}")
        raise


def unmount_ssh_folder(local_path):
    """
    Размонтирует папку
    """
    try:
        #        unmount_command = f"fusermount -u {local_path}"
        unmount_command = f"umount {local_path}"
        subprocess.call(unmount_command, shell=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Ошибка при выполнении команды: {e}")
    except Exception as e:
        logger.error(f"Произошла ошибка: {str(e)}")
        raise
