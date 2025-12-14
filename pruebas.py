# Importar librerias
#  -----------------------------------------------
try:
    import sys, logging, traceback, requests, datetime, flask
    from tvDatafeed import TvDatafeed, Interval
except Exception as e:
    print(f"ERROR IMPORTANDO LIBRERIAS: {e}")
    input("ENTER PARA SALIR")
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

if __name__ == "__main__":

    # Capturar errores no manejados y configurar logger
    # -------------------------------------------------
    try:
        logger = configurar_logging()
        sys.excepthook = registrar_excepciones # Ejecutar registrar_excepciones() cada vez que ocurre un error no manejado 
    except:
        print(f"ERROR INICIAMDO LOGGER: {traceback.format_exc()}")
        input("ENTER PARA SALIR")
        sys.exit()
    # -----------------------------------------------
    
    # Definir sesion de tvDatafeed
    # -------------------------------------------------
    try:
        tv = TvDatafeed()
        logger.info("Sesión de tvDatafeed iniciada correctamente")
    except Exception as e:
        logger.error(f"ERROR INICIANDO SESION DE TVDATAFEED: {e}")
        input("ENTER PARA SALIR")
        sys.exit()
    # -------------------------------------------------
    
    # Flask app
    # -------------------------------------------------
    app = flask.Flask(__name__)
    @app.route("/")
    def index():
        try:
            df = tv.get_hist(symbol="GC1!", exchange="COMEX", interval=Interval.in_1_minute)
            csv = df.to_csv(index=True)
            json_data = df.to_json(orient="records")
            print(csv)
            return csv
        except Exception as e:
            logger.error(f"ERROR EN INDEX(): {e}")
            return flask.Response("ERROR INTERNO DEL SERVIDOR", status=500)
    app.run(host="0.0.0.0", port=5000, debug=True)
    # -------------------------------------------------

# Evitar cierre del terminal 
# -----------------------------------------------
input("ENTER PARA SALIR")
# -----------------------------------------------