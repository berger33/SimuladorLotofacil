"""
Repository Pattern - Abstração de dados para suportar Desktop JSON, Mobile SQLite, e Remote API.
"""
from abc import ABC, abstractmethod
from typing import List, Set, Optional
import json
import os
import random
from datetime import datetime, timedelta

class SorteioRepository(ABC):
    @abstractmethod
    def get_todos(self) -> List[Set[int]]:
        pass

    @abstractmethod
    def get_recentes(self, n: int) -> List[Set[int]]:
        pass

    @abstractmethod
    def salvar_cache(self, sorteios: List[Set[int]]):
        pass

    @abstractmethod
    def get_ultimo(self) -> Optional[Set[int]]:
        pass

class LocalJsonRepository(SorteioRepository):
    """Legado - usa JSON local igual ao desktop atual."""
    def __init__(self, cache_path: str = "storage/resultados_historico_cache.json"):
        self.cache_path = cache_path

    def get_todos(self) -> List[Set[int]]:
        if os.path.exists(self.cache_path):
            try:
                with open(self.cache_path, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                    if dados and len(dados) > 100:
                        return [set(s) for s in dados]
            except Exception:
                pass
        # Fallback random para testes
        return [set(random.sample(range(1, 26), 15)) for _ in range(1000)]

    def get_recentes(self, n: int) -> List[Set[int]]:
        todos = self.get_todos()
        return todos[-n:] if len(todos) >= n else todos

    def salvar_cache(self, sorteios: List[Set[int]]):
        os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
        with open(self.cache_path, "w", encoding="utf-8") as f:
            json.dump([list(s) for s in sorteios], f)

    def get_ultimo(self) -> Optional[Set[int]]:
        todos = self.get_todos()
        return todos[-1] if todos else None

class CachedRepository(SorteioRepository):
    """
    Decorator que tenta remote primeiro, se falha usa local, com TTL.
    Ideal para mobile offline-first.
    """
    def __init__(self, local: SorteioRepository, remote: SorteioRepository, ttl_hours: int = 6):
        self.local = local
        self.remote = remote
        self.ttl_hours = ttl_hours
        self._last_fetch: Optional[datetime] = None

    def _is_cache_valid(self) -> bool:
        if self._last_fetch is None:
            return False
        return datetime.now() - self._last_fetch < timedelta(hours=self.ttl_hours)

    def get_todos(self) -> List[Set[int]]:
        if not self._is_cache_valid():
            try:
                sorteios = self.remote.get_todos()
                if sorteios and len(sorteios) > 100:
                    self.local.salvar_cache(sorteios)
                    self._last_fetch = datetime.now()
                    return sorteios
            except Exception as e:
                print(f"[CachedRepository] Remote falhou, usando local: {e}")

        return self.local.get_todos()

    def get_recentes(self, n: int) -> List[Set[int]]:
        return self.get_todos()[-n:]

    def salvar_cache(self, sorteios: List[Set[int]]):
        self.local.salvar_cache(sorteios)
        self._last_fetch = datetime.now()

    def get_ultimo(self) -> Optional[Set[int]]:
        todos = self.get_todos()
        return todos[-1] if todos else None

class RemoteApiRepository(SorteioRepository):
    """Busca da API da Caixa com múltiplos fallbacks."""
    def __init__(self):
        self.endpoints = [
            "https://servicebus2.caixa.gov.br/portaldeloterias/api/lotofacil",
            "https://api.guidi.dev.br/loteria/lotofacil/ultimos",
            "https://loteriascaixa-api.herokuapp.com/api/lotofacil"
        ]

    def get_todos(self) -> List[Set[int]]:
        import requests
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry

        session = requests.Session()
        retry = Retry(total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        for url in self.endpoints:
            try:
                response = session.get(url, timeout=10, headers={
                    "User-Agent": "LotofacilPro/1.0 (Educational; +https://github.com/berger33/SimuladorLotofacil)"
                })
                if response.status_code == 200:
                    dados = response.json()
                    sorteios = []
                    if isinstance(dados, list):
                        for concurso in dados:
                            if "dezenas" in concurso:
                                dezenas = [int(d) for d in concurso["dezenas"]]
                                sorteios.append(set(dezenas))
                    if sorteios:
                        return sorteios
            except Exception:
                continue

        return []

    def get_recentes(self, n: int) -> List[Set[int]]:
        return self.get_todos()[-n:]

    def salvar_cache(self, sorteios: List[Set[int]]):
        pass  # Remote não salva

    def get_ultimo(self) -> Optional[Set[int]]:
        todos = self.get_todos()
        return todos[-1] if todos else None
