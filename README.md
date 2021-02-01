# the-backend [![Build Status](https://travis-ci.com/project-lolquiz/the-backend.svg?branch=main)](https://travis-ci.com/project-lolquiz/the-backend) [![codecov](https://codecov.io/gh/project-lolquiz/the-backend/branch/main/graph/badge.svg?token=3K61M4E0LR)](https://codecov.io/gh/project-lolquiz/the-backend) ![main-worklfow](https://github.com/project-lolquiz/the-backend/workflows/main-worklfow/badge.svg)
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
## Executando os testes de unidade da aplicação
```
> pytest -v
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
### Operações API users
```
/lolquiz/users/register (POST) curl -v -XPOST -H "Content-type: application/json" -d '{"uid":"4b8c2cfe-e0f1-4e8b-b289-97f4591e2069","nickname":"john-doe","avatar":{"type":"1","current":"10"}}' 'http://localhost:5000/lolquiz/users/register'
/lolquiz/users/<string:uid> (GET) curl -v -XGET -H "Content-type: application/json" 'http://localhost:5000/lolquiz/users/4b8c2cfe-e0f1-4e8b-b289-97f4591e2069'
/lolquiz/users/<string:uid> (PUT) curl -v -XPUT -H "Content-type: application/json" -d '{"nickname":"johndoey","avatar":{"type":"2","current":"11"}}' 'http://localhost:5000/lolquiz/users/4b8c2cfe-e0f1-4e8b-b289-97f4591e2069'
/lolquiz/users/<string:uid>/avatar (PUT) curl -v -XPUT -H "Content-type: application/json" -d '{"type":"3","current":"11"}' 'http://localhost:5000/lolquiz/users/4b8c2cfe-e0f1-4e8b-b289-97f4591e2069/avatar'
```
### Operações API games
```
/lolquiz/games/types (GET) curl -v -XGET -H "Content-type: application/json" 'http://localhost:5000/lolquiz/games/types'
/lolquiz/games/modes (GET) curl -v -XGET -H "Content-type: application/json" 'http://localhost:5000/lolquiz/games/modes'
```
### Swagger API
```
/apidocs/
```
### Endereço no Heroku
```
https://lolquizbe.herokuapp.com/
```