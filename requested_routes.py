from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from depedencies import pegar_sessao


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
async def create_request(session: Session = Depends(pegar_sessao)):
    return 