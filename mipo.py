from skills.notas import añadir_nota, ver_notas
from skills.configuracion import cargar_config
from skills.historial import guardar_historial, ver_historial
from skills.temporizador import iniciar_temporizador
from skills.cerebro import preguntar, historial_conversacion
from skills.voz import escuchar, hablar, esperar_wake_word, mipo_hablando
from skills.emails import send_email, obtener_correos_hoy
from skills.contactos import buscar_contacto
from skills.spotify import transfer_playback, set_volume, pause_playback, start_playback, next_track, previous_track
import traceback

TIMEOUT_SESION = 10

robot = {}

SKILLS_PENDIENTES = {
    "start_spotify": lambda respuesta: preguntar(
        f"El usuario quiere reproducir música. Dijo: '{respuesta}'. "
        f"Llama a la herramienta start_spotify con el nombre del dispositivo que mencionó."
    ),
    "transfer_playback": lambda respuesta: transfer_playback(respuesta)
}

def cargar_info():
    global robot
    robot = cargar_config()

def ejecutar_herramienta(tool_name, params):
    if tool_name == "temporizador":
        iniciar_temporizador(params["segundos"])
    elif tool_name == "guardar_nota":
        añadir_nota(params["text"])
        hablar("Nota guardada.")
    elif tool_name == "ver_notas":
        ver_notas()
        hablar("Te muestro tus notas.")
    elif tool_name == "ver_historial":
        ver_historial()
        hablar("Te muestro el historial.")
    elif tool_name == "consultar_bateria":
        if robot["bateria"] < 20:
            hablar(f"Tengo {robot['bateria']}% de batería, necesito carga")
        else:
            hablar(f"Tengo {robot['bateria']}% de batería")
    elif tool_name == "enviar_mail":
        destinatario = params["recipients"]
        print(destinatario)
        if "@" in destinatario:
            email = destinatario
        else:
            email = buscar_contacto(params["recipients"])
            email = email["email"]
        if email:
            send_email(email, params["body"], params["subject"])
        else:
            hablar(f"No encontré el contacto {params['recipients']} en tu lista de contactos.")
    elif tool_name == "ver_correos":
        correos = obtener_correos_hoy()
        if isinstance(correos, str):
            hablar(correos)
        else:
            contenido = ""
            for i, correo in enumerate(correos):
                contenido += f"Correo {i+1}:\nDe: {correo["remitente"]}\nAsunto: {correo["asunto"]}\n\n"
                
            resultado = preguntar(
                f"Tengo {len(correos)} correos de hoy. Haz un resumen MUY breve de cada uno en una sola frase, "
                f"para escucharlo por voz. Sin listas, sin números, sin formato. "
                f"Habla de forma natural como si me lo contaras. Aquí están:\n\n{contenido}"
            )
                        
            hablar(resultado["contenido"])
    elif tool_name == "cambiar_dispositivo_spotify":
        transfer_playback(params["name"])
    elif tool_name == "setear_volumen_spotify":
        set_volume(params["percent"])
    elif tool_name == "pause_spotify":
        pause_playback()
    elif tool_name == "start_spotify":
        start_playback()
    elif tool_name == "next_track_spotify":
        next_track()
    elif tool_name == "previous_track_spotify":
        previous_track()      
        
def responder(comando):
    if "historial" not in comando:
        guardar_historial(comando)
    try:
        result = preguntar(comando)

        if result["tipo"] == "herramienta":
            pendiente = ejecutar_herramienta(result["nombre"], result["params"])
            # Siempre informar a Claude del resultado antes de salir
            historial_conversacion.append({
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": result["id"],
                        "content": "Pendiente de respuesta del usuario." if pendiente else "Hecho."
                    }
                ]
            })
            return pendiente # Esto puede ser None (flujo normal) o {"pendiente":True...}
        else:
            hablar(result["contenido"])
            return None
    except Exception as e:
        traceback.print_exc()
        return None

def sesion():
    hablar("Te escucho")
    TIMEOUT = 10
    segundos_inactividad = 0
    
    while True:
        try:
            comando = escuchar()
            
            if comando:
                segundos_inactividad = 0
                pendiente = responder(comando)
                
                if pendiente and pendiente.get("pendiente"):
                    hablar(pendiente['pregunta'])
                    respuesta = escuchar()
                    
                    if respuesta:
                        skill_fn = SKILLS_PENDIENTES.get(pendiente['skill'])
                        if skill_fn:
                            resultado = skill_fn(respuesta)
                            if resultado and resultado["tipo"] == "herramienta":
                                ejecutar_herramienta(resultado["nombre"], resultado["params"])
                        else:
                            hablar("No se como procesar esta solicitud")
            elif not mipo_hablando:
                segundos_inactividad += TIMEOUT
            
            if segundos_inactividad >= TIMEOUT_SESION:
                hablar("Me quedo a la espera")
                return

        except Exception as e:
            traceback.print_exc()
            return


cargar_info()


while True:
    try:
        esperar_wake_word()
        sesion()
    except KeyboardInterrupt:
        hablar("Hasta luego.")
        break
    except Exception as e:
        traceback.print_exc()