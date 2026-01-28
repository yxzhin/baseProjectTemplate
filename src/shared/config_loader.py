from pathlib import Path


class ConfigLoader:
    """Класс для загрузки переменных окружения из файла .env."""

    BASE_PATH = Path(__file__).resolve().parent.parent.parent

    @staticmethod
    def import_env() -> None:
        """
        Загружает переменные окружения из файла .env, если он существует.
        Если файл не найден, выводится сообщение и загрузка пропускается.
        """
        try:
            from dotenv import load_dotenv
        except Exception:
            print("Starting without .env")
            return

        env_file = ConfigLoader.BASE_PATH / ".env"
        print(f"Loading environment variables from {env_file}")
        if not env_file.exists():
            print(f"File {env_file} not found. Skipping loading environment variables.")
            return
        load_dotenv(dotenv_path=env_file)
