# Taxímetro Digital en Python

Este proyecto simula un sistema de taxímetro digital en la terminal.

Calcula el precio de un viaje en función del tiempo detenido y en movimiento, registrando los datos en logs y archivos de texto.

Además posee test unitarios para pruebas de las funciones.


## 💾 Descargar proyecto
Elegir carpeta y ejecutar en el terminal:

```bash
git clone https://github.com/Factoria-F5-madrid/Taximeter-AzulFayos.git
```

## 🐍 Uso con python

## 📦 Requisitos (Windows)

- [Pyhton](https://www.python.org/downloads/windows/)

### 1. Lanzar el táximetro

```bash
python taximeter.py
```
### 2. Ejecutar test unitario

```bash
python -m unittest test_taximeter.py
```

## 🚀 Uso con Docker

## 📦 Requisitos

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### 1. Lanzar el táximetro

```bash
docker compose run --rm taximeter
```
### 2. Ejecutar test unitario

```bash
docker compose run --rm taximeter python -m unittest test_taximeter.py
```
