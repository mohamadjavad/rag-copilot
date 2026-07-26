from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from supabase import AsyncClient

from app.auth.schemas import AuthenticatedUser
from app.database.supabase import get_client

_bearer = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
    client: AsyncClient = Depends(get_client),
) -> AuthenticatedUser:
    try:
        response = await client.auth.get_user(credentials.credentials)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    user = response.user
    return AuthenticatedUser(id=user.id, email=user.email)
