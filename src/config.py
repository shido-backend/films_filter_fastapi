from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    kinopoisk_api_key: str
    api_base_url: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()