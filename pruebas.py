# Importar librerias
#  -----------------------------------------------
try:
    import sys, logging, traceback, flask, pandas_ta as ta
    from tvDatafeed import TvDatafeed, Interval
except Exception as e:
    print(f"ERROR IMPORTANDO LIBRERIAS: {e}")
    sys.exit()
#  -----------------------------------------------

# Función para configurar_logging()
#  -----------------------------------------------
def configurar_logging(archivo: str = "app.log", debug: bool = False):
    try:
        # 1️⃣ Crea un logger
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG if debug else logging.INFO)
        logger.handlers.clear()


        # 2️⃣ Handler para escribir en archivo
        file_handler = logging.FileHandler(archivo, mode="w", encoding="utf-8")
        file_handler.setFormatter(logging.Formatter("[%(levelname)s]: %(message)s (%(asctime)s)", datefmt="%Y-%m-%d %H:%M:%S"))
        logger.addHandler(file_handler)

        # 3️⃣ Handler para imprimir en consola
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter("\n[%(levelname)s]: %(message)s (%(asctime)s)", datefmt="%Y-%m-%d %H:%M:%S"))
        logger.addHandler(console_handler)

        logger.info("Logging configurado correctamente")

        return logger
    except:
        print(f"\nERROR CONFIGURANDO LOGGING: {traceback.format_exc()}")
#  -----------------------------------------------

# Función para capturar errores no controlados (tracebacks)
#  -----------------------------------------------
def registrar_excepciones(exc_type, exc_value, exc_traceback):
    try:
        tb = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        logger.error(tb)
    except:
        logger.error(f"Error en registrar_excepciones() {traceback.format_exc()}")
#  -----------------------------------------------

# Enviar datos de EMAs 954 al GSheets
#  -----------------------------------------------
def main():

    # Definir una sesion para la API de Trading View:
    tv = TvDatafeed()
    
    while True:
        try:
            # Enviar cada minuto
            if datetime.datetime.now().second != 0:
                continue
            
            # Obtener el precio actual (RETRASADO 10 MINUTOS POT TV):
            precio_actual = tv.get_hist("GC1!", "COMEX", Interval.in_1_minute)['close'].iloc[-1]

            # Enviar precio actual
            logger.info(f"Enviando precio actual - {precio_actual} ...")
            url = "https://script.google.com/macros/s/AKfycbwgc5ERbXC-Vuoo0YHSUcmihDwlsxztNC9Tlsdy7snjesr2rvXOjD0wxwnmvnAY38YY/exec"
            enviar_datos(url, {"precio": precio_actual})
                
        except Exception as e:
            print(f"ERROR EN EL CICLO main() - {e}")
#  -----------------------------------------------


if __name__ == "__main__":

    # Capturar errores no manejados y configurar logger
    # -------------------------------------------------
    try:
        logger = configurar_logging()
        sys.excepthook = registrar_excepciones # Ejecutar registrar_excepciones() cada vez que ocurre un error no manejado 
    except:
        print(f"ERROR INICIAMDO LOGGER: {traceback.format_exc()}")
        sys.exit()
    # -----------------------------------------------

    # Ejecutar el programa principal
    # -----------------------------------------------
    main()
    # -----------------------------------------------
    print("Corrida exitosa")
