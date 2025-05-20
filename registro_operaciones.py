import csv
import os
from datetime import datetime

ARCHIVO_REGISTRO = "registro_operaciones.csv"

def registrar_operacion(par, tipo, precio_entrada, capital):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    precio_salida = precio_entrada * (1.05 if tipo == 'compra' else 0.95)
    capital_final = capital * (1.05 if tipo == 'compra' else 0.95)

    operacion = {
        'fecha': fecha,
        'par': par,
        'tipo': tipo,
        'precio_entrada': round(precio_entrada, 4),
        'precio_salida': round(precio_salida, 4),
        'capital_inicial': round(capital, 2),
        'capital_final': round(capital_final, 2)
    }

    archivo_existe = os.path.isfile(ARCHIVO_REGISTRO)
    with open(ARCHIVO_REGISTRO, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=operacion.keys())
        if not archivo_existe:
            writer.writeheader()
        writer.writerow(operacion)

    return f"🧾 Operación registrada\nEntrada: {operacion['precio_entrada']} → Salida: {operacion['precio_salida']}\nCapital Final: ${operacion['capital_final']}"
