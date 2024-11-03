# ChatBotBelcorp

Este repositorio contiene el código fuente del proyecto ChatBotBelcorp. El proyecto está desarrollado en Python y tiene como objetivo crear un chatbot para mejorar la interacción con los clientes de Belcorp.

## Estructura del Proyecto

- **/app.py**: Contiene el código principal que corre los servicios API de whatsapp.
- **/services**: Contiene el codigo de la lógica de negocio.
- **/sett**: Contiene los secrets del repositorio y configuraciones globales.

## Requisitos

- Python 3.x
- Librerías especificadas en `requirements.txt`

## Instalación

1. Clona el repositorio:
    ```bash
    git clone https://github.com/SantiagoSantafe/ChatBotBelcorp.git
    ```
2. Accede al directorio del proyecto:
    ```bash
    cd ChatBotBelcorp
    ```
3. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```
Haz uso de POSTMAN junto con JSON para enviar tus mensajes por whatsapp luego de las configuraciones en Meta Business Suite
```json
curl -i -X POST `
  https://graph.facebook.com/v20.0/503431269513746/messages `
  -H 'Authorization: Bearer EAAbsmFU0KS4BO3zXg8ZATUfjl3xWGwZAupE5xwGv4TlOAJ2XFK7XpxrCZCzH7fbfWwHIL8AZCZA1WjeASavRFcMJZCTQrvsjFVCZCMGdJlleI2MPavI9Q8nSYZADHV04lMYZBUI1USOqZAPlxw3QQZBOgWHiWvopeyINBvIks3okg0boJfDQvnsqFdgCkFvlAcLnF0rdSTN6YLEosmgNUuUR8o4XQu2xE8ZD' `
  -H 'Content-Type: application/json' `
  -d '{ \"messaging_product\": \"whatsapp\", \"to\": \"*TU NUMERO CELULAR REGISTRADO EN META*\", \"type\": \"template\", \"template\": { \"name\": \"hello_world\", \"language\": { \"code\": \"en_US\" } } }'
```
