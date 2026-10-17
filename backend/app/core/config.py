import os


class Settings:
    PROJECT_NAME: str = "C216 - Sistemas Distribuídos"
    VERSION: str = "5.0.0"

    # Configuracoes de Banco de Dados
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "postgrespassword")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_NAME: str = os.getenv("DB_NAME", "c216_db")

    @property
    def DATABASE_URL(self) -> str:
        url = os.getenv(
            "DATABASE_URL",
            f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}",
        )
        # Garante compatibilidade do dialeto psycopg 3
        if url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+psycopg://", 1)
        return url


settings = Settings()
