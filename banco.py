from sqlalchemy import (
    Column, Integer, String, Float, Boolean, ForeignKey, create_engine, Table
)
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

Base = declarative_base()


pedido_produto = Table(
    'pedido_produto',
    Base.metadata,
    Column('pedido_id', Integer, ForeignKey('pedidos.id')),
    Column('produto_id', Integer, ForeignKey('produtos.id'))
)


class Restaurante(Base):
    __tablename__ = 'restaurantes'
    id = Column(Integer, primary_key=True)
    categoria = Column(String, nullable=False)
    nome = Column(String, nullable=False)

    produtos = relationship("Produto", back_populates="restaurante")

    def __repr__(self):
        return f"<Restaurante(nome='{self.nome}', categoria='{self.categoria}')>"



class Produto(Base):
    __tablename__ = 'produtos'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    restaurante_id = Column(Integer, ForeignKey('restaurantes.id'))

    restaurante = relationship("Restaurante", back_populates="produtos")
    pedidos = relationship("Pedido", secondary=pedido_produto, back_populates="produtos")

    def __repr__(self):
        return f"<Produto(nome='{self.nome}', preco={self.preco})>"



class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, nullable=False, unique=True)
    telefone = Column(String, nullable=False)
    clube = Column(Boolean, default=False)

    pedidos = relationship("Pedido", back_populates="cliente")

    def __repr__(self):
        return f"<Cliente(nome='{self.nome}', clube={self.clube})>"



class Funcionario(Base):
    __tablename__ = 'funcionarios'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, nullable=False, unique=True)
    telefone = Column(String, nullable=False)
    cargo = Column(String, nullable=False)
    salario = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Funcionario(nome='{self.nome}', cargo='{self.cargo}')>"



class Pagamento(Base):
    __tablename__ = 'pagamentos'
    id = Column(Integer, primary_key=True)
    tipo = Column(String, nullable=False)  
    valor_total = Column(Float, nullable=False)

    pedido = relationship("Pedido", back_populates="pagamento")

    def __repr__(self):
        return f"<Pagamento(tipo='{self.tipo}', valor_total={self.valor_total})>"



class Pedido(Base):
    __tablename__ = 'pedidos'
    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    restaurante_id = Column(Integer, ForeignKey('restaurantes.id'))
    pagamento_id = Column(Integer, ForeignKey('pagamentos.id'))

    cliente = relationship("Cliente", back_populates="pedidos")
    restaurante = relationship("Restaurante")
    produtos = relationship("Produto", secondary=pedido_produto, back_populates="pedidos")
    pagamento = relationship("Pagamento", back_populates="pedido", uselist=False)

    def __repr__(self):
        return f"<Pedido(id={self.id}, cliente={self.cliente.nome})>"



def criar_banco(url_banco='sqlite:///restaurante.db'):
    engine = create_engine(url_banco, echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()
