-- Script SQL de apoyo 

CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_completo VARCHAR(120) NOT NULL,
    direccion VARCHAR(200) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    created_at DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS pizzas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tamano VARCHAR(20) NOT NULL,
    ingredientes VARCHAR(200) NOT NULL,
    precio_unitario FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    fecha_pedido DATE NOT NULL,
    total FLOAT NOT NULL,
    created_at DATETIME NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

CREATE TABLE IF NOT EXISTS detalle_pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pedido_id INTEGER NOT NULL,
    pizza_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    subtotal FLOAT NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
    FOREIGN KEY (pizza_id) REFERENCES pizzas(id)
);
