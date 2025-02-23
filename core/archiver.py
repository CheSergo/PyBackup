import os
import zipfile
from pathlib import Path

from logger import logger
from progress_tracker import ArchiveProgressTracker


def create_arhive(
    source_folder_path: Path, exclusions: list[Path] = [], target_path: Path = None
):
    """
    Создаёт архив из указанной папки, исключая файлы и директории из списка исключений

    Args:
        source_folder_path (str): Путь к папке для архивации
        exclusions (list): Список путей или имён файлов/папок для исключения
        target_path (str, optional): Путь для сохранения архива. Если не указан,
            архив будет создан в той же папке, где находится исходная директория

    Returns:
        str: Путь к созданному архиву
    """
    # Проверяем существование папки источника
    if not os.path.exists(source_folder_path):
        logger.error(f"Directory {source_folder_path} doesn't exist")
        raise FileNotFoundError(f"Папка {source_folder_path} не существует")

    # Определяем базовое имя архива
    archive_name = f"{os.path.basename(source_folder_path)}.zip"

    # Если целевой путь не указан, используем директорию исходной папки
    final_target_path = os.path.join(
        target_path if target_path else os.path.dirname(source_folder_path),
        archive_name,
    )

    # Создаем все необходимые директории в пути назначения
    target_dir = os.path.dirname(final_target_path)
    if target_dir and not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Считаем файлы
    files = count_files_to_archive(source_folder_path, exclusions)
    tracker = ArchiveProgressTracker(files, os.path.basename(source_folder_path))
    print(f"Total files - {files}")

    try:
        # Создаем архив
        with zipfile.ZipFile(
            final_target_path, "w", compression=zipfile.ZIP_DEFLATED
        ) as zf:
            # Проходим по всем файлам и папкам
            for root, dirs, files in os.walk(source_folder_path):
                # Фильтруем директории согласно исключениям
                dirs[:] = [
                    d for d in dirs if Path(os.path.join(root, d)) not in exclusions
                ]

                # Добавляем текущую директорию в архив
                rel_path = os.path.relpath(
                    root, start=os.path.dirname(source_folder_path)
                )
                if len(os.listdir(root)) == 0:
                    zf.write(os.path.join(root, ""), rel_path + "/")

                # Добавляем оставшиеся файлы в архив
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(
                        full_path, start=os.path.dirname(source_folder_path)
                    )

                    # Проверяем, не находится ли файл в списке исключений
                    if Path(full_path) not in exclusions:
                        zf.write(full_path, rel_path)
                        tracker.update(file)

        return final_target_path

    except Exception as e:
        raise RuntimeError(f"Ошибка при создании архива: {str(e)}")


def is_path_in_any_base_path(target_path: Path, base_paths: list[Path]) -> bool:
    return any(target_path.is_relative_to(base_path) for base_path in base_paths)


# def count_files_to_archive(source_folder_path: Path, exclusions: list[Path]) -> tuple[int, int]:
def count_files_to_archive(source_folder_path: Path, exclusions: list[Path]) -> int:
    """
    Подсчитывает количество файлов, которые будут включены в архив.

    Args:
        source_folder_path: путь к исходной директории
        exclusions: список путей для исключения

    Returns:
        int: количество файлов для архивации
    """

    if not source_folder_path.exists():
        raise FileNotFoundError(f"Путь '{source_folder_path}' не существует")

    total_files = 0
    total_folders = 0

    for root, dirs, files in os.walk(source_folder_path):
        dirs[:] = [d for d in dirs if Path(os.path.join(root, d)) not in exclusions]
        total_folders += len(dirs)

        for file in files:
            full_path = os.path.join(root, file)
            # Проверяем, не находится ли файл в списке исключений
            if Path(full_path) not in exclusions:
                total_files += 1

    # Добавляем корневую папку
    total_folders += 1
    # return total_files, total_folders
    return total_files + total_folders


def create_exclusion_list(root: Path, exclusions: list[str]) -> list[Path]:
    """
    Создаёт список исключений на основе корнейвого каталога и списка исключений из конфига

    Args:
        root (Path): root path
        exclusions (list[str]): Список имён файлов/папок для исключения

    Returns:
        list[Path]: list of paths as Path class
    """
    return [root / exclusion.strip("/") for exclusion in exclusions]
