from flask import render_template, request
from sqlalchemy import func
from models import DetallePedido, Pedido
from . import reportes_bp

DIAS_SEMANA = {
    "1": "Domingo",
    "2": "Lunes",
    "3": "Martes",
    "4": "Miercoles",
    "5": "Jueves",
    "6": "Viernes",
    "7": "Sabado",
}

MESES = {
    "1": "Enero",
    "2": "Febrero",
    "3": "Marzo",
    "4": "Abril",
    "5": "Mayo",
    "6": "Junio",
    "7": "Julio",
    "8": "Agosto",
    "9": "Septiembre",
    "10": "Octubre",
    "11": "Noviembre",
    "12": "Diciembre",
}


@reportes_bp.route("/ventas-dia")
def ventas_por_dia():
    resumen_raw = (
        Pedido.query.with_entities(
            func.dayofweek(Pedido.fecha_pedido).label("dia_num"),
            func.count(Pedido.id).label("total_pedidos"),
            func.sum(Pedido.total).label("total_ventas"),
        )
        .group_by(func.dayofweek(Pedido.fecha_pedido))
        .order_by(func.dayofweek(Pedido.fecha_pedido))
        .all()
    )

    resumen = [
        {
            "dia_num": str(row.dia_num),
            "dia": DIAS_SEMANA.get(str(row.dia_num), "Desconocido"),
            "total_pedidos": row.total_pedidos,
            "total_ventas": float(row.total_ventas or 0),
        }
        for row in resumen_raw
    ]

    dia_filtro = request.args.get("dia", "").strip()
    pedidos_filtrados = []

    if dia_filtro in DIAS_SEMANA:
        pedidos_filtrados = (
            Pedido.query.filter(func.dayofweek(Pedido.fecha_pedido) == int(dia_filtro))
            .order_by(Pedido.fecha_pedido.desc(), Pedido.id.desc())
            .all()
        )

    return render_template(
        "reportes/ventas_dia.html",
        resumen=resumen,
        dias_semana=DIAS_SEMANA,
        dia_filtro=dia_filtro,
        pedidos_filtrados=pedidos_filtrados,
    )


@reportes_bp.route("/ventas-mes")
def ventas_por_mes():
    resumen_raw = (
        Pedido.query.with_entities(
            func.month(Pedido.fecha_pedido).label("mes_num"),
            func.count(Pedido.id).label("total_pedidos"),
            func.sum(Pedido.total).label("total_ventas"),
        )
        .group_by(func.month(Pedido.fecha_pedido))
        .order_by(func.month(Pedido.fecha_pedido))
        .all()
    )

    resumen = [
        {
            "mes_num": str(row.mes_num),
            "mes": MESES.get(str(row.mes_num), "Desconocido"),
            "total_pedidos": row.total_pedidos,
            "total_ventas": float(row.total_ventas or 0),
        }
        for row in resumen_raw
    ]

    mes_filtro = request.args.get("mes", "").strip()
    pedidos_filtrados = []

    if mes_filtro in MESES:
        pedidos_filtrados = (
            Pedido.query.filter(func.month(Pedido.fecha_pedido) == int(mes_filtro))
            .order_by(Pedido.fecha_pedido.desc(), Pedido.id.desc())
            .all()
        )

    return render_template(
        "reportes/ventas_mes.html",
        resumen=resumen,
        meses=MESES,
        mes_filtro=mes_filtro,
        pedidos_filtrados=pedidos_filtrados,
    )


@reportes_bp.route("/detalle-venta/<int:pedido_id>")
def detalle_venta(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    detalles = (
        DetallePedido.query.filter_by(pedido_id=pedido_id)
        .order_by(DetallePedido.id.asc())
        .all()
    )

    return render_template(
        "reportes/detalle_venta.html",
        pedido=pedido,
        detalles=detalles,
    )