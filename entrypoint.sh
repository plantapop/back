#!/bin/bash

# Ejecutar las migraciones
alembic upgrade head

# Iniciar la aplicación
python3 plantapop

