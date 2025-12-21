# Importar librerias
#  -----------------------------------------------
try:
    import sys, logging, traceback, flask, pandas_ta as ta
    from tvDatafeed import TvDatafeed, Interval
except Exception as e:
    print(f"ERROR IMPORTANDO LIBRERIAS: {e}")
    sys.exit()
#  -----------------------------------------------
print("Librerias cargadas con éxito")
