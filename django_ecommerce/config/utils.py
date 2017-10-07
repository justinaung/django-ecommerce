import os

from typing import Union


def get_file_secret(file_path: str) -> Union[str, None]:
    return open(os.path.expanduser(file_path)).read().strip() \
           if file_path else None
