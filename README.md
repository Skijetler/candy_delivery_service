Вступительное задание в Школу бэкенд-разработки Яндекса в 2021 году - REST-API сервис, написанный на Python с помощью фреймворка FastAPI.

Как развернуть проект?
--------
Приложение работает через Docker-контейнер и разворачивается с помощью Ansible.

Перед тем как разворачивать приложение через Ansible, необходимо собрать Docker-контейнер с приложением и упаковать его в `tar` архив, а полученный архив поместить в папку `deploy`
```bash
python setup.py sdist
sudo docker build -t skijetler/candy_delivery_service:1.1 .
cd ./deploy
docker save -o ./candy_delivery_service_image.tar skijetler/candy_delivery_service:1.1
```
Когда образ собран, можно задеплоить его на сервер
```bash
export ANSIBLE_MAX_DIFF_SIZE=104857600; ansible-playbook -c paramiko -i hosts.ini --user=root deploy.yaml
```
По-умолчанию сервис будет доступен на порту `8080`

Как работать с Docker-контейнером?
--------
Внутри Docker-контейнера доступны две команды: `candy_delivery-db` — утилита для управления состоянием базы данных и `candy_delivery-api` — утилита для запуска REST API сервиса.

Как применить миграции:
```bash
docker run -it \
  -e CANDY_DELIVERY_DB_URL=postgresql://candy_man:2fkI2Rd39C@localhost/candy_service \
  skijetler/candy_delivery_service:1.1 candy_delivery-db upgrade head
```
Как запустить REST API сервис локально на порту 8081:
```bash
docker run -it -p 8081:8081 \
    -e CANDY_DELIVERY_DB_URL=postgresql://candy_man:2fkI2Rd39C@localhost/candy_service \
    -e CANDY_DELIVERY_PORT=8081 \
    skijetler/candy_delivery_service:1.1
```
Все доступные опции запуска любой команды можно получить с помощью аргумента `--help`:
```bash
docker run skijetler/candy_delivery_service:1.1 candy_delivery-db --help
docker run skijetler/candy_delivery_service:1.1 candy_delivery-api --help
```
Опции для запуска можно указывать как аргументами командной строки, так и переменными окружения с префиксом CANDY_DELIVERY (например: вместо аргумента --db-url можно воспользоваться CANDY_DELIVERY_DB_URL).

Как запустить тесты локально?
--------
Для начала нужно поднять postgres на порту `5432` и добавить пользователся `candy_man` с паролем `2fkI2Rd39C`
```bash
python3 -m venv venv
source venv/bin/activate
pip install -e '.[dev]'
pytest tests
```
