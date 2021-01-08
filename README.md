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

