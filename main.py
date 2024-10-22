from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, model_validator
from typing import Dict
from app.services.rest.user_authentication_service import UserAuthenticationService
from app.services.rest.user_post_limit_check_service import UserPostLimitCheckService
from app.excpetions.rest.user_authentication_excpetion import UserAuthenticationException
from app.excpetions.db.db_connection_exception import DBConnectionException
from app.excpetions.rest.user_limits_exception import UserLimitsException
from app.config.logger_config import Logger
from app.models.order import Order
from app.core.post_creation.post_creation_manager import PostCreationManager
import traceback
from app.filters.rate_limit_middleware_filter import RateLimitMiddleware
from app.services.rest.user_analytics_limit_check import UserAnalyticsLimitCheckService


app = FastAPI()
logger = Logger.get_logger()
rate_limit_middleware = RateLimitMiddleware(app, default_limit="1 per 5 minutes")


class AccountInfo(BaseModel):
    user_id: str
    username: str
    email: str
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
            else:
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
            else:
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


class RequestDataPosts(BaseModel):
    request_info: RequestInfo
    account_info: AccountInfo
    company_info: CompanyInfo
    product_info: ProductInfo


@app.get("/api/get_posts")
@rate_limit_middleware.limiter.limit("10 per 5 minutes")
async def get_posts(request: Request, data: RequestDataPosts):
    try:
        authentication: bool = UserAuthenticationService().authenticate_user(
            data.account_info.username, data.account_info.email, data.account_info.token
        )

        limitcheck: bool = UserPostLimitCheckService().check_user_limit(
            data.account_info.user_id
        )

        if authentication and limitcheck:
            order: Order = Order(services=data.request_info.services, company_info=data.company_info.dict(), product_info=data.product_info.dict(), sscop=data.request_info.sscop, cpop=data.request_info.cpop, sspop=data.request_info.sspop, ppsop=data.request_info.ppsop)

            post_creation_manager: PostCreationManager = PostCreationManager(request_id=data.request_info.request_id, order=order, user_id=data.account_info.user_id, campaign_id=data.request_info.campaign_id, product_id=data.request_info.product_id)

            response: Dict[str, Dict[str, str]] = post_creation_manager.get_posts()

            return response
        else:
            raise UserAuthenticationException("User is not allowed to access this resource.")

    except UserAuthenticationException as e:
        raise HTTPException(status_code=401, detail=str(e)) from e

    except UserLimitsException as e:
        raise HTTPException(status_code=403, detail=str(e)) from e

    except DBConnectionException as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    except Exception as e:
        logger.error(f"Unexpected error: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.") from e



class RequestDataAnalytics(BaseModel):
    request_info: str
    account_info: AccountInfo

@app.get("/api/get_analytics")
@rate_limit_middleware.limiter.limit("10 per 5 minutes")
async def get_analytics(request: Request, data: RequestDataAnalytics):
    try:
        authentication: bool = UserAuthenticationService().authenticate_user(
            data.account_info.username, data.account_info.email, data.account_info.token
        )

        limitcheck: bool = UserAnalyticsLimitCheckService().check_user_limit(
            data.account_info.user_id
        )

        if authentication and limitcheck:
            return {"status": "ok"}
        else:
            raise UserAuthenticationException("User is not allowed to access this resource.")

    except UserAuthenticationException as e:
        raise HTTPException(status_code=401, detail=str(e)) from e

    except UserLimitsException as e:
        raise HTTPException(status_code=403, detail=str(e)) from e

    except DBConnectionException as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    except Exception as e:
        logger.error(f"Unexpected error: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.") from e
