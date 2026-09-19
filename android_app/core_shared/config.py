"""
Config - Pydantic Settings para mobile e desktop
"""
from typing import List
try:
    from pydantic_settings import BaseSettings
    from pydantic import Field
    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False
    BaseSettings = object
    Field = lambda default, **kwargs: default

if PYDANTIC_AVAILABLE:
    class AppConfig(BaseSettings):
        # Engine
        num_jogos_default: int = Field(15, description="Qtd jogos padrão")
        tam_base: int = 20
        tam_jogo: int = 15
        populacao: int = 30  # mobile
        populacao_desktop: int = 50
        elite: int = 8
        simulacoes_mobile: int = 1000
        simulacoes_desktop: int = 5000

        # Custos
        custo_aposta: float = 3.0
        premio_11: float = 6.0
        premio_12: float = 12.0
        premio_13: float = 30.0
        premio_14: float = 2000.0
        premio_15: float = 600000.0

        # Filtros
        soma_min: int = 180
        soma_max: int = 220
        primos_alvo: List[int] = [5, 6]
        pares_alvo: List[int] = [7, 8]
        max_sequencia: int = 4

        # ML
        lstm_time_steps: int = 15
        lstm_epochs: int = 30

        # App
        app_name: str = "Lotofácil Pro"
        app_version: str = "1.0.0"
        is_premium: bool = False
        max_jogos_free: int = 10
        max_jogos_premium: int = 33

        # API
        api_base_url: str = "https://api.lotofacilpro.com"
        cache_ttl_hours: int = 6

        # AdMob (teste IDs)
        admob_app_id: str = "ca-app-pub-3940256099942544~3347511713"
        admob_banner_id: str = "ca-app-pub-3940256099942544/6300978111"
        admob_interstitial_id: str = "ca-app-pub-3940256099942544/1033173712"
        admob_rewarded_id: str = "ca-app-pub-3940256099942544/5224354917"

        class Config:
            env_file = ".env"
            env_file_encoding = "utf-8"

    config = AppConfig()
else:
    # Fallback sem pydantic
    class AppConfigFallback:
        num_jogos_default = 15
        tam_base = 20
        tam_jogo = 15
        populacao = 30
        populacao_desktop = 50
        elite = 8
        simulacoes_mobile = 1000
        simulacoes_desktop = 5000
        custo_aposta = 3.0
        premio_11 = 6.0
        premio_12 = 12.0
        premio_13 = 30.0
        premio_14 = 2000.0
        premio_15 = 600000.0
        soma_min = 180
        soma_max = 220
        primos_alvo = [5, 6]
        pares_alvo = [7, 8]
        max_sequencia = 4
        app_name = "Lotofácil Pro"
        app_version = "1.0.0"
        is_premium = False
        max_jogos_free = 10
        max_jogos_premium = 33
        api_base_url = "https://api.lotofacilpro.com"
        cache_ttl_hours = 6
        admob_app_id = "ca-app-pub-3940256099942544~3347511713"
        admob_banner_id = "ca-app-pub-3940256099942544/6300978111"
        admob_interstitial_id = "ca-app-pub-3940256099942544/1033173712"
        admob_rewarded_id = "ca-app-pub-3940256099942544/5224354917"

    config = AppConfigFallback()
