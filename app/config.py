from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    openrouter_api_key: str
    openrouter_model: str = "meta-llama/llama-3.1-8b-instruct"
    
    cors_allowed_origins_raw: str="http://localhost:3000"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    def cors_allowed_origins(self) -> list[str]:
        """
        Returns the list of allowed origins for CORS, parsed from the raw string.
        """
        return [origin.strip() for origin in self.cors_allowed_origins_raw.split(",") if origin.strip()]


settings = Settings()