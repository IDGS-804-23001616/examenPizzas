from flask import flash, redirect, render_template, request, session, url_for

from forms import ClienteForm, PizzaForm, QuitarDetalleForm
from models import Cliente, DetallePedido, Pedido, Pizza, db
from . import pedidos_bp

PRECIOS_TAMANO = {
    "chica": 90,
    "mediana": 130,
    "grande": 170,
}

@pedidos_bp.route("/", methods=["GET", "POST"])
@pedidos_bp.route("/nuevo", methods=["GET", "POST"])
def nuevo_pedido():
    cliente_form = ClienteForm(request.form)
    pizza_form = PizzaForm(request.form)
    quitar_form = QuitarDetalleForm(request.form)

    detalles_temp = session.get("detalles_temp", [])

    if request.method == "POST":
        accion = request.form.get("accion", "")

        if accion == "agregar":
            if pizza_form.validate():
                precio_unitario = PRECIOS_TAMANO[pizza_form.tamano.data]
                cantidad = pizza_form.cantidad.data
                subtotal = precio_unitario * cantidad

                detalles_temp.append(
                    {
                        "tamano": pizza_form.tamano.data,
                        "ingredientes": pizza_form.ingredientes.data,
                        "cantidad": cantidad,
                        "precio_unitario": precio_unitario,
                        "subtotal": subtotal,
                    }
                )
                session["detalles_temp"] = detalles_temp
                flash("Pizza agregada al detalle temporal.", "success")
                return redirect(url_for("pedidos.nuevo_pedido"))

            flash("Revisa los datos de la pizza para poder agregar.", "error")

        elif accion == "quitar":
            if quitar_form.validate():
                indice = int(quitar_form.indice.data)
                if 0 <= indice < len(detalles_temp):
                    detalles_temp.pop(indice)
                    session["detalles_temp"] = detalles_temp
                    flash("Elemento eliminado del detalle.", "success")
                else:
                    flash("No se encontro el elemento a eliminar.", "error")
            else:
                flash("No se pudo eliminar el elemento seleccionado.", "error")

            return redirect(url_for("pedidos.nuevo_pedido"))

        elif accion == "terminar":
            if not detalles_temp:
                flash("Primero agrega al menos una pizza al detalle.", "error")
                return redirect(url_for("pedidos.nuevo_pedido"))

            if cliente_form.validate():
                cliente = Cliente(
                    nombre_completo=cliente_form.nombre_completo.data,
                    direccion=cliente_form.direccion.data,
                    telefono=cliente_form.telefono.data,
                )
                db.session.add(cliente)
                db.session.flush()

                pedido = Pedido(
                    cliente_id=cliente.id,
                    fecha_pedido=cliente_form.fecha_pedido.data,
                    total=0,
                )
                db.session.add(pedido)
                db.session.flush()

                total = 0
                for item in detalles_temp:
                    pizza = Pizza.query.filter_by(
                        tamano=item["tamano"],
                        ingredientes=item["ingredientes"],
                        precio_unitario=item["precio_unitario"],
                    ).first()

                    if not pizza:
                        pizza = Pizza(
                            tamano=item["tamano"],
                            ingredientes=item["ingredientes"],
                            precio_unitario=item["precio_unitario"],
                        )
                        db.session.add(pizza)
                        db.session.flush()

                    detalle = DetallePedido(
                        pedido_id=pedido.id,
                        pizza_id=pizza.id,
                        cantidad=item["cantidad"],
                        subtotal=item["subtotal"],
                    )
                    db.session.add(detalle)
                    total += item["subtotal"]

                pedido.total = total
                db.session.commit()

                session.pop("detalles_temp", None)
                flash(f"Pedido guardado correctamente. Total: ${total:.2f}", "success")
                return redirect(url_for("pedidos.nuevo_pedido"))

            flash("Revisa los datos del cliente y fecha para terminar el pedido.", "error")

    total_temporal = sum(item["subtotal"] for item in detalles_temp)
    return render_template(
        "pedidos/nuevo.html",
        cliente_form=cliente_form,
        pizza_form=pizza_form,
        quitar_form=quitar_form,
        detalles_temp=detalles_temp,
        total_temporal=total_temporal,
    )
