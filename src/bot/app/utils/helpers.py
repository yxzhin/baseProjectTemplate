from os import getcwd
from os.path import relpath


class Helpers:
    """Вспомогательные методы для работы с путями и расширениями."""

    @staticmethod
    def get_extension_path(abs_cogs_path: str, file: str) -> str:
        """Возвращает путь расширения для загрузки когов."""
        abs_cog_path = f"{abs_cogs_path}/{file}"
        working_dir = getcwd()
        rel_path = relpath(abs_cog_path, working_dir)
        ext_path = rel_path.replace("\\", ".")[:-3]

        return ext_path
