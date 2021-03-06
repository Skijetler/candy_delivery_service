############### Образ для сборки виртуального окружения ################
# Основа - "тяжелый" (~1GB, в сжатом виде ~500M) образ со всеми необходимыми
# библиотеками для сборки модулей
FROM snakepacker/python:all as builder

# Создаем виртуальное окружение и обновляем pip
RUN python3.9 -m venv /usr/share/python3/candy_delivery_venv
RUN /usr/share/python3/candy_delivery_venv/bin/pip install -U pip

# Устанавливаем зависимости отдельно чтобы закешировать, при последующей сборке
# Docker пропустит этот шаг если requirements.txt не изменится
COPY requirements.txt /mnt/
RUN /usr/share/python3/candy_delivery_venv/bin/pip install -Ur /mnt/requirements.txt

# Копируем source distribution в контейнер и устанавливаем его
COPY dist/ /mnt/dist/
RUN /usr/share/python3/candy_delivery_venv/bin/pip install /mnt/dist/* \
    && /usr/share/python3/candy_delivery_venv/bin/pip check

########################### Финальный образ ############################
# За основу берем "легкий" (~100M, в сжатом виде ~50M) образ с python
FROM snakepacker/python:3.9 as api

# Копируем в него готовое виртуальное окружение из контейнера builder
COPY --from=builder /usr/share/python3/candy_delivery_venv /usr/share/python3/candy_delivery_venv

# Устанавливаем ссылки, чтобы можно было воспользоваться командами приложения
RUN ln -snf /usr/share/python3/candy_delivery_venv/bin/candy_delivery-* /usr/local/bin/

# Автоматически запускаем сервис при запуске контейнера
CMD ["candy_delivery-api"]