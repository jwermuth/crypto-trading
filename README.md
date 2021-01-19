# Whats this for

Algotrading on binance.

start database with 
```shell
docker-compose up -d
```

start django
```
cd binance_django
python3 manage.py runserver 
```
install postgres deps


python3 manage.py makemigrations
python3 manage.py migrate
