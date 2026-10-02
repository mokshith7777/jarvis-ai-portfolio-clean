from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 8080
    db: str = "data/jarvis.db"
    max_context_tokens: int = 128_000
    compression_threshold: float = 0.50
    compression_target_ratio: float = 0.20
    protect_last_n: int = 20
    exec_timeout: int = 300
    max_rpc_calls: int = 50
    approval_mode: str = "smart"
    primary_provider: str = "mock"
    aux_provider: str = "mock"
    api_key: str = ""
    model_config = SettingsConfigDict(env_prefix="JARVIS_", env_file=".env", extra="ignore")

    def ensure_dirs(self) -> None:
        Path(self.db).parent.mkdir(parents=True, exist_ok=True)

settings = Settings()
