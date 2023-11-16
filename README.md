# Proyecto BESS

Este proyecto fue realizado para extraer datos del sistema de almacenamiento de energía en baterias (BESS), enviarlos al sistema Fiware y finalmente ser usados en tableros de visualización hechos en Grafana.

## Tecnologías usadas

- Python (pymodbus, requests, pandas)
- Docker
- Fiware (Orion Context Broker)
- QuantumLeap
- CrateDB
- Grafana

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

Una vez creadas, puede ver la informacion de las entidades accediendo a:

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

Finalmente, ejecuta el siguiente comando para iniciar la extracción de datos desde las baterías:

```bash
  python data_collector.py
```

Adicionalmente, se puede acceder al motor de base de datos mediante:

```http
  http://localhost:4200
```
