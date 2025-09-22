from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from dotenv import load_dotenv #importação pra pegar a variável de ambiente
import os #pega arquivos do projeto 

load_dotenv() #carrega as variáveis de ambiente

SECRET_KEY = os.getenv('SECRET_KEY_V') #pega a variável de ambiente com esse nome
ALGORITHM = os.getenv('ALGORITHM_V')
ACESS_TOKEN_EXIPIRE_MINUTES = int(os.getenv('ACESS_TOKEN_EXIPIRE_MINUTES_V'))

app = FastAPI()

#depois de ter criado a aplicação

#Crie um contexto que use o algoritmo bcrypt para hash de senhas. Se no futuro eu adicionar outro algoritmo, o Passlib vai cuidar da compatibilidade e migração automática.
bycrypt_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")



# Declara um "schema" OAuth2 que diz: "espero receber o token via header Authorization: Bearer <token>"
# tokenUrl é usado PELO SWAGGER/CLIENTE para saber onde o cliente pede o token (rota de login).
# Importante: isso NÃO faz validação automática do token — só ajuda o FastAPI a extrair o token do header.
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/form-authorization")






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