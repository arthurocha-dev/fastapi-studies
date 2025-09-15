from fastapi import APIRouter


requested_routerr = APIRouter(prefix="/requested", tags=["requested"])


@requested_routerr.get("/requested_food")
async def requested():

    """Teste de mensagem"""

    return {
        "food1": "apple",
        "food2": "banana",
        "food3": "almoço do ltv",
        "pagou": False
           
    }