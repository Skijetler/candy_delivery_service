import uvicorn
import argparse
from fastapi import FastAPI, Depends
from configargparse import ArgumentParser

from candy_delivery.utils.argparse_u import positive_int
from candy_delivery.utils.db import DEFAULT_DB_URL
from candy_delivery.api.db_session import create_db_session
from candy_delivery.api.routers import couriers, orders


ENV_VAR_PREFIX = 'CANDY_DELIVERY_'

parser = ArgumentParser(
    auto_env_var_prefix=ENV_VAR_PREFIX,
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)


group = parser.add_argument_group('API Options')
group.add_argument('--address', default='0.0.0.0',
                   help='IPv4/IPv6 address API server would listen on')
group.add_argument('--port', type=positive_int, default=8081,
                   help='TCP port API server would listen on')

group = parser.add_argument_group('Database options')
group.add_argument('--db-url', type=str, default=str(DEFAULT_DB_URL),
                   help='URL to use to connect to the database')



def main():   
    args = parser.parse_args()

    Session = create_db_session(args.db_url)

    def get_db():
        db = Session()
        try:
            yield db
        finally:
            db.close()

    
    app = FastAPI()

    app.include_router(couriers.router,
                       prefix="/couriers",
                       tags=["courier"], 
                       dependencies=[Depends(get_db)])
    app.include_router(orders.router,
                       prefix="/orders",
                       tags=["order"], 
                       dependencies=[Depends(get_db)])

    uvicorn.run(app, host=args.address, port=args.port)


if __name__ == '__main__': 
    main()