import time
import random
import os
from datetime import datetime
import logging

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(BASE_DIR, "logs\\taximeter.log")

# Configuración del log
logging.basicConfig(filename=LOG_PATH, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
'''
logging.info("Programa iniciado")
logging.warning("Velocidad nula detectada")
logging.error("Error al leer entrada del usuario")
'''
#Cerrar y renombrar el log
def log_on_end():
  for handler in logging.root.handlers[:]:
    handler.close()
    logging.root.removeHandler(handler)

  timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
  new_log_path = os.path.join(BASE_DIR, "logs", f"{timestamp}.log")

  try:
    os.rename(LOG_PATH, new_log_path)
    print(f"Log renombrado correctamente a: {new_log_path}")
  except Exception as e:
    print(f"Error al renombrar el log: {e}")

#Función para confirmar con s o n
def confirm(question):
  while True:
    user_input = input(question + " (s/n): ")
    if user_input.lower() in ["si", "s"]:
      return True
    elif user_input.lower() in ["no", "n"]:
      return False
    else:
      print("Entrada inválida, escriba s/n.")
      continue

def txt(name, text):
  with open(os.path.join(BASE_DIR, name), "a", encoding='utf-8') as f:
    f.write(text)

def change_price():
  minimum = 0
  while True:
    try:
      valor = int(input("Ingresa el valor en \033[93mcéntimos\033[0m: "))
      if (minimum is not None and valor <= minimum):
        print(f"El valor debe ser mayor a {minimum}.")
        logging.info("Invalid price")
        continue
      return valor
    except ValueError:
      print("Por favor, ingresa un número entero válido.")

def ask_prices():
  try:
    global moving_price, stop_price
    logging.info("Options to change price")
    while True:
      print("\n1) Precio en parado")
      print("2) Precio en marcha")
      print("0) Cancelar cambio")
      price_option = input("Elige una opción (1, 2 o 0): ")
      if price_option == "1":
        logging.info("Stoped price selected")
        temp = change_price()
        stop_price = temp
        logging.info(f"Stoped price changed to: {temp} cents")
        print("Precio en parada cambiado a: " + str(temp))
        break
      elif price_option == "2":
        logging.info("Moving price selected")
        temp = change_price()
        moving_price = temp
        logging.info(f"Moving price changed to: {temp} cents")
        print("Precio en marcha cambiado a: " + str(temp))
        break
      elif price_option == "0":
        logging.info("Canceled changing prices")
        break
      else:
        logging.info("Invalid selection")
        print("Entrada inválida, escriba 1, 2 o 0.")
        continue
    
    if confirm("¿Quieres cambiar más precios?"):
      logging.info("Changing more prices")
      ask_prices()
    else:
      logging.info("Go to trip")
  except Exception:
    logging.error("Error on changing prices")
    log_on_end()
    quit()

def trip():
  try:
    global stop_count, moving_count, trip_bool, moving_price, stop_price
    print(f"\nCalcula \033[93m{stop_price}\033[0m céntimos por segundo en parada y \033[93m{moving_price}\033[0m céntimos por segundo en marcha.")
    if confirm("¿Quieres continuar con estos precios?"):
      logging.info("Confirmed prices")
    else:
      logging.info("Go to prices change")
      ask_prices()
    #Reiniciar variables por si se inicia otro viaje
    moving_count = 0
    stop_count = 0
    logging.info("Reset count variables")
    logging.info("Trip started")
    print("\nViaje iniciado\n" \
    "Presiona \033[93m'Ctrl+C'\033[0m para \033[93mterminar\033[0m el viaje\n" \
    "¡Disfruta del viaje!\n")
    
    while trip_bool:
      try:
        start = time.perf_counter()
        km_ph = random.choice([0, 30]) #Lo hice aleatorio para pruebas, pero se puede usar la librería gpsd para detectar movimiento
        if km_ph == 0:
          stop_count += 1
          logging.info(f"Stoped time: {stop_count}")
        else:
          moving_count += 1
          logging.info(f"Moving time: {moving_count}")
        duration = time.perf_counter() - start
        subtrac = 1.0 - duration
        logging.info("Calculated exact time to wait")
        time.sleep(max(0, subtrac))
      except KeyboardInterrupt:
        logging.info("Trip finished")
        on_end(subtrac)
        break

  except Exception:
    logging.error("Error on the trip")
    log_on_end()
    quit()

def on_end(subtrac):
  global stop_count, moving_count, trip_bool, moving_price, stop_price
  trip_bool = False
  print("Gracias por usar este sitema.\n" \
  "Calculando el precio de este viaje...")
  #Al ser while hay que restar la ultima duración al contador por el tipo de bucle
  if moving_count > 0:
    moving_count -= subtrac
  if stop_count > 0:
    stop_count -= subtrac
  logging.info("Subtracted leftover time")
  final_fare = round(((moving_count * moving_price) + (stop_count * stop_price)) / 100, 2)
  logging.info(f"Final fare in euros: {final_fare}")
  print(f"Tienes que pagar {final_fare}€")

  txt("trips.txt", f"Viaje terminado en fecha: {datetime.now()}\n" \
      f"Con {stop_price} céntimos por segundo en parada y {moving_price} céntimos por segundo en marcha.\n" \
      f"Este viaje a durado {moving_count + stop_count} segundos totales y se ha pagado {final_fare}€ por el mismo\n" \
      "Viaje finalizado, gracias\n\n" \
      "-----------------------------------------------------------------------------------------\n\n")
  logging.info("Trip registered in " + BASE_DIR + "\\trips.txt")

  if confirm("¿Quieres inciar otro trayecto?"):
    logging.info("Another trip started")
    trip_bool = True
    trip()
  else:
    print("¡Gracias por usar este sistema! Hasta pronto")
    logging.info("Program finised")
    log_on_end()
    quit()

if __name__ == "__main__":
  logging.info("Program started")
  #Definir variables globales
  stop_price = 2
  moving_price = 5
  moving_count = 0
  stop_count = 0
  trip_bool = True
  logging.info("Trip prices established")
  print("Bienvenide al taxímetro digital\n" \
  "Este sistema te ayuda a calcular el precio de los viajes en taxi")
  #keyboard.add_hotkey('ctrl+q', on_end)
  #keyboard.wait()
  trip()