import time
import random
import os
from datetime import datetime
import logging

class Taximeter:
  def __init__(self, stop_price=2, moving_price=5):
    self.stop_price = stop_price
    self.moving_price = moving_price
    self.moving_count = 0
    self.stop_count = 0
    self.trip_active = True
    self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    self.DATA = os.path.join(self.BASE_DIR, "data")
    os.makedirs(self.DATA, exist_ok=True)
    self.LOG_DIR = os.path.join(self.BASE_DIR, "logs")
    os.makedirs(self.LOG_DIR, exist_ok=True)
    self.LOG_PATH = os.path.join(self.LOG_DIR, "taximeter.log")

    self.logger = logging.getLogger("taximeter")
    self.logger.setLevel(logging.INFO)

    # Evita añadir múltiples handlers si ya existen
    if not self.logger.handlers:
      handler = logging.FileHandler(self.LOG_PATH, encoding='utf-8')
      formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
      handler.setFormatter(formatter)
      self.logger.addHandler(handler)
    
  def confirm(self, question):
    while True:
      user_input = input(question + " (s/n): ")
      if user_input.lower() in ["si", "s"]:
        return True
      elif user_input.lower() in ["no", "n"]:
        return False
      else:
        print("Entrada inválida, escriba s/n.")

  def change_price(self):
    while True:
      try:
        valor = int(input("Ingresa el valor en \033[93mcéntimos\033[0m: "))
        if valor <= 0:
          print("El valor debe ser mayor que 0.")
          self.logger.info("Invalid price")
          continue
        return valor
      except ValueError:
        print("Por favor, ingresa un número entero válido.")

  def ask_prices(self):
    try:
      while True:
        self.logger.info("Options to change price")
        print("\n1) Precio en parado")
        print("2) Precio en marcha")
        print("0) Cancelar cambio")
        option = input("Elige una opción (1, 2 o 0): ")
        if option == "1":
          self.logger.info("Stoped price selected")
          self.stop_price = self.change_price()
          print(f"Precio en parada cambiado a: {self.stop_price}")
          self.logger.info(f"Stop price changed to {self.stop_price}")
          break
        elif option == "2":
          self.logger.info("Moving price selected")
          self.moving_price = self.change_price()
          print(f"Precio en marcha cambiado a: {self.moving_price}")
          self.logger.info(f"Moving price changed to {self.moving_price}")
          break
        elif option == "0":
          self.logger.info("Cancelled price change")
          return
        else:
          self.logger.info("Invalid selection")
          print("Entrada inválida, escribe 1, 2 o 0.")

      if self.confirm("¿Quieres cambiar más precios?"):
        self.logger.info("Changing more prices")
        self.ask_prices()
      else:
        self.logger.info("Go to trip")
    except Exception as e:
      self.logger.error(f"Error al cambiar precios: {e}")
      self.log_on_end()
      quit()

  def log_on_end(self):
    handlers = self.logger.handlers[:]
    for handler in handlers:
      handler.close()
      self.logger.removeHandler(handler)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    new_log_path = os.path.join(self.LOG_DIR, f"{timestamp}.log")

    try:
      os.rename(self.LOG_PATH, new_log_path)
      print(f"Log renombrado correctamente a: {new_log_path}")
    except Exception as e:
      print(f"Error al renombrar el log: {e}")

  def on_end(self, subtrac):
    self.trip_active = False
    print("Gracias por usar este sistema.\nCalculando el precio del viaje...")

    if self.moving_count > 0:
      self.moving_count -= subtrac
    if self.stop_count > 0:
      self.stop_count -= subtrac
    self.logger.info("Subtracted leftover time")

    total = ((self.moving_count * self.moving_price) + (self.stop_count * self.stop_price)) / 100
    total = round(total, 2)
    self.logger.info(f"Total trip price in euros: {total}")

    print(f"Tienes que pagar {total}€")

    with open(os.path.join(self.DATA, "txt_log.txt"), "a", encoding='utf-8') as f:
      f.write(f"Viaje terminado en: {datetime.now()}\n" \
      f"Parada: {self.stop_price} cents/s, Marcha: {self.moving_price} cents/s\n" \
      f"Duración: {self.moving_count + self.stop_count} s - Total: {total}€\n\n" \
      "------------------------------------------------------------\n")

    if self.confirm("¿Quieres iniciar otro trayecto?"):
      self.logger.info("Another trip started")
      self.trip_active = True
      self.start_trip()
    else:
      print("¡Gracias por usar este sistema! Hasta pronto.")
      self.logger.info("Program finished")
      self.log_on_end()
      quit()

  def start_trip(self):
    try:
      print(f"\nCalcula \033[93m{self.stop_price}\033[0m céntimos por segundo en parada y \033[93m{self.moving_price}\033[0m en marcha.")
      if not self.confirm("¿Quieres continuar con estos precios?"):
        self.logger.info("Go to prices change")
        self.ask_prices()
      else:
        self.logger.info("Confirmed prices")

      #Reiniciar variables por si se inicia otro viaje
      self.moving_count = 0
      self.stop_count = 0
      self.logger.info("Reset count variables")
      self.logger.info("Trip started")
      print("\nViaje iniciado\nPresiona \033[93m'Ctrl+C'\033[0m para \033[93mterminar\033[0m el viaje\n¡Buen viaje!\n")

      while self.trip_active:
        try:
          start = time.perf_counter()
          km_ph = random.choice([0, 30]) #Lo hice aleatorio para pruebas, pero se puede usar la librería gpsd para detectar movimiento
          if km_ph == 0:
            self.stop_count += 1
            self.logger.info(f"Stopped time: {self.stop_count}")
          else:
            self.moving_count += 1
            self.logger.info(f"Moving time: {self.moving_count}")
          self.logger.info("Calculated exact time to wait")
          duration = time.perf_counter() - start
          subtrac = 1.0 - duration
          time.sleep(max(0, subtrac))
        except KeyboardInterrupt:
          self.logger.info("Trip finished")
          self.on_end(subtrac)
    except Exception as e:
      self.logger.error(f"Error during trip: {e}")
      self.logger.error("Contact with your system administrator")
      self.log_on_end()
      quit()


if __name__ == "__main__":
  print("Bienvenide al taxímetro digital\n" \
  "Este sistema te ayuda a calcular el precio de los viajes en taxi")
  taximeter = Taximeter()
  taximeter.start_trip()
