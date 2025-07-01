import time
import random
import os
from datetime import datetime

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
  with open(name, "a", encoding='utf-8') as f:
    f.write(text)

def change_price():
  minimum = 0
  while True:
    try:
      valor = int(input("Ingresa el valor en \033[93mcéntimos\033[0m: "))
      if (minimum is not None and valor <= minimum):
        print(f"El valor debe ser mayor a {minimum}.")
        continue
      return valor
    except ValueError:
      print("Por favor, ingresa un número entero válido.")

def ask_prices():
  global moving_price, stop_price
  
  while True:
    print("\n1) Precio en parado")
    print("2) Precio en marcha")
    print("0) Cancelar cambio")
    price_option = input("Elige una opción (1, 2 o 0): ")
    if price_option == "1":
      temp = change_price()
      stop_price = temp
      print("Precio en parada cambiado a: " + str(temp))
      break
    elif price_option == "2":
      temp = change_price()
      moving_price = temp
      print("Precio en marcha cambiado a: " + str(temp))
      break
    elif price_option == "0":
      break
    else:
      print("Entrada inválida, escriba 1, 2 o 0.")
      continue
  
  if confirm("¿Quieres cambiar más precios?"):
    ask_prices()
  else:
    trip()

def trip():
  global stop_count, moving_count, trip_bool, moving_price, stop_price
  print(f"\nCalcula \033[93m{stop_price}\033[0m céntimos por segundo en parada y \033[93m{moving_price}\033[0m céntimos por segundo en marcha.")
  if confirm("¿Quieres continuar con estos precios?"):
    True
  else:
    ask_prices()
  #Reiniciar variables por si se inicia otro viaje
  moving_count = 0
  stop_count = 0
  print("\nViaje iniciado\n" \
  "Presiona \033[93m'Ctrl+C'\033[0m para \033[93mterminar\033[0m el viaje\n" \
  "¡Disfruta del viaje!\n")
  try:
    while trip_bool:
      inicio = time.perf_counter()
      km_ph = random.choice([0, 30]) #Lo hice aleatorio para pruebas, pero se puede usar la librería gpsd para detectar movimiento
      if km_ph == 0:
        stop_count += 1
      else:
        moving_count += 1
      duracion = time.perf_counter() - inicio
      time.sleep(max(0, 1.0 - duracion))
  except KeyboardInterrupt:
    on_end()

def on_end():
  global stop_count, moving_count, trip_bool, moving_price, stop_price
  trip_bool = False
  print("Gracias por usar este sitema.\n" \
  "Calculando el precio de este viaje...")
  #Al ser while hay que restar 1 al contador por el tipo de bucle
  if moving_count > 0:
    moving_count -= 1
  if stop_count > 0:
    stop_count -= 1
  precio_final = ((moving_count * moving_price) + (stop_count * stop_price)) / 100
  print(f"Tienes que pagar {precio_final}€")

  txt(".\\taximeter\\trips.txt", f"Viaje en fecha: {datetime.now()}\n" \
      f"Con {stop_price} céntimos por segundo en parada y {moving_price} céntimos por segundo en marcha.\n" \
      f"Este viaje a durado {moving_count + stop_count} segundos totales y se ha pagado {precio_final} por el mismo\n" \
      "Viaje finalizado, gracias\n\n" \
      "-----------------------------------------------------------------------------------------\n\n")

  if confirm("¿Quieres inciar otro trayecto?"):
    trip_bool = True
    trip()
  else:
    quit()

if __name__ == "__main__":
  #Definir variables globales
  stop_price = 2
  moving_price = 5
  moving_count = 0
  stop_count = 0
  trip_bool = True

  print("Bienvenide al taxímetro digital\n" \
  "Este sistema te ayuda a calcular el precio de los viajes en taxi\n" \
  f"\nCalcula \033[93m{stop_price}\033[0m céntimos por segundo en parada y \033[93m{moving_price}\033[0m céntimos por segundo en marcha.\n")
  #keyboard.add_hotkey('ctrl+q', on_end)
  #keyboard.wait()
  if confirm("¿Quieres ajustar los precios?"):
    ask_prices()
  else:
    trip()