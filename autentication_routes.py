from fastapi import APIRouter, Depends
from database import model
from dependencies import pegar_session


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








# 👉 Esse é o decorator:
@auth_routerr.get("teste")
# Ele diz ao FastAPI: “essa função abaixo é o que deve ser executado quando alguém fizer uma requisição GET para /requested/requested_food”.
# O caminho "/requested_food" se junta ao prefixo lá de cima, formando /requested/requested_food











# 👉 Essa é a função handler.
async def cadastros():

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

# A resposta do cliente vai ser: "mensagem": "teste de response"







@auth_routerr.post("/cadastro")
async def create_user(email: str, senha: str, nome: str, session = Depends(pegar_session)):
    existe_usuario = session.query(model.Usuario).filter(model.Usuario.emailT==email).first()

    if existe_usuario:
        #já existe um usuário com esse email
        return {"Mensagem": "já existe um usuário com esse email"}
    
    else:
        novo_usuario = model.Usuario(nome, email, senha)
        session.add(novo_usuario)
        session.commit()
        return {"Mensagem": "usuário cadastrado com sucesso"}
