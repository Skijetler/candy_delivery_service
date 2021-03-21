import uvicorn
import argparse
import os
from sys import argv
from configargparse import ArgumentParser
from setproctitle import setproctitle

from candy_delivery.utils.argparse_u import positive_int, clear_environ
from candy_delivery.utils.db import DEFAULT_DB_URL
from candy_delivery.api.app import create_app

# перфикс для переменных окружения
ENV_VAR_PREFIX = 'CANDY_DELIVERY_'

# парсер параметров программы
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

    # выводит в списке процессов название программы
    setproctitle(os.path.basename(argv[0]))

    # очистка переменных окружения
    clear_environ(lambda i: i.startswith(ENV_VAR_PREFIX))

    app = create_app(args.db_url)
    uvicorn.run(app, host=args.address, port=args.port)


if __name__ == '__main__': 
    main()