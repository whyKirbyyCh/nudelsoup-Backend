from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, model_validator
from typing import Dict
from app.services.rest.user_authentication_service import UserAuthenticationService
from app.excpetions.rest.user_authentication_excpetion import UserAuthenticationException
from app.excpetions.rest.user_limits_exception import UserLimitsException
from app.config.logger_config import Logger
from app.models.order import Order
from app.core.post_creation.post_creation_manager import PostCreationManager
import traceback
from app.filters.rate_limit_middleware_filter import RateLimitMiddleware


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


# TODO: complete this
class ProductInfo(BaseModel):
    product_name: str
    product_description: str


class RequestData(BaseModel):
    ip: str
    request_id: str
    account_info: AccountInfo
    company_info: CompanyInfo
    product_info: ProductInfo
    services: Dict[str, bool]


@app.get("/api/get_posts")
@rate_limit_middleware.limiter.limit("1 per 5 minutes")
async def get_posts(request: Request, data: RequestData):
    try:
        authentication: bool = UserAuthenticationService().authenticate_user(
            data.account_info.username, data.account_info.email, data.account_info.token
        )

        if authentication:
            order: Order = Order(services=data.services, company_info=data.company_info.dict(), product_info=data.product_info, sscop=False, cpop=False, sspop=False, ppsop=False)

            post_creation_manager: PostCreationManager = PostCreationManager(request_id=data.request_id, order=order)

            response: Dict[str, Dict[str, str]] = post_creation_manager.get_posts()

            return response
        else:
            raise UserAuthenticationException("User is not allowed to access this resource.")

    except UserAuthenticationException as e:
        raise HTTPException(status_code=401, detail=str(e))

    except UserLimitsException as e:
        raise HTTPException(status_code=429, detail=str(e))

    except Exception as e:
        logger.error(f"Unexpected error: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")

