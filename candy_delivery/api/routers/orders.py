from fastapi import APIRouter
from fastapi.responses import ORJSONResponse
from fastapi_sqlalchemy import db

import candy_delivery.db.crud as crud
import candy_delivery.api.schema as schema


router = APIRouter()