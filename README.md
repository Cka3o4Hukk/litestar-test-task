# litestar-test-task

## env
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=testdb
DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/testdb
```


## Command

```
docker-compose up --build
```

```
curl -X POST http://localhost:8000/users -H "Content-Type: application/json; charset=utf-8" -d '{"name": "Alex", "surname": "Ivanov", 
"password": "secure123"}'
```