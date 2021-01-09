# the-backend
Projeto backend com integrações com redis + postgres

## Iniciando o ambiente
```
> python3 -m venv venv (somente para o caso de não existir um virtual environment)
> . ./run.sh
```
O comando **. ./run.sh** irá:
- Inicializar o docker-compose 
- Definir as variáveis de ambiente local
- Executar as migrações na base de dados
- Ativar o virtual environment
- Instalar as dependências
- Iniciar a aplicação

## Desativando o ambiente
```
> CTRL + C (para interromper o shell)
> deactivate (para desativar o virtual environment)
```
## Atualizando as dependências do projeto
```
> python -m pip install <DEPENDENCIA>[==VERSION]
> python -m pip freeze > requirements.txt
```
## Iniciando/desativando serviços externos através do docker-compose
```
> docker-compose up | down
```
## Definindo variáveis de ambiente (para execução em ambiente local)
```
> export REDIS_PASSWORD=<VALOR>
```
## Rotas
### Para exemplos
```
http://localhost:5000/
http://localhost:5000/ping
```
### Operações com Redis
```
/lolquiz/redis-add (POST) curl -v -XPOST -H "Content-type: application/json" -d '{"key": 2, "value": "A new value", "expires_in": 25}' 'http://localhost:5000/lolquiz/redis-add'
/lolquiz/redis-get-by-key/<string:key> (GET) 
/lolquiz/redis-get-all (GET)
/lolquiz/redis-delete-all (DELETE) curl -XDELETE -H "Content-type: application/json" 'http://localhost:5000/lolquiz/redis-delete-all'
/lolquiz/redis-delete-by-key/<string:key> (DELETE) curl -XDELETE -H "Content-type: application/json" 'http://localhost:5000/lolquiz/redis-delete-by-key/version'
```
### Operações com base de dados
```
/lolquiz/db-add (POST) curl -v -XPOST -H "Content-type: application/json" -d '{"value": "A new content"}' 'http://localhost:5000/lolquiz/db-add'
/lolquiz/db-get-by-id/<int:by_id> (GET)
/lolquiz/db-get-all (GET)
```