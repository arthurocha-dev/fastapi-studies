from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from depedencies import pegar_sessao
from schemas import PedidosSchema
from database import model

requested_routerr = APIRouter(prefix="/requested", tags=["requested"])


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