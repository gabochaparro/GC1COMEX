# Importar librerias
#  -----------------------------------------------
try:
    import talib, sys, logging, traceback, requests, datetime, asyncio, time
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

# Función EMAs 954
#  -----------------------------------------------
async def emas954(tv:TvDatafeed=TvDatafeed(), intervalo:Interval=Interval.in_1_minute, vela:int=1) -> str:
    try:
        print(f"Obteniendo historial en {intervalo}")
        await asyncio.sleep(0.099)
        ohlc_df_1m = tv.get_hist(symbol="GC1!", exchange="COMEX", interval=intervalo, n_bars=5000)
        #print(ohlc_df_1m)

        ema9 = talib.EMA(ohlc_df_1m["close"], timeperiod=9).iloc[-1]
        ema9_anterior = talib.EMA(ohlc_df_1m["close"], timeperiod=9).iloc[-2]
        ema54 = talib.EMA(ohlc_df_1m["close"], timeperiod=54).iloc[-1]
        ema54_anterior = talib.EMA(ohlc_df_1m["close"], timeperiod=54).iloc[-2]
        if ema9 > ema54 and ema9_anterior > ema54_anterior:
            return "BUY"
        if ema9 < ema54 and ema9_anterior < ema54_anterior:
            return "SELL"
        return ""
    except Exception as e:
        logger.error(f"ERROR EN emas954({intervalo}) - {e}")
        return ""
#  -----------------------------------------------

# Función para enviar info a una GSheets
#  -----------------------------------------------
def enviar_datos(url, emas954_1m, emas954_5m, emas954_15m, emas954_1h, emas954_4h, emas954_d, emas954_w):
    try:
        params = {"activo": "GC1!", 
                "ema954_1m": emas954_1m, 
                "ema954_5m": emas954_5m, 
                "ema954_15m": emas954_15m, 
                "ema954_1h": emas954_1h,
                "ema954_4h": emas954_4h,
                "ema954_1d": emas954_d,
                "ema954_w": emas954_w}
        r = requests.get(url=url, params=params)
        if r.status_code == 200:
            logger.info(r.text)
            #logger.info(f"EMA954_1m: {emas954_1m}, EMA954_5m: {emas954_5m}, EMA954_15m: {emas954_15m}, EMA954_1h: {emas954_1h}, EMA954_4h: {emas954_4h}, EMA954_D: {emas954_d}, EMA954_w: {emas954_w}")
        else:
            logger.error(f"ERROR ENVINDO DATOS DE GC1! AL GSHEETS. STATUS CODE: {r.status_code}" )
    except Exception as e:
        logger.error("ERROR EN enviar_datos()")
#  -----------------------------------------------

# Enviar datos de EMAs 954 al GSheets
#  -----------------------------------------------
async def main():

    # Definir una sesion para la API de Trading View
    tv = TvDatafeed()

    # Variables iniciales
    emas954_1m = ""
    emas954_5m = ""
    emas954_15m = ""
    emas954_1h = ""
    emas954_4h = ""
    emas954_d = ""
    emas954_w = ""
    
    try:
        ti = datetime.datetime.now()
        resultados = await asyncio.gather(emas954(tv, Interval.in_1_minute, 1), 
                                        emas954(tv, Interval.in_5_minute, 1), 
                                        emas954(tv, Interval.in_15_minute, 1), 
                                        emas954(tv, Interval.in_1_hour, 1), 
                                        emas954(tv, Interval.in_4_hour, 1), 
                                        emas954(tv, Interval.in_daily, 1), 
                                        emas954(tv, Interval.in_weekly, 1))

        emas954_1m_actual, emas954_5m_actual, emas954_15m_actual, \
        emas954_1h_actual, emas954_4h_actual, emas954_d_actual, \
        emas954_w_actual = resultados
        print(datetime.datetime.now()-ti, f"- ({datetime.datetime.now()})")
        
        # Enviar solo si hay cambios
        if (emas954_1m != emas954_1m_actual and emas954_1m_actual != "" or 
            emas954_5m != emas954_5m_actual and emas954_5m_actual != "" or 
            emas954_15m != emas954_15m_actual and emas954_15m_actual != "" or 
            emas954_1h != emas954_1h_actual and emas954_1h_actual != "" or 
            emas954_4h != emas954_4h_actual and emas954_4h_actual != "" or 
            emas954_d != emas954_d_actual and emas954_d_actual != "" or 
            emas954_w != emas954_w_actual and emas954_w_actual != ""):

            emas954_1m = emas954_1m_actual if emas954_1m_actual != "" else emas954_1m
            emas954_5m = emas954_5m_actual if emas954_5m_actual != "" else emas954_5m
            emas954_15m = emas954_15m_actual if emas954_15m_actual != "" else emas954_15m
            emas954_1h = emas954_1h_actual if emas954_1h_actual != "" else emas954_1h
            emas954_4h = emas954_4h_actual if emas954_4h_actual != "" else emas954_4h
            emas954_d = emas954_d_actual if emas954_d_actual != "" else emas954_d
            emas954_w = emas954_w_actual if emas954_w_actual != "" else emas954_w
            
            url_enviar_datos="https://script.google.com/macros/s/AKfycbx4tSmQ5UrUOa-mwRonzfHWms8jjEBjy0RTFoesA-wZshTztxjKMjs348DhQYOvTKCHGw/exec"
            enviar_datos(url_enviar_datos, emas954_1m, emas954_5m, emas954_15m, emas954_1h, emas954_4h, emas954_d, emas954_w)

    except Exception as e:
        logger.error(f"ERROR EN EL CICLO main() - {e}")
#  -----------------------------------------------

if __name__ == "__main__":
    
    # Capturar errores no manejados y configurar logger
    # -------------------------------------------------
    try:
        log = "ema954_gc1_cme.log"
        logger = configurar_logging(log)
        sys.excepthook = registrar_excepciones # Ejecutar registrar_excepciones() cada vez que ocurre un error no manejado 
    except:
        print(f"ERROR INICIAMDO LOGGER: {traceback.format_exc()}")
        input("ENTER PARA SALIR")
        sys.exit()
    # -----------------------------------------------
    
    # Ejecutar el programa principal
    # -----------------------------------------------
    asyncio.run(main())
    # -----------------------------------------------
