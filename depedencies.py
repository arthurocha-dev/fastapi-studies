from database import model
from sqlalchemy.orm import sessionmaker

# Dependency que será usada pelo FastAPI para entregar uma sessão de banco
def pegar_sessao():
    try:
        # 1. Cria uma "fábrica de sessões".
        #    Isso NÃO conecta ainda, apenas cria uma receita que sabe abrir sessões ligadas ao 'model.db' (Engine).
        Session = sessionmaker(bind=model.db)

        # 2. Agora sim, abre uma sessão real a partir da fábrica.
        #    Aqui o SQLAlchemy pega uma conexão do pool do Engine e associa à sessão.
        session = Session()

        # 3. Entrega essa sessão para a rota que chamou.
        #    O 'yield' serve como "ponto de pausa":
        #    enquanto a rota roda, a sessão está ativa e pode ser usada em queries.
        yield session

    finally:
        # 4. Quando a rota terminar (seja com sucesso ou erro),
        #    esse bloco roda garantindo que a sessão seja fechada
        #    e a conexão devolvida ao pool.
        session.close()
