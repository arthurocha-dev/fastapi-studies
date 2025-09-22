from fastapi import APIRouter, Depends, HTTPException
from database import model
from depedencies import verificar_token, pegar_sessao # função que devolve a sessão do banco
from main import bycrypt_context, ALGORITHM, ACESS_TOKEN_EXIPIRE_MINUTES, SECRET_KEY
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone

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
auth_routerr = APIRouter(prefix="/auth", tags=["autenticação"])


def create_token(id_user,duration_token= timedelta(minutes=ACESS_TOKEN_EXIPIRE_MINUTES) ):
    #timezone.utc(fuso horário da linha central de greniwch)  timedelta(variacao de tempo)
    data_expiracao = datetime.now(timezone.utc) + duration_token

    #dicionário com as informações do usuário oara gerar o token, as chaves tem que ser 'sub' e 'exp', se nao a codificao do jwt não vai entender
    dic_info = {"sub": str(id_user), "exp": data_expiracao}

    #pra gerar o token, vc precisa usar a função jwt.encode(dicionario com as informações do usuario, a chave secreta que vai esconder as infromações nesse texto, e o tipo de algoritimo)
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)

    return jwt_codificado




def usuario_login(email, senha, session):
    usario_cadastrado = session.query(model.Usuario).filter(model.Usuario.emailT == email).first()
    
    if not usario_cadastrado:
        return False

    elif not bycrypt_context.verify(senha, usario_cadastrado.passwordT):
        return False
    # Se no banco a senha tá salva em texto plano (ex: "12345"), o verify vai quebrar, tem que ser uma senha já codificada pra verificar com a senha tamabem codificada que o bycrypt vai gerar .
    
    return usario_cadastrado


def usuario_login_authorize(name, senha, session):
    usario_cadastrado = session.query(model.Usuario).filter(model.Usuario.nameT == name).first()
    
    if not usario_cadastrado:
        return False

    elif not bycrypt_context.verify(senha, usario_cadastrado.passwordT):
        return False
    # Se no banco a senha tá salva em texto plano (ex: "12345"), o verify vai quebrar, tem que ser uma senha já codificada pra verificar com a senha tamabem codificada que o bycrypt vai gerar .
    
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
        acess_token = create_token(user.idT)
        refresh_token = create_token(user.idT, timedelta(days=7) )

        return {
            "acess_token": acess_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"        # Mas por que tem que informar token_type?      
                                          # O cliente (frontend, app, outro serviço) precisa saber como usar o token quando for mandar requisições futuras.
                                          # O tipo mais comum é Bearer, que significa literalmente: “se você tem o token, você pode usá-lo”. 
        }   
    
    if not user:
        # return {"Mensagem": f"{ {login_schema.email_login} } logado"}
        raise HTTPException(status_code=400, detail= f"usuário { {login_schema.email_login} } não foi cadastrado ou credencias inválidas")
    





#formulario de atalho pra vc inserir o token e as rotas onde pedem o token automaticamente serem liberadas
@auth_routerr.post('/form-authorization')
async def login(dados_form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    user = usuario_login_authorize(dados_form.username, dados_form.password, session)

    if user:
        acess_token = create_token(user.idT)

        return {
            "acess_token": acess_token,
            "token_type": "Bearer"        
        }   
    
    if not user:
        # return {"Mensagem": f"{ {login_schema.email_login} } logado"}
        raise HTTPException(status_code=400, detail= f"usuário { {dados_form.username} } não foi cadastrado ou credencias inválidas")
    

  

@auth_routerr.get("/refresh")
async def use_refresh_token(usuario: model.Usuario = Depends(verificar_token)):
    """
    O que acontece aqui:
    - Quando alguém chama GET /auth/refresh, o FastAPI automaticamente:
       1) pega o header Authorization (se existir),
       2) passa o token para oauth2_schema, que entrega só a string do JWT,
       3) chama verificar_token(token=..., session=...) — que decodifica e retorna `usuario`.
    - Se verificar_token levantar HTTPException(401), a rota NUNCA roda.
    - Se verificar_token retornar um usuário, a variável `usuario` já é esse modelo do DB
      e você pode criar um novo access token pra ele.
    """

    # >>> Atenção importante de segurança:
    # No seu código atual, qualquer token válido (seja access ou refresh) permite chamar /refresh.
    # Boa prática: distinguir **refresh tokens** de **access tokens**.
    #   - ao criar o refresh token, adicionar uma claim: {"sub": id, "type": "refresh", ...}
    #   - então aqui verificar dic_info.get("type") == "refresh"
    # Ou: armazenar refresh tokens no DB (mais seguro), e validar contra o DB.
    #
    # Sem essa distinção, um access token roubado poderia ser usado para gerar novos access tokens.
    access_token = create_token(usuario.idT)
    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }
