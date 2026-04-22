from skills.notas import añadir_nota, ver_notas
from skills.configuracion import cargar_config
from skills.historial import guardar_historial, ver_historial
from skills.temporizador import iniciar_temporizador
from skills.cerebro import preguntar, historial_conversacion
from skills.voz import escuchar, hablar, esperar_wake_word, mipo_hablando
from skills.emails import send_email, obtener_correos_hoy
from skills.contactos import buscar_contacto
import traceback

TIMEOUT_SESION = 10

robot = {}

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
        
def responder(comando):
    if "historial" not in comando:
        guardar_historial(comando)
    
    try:
        result = preguntar(comando)

        if result["tipo"] == "herramienta":
            ejecutar_herramienta(result["nombre"], result["params"])
        else:
            hablar(result["contenido"])
    except Exception as e:
        traceback.print_exc()


def sesion():
    hablar("Te escucho")
    TIMEOUT = 10
    segundos_inactividad = 0
    
    while True:
        try:
            comando = escuchar()
            
            if comando:
                segundos_inactividad = 0
                responder(comando)
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