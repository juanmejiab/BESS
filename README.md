# Proyecto BESS

Este proyecto fue realizado para extraer datos del sistema de almacenamiento de energía en baterias (BESS), enviarlos al sistema Fiware y finalmente ser usados en tableros de visualización hechos en Grafana.

## Dependencias

- openpyxl v3.1.2
- pandas v2.1.3
- pymodbus v3.5.4
- requests v2.31.0
- crate v0.34.0

## Tecnologías usadas

- Python v3.11
- Docker
- Orion v1.13.0
- MongoDB v3.2
- QuantumLeap v0.8
- CrateDB v5.4.3
- Grafana v10.1.4

## Ejecutar el proyecto de manera local

Para ejecutar el proyecto clona el repositorio

```bash
  git clone https://github.com/juanmejiab/BESS
```

y ejecuta el siguiente comando para crear los contenedores:

```bash
  docker-compose up -d
```

Luego, ejecutar el siguiente comando para crear las entidades y suscripciones:

```bash
  python entity_subscription_creation.py
```

Una vez creadas, puede ver la información de las entidades accediendo a:

```http
  http://localhost:1026/v2/entities
```

Y para las suscripciones:

```http
  http://localhost:1026/v2/subscriptions
```

Para ver los tableros de visualización, ingresa a

```http
  http://localhost:3000
```

inicia sesión e importa los tableros que se encuentran en la carpeta **dashboards.**

Finalmente, ejecuta el siguiente comando para iniciar la extracción de datos:

```bash
  python data_collector.py
```

Adicionalmente, se puede acceder al motor de base de datos mediante:

```http
  http://localhost:4200
```
