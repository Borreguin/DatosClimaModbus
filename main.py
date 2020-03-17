# Python program to find current
# weather details of any city
# using openweathermap api
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import traceback
from logging.handlers import RotatingFileHandler
from typing import Any, Union
import requests
import pandas as pd
from ModbusClass import FloatModbusClient
import datetime as dt
import os

"""
Configuraciones generales del script
"""
# configuración de Excel
lb_index = "Identificador"
lb_city = "Ciudad"
lb_modbus_add = "Modbus_Add"
lb_modbus_ala ="Modbus_Ala"
lb_activa = "Activa"
excel_file = "config.xlsx"
script_path = os.path.dirname(os.path.abspath(__file__))
logger = None

# Configuración: Host equipo a conectar como Master, el host pregunta a este equipo por información
# c = FloatModbusClient(host='10.0.0.38', port=502, auto_open=True)
c = FloatModbusClient(host='10.0.0.38', port=502, auto_open=True)

# API del Open Wheather
api_key = "c2034400bbe0df1a97db8d4c6b567b83"

# base_url variable to store url
base_url = "http://api.openweathermap.org/data/2.5/weather?"


def get_info_from_api():

    df = pd.read_excel(excel_file)
    n_cities = 0
    for ix in df.index:
        city_name = df[lb_city].loc[ix]
        modbus_add = df[lb_modbus_add].loc[ix]
        modbus_alarm = df[lb_modbus_ala].loc[ix]
        complete_url = base_url + f"appid={api_key}&q={city_name}"

        response = requests.get(complete_url)
        resp_dict = response.json()
        print(f"\n[{dt.datetime.now()}] respuesta para ciudad [{city_name}]: {resp_dict}")
        if resp_dict["cod"] != "404":
            # filtrado de información:
            try:
                #main_content = resp_dict["main"]
                #current_temperature = main_content["temp"]
                #current_humidiy = main_content["humidity"]
                weather_dict = resp_dict["weather"]
                weather_description = weather_dict[0]["description"]
                weather_id = int(weather_dict[0]["id"])

                # procesamiento de los datos
                # Temperatura en grados Kelvin, transformación a grados centigrados
                #current_temperature = current_temperature - 273.15
                w_condition_alarm = (weather_id > 199 and weather_id < 300)

                # enviando por Modbus
               
                c.write_float(modbus_add, [weather_id])

                #c.write_float(modbus_add + 2, [current_humidiy])
                c.write_single_coil(modbus_alarm, w_condition_alarm)
                n_cities += 1
            except Exception as e:
                tb = traceback.format_exc()
                msg = tb + "\n" + str(e)
                print(msg)
                logger.error(msg)
        else:
            print("City Not Found")
    return f"[{dt.datetime.now()}] Obtención de datos correcto. " \
                     f"Se han obtenido datos de {n_cities} ciudades"

def init_logger():
    global logger
    # maxBytes to small number, in order to demonstrate the generation of multiple log files (backupCount).
    handler = RotatingFileHandler(os.path.join(script_path, 'logs', 'weather.log'), maxBytes=500000, backupCount=3)
    # getLogger(__name__):   decorators loggers to file + werkzeug loggers to stdout
    # getLogger('werkzeug'): decorators loggers to file + nothing to stdout
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)


if __name__ == '__main__':

    # iniciar el Log de la aplicacion:
    init_logger()
    # ejecutar proceso
    try:
        msg = get_info_from_api()
        print(msg)
        logger.info(msg)
    except Exception as e:
        tb = traceback.format_exc()
        msg = f"[{dt.datetime.now()}] No se pudo correr el proceso de manera normal \n" + str(e) + "\n" + str(tb)
        print(msg, "\n", tb)
        logger.error(msg)
