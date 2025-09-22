from fastapi import Depends, HTTPException
from main import SECRET_KEY, ALGORITHM, oauth2_schema
from database import model
from jose import jwt, JWTError
from sqlalchemy.orm import sessionmaker, Session

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




def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    """
    Explicação passo-a-passo (mapeando com o que você entendeu):
    - Passo1: oauth2_schema faz o trabalho de *pegar* o token do header Authorization.
             Aqui, o parâmetro `token` já vem **somente** com a string do JWT (ex: "eyJhbGci..."),
             sem o prefixo "Bearer".
    - Passo2: essa função usa o token pra validar (decodificar) e transformar em id de usuário.
    - Passo3: se o token for válido, a função retorna o usuário do DB; caso contrário, levanta 401.
    """

    # --- AQUI: o token já veio do header, via oauth2_schema ---
    # Exemplo de header original que o cliente manda:
    # Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6...
    # oauth2_schema extrai só o "eyJhbGci..." e passa pra esse parâmetro `token`.

    try:
        # Decodifica o JWT (verifica assinatura, validade, etc).
        # Use `algorithms=[ALGORITHM]` (lista) — é o jeito correto com python-jose.
        dic_info = jwt.decode(token, SECRET_KEY, algorithms= "HS256")

        # Pegamos a claim "sub" (subject) que foi colocada no token quando ele foi criado.
        # Por convenção costumamos colocar o id do usuário em "sub".
        id_usuario = int(dic_info.get("sub"))

        # OBS: se o token expirou, ou assinatura inválida, o jwt.decode vai lançar uma exceção
        # e cair no except abaixo.
    except JWTError:
        # Se qualquer problema na validação do token → negar o acesso.
        # Isso cobre token inválido, token adulterado, token expirado (dependendo da lib).
        raise HTTPException(status_code=401, detail="Acesso negado, verifique validade do token")

    # --- A seguir, garantimos que o usuário indicado pelo token realmente existe no banco ---
    usuario = session.query(model.Usuario).filter(model.Usuario.idT == id_usuario).first()
    if not usuario:
        # Mesmo com token válido, se o id não existir no DB, negamos o acesso.
        raise HTTPException(status_code=401, detail="Acesso negado")

    # Se chegou até aqui: token válido e usuário existe -> retornamos o objeto usuário.
    # Esse objeto será injetado nas rotas que fizerem Depends(verificar_token).
    return usuario













# ============================
# Extras / Observações finais
# ============================
# - O server (FastAPI) NÃO guarda o token em memória ou "histórico".
#   O token é *stateless*: ele contém as informações assinado criptograficamente.
#   Quem guarda o token é o CLIENTE (navegador/app/etc).
#
# - O botão "Authorize" do Swagger (docs) só faz 2 coisas:
#   1) te permite colar o token uma vez,
#   2) então o Swagger adiciona automaticamente o header Authorization: Bearer <token>
#      em todas as requisições feitas dentro do UI. Nada é salvo no servidor.
#
# - Onde o cliente guarda o token (no mundo real):
#   * Access token (curta duração) -> idealmente em memória do app (não em localStorage),
#     porque localStorage é vulnerável a XSS. Em SPAs às vezes guardam em memória + renovaçao via refresh.
#   * Refresh token (longa duração) -> idealmente em cookie HttpOnly + Secure (não acessível via JS),
#     assim o XSS não rouba o refresh token. O cookie é enviado automaticamente pelo browser.
#
# - Como o cliente envia o token depois:
#   Em cada requisição a rota protegida, o cliente adiciona o header:
#     Authorization: Bearer <access_token>
#   O OAuth2PasswordBearer espera esse header e te entrega só a parte do token (string).
#
# - Sobre distinguir tokens:
#   Para uma implementação segura, ao gerar tokens você pode:
#     - adicionar claim "type": "access" ou "refresh"
#     - usar tempos diferentes ("exp")
#     - armazenar refresh tokens no DB (para poder invalidar / revogar)
#
# - Dependências (Depends) são chamadas POR REQUISIÇÃO. Elas não "guardam" o token entre requisições.
#   Cada nova request segue o mesmo processo (cliente envia header -> FastAPI extrai -> chama verificar_token).
#
# -------------------------
# Exemplo minimal de como o cliente usa o token (JS):
# -------------------------
# // supondo que o cliente recebeu { access_token, refresh_token } do login
# // e guardou accessToken numa variável em memória:
# fetch("/api/protegida", {
#   method: "GET",
#   headers: {
#     "Authorization": "Bearer " + accessToken
#   }
# })
#
# Se o accessToken expirar, o cliente chama /auth/refresh (mandando o refresh token
# no cookie ou no header, dependendo da sua arquitetura) e troca pelo novo access token.