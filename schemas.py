from pydantic import BaseModel
from typing import Optional

# =========================
# Definindo um Schema com Pydantic
# =========================
class UsuarioSchema(BaseModel):
    # -------------------------
    # Campos obrigatórios
    # -------------------------
    nome: str       # Nome do usuário → obrigatório na requisição
    email: str      # Email → obrigatório
    senha: str      # Senha → obrigatório

    # -------------------------
    # Campos opcionais
    # -------------------------
    telefone: Optional[int]   # Telefone → opcional, pode não ser enviado pelo cliente
    active: Optional[bool]    # Usuário ativo → opcional, padrão definido no model se não enviado
    admin: Optional[bool]     # Administrador → opcional, padrão definido no model se não enviado

    # =========================
    # Configurações extras do schema
    # =========================
    class Config:
        # Permite criar o schema diretamente a partir de objetos Python (como instâncias do SQLAlchemy)
        # Exemplo: UsuarioSchema.from_orm(usuario_model)
        # Útil para rotas GET, onde você quer retornar JSON a partir de um objeto do banco
        from_attributes = True
        # ⚠️ Atenção: se você usar o mesmo schema de entrada para saída, campos sensíveis como senha vão aparecer no JSON, o que geralmente não é desejado.
        # Boa prática: criar um schema de saída separado (UsuarioOutSchema) sem o campo senha para rotas GET.





class PedidosSchema(BaseModel):
    id_pedido: int

    class Config:
        from_attribute = True





class LoginSchema(BaseModel):
    email_login: str
    senha_login: str

    class Config:
        from_attribute = True