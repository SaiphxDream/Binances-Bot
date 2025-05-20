import pandas as pd
from datetime import datetime

def generar_resumen_semanal(archivo_csv="registro_operaciones.csv"):
    try:
        df = pd.read_csv(archivo_csv, parse_dates=["fecha"])
        if df.empty:
            return "📭 No hay operaciones registradas aún."

        # Agrupar por semana
        df["semana"] = df["fecha"].dt.isocalendar().week
        resumen = df.groupby("semana").agg({
            "capital_inicial": "first",
            "capital_final": "last",
            "tipo": "count"
        }).rename(columns={"tipo": "operaciones"})

        texto = "📈 *Resumen Semanal de Operaciones*\n"
        for index, fila in resumen.iterrows():
            texto += f"\n🗓 Semana {index}:\n"
            texto += f"• Capital Inicial: ${fila['capital_inicial']:.2f}\n"
            texto += f"• Capital Final: ${fila['capital_final']:.2f}\n"
            texto += f"• Operaciones: {int(fila['operaciones'])}\n"

        return texto
    except Exception as e:
        return f"❌ Error al generar resumen: {e}"
