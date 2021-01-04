# the-backend
Projeto backend com integrações com redis + postgres

## Iniciando o ambiente
```
> python3 -m venv venv (somente para o caso de não existir um virtual environment)
> source env/bin/activate
> pip install -r requirements.txt
> python app.py | flask run --host=0.0.0.0 --port=3000
```
## Desativando o ambiente
```
> source env/bin/deactivate
```
## Atualizando as dependências do projeto
```
> python -m pip install <DEPENDENCIA>[==VERSION]
> python -m pip freeze > requirements.txt
```
