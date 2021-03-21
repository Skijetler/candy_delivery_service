from fastapi import Request, status
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.responses import ORJSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from candy_delivery.api.schema import (Id,
                                       CouriersPostValidationErrorResponse, 
                                       CourierPostRequest,
                                       CouriersPostRequest,
                                       CouriersPostResponse,
                                       OrdersPostValidationErrorResponse,
                                       OrderPostRequest,
                                       OrdersPostRequest,
                                       OrdersPostResponse)


async def RequestValidationHandler(request: Request, exc: RequestValidationError):
    if "/couriers" in request.url.path and request.method == "POST":
        err_val = CouriersPostValidationErrorResponse(validation_error=CouriersPostResponse(couriers=[])).dict()
        if type(exc.body) == dict: # а массив ли нам передали
            if 'data' in exc.body.keys(): # есть ли ключ data
                for item in exc.body['data']:
                    try:
                        CourierPostRequest(**item)
                    except ValidationError as e:
                        if type(item) == dict:
                            if 'courier_id' in item.keys(): # есть ли ключ courier_id
                                if type(item["courier_id"]) != int: # проверка типа ключа
                                    err_val["validation_error"]["couriers"].append(Id(id=0).dict())
                                else:
                                    err_val["validation_error"]["couriers"].append(Id(id=item["courier_id"]).dict())
                                for error in e.errors():
                                    if error["type"] == 'value_error.extra':
                                        err_val["validation_error"]["couriers"][-1][error["loc"][0]] = item[error["loc"][0]]
                            else:
                                err_val["validation_error"]["couriers"].append(Id(id=0).dict())
                                return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=err_val)
                        else:
                            err_val["validation_error"]["couriers"].append(Id(id=0).dict())
                            return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=err_val)
                try:
                    CouriersPostRequest(**exc.body)
                except ValidationError as e:
                    for error in e.errors():
                        if error["type"] == 'value_error.extra' and len(error["loc"]) == 1:
                            err_val["validation_error"][error["loc"][0]] = exc.body[error["loc"][0]]
                return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=err_val)
            else:
                err_val["validation_error"]["couriers"].append(Id(id=0).dict())
                try:
                    CouriersPostRequest(**exc.body)
                except ValidationError as e:
                    for error in e.errors():
                        if error["type"] == 'value_error.extra' and len(error["loc"]) == 1:
                            err_val["validation_error"][error["loc"][0]] = exc.body[error["loc"][0]]
                return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=err_val)
        else:
            err_val["validation_error"]["couriers"].append(Id(id=0).dict())
            return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=err_val)
    elif "/couriers/" in request.url.path and request.method == "GET":
        return ORJSONResponse(status_code=status.HTTP_404_NOT_FOUND)
    elif "/couriers/" in request.url.path and request.method == "PATCH":
        return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST)
    elif request.url.path.endswith("/orders") and request.method == "POST":
        err_val = OrdersPostValidationErrorResponse(validation_error=OrdersPostResponse(orders=[])).dict()
        if type(exc.body) == dict: # а массив ли нам передали
            if 'data' in exc.body.keys(): # есть ли ключ data
                for item in exc.body['data']:
                    try:
                        OrderPostRequest(**item)
                    except ValidationError as e:
                        if type(item) == dict:
                            if 'order_id' in item.keys(): # есть ли ключ order_id
                                if type(item["order_id"]) != int: # проверка типа ключа
                                    err_val["validation_error"]["orders"].append(Id(id=0).dict())
                                else:
                                    err_val["validation_error"]["orders"].append(Id(id=item["order_id"]).dict())
                                for error in e.errors():
                                    if error["type"] == 'value_error.extra':
                                        err_val["validation_error"]["orders"][-1][error["loc"][0]] = item[error["loc"][0]]
                            else:
                                err_val["validation_error"]["orders"].append(Id(id=0).dict())
                                return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=err_val)
                        else:
                            err_val["validation_error"]["orders"].append(Id(id=0).dict())
                            return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=err_val)
                try:
                    OrdersPostRequest(**exc.body)
                except ValidationError as e:
                    for error in e.errors():
                        if error["type"] == 'value_error.extra' and len(error["loc"]) == 1:
                            err_val["validation_error"][error["loc"][0]] = exc.body[error["loc"][0]]
                return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=err_val)
            else:
                err_val["validation_error"]["couriers"].append(Id(id=0).dict())
                try:
                    OrdersPostRequest(**exc.body)
                except ValidationError as e:
                    for error in e.errors():
                        if error["type"] == 'value_error.extra' and len(error["loc"]) == 1:
                            err_val["validation_error"][error["loc"][0]] = exc.body[error["loc"][0]]
                return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=err_val)
        else:
            err_val["validation_error"]["orders"].append(Id(id=0).dict())
            return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=err_val)
    elif request.url.path.endswith("/orders/assign") and request.method == "POST":
        return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST)
    elif request.url.path.endswith("/orders/complete") and request.method == "POST":
        return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST)
    else:
        return await request_validation_exception_handler(request, exc)
