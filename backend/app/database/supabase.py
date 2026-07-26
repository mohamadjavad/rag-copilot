from __future__ import annotations

from supabase import AsyncClient, acreate_client
from supabase.lib.client_options import AsyncClientOptions

from app.config import settings

_client: AsyncClient | None = None
_service_client: AsyncClient | None = None


async def get_client() -> AsyncClient:
    global _client
    if _client is None:
        _client = await acreate_client(
            settings.supabase_url,
            settings.supabase_anon_key,
            options=AsyncClientOptions(),
        )
    return _client


async def get_service_client() -> AsyncClient:
    global _service_client
    if _service_client is None:
        _service_client = await acreate_client(
            settings.supabase_url,
            settings.supabase_service_role_key,
            options=AsyncClientOptions(),
        )
    return _service_client
