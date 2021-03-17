from fastapi import Request, status
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.responses import ORJSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from candy_delivery.api.schema import (Id,
                                       CouriersPostValidationErrorResponse, 
                                       CourierPostRequest,
                                       CouriersPostResponse,
                                       OrdersPostValidationErrorResponse,
                                       OrderPostRequest,
                                       OrdersPostResponse)


async def RequestValidationHandler(request: Request, exc: RequestValidationError):
    if "/couriers" in request.url.path and request.method == "POST":
        err_val = CouriersPostValidationErrorResponse(validation_error=CouriersPostResponse(couriers=[]))
        if type(exc.body) == dict: # а массив ли нам передали
            if 'data' in exc.body.keys(): # есть ли ключ data
                for item in exc.body['data']:
                    try:
                        CourierPostRequest(**item)
                    except ValidationError:
                        if 'courier_id' in item.keys(): # есть ли ключ courier_id
                            if type(item["courier_id"]) != int: # проверка типа ключа
                                err_val.validation_error.couriers.append(Id(id=0))
                            else:
                                err_val.validation_error.couriers.append(Id(id=item["courier_id"]))
                        else:
                            err_val.validation_error.couriers.append(Id(id=0))
                            return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=err_val.dict())
                return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=err_val.dict())
            else:
                err_val.validation_error.couriers.append(Id(id=0))
                return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=err_val.dict())
        else:
            err_val.validation_error.couriers.append(Id(id=0))
            return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=err_val.dict())
    elif "/couriers/" in request.url.path and request.method == "GET":
        return ORJSONResponse(status_code=status.HTTP_404_NOT_FOUND)
    elif "/couriers/" in request.url.path and request.method == "PATCH":
        return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST)
    elif request.url.path.endswith("/orders") and request.method == "POST":
        err_val = OrdersPostValidationErrorResponse(validation_error=OrdersPostResponse(orders=[]))
        if type(exc.body) == dict: # а массив ли нам передали
            if 'data' in exc.body.keys(): # есть ли ключ data
                for item in exc.body['data']:
                    try:
                        OrderPostRequest(**item)
                    except ValidationError:
                        if 'order_id' in item.keys(): # есть ли ключ order_id
                            if type(item["order_id"]) != int: # проверка типа ключа
                                err_val.validation_error.orders.append(Id(id=0))
                            else:
                                err_val.validation_error.orders.append(Id(id=item["order_id"]))
                        else:
                            err_val.validation_error.orders.append(Id(id=0))
                            return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=err_val.dict())
                return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=err_val.dict())
            else:
                err_val.validation_error.orders.append(Id(id=0))
                return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=err_val.dict())
        else:
            err_val.validation_error.orders.append(Id(id=0))
            return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=err_val.dict())
    elif request.url.path.endswith("/orders/assign") and request.method == "POST":
        return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST)
    elif request.url.path.endswith("/orders/complete") and request.method == "POST":
        return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST)
    else:
        return await request_validation_exception_handler(request, exc)
