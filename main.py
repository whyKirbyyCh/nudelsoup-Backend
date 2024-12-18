from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, model_validator
from typing import Dict, Callable, Tuple
from functools import wraps
from app.services.rest.user_authentication_service import UserAuthenticationService
from app.services.rest.user_limit_check_service import UserLimitCheckService
from app.excpetions.rest.user_authentication_excpetion import UserAuthenticationException
from app.excpetions.db.db_connection_exception import DBConnectionException
from app.excpetions.rest.user_limits_exception import UserLimitsException
from app.config.logger_config import Logger
from app.models.order import Order
from app.core.post_creation.post_creation_manager import PostCreationManager
from app.core.post_connection.post_connection_manager import PostConnectionManager
from app.excpetions.post_connection_exception.post_connection_exception import PostConnectionException
import traceback
from app.filters.rate_limit_middleware_filter import RateLimitMiddleware

app = FastAPI()
logger = Logger.get_logger()
rate_limit_middleware = RateLimitMiddleware(app, default_limit="1 per 5 minutes")


class AccountInfo(BaseModel):
    token: str


class CompanyInfo(BaseModel):
    company_name: str
    company_description: str
    company_country: str
    company_size: int
    company_age: str
    company_industry: str

    class Config:
        extra = "allow"

    @model_validator(mode="before")
    def check_additional_fields(cls, values):
        for field in values:
            if field in cls.model_fields:
                continue
            elif field.startswith("additional_"):
                if not isinstance(values[field], str):
                    raise ValueError(f"{field} must be a string")
            else:  # Invalid field
                raise ValueError(
                    f"Unexpected field: {field}. It must start with 'additional_' or be a defined model field.")
        return values


class ProductInfo(BaseModel):
    product_name: str
    product_description: str
    product_business_model: str
    product_type: str
    product_market: str

    class Config:
        extra = "allow"

    @model_validator(mode="before")
    def check_additional_fields(cls, values):
        for field in values:
            if field in cls.model_fields:
                continue
            elif field.startswith("additional_"):
                if not isinstance(values[field], str):
                    raise ValueError(f"{field} must be a string")
            else:  # Invalid field
                raise ValueError(
                    f"Unexpected field: {field}. It must start with 'additional_' or be a defined model field.")
        return values


class RequestInfo(BaseModel):
    ip: str
    request_id: str
    product_id: str
    campaign_id: str
    services: Dict[str, bool]
    sscop: bool
    cpop: bool
    sspop: bool
    ppsop: bool


def authenticate_and_check_limits(token: str, limit_check_func: Callable[[str, str], bool], flag: str) -> str:
    """
    Helper function for authentication and user limit checks.

    Args:
        token (str): The token.
        limit_check_func (Callable[[str, str], bool]): The user limit check function.
        flag (str): The flag for the limit check.

    Raises:
        UserAuthenticationException: If the user authentication fails.
        UserLimitsException: If the user limit check fails.
    """
    authenticated, user_id = UserAuthenticationService().authenticate_user(token=token)
    limit_check_passed = limit_check_func(user_id, flag)

    if not authenticated:
        raise UserAuthenticationException("User authentication failed.")
    if not limit_check_passed:
        raise UserLimitsException("User limit exceeded.")

    return user_id


def authenticate_user(token: str) -> None:
    """
    Helper function for authentication.

    Args:
        token (str): The token.

    Raises:
        UserAuthenticationException: If the user authentication fails.
    """
    authenticated = UserAuthenticationService().authenticate_user(token=token)

    if not authenticated:
        raise UserAuthenticationException("User authentication failed.")


def error_handling(func):
    """Decorator for handling common errors."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except UserAuthenticationException as e:
            raise HTTPException(status_code=401, detail=str(e)) from e
        except UserLimitsException as e:
            raise HTTPException(status_code=403, detail=str(e)) from e
        except DBConnectionException as e:
            raise HTTPException(status_code=500, detail=str(e)) from e
        except PostConnectionException as e:
            raise HTTPException(status_code=500, detail=str(e)) from e
        except Exception as e:
            logger.error(f"Unexpected error: {e}\n{traceback.format_exc()}")
            raise HTTPException(status_code=500, detail="An unexpected error occurred.") from e
    return wrapper


class RequestDataPosts(BaseModel):
    request_info: RequestInfo
    account_info: AccountInfo
    company_info: CompanyInfo
    product_info: ProductInfo


@app.put("/api/get_posts")
@rate_limit_middleware.limiter.limit("10 per 5 minutes")
@error_handling
async def get_posts(request: Request, data: RequestDataPosts):
    user_id: str = authenticate_and_check_limits(
        token=data.account_info.token,
        limit_check_func=UserLimitCheckService().check_user_limit,
        flag="posts"
    )

    order = Order(
        services=data.request_info.services,
        company_info=data.company_info.dict(),
        product_info=data.product_info.dict(),
        sscop=data.request_info.sscop,
        cpop=data.request_info.cpop,
        sspop=data.request_info.sspop,
        ppsop=data.request_info.ppsop
    )

    post_creation_manager = PostCreationManager(
        request_id=data.request_info.request_id,
        order=order,
        user_id=user_id,
        campaign_id=data.request_info.campaign_id,
        product_id=data.request_info.product_id
    )

    response: Dict[str, Dict[str, str]] = post_creation_manager.get_posts()

    return response


class RequestDataAnalytics(BaseModel):
    request_info: str
    account_info: AccountInfo


@app.get("/api/get_analytics")
@rate_limit_middleware.limiter.limit("10 per 5 minutes")
@error_handling
async def get_analytics(request: Request, data: RequestDataAnalytics):
    authenticate_and_check_limits(
        token=data.account_info.token,
        limit_check_func=UserLimitCheckService().check_user_limit,
        flag="analytics"
    )

    return {"status": "ok"}


@app.put("/api/give_token")
@rate_limit_middleware.limiter.limit("10 per 5 minutes")
@error_handling
async def get_analytics(request: Request, data: RequestDataAnalytics):
    authenticate_user(
        token=data.account_info.token
    )

    return {"status": "ok"}


class PostInfo(BaseModel):
    posts: Dict[str, Tuple[str, str]]


class RequestDataConnection(BaseModel):
    request_info: str
    account_info: AccountInfo
    post_info: PostInfo


@app.put("/api/connect_posts")
@rate_limit_middleware.limiter.limit("10 per 5 minutes")
@error_handling
async def get_analytics(request: Request, data: RequestDataConnection):
    authenticate_user(
        token=data.account_info.token
    )

    post_connection_manager = PostConnectionManager(
        posts=data.post_info.posts,
        user_id=data.account_info.user_id
    )

    response = post_connection_manager.connect_posts()

    return response
