# Тестовое задание

## Архитектура решения

Для реализации межсервисного взаимодействия была выбрана модель pub-sub. Основной обмен происходит на уровне HTTP запросов к callback url. Для реализации эффективного оповещения всех sub была реализована асинхронная работа запросов. 

В момент, когда сервер line-provider обрабатывает создание/обновление события, в очередь добавляется задача на выполнение оповещения. Далее line-provider-worker выполняет запросы ко всем sub's. Таким образом основной сервис line-provider не нагружен обработкой рассылки нового состояния.

![bet-services drawio](https://github.com/user-attachments/assets/f1cc442a-c242-439c-a4ca-8a3afae53463)

## Технологии

- Python
  - FastAPI
  - SQLAlchemy
  - Alembic
  - PyTests
- PostgreSQL
- Redis
- Docker
- docker-compose

## Запуск 

1. Переменные окружения
   
   Необходимо определить перменные окрежения в файлах `.env` по шаблону `.env.example` в каждом проекте
2. Запуск

   Для запуска необходимо выполнить команду `docker-compose up -d`

3. Настройка callback url

  Для настройки callback url необходимо открыть API Swagger сервиса line-provider по стандартному адресу `/docs`. Перейти к `[POST] api/v1/subscribers/` и ввести необходимый callback url.
  
  При запуске через docker-compose необходимым base_url для callback url является `http://bet-maker-app:{PORT}` а `path` `/api/v1/events/external/update`
