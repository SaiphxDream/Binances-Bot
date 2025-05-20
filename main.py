import time
from datetime import datetime, timedelta
from capital_control import obtener_capital_total, determinar_fase
from analisis_tecnico import seleccionar_mejor_par, generar_senal
from registro_operaciones import registrar_operacion
from notificador import enviar_mensaje

def ejecutar_bot(ultima_operacion):
    capital = obtener_capital_total()
    fase = determinar_fase(capital)

    mejor_par, datos = seleccionar_mejor_par()
    if not mejor_par:
        enviar_mensaje("❌ No se encontró un par adecuado.")
        return ultima_operacion

    senal, info = generar_senal(datos, fase)
    if senal in ['compra', 'venta']:
        resultado = registrar_operacion(mejor_par, senal, info['precio'], capital)
        enviar_mensaje(f"✅ Operación realizada:\nPar: {mejor_par}\nAcción: {senal}\n{resultado}")
        return datetime.now()  # Actualizamos hora de última operación
    else:
        enviar_mensaje("⏸️ No se detectó señal clara.")
        return ultima_operacion  # No hubo operación, no actualizamos

if __name__ == "__main__":
    enviar_mensaje("🚀 Bot iniciado manualmente.")

    ultima_operacion = datetime.now()

    while True:
        ultima_operacion = ejecutar_bot(ultima_operacion)

        # Verificar si han pasado más de 24 horas sin operación
        if datetime.now() - ultima_operacion > timedelta(hours=24):
            enviar_mensaje("⏰ Han pasado más de 24 horas sin ninguna operación.")

            # Para no enviar mensajes repetidos cada ciclo, actualizamos ultima_operacion aquí también
            ultima_operacion = datetime.now()

        time.sleep(300)  # espera 5 minutos antes de la siguiente ejecución
