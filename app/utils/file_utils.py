from os import makedirs, mkdir, path
from shutil import rmtree


def create_file_with_content(file_path, file_name, content) -> None:
    """

    :param file_path: File path, for creating file
    :param file_name: Name for the file
    :param content: Content of the file
    :return:
    """

    if not path.exists(file_path):
        makedirs(file_path, exist_ok=True)
    with open(file_path + file_name, mode='w') as file:
        file.write(content)
        file.close()


def reset_folder(folder_path: str = "output/") -> None:
    """

    :param folder_path: Folder path which we are going to reset
    :return:
    """
    if path.exists(folder_path):
        rmtree(folder_path)
    mkdir(folder_path)
