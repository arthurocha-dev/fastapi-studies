from fastapi import FastAPI

app = FastAPI()

#para rodar nossa aplicação, executar no terminal: uvicorn main:app --reload

#uvicorn: criar um servidor usando uvicorn
# main: nome do arquivo
# app: nome da variavel que esta instanciando a classe FastAPI
# --reload pra ficar atualizando automaticamente as alterações



# importante ressaltar que vc importa as rotas depois de ter criado a aplicação,
# pq as rotas dependem da aplicação já ter sido criada, funciona de maneira sequencial

from autentication_routes import auth_routerr
from requested_routes import requested_routerr


# agora temos que incluir essas rotas importadas,
# elas foram importadas mas não esavam sendo usadas
app.include_router(auth_routerr)
app.include_router(requested_routerr)