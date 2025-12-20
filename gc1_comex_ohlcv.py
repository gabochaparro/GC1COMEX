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
    
    # Definir sesion de tvDatafeed
    # -------------------------------------------------
    try:
        tv = TvDatafeed()
        logger.info("Sesión de tvDatafeed iniciada correctamente")
    except Exception as e:
        logger.error(f"ERROR INICIANDO SESION DE TVDATAFEED: {e}")
        sys.exit()
    # -------------------------------------------------
    
    # Flask app
    # -------------------------------------------------
    app = flask.Flask(__name__)
    @app.route("/")
    def index():
        try:
            return "API de datos OHLCV de GC1! en COMEX. Rutas disponibles: /ohlcv_1m, /ohlcv_4h, /ohlcv_d, /ohlcv_w"
        except Exception as e:
            logger.error(f"ERROR EN INDEX(): {e}")
            return flask.Response("ERROR INTERNO DEL SERVIDOR", status=500)

    @app.route("/ohlcv_1m")
    def ohlcv_1m():
        try:
            df = tv.get_hist(symbol="GC1!", exchange="COMEX", interval=Interval.in_1_minute)
            csv = df.to_csv(index=True)
            #print(csv)
            return csv
        except Exception as e:
            logger.error(f"ERROR EN ohlcv_1m(): {e}")
            return flask.Response("ERROR INTERNO DEL SERVIDOR", status=500)
        
    @app.route("/ohlcv_1h")
    def ohlcv_1h():
        try:
            df = tv.get_hist(symbol="GC1!", exchange="COMEX", interval=Interval.in_1_hour, n_bars=99)
            csv = df.to_csv(index=True)
            #print(csv)
            return csv
        except Exception as e:
            logger.error(f"ERROR EN ohlcv_1h(): {e}")
            return flask.Response("ERROR INTERNO DEL SERVIDOR", status=500)
        
    @app.route("/ohlcv_4h")
    def ohlcv_4h():
        try:
            df = tv.get_hist(symbol="GC1!", exchange="COMEX", interval=Interval.in_4_hour, n_bars=99)
            csv = df.to_csv(index=True)
            #print(csv)
            return csv
        except Exception as e:
            logger.error(f"ERROR EN ohlcv_4h(): {e}")
            return flask.Response("ERROR INTERNO DEL SERVIDOR", status=500)
        
    @app.route("/ohlcv_d")
    def ohlcv_d():
        try:
            df = tv.get_hist(symbol="GC1!", exchange="COMEX", interval=Interval.in_daily, n_bars=99)
            csv = df.to_csv(index=True)
            #print(csv)
            return csv
        except Exception as e:
            logger.error(f"ERROR EN ohlcv_d(): {e}")
            return flask.Response("ERROR INTERNO DEL SERVIDOR", status=500)
        
    @app.route("/ohlcv_w")
    def ohlcv_w():
        try:
            df = tv.get_hist(symbol="GC1!", exchange="COMEX", interval=Interval.in_weekly, n_bars=99)
            csv = df.to_csv(index=True)
            #print(csv)
            return csv
        except Exception as e:
            logger.error(f"ERROR EN ohlcv_w(): {e}")
            return flask.Response("ERROR INTERNO DEL SERVIDOR", status=500)
        
    @app.route("/emas954_w")
    def emas954_w():
        try:
            df = tv.get_hist(symbol="GC1!", exchange="COMEX", interval=Interval.in_weekly, n_bars=5000)
            df_ema9 = ta.ema(df["close"], length=9)
            df_ema54 = ta.ema(df["close"], length=54)
            df["ema"] = df_ema9
            df["ema54"] = df_ema54
            csv = df.tail().to_csv(index=True)
            #print(csv)
            return csv
        except Exception as e:
            logger.error(f"ERROR EN emas954_w(): {e}")
            return flask.Response("ERROR INTERNO DEL SERVIDOR", status=500)
        
    @app.route("/emas954_d")
    def emas954_d():
        try:
            df = tv.get_hist(symbol="GC1!", exchange="COMEX", interval=Interval.in_daily, n_bars=5000)
            df_ema9 = ta.ema(df["close"], length=9)
            df_ema54 = ta.ema(df["close"], length=54)
            df["ema"] = df_ema9
            df["ema54"] = df_ema54
            csv = df.tail().to_csv(index=True)
            #print(csv)
            return csv
        except Exception as e:
            logger.error(f"ERROR EN emas954_d(): {e}")
            return flask.Response("ERROR INTERNO DEL SERVIDOR", status=500)
        
    @app.route("/emas954_4h")
    def emas954_4h():
        try:
            df = tv.get_hist(symbol="GC1!", exchange="COMEX", interval=Interval.in_4_hour, n_bars=5000)
            df_ema9 = ta.ema(df["close"], length=9)
            df_ema54 = ta.ema(df["close"], length=54)
            df["ema"] = df_ema9
            df["ema54"] = df_ema54
            csv = df.tail().to_csv(index=True)
            #print(csv)
            return csv
        except Exception as e:
            logger.error(f"ERROR EN emas954_4h(): {e}")
            return flask.Response("ERROR INTERNO DEL SERVIDOR", status=500)

    @app.route("/emas954_1h")
    def emas954_1h():
        try:
            df = tv.get_hist(symbol="GC1!", exchange="COMEX", interval=Interval.in_1_hour, n_bars=5000)
            df_ema9 = ta.ema(df["close"], length=9)
            df_ema54 = ta.ema(df["close"], length=54)
            df["ema"] = df_ema9
            df["ema54"] = df_ema54
            csv = df.tail().to_csv(index=True)
            #print(csv)
            return csv
        except Exception as e:
            logger.error(f"ERROR EN emas954_w(): {e}")
            return flask.Response("ERROR INTERNO DEL SERVIDOR", status=500)

    app.run(host="0.0.0.0", port=8000, debug=False)
    # -------------------------------------------------
