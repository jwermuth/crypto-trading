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

```shell
python3 manage.py makemigrations
python3 manage.py migrate
```

If you want to connect the the database, use
```shell
psql -h localhost -p 5432 -U postgres
```

## Running tests
```shell
source WHEREEVER YOUR BINANCE TEST CREDENTIALS ARE
python3 manage.py test main
```
