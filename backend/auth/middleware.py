from fastapi import Request, HTTPException
from .jwt_handler import verify_token
import re

class AuthMiddleware:
    def __init__(self, excluded_paths=None):
        self.excluded_paths = excluded_paths or [
            r"/api/auth/token",
            r"/api/auth/register",
            r"/docs",
            r"/openapi.json"
        ]

    async def __call__(self, request: Request, call_next):
        path = request.url.path
        
        # Check if path is excluded from authentication
        if any(re.match(pattern, path) for pattern in self.excluded_paths):
            return await call_next(request)
            
        # Check for authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise HTTPException(status_code=401, detail="Missing authentication token")
            
        token = auth_header.split(' ')[1]
        try:
            verify_token(token)
        except Exception as e:
            raise HTTPException(status_code=401, detail="Invalid authentication token")
            
        return await call_next(request) 