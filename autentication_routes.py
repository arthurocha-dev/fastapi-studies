from fastapi import APIRouter, Depends, HTTPException
from database import model
from depedencies import pegar_sessao # função que devolve a sessão do banco
from main import bycrypt_context
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from sqlalchemy import and_

# a aplicacao vai ser organizada por exemplo: "dominiosite/auth/cadastro"


#variável que é responsável por uma caixa organizadora
# Dentro dele você coloca várias rotas (@get, @post, etc).
# Ele por si só não é uma rota, é só o agrupador.

# prefix: é usado pra organizar a rota que tem a sua funcionalidade,
# por exemplo, pode ser = "/auth/cadastro" (vai fazer o cadastro)
#                         "/auth/login" (vai fazer o login)


# Já as tags não têm nenhum efeito técnico na URL ou no roteamento.

# Elas servem somente pra documentação automática (/docs e /redoc).

# É só um "rótulo" que aparece no Swagger UI pra você não se perder.

# 👉 Então:

# O router organiza de forma prática no código e nas URLs reais.

# A tag organiza de forma visual e descritiva na doc.
auth_routerr = APIRouter(prefix="/auth", tags=["auth"])





def usuario_login(email, senha, session):
    usario_cadastrado = session.query(model.Usuario).filter(email == model.Usuario.emailT).first()
    
    if not usario_cadastrado:
        return False

    elif not bycrypt_context.verify(senha, usario_cadastrado.passwordT):
        return False
    
    return usario_cadastrado




# 👉 Esse é o decorator:
@auth_routerr.get("/teste")

# Ele diz ao FastAPI: “essa função abaixo é o que deve ser executado quando alguém fizer uma requisição GET para /requested/requested_food”.
# O caminho "/requested_food" se junta ao prefixo lá de cima, formando /requested/requested_food











# 👉 Essa é a função handler.
async def teste():

# async def = função assíncrona.

# Ela é chamada quando a rota é acessada.

# O async significa que essa função pode pausar em pontos estratégicos (quando usar await dentro dela) e liberar o servidor pra cuidar de outras requisições nesse meio tempo.

# ⚡ Diferença prática:

# Se fosse def requested(), o FastAPI executaria de forma bloqueante → enquanto essa função não terminasse, o servidor estaria ocupado.

# Com async def, o servidor pode “pular” pra outra tarefa enquanto espera (exemplo: chamar banco de dados, API externa, leitura de arquivo demorado).

# Ou seja: não é que ele roda tudo ao mesmo tempo, mas ele consegue intercalar tarefas.
# É tipo:
# “Enquanto esse cara espera a resposta do banco de dados, vou atender outro usuário aqui rapidão.”
   



   
#👉 Esse docstring aparece na documentação Swagger como descrição da rota.
    '''teste teste de mensagem'''
   
   
   
   
#👉 O que a função retorna.
    return {
        "mensagem": "teste de response"
    }

# No FastAPI, se você retorna um dicionário Python, ele vira JSON automaticamente na resposta HTTP.

# A resposta do cliente vai ser: "teste de mensagem"










# Define uma rota POST em /auth/create_user
# Ela recebe: nome, email, senha e uma sessão de banco (injeção via Depends)
@auth_routerr.post("/create_user")
async def create_user(usuario:UsuarioSchema, session: Session = Depends(pegar_sessao)):

       # 1. Verifica se já existe um usuário com esse email
    usuario_existe = session.query(model.Usuario).filter(model.Usuario.emailT == usuario.email).first()

    if usuario_existe:
        #se o usuário existir
        raise HTTPException(status_code=400, detail= f"Usuário { {usuario.nome} } já existe ")
        #raise levanta um erro, ao invés de return que retorna um response de positivo(200)
    
    else:

        senha_cryptografada = bycrypt_context.hash(usuario.senha) # esse hash é uma função gerador de código, ou seja, ele vai gerar um códig em cima da senha que o usuário criou

        # Se não existir:
        # cria um novo objeto Usuario com os dados recebidos
        novo_usuario = model.Usuario(usuario.nome, usuario.email, senha_cryptografada, usuario.telefone, usuario.active, usuario.admin)

        # adiciona esse novo usuário à sessão (ainda não gravou no banco)
        session.add(novo_usuario)

         # confirma a transação, salvando no banco de dados de fato
        session.commit()

        #retorna mensagem de sucesso
        return {"Mensagem": f"usuário { {usuario.nome} } criado com sucesso"}
    




@auth_routerr.post('/login')
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    
    user = usuario_login(login_schema.email_login, login_schema.senha_login, session)

    if user:
        return {'mensagem': f'usuario { {login_schema.email_login} } logado'}
    
    if not user:
        # return {"Mensagem": f"{ {login_schema.email_login} } logado"}
        raise HTTPException(status_code=400, detail= f"usuário { {login_schema.email_login} } não foi cadastrado ou credencias inválidas")
       
  