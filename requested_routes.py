from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from depedencies import pegar_sessao, verificar_token
from schemas import PedidosSchema
from database import model

requested_routerr = APIRouter(prefix="/requested", tags=["pedidos"], dependencies = [Depends(verificar_token)])

@requested_routerr.get("/teste")
async def requested():

    """Teste de mensagem"""

    return {
        "food1": "apple",
        "food2": "banana",
        "food3": "almoço do ltv",
        "pagou": False
           
    }


@requested_routerr.post("/create_pedidos")
async def create_request(pedido_Schema: PedidosSchema, session: Session = Depends(pegar_sessao)):
    """passe um id de um pedido"""
    pedido = model.Pedido(pedido_Schema.id_pedido) 
    session.add(pedido)
    session.commit()
    return {"mensagem": f"pedido { {pedido_Schema.id_pedido} } feito"}      



@requested_routerr.post('/request/cancel/{id_pedido}')
async def cancel_request(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: model.Usuario = Depends(verificar_token)):
    pedido = session.query(model.Pedido).filter(model.Pedido.idT == id_pedido).first()

    if not pedido:
        raise HTTPException(status_code=400, detail=f"Pedido {id_pedido} não encontrado")
    
    if not usuario.admT and usuario.idT != pedido.user:
        raise HTTPException(status_code=401, detail= "Você não tem acesso pra fazer modificação")
    
    pedido.status = "CANCELADO"
    session.commit()
    return{
        "mensagem": f"pedido {id_pedido} foi cancelado",
        "pedido": pedido
    }



@requested_routerr.get("/list_request")
async def listar(
    session: Session = Depends(pegar_sessao),

    
#  🧠 Passo a passo do que acontece nos bastidores

# O FastAPI vê o Depends(verificar_token) e entende:
# 👉 “Antes de chamar essa rota, eu preciso executar a função verificar_token().”

# A função verificar_token() é chamada automaticamente.

# Ela provavelmente extrai o token JWT do header Authorization.

# Decodifica esse token pra descobrir o id do usuário.

# Vai no banco com esse id e faz algo como:

# user = session.query(model.Usuario).filter(model.Usuario.idT == user_id).first()
# return user


# O valor retornado por verificar_token() é injetado no parâmetro usuario.

# Ou seja: usuario agora é uma instância do teu modelo Usuario carregada direto do banco.

# Tu pode acessar tudo: usuario.idT, usuario.nome, usuario.admT, etc.
    usuario: model.Usuario = Depends(verificar_token)):
    if not usuario.admT:
        raise HTTPException(status_code=401, detail="Você não tem alturização pra fazer essa requisição")
    else:
        pedido = session.query(model.Pedido).all()

    return {
        "pedidos": pedido
    }
