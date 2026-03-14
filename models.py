from datetime import datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)
    nombre_completo = db.Column(db.String(120), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    pedidos = db.relationship("Pedido", back_populates="cliente", cascade="all, delete-orphan")


class Pizza(db.Model):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    tamano = db.Column(db.String(20), nullable=False)
    ingredientes = db.Column(db.String(200), nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)

    detalles = db.relationship("DetallePedido", back_populates="pizza")


class Pedido(db.Model):
    __tablename__ = "pedidos"

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)
    fecha_pedido = db.Column(db.Date, nullable=False)
    total = db.Column(db.Float, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    cliente = db.relationship("Cliente", back_populates="pedidos")
    detalles = db.relationship("DetallePedido", back_populates="pedido", cascade="all, delete-orphan")


class DetallePedido(db.Model):
    __tablename__ = "detalle_pedidos"

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedidos.id"), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey("pizzas.id"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    pedido = db.relationship("Pedido", back_populates="detalles")
    pizza = db.relationship("Pizza", back_populates="detalles")
