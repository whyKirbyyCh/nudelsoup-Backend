from fastapi import Request, Response
from starlette.responses import JSONResponse
from slowapi import Limiter
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from typing import Optional


class RateLimitMiddleware:
    """ Middleware class to add rate limiting to the FastAPI API. """
    def __init__(self, app, default_limit: Optional[str] = "10 per 5 minutes") -> None:
        """
        Initialize the RateLimitMiddleware class.

        Args:
            app (FastAPI): The FastAPI application.
            default_limit (Optional[str], optional): The default rate limit. Defaults to "1 per 5 minutes".
        """
        self.limiter = Limiter(key_func=lambda request: request.state.username, default_limits=[default_limit])

        app.state.limiter = self.limiter
        app.add_middleware(SlowAPIMiddleware)
        app.add_exception_handler(RateLimitExceeded, self.rate_limit_exceeded_handler)
        app.middleware("http")(self.add_username_to_state)

    @staticmethod
    async def add_username_to_state(request: Request, call_next) -> Response:
        """
        Middleware to add the username from RequestData to the request state.

        Args:
            request (Request): The FastAPI request object.
            call_next (Callable): The FastAPI request handler.
        Returns:
            Response: The FastAPI response object.
        """
        try:
            request_data = await request.json()
            account_info = request_data.get('account_info', {})
            username = account_info.get('username')

            if not username:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Username is required"}
                )

            request.state.username = username
        except Exception as e:
            return JSONResponse(
                status_code=400,
                content={"detail": f"Error processing username: {str(e)}"}
            )

        response = await call_next(request)
        return response

    @staticmethod
    async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> Response:
        """
        Handle rate limit exceeded error by returning a 429 HTTP response.

        Args:
            request (Request): The FastAPI request object.
            exc (RateLimitExceeded): The rate limit exceeded exception.
        Returns:
            Response: The FastAPI response object.
        """
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded. Please try again later."}
        )
