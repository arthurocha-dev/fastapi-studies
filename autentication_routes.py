from fastapi import APIRouter
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


@auth_routerr.get("/cadastro")
async def cadastros():
    return {
        "mensagem": "Usuário cadastrado com suecesso!"
    }