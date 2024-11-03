import requests
import sett
import json
import time
import openai
import unicodedata

sesiones_usuarios = {}

# Inicializa tu API Key de OpenAI
openai.api_key = "TU OPEN AI API KEY"

def obtener_Mensaje_whatsapp(message):
    if 'type' not in message :
        text = 'mensaje no reconocido'
        return text

    typeMessage = message['type']
    if typeMessage == 'text':
        text = message['text']['body']
    elif typeMessage == 'button':
        text = message['button']['text']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'list_reply':
        text = message['interactive']['list_reply']['title']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply':
        text = message['interactive']['button_reply']['title']
    else:
        text = 'mensaje no procesado'
    
    
    return text

def enviar_Mensaje_whatsapp(data):
    try:
        whatsapp_token = sett.whatsapp_token
        whatsapp_url = sett.whatsapp_url
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer ' + whatsapp_token}
        print("se envia ", data)
        response = requests.post(whatsapp_url, 
                                 headers=headers, 
                                 data=data)
        
        if response.status_code == 200:
            return 'mensaje enviado', 200
        else:
            return 'error al enviar mensaje', response.status_code
    except Exception as e:
        return e,403
    
def text_Message(number,text):
    data = json.dumps(
            {
                "messaging_product": "whatsapp",    
                "recipient_type": "individual",
                "to": number,
                "type": "text",
                "text": {
                    "body": text
                }
            }
    )
    return data

def buttonReply_Message(number, options, body, footer, sedd,messageId):
    buttons = []
    for i, option in enumerate(options):
        buttons.append(
            {
                "type": "reply",
                "reply": {
                    "id": sedd + "_btn_" + str(i+1),
                    "title": option
                }
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "buttons": buttons
                }
            }
        }
    )
    return data

def listReply_Message(number, options, body, footer, sedd, messageId):
    rows = []
    for i, option in enumerate(options):
        rows.append(
            {
                "id": f"{sedd}_row_{i+1}",
                "title": option[:24],  # Limitar el título a 24 caracteres
                "description": ""  # Descripción vacía
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "button": "Ver Opciones",
                    "sections": [
                        {
                            "title": "Selecciona una opción",  # Título obligatorio para la sección
                            "rows": rows
                        }
                    ]
                }
            }
        }
    )
    return data

def document_Message(number, url, caption, filename):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "document",
            "document": {
                "link": url,
                "caption": caption,
                "filename": filename
            }
        }
    )
    return data
  
def enviar_Mensaje_whatsapp(data):
    """Envía el mensaje formateado a través del API de WhatsApp."""
    try:
        whatsapp_token = sett.whatsapp_token
        whatsapp_url = sett.whatsapp_url
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + whatsapp_token}
        print("se envia ", data)
        response = requests.post(whatsapp_url, headers=headers, data=data)
        return 'mensaje enviado', response.status_code
    except Exception as e:
        print("Error al enviar mensaje:", e)
        return str(e), 403
  
def sticker_Message(number, sticker_id):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "sticker",
            "sticker": {
                "id": sticker_id
            }
        }
    )
    return data

def get_media_id(media_name , media_type):
    media_id = ""
    if media_type == "sticker":
        media_id = sett.stickers.get(media_name, None)
    #elif media_type == "image":
    #    media_id = sett.images.get(media_name, None)
    #elif media_type == "video":
    #    media_id = sett.videos.get(media_name, None)
    #elif media_type == "audio":
    #    media_id = sett.audio.get(media_name, None)
    return media_id

def replyReaction_Message(number, messageId, emoji):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "reaction",
            "reaction": {
                "message_id": messageId,
                "emoji": emoji
            }
        }
    )
    return data

def replyText_Message(number, messageId, text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "context": { "message_id": messageId },
            "type": "text",
            "text": {
                "body": text
            }
        }
    )
    return data

def markRead_Message(messageId):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id":  messageId
        }
    )
    return data
  
    
   
def sanitize_text(text, max_length=450):
    """Remove accents, emojis, and limit length."""
    # Remove accents
    text = ''.join(
        (c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    )
    # Remove non-ASCII characters (including emojis)
    text = text.encode('ascii', 'ignore').decode('utf-8')
    # Truncate text if too long
    if len(text) > max_length:
        text = text[:max_length] + "..."
    return text

def obtener_respuesta_usuario():
    """Simula la espera hasta que se reciba un nuevo mensaje de WhatsApp."""
    while True:
        print("Esperando la entrada del usuario...")
        user_message = obtener_Mensaje_whatsapp({"type": "text", "text": {"body": "Mensaje del usuario"}})
        if user_message:
            return user_message.lower()
        time.sleep(2)  # Espera antes de verificar de nuevo  

def gestionar_respuesta_openai(user_id, user_input):
    """Gestiona la conversación con OpenAI basada en el input del usuario."""
    if user_id not in sesiones_usuarios:
        sesiones_usuarios[user_id] = [
            {"role": "system", "content": "Eres un asistente para consultores de Belcorp. Proporciona respuestas breves sobre productos y ventas. Todo basado en los productos de Belcorp, si necesitas consulta en internet acerca de los preguntos, todo segun los valores institucionales de la empresa Belcorp. Los mensajes tienen que ser muy condensados."}
        ]
    
    # Añadir el mensaje del usuario al historial de conversación
    sesiones_usuarios[user_id].append({"role": "user", "content": user_input})

    try:
        # Solicita respuesta de OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=sesiones_usuarios[user_id]
        )
        assistant_response = response['choices'][0]['message']['content']
        sesiones_usuarios[user_id].append({"role": "assistant", "content": assistant_response})
        return assistant_response
    except Exception as e:
        print("Error al obtener respuesta de OpenAI:", e)
        return "Lo siento, hubo un problema al obtener la ayuda. Inténtalo de nuevo más tarde."

def webhook_respuesta_whatsapp(data):
    """Función para procesar las respuestas entrantes desde el webhook de WhatsApp."""
    user_id = data.get('from')
    user_message = obtener_Mensaje_whatsapp(data.get('message'))
    
    if user_message:
        if user_message.lower() in ["salir", "adios"]:
            respuesta_final = "Gracias por usar el modo de ayuda. Regresando al menú principal."
            enviar_Mensaje_whatsapp(text_Message(user_id, respuesta_final))
            # Limpiar la conversación del usuario
            sesiones_usuarios.pop(user_id, None)
        else:
            # Obtener respuesta de OpenAI usando el mensaje del usuario
            respuesta_openai = gestionar_respuesta_openai(user_id, user_message)
            enviar_Mensaje_whatsapp(text_Message(user_id, respuesta_openai))

# Ejemplo de llamada del webhook cuando un mensaje es recibido
def procesar_mensaje_recibido(request_data):
    """Función principal que simula la entrada desde el webhook de WhatsApp."""
    user_id = request_data.get("from")
    message = request_data.get("message")
    user_message = obtener_Mensaje_whatsapp(message)
    
    # Confirmar que el mensaje viene del usuario y no es duplicado
    if user_message and user_id:
        webhook_respuesta_whatsapp(request_data)

def administrar_chatbot(text,number, messageId, name):
    text = text.lower() #mensaje que envio el usuario
    list = []
    print("mensaje del usuario: ",text)

    markRead = markRead_Message(messageId)
    list.append(markRead)
    time.sleep(1)


    # Menú principal que se muestra cuando el usuario elige "Volver" o "Salir"
    def mostrar_menu_principal():
        body = "¡Hola! 👋 Bienvenido/a a Ésika, L'BEL y Cyzone. Estamos listos para ayudarte con lo que necesites."
        footer = "Equipo Belcorp"
        options = ["Pedidos", "Mis Clientes", "Ayuda"]
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed1", messageId)
        replyReaction = replyReaction_Message(number, messageId, "🫡")
        list.append(replyReaction)
        list.append(replyButtonData)
        
    # Verificar si el usuario quiere volver al menú principal
    if "hola" in text or "salir" in text or "volver" in text:
        mostrar_menu_principal()
        

    elif "revisar pedidos actuales" in text:
      # Mensaje para mostrar los pedidos actuales
      body = (
          "📋 Aquí tienes el resumen de tus pedidos actuales:\n\n"
          "1. Pedido #1234 - En camino 🚚\n"
          "2. Pedido #5678 - Preparando 📦\n"
          "3. Pedido #9101 - Confirmado ✅\n\n"
          "¿Deseas realizar alguna otra acción?"
      )
      footer = "Selecciona una opción"
      options = ["🔙 Volver al menú", "⛔ Finalizar consulta"]

      # Crear el mensaje de respuesta con botones
      replyButtonData = buttonReply_Message(number, options, body, footer, "sed_revisar_pedidos", messageId)

      # Agregar el mensaje a la lista de mensajes a enviar
      list.append(replyButtonData)
      
    elif "pedidos" in text:
        body = "Selecciona la opción que deseas.📦"
        footer = "Equipo Belcorp"
        options = ["Añadir pedido","Informacion de mi pedido", "Revisar Pedidos Actuales", "Salir"] #

        listReplyData = listReply_Message(number, options, body, footer, "sed2",messageId)
        sticker = sticker_Message(number, get_media_id("perro_traje", "sticker"))

        list.append(listReplyData)
        list.append(sticker)
    
      
    elif "revisar" in text:
      body = "📋 Estos son tus pedidos actuales:\n\n1. Pedido #1234 - En camino 🚚\n2. Pedido #5678 - Preparando 📦\n3. Pedido #9101 - Confirmado ✅"
      footer = "Selecciona una opción"
      options = ["🔙 Volver", "⛔ Finalizar"]

      replyButtonData = buttonReply_Message(number, options, body, footer, "sed_revisar", messageId)
      list.append(replyButtonData)
        
    elif "informacion de mi pedido" in text:
        body = "Actualmente, tu pedido esta en camino. El valor total de tu pedido es: $330,000. \n Tu comision por el pedido es: $132,000."
        footer = "Si deseas volver, haz clic en Volver."
        options = ["Volver", "Acabar conversacion"]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed3", messageId)
        list.append(replyButtonData)


    elif "añadir pedido" in text:
      body = "Te gustaria añadir los productos de tus clientes para potenciar tus ventas?"
      footer = "Elige una opcion"
      options = ["Si, cargar cliente", "No, pedir sin mas", "Salir"]

      replyButtonData = buttonReply_Message(number, options, body, footer, "sed4", messageId)
      list.append(replyButtonData)

    elif "si, cargar cliente" in text:
      # Primer mensaje solicitando el número
      body_numero = "Por favor, escribe el número de la persona para la que quieres añadir productos."
      textMessage_numero = text_Message(number, body_numero)
      list.append(textMessage_numero)

      # Segundo mensaje solicitando el nombre (puede incluir una pequeña pausa antes de enviarlo)
      time.sleep(1)  # Pausa opcional para evitar que los mensajes se envíen demasiado rápido
      body_nombre = "Ahora, escribe el nombre de la persona."
      textMessage_nombre = text_Message(number, body_nombre)
      list.append(textMessage_nombre)

    elif "no, pedir sin mas" in text or "agregar mas" in text:
        body = "¿Cómo deseas buscar el producto? 🔍"
        footer = "Selecciona la opción"
        options = ["Ingresar codigo", "Buscar por nombre", "Buscar por foto", "Ver carrito", "Borrar del carrito"]

        listReplyData = listReply_Message(number, options, body, footer, "sed5", messageId)
        list.append(listReplyData)


    elif "ingresar codigo" in text:
        body = "Por favor, escribe el código del producto 📋."
        textMessage = text_Message(number, body)
        list.append(textMessage)

    elif "buscar por nombre" in text:
        body = "Escribe el nombre del producto que deseas buscar 📝."
        textMessage = text_Message(number, body)
        list.append(textMessage)

    elif "buscar por foto" in text:
        body = "Envía la foto del producto 📸. Te mostraré los resultados."
        textMessage = text_Message(number, body)
        list.append(textMessage)
    
    elif "mensaje no procesado" in text:
        body = "La foto que muestras es el producto: \n Loción Mitika \n Costo: 24.000$ \n Tu ganancia: 24.000$"
        textMessage = text_Message(number, body)
        list.append(textMessage)

    elif "ver carrito" in text:
        body = "🛒 Aquí está todo lo que tienes en el carrito:\n1. Producto A - $Precio\n2. Producto B - $Precio\n3. Producto C - $Precio\n\n¿Quieres agregar más productos o confirmar el pedido?"
        footer = "Selecciona una opción"
        options = ["Agregar mas productos", "Confirmar pedido", "Borrar producto", "Eliminar pedido"]

        listReplyData = listReply_Message(number, options, body, footer, "sed6", messageId)
        list.append(listReplyData)

    elif "borrar del carrito" in text:
        body = "Escribe el nombre del producto que deseas eliminar del carrito 🗑️."
        textMessage = text_Message(number, body)
        list.append(textMessage)

    elif "mis clientes" in text:
        body = "📊 Aquí puedes ver información sobre tus clientes."
        footer = "Selecciona una opción"
        options = ["Clientes con más ventas", "Clientes a reforzar", "Salir"]

        listReplyData = listReply_Message(number, options, body, footer, "sed7", messageId)
        list.append(listReplyData)

    elif "clientes con más ventas" in text:
        body = "Tu cliente con más ventas es [Nombre del Cliente] con un total de $[monto]. ¡Excelente! 🌟"
        textMessage = text_Message(number, body)
        list.append(textMessage)

    elif "clientes a reforzar" in text:
        body = "Algunos clientes que podrían necesitar un refuerzo en ventas son:\n- Cliente 1\n- Cliente 2\n\n¿Quieres enviarles un mensaje especial? 📩"
        footer = "Selecciona una opción"
        options = ["Sí, enviar mensaje", "No, gracias"]

        listReplyData = listReply_Message(number, options, body, footer, "sed8", messageId)
        list.append(listReplyData)

    elif "reactivacion" in text:
        body = "¡Hola de nuevo! 😊 Noté que hace tiempo no haces un pedido. Queremos ofrecerte una oferta especial para reactivarte. 🎉 ¿Te gustaría conocerla?"
        footer = "Elige una opción"
        options = ["Si, quiero la oferta", "No, gracias"]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed9", messageId)
        list.append(replyButtonData)

    elif "si, quiero la oferta" in text:
        body = "¡Genial! 🥳 Aquí está tu oferta especial: [Descripción de la Oferta]. ¡Aprovecha antes de que se termine!"
        textMessage = text_Message(number, body)
        list.append(textMessage)

    elif "no, gracias." in text:
        textMessage = text_Message(number, "Perfecto! No dudes en contactarnos si tienes más preguntas. Recuerda que también ofrecemos material gratuito para la comunidad. ¡Hasta luego! 😊")
        list.append(textMessage)
        
    elif "ayuda" in text:
        print("Entrando en modo de ayuda con OpenAI")

        # Mensaje inicial para empezar la conversación
        respuesta_inicial = "Estoy aquí para ayudarte. ¿Qué necesitas saber o en qué te puedo ayudar?"
        enviar_Mensaje_whatsapp(text_Message(number, respuesta_inicial))

        # Guardar el estado inicial de la conversación en el diccionario de sesiones
        if number not in sesiones_usuarios:
            sesiones_usuarios[number] = [
                {"role": "system", "content": "Eres un asistente para consultores de Belcorp. Proporciona respuestas breves sobre productos y ventas."}
            ]
            sesiones_usuarios[number].append({"role": "assistant", "content": respuesta_inicial})
        
        # Esperamos que el webhook maneje la próxima respuesta del usuario
        print("Esperando la respuesta del usuario en el webhook...")
        
    else:
        # Para cualquier otro texto, reenviamos el mensaje al webhook para gestión de OpenAI
        request_data = {
            "from": number,
            "message": {"type": "text", "text": {"body": text}}
        }
        procesar_mensaje_recibido(request_data)


    # Enviar los mensajes con pausas para evitar problemas de saturación
    for item in list:
        enviar_Mensaje_whatsapp(item)


#al parecer para mexico, whatsapp agrega 521 como prefijo en lugar de 52,
# este codigo soluciona ese inconveniente.
def replace_start(s):
    number = s[3:]
    if s.startswith("521"):
        return "52" + number
    elif s.startswith("549"):
        return "54" + number
    else:
        return s
        

