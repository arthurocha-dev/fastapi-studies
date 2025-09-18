from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey #coluna e tipos dos campos
from sqlalchemy.orm import declarative_base #estrutura da tabela
from sqlalchemy_utils.types import ChoiceType

#cria a conexão com o banco
db = create_engine("sqlite:///database/banco.db")


#cria a base do banco de dados
Base = declarative_base()


#criar as classes/tabela do banco (o sqlalchemy converte as classes python em tabelas sql)
class Usuario(Base): #herda a estrutura de tabela

    #nome da tabela
    __tablename__ = "usuarios"


    #campos
    idT = Column("id", Integer, primary_key = True, autoincrement = True)
    nameT = Column("nome", String)
    emailT = Column("email", String, nullable = False)
    telephoneT = Column("telefone", Integer)
    passwordT = Column("senha", String)
    activeT = Column("ativo", Boolean)
    admT = Column("administrador", Boolean)
    

    #parametros de quando for chamada a classe pra fazer o novo usuario(instância)
    def __init__ (self, name, email, password, telephone = "NÃO PASSADO", active =  True, adm=False):
        self.nameT = name
        self.emailT = email
        self.telephoneT = telephone
        self.passwordT = password
        self.activeT = active
        self.admT = adm




class Pedido(Base):
    __tablename__ = "pedidos"

    # Status_pedido = (
    #     # (chave, valor) chave: valor que vai ficar armazenado no bd, valor quando se quiser printar
    #     ("PENDENTE", "PENDENTE"),
    #     ("CANCELADO", "CANCELADO"),
    #     ("FINALIZADO", "FINALIZADO")
    # )

    idT = Column("id", Integer, primary_key = True, autoincrement = True)
    status = Column("status", String)
    user = Column("usuario", ForeignKey("usuarios.id"))
    price = Column("preco", Float)
    # itens = 

    def __init__(self, usuario, status="PENDENTE", preco=0):
        self.user = usuario
        self.status = status
        self.price = preco



class ItenPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column("id", Integer, autoincrement=True, primary_key=True)
    amount = Column("quantidade", Integer)
    flavor = Column("sabor", String)
    size = Column("tamanho", String)
    price_unitary = Column("preco_unitario", Float)
    request = Column("pedido", ForeignKey("pedidos.id"))

    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.amount = quantidade
        self.flavor = sabor
        self.size = tamanho
        self.price_unitary = preco_unitario
        self.request = pedido