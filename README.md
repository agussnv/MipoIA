# Mipo — Personal AI Voice Assistant

Mipo es un asistente de voz personal con inteligencia artificial integrada, construido completamente en Python desde cero. Diseñado para ser compacto, portátil y extensible — con la visión de convertirse en un gadget físico que puedas llevar siempre encima.

El proyecto nació como un ejercicio de aprendizaje: construir algo real y útil mientras se aprende a programar. Sin conocimientos previos de Python, sin atajos.

---

## ¿Qué es Mipo?

Mipo escucha, entiende y actúa. No es un chatbot — es un asistente que vive en tu entorno, responde a tu voz y ejecuta tareas reales en segundo plano mientras sigues con tu vida.

A diferencia de Alexa o Google Assistant, Mipo es completamente tuyo — el código, los datos, la lógica. Sin suscripciones, sin datos enviados a terceros salvo las APIs que tú mismo configuras, sin cajas negras.

---

## Cómo funciona

El flujo es simple:

```
Di "Alexa" → Mipo se activa → hablas → Mipo entiende → ejecuta → responde por voz → se suspende
```

Por dentro, cada paso tiene su tecnología:

- **Wake word** detecta la palabra de activación en tiempo real sin consumir recursos
- **Whisper** transcribe tu voz a texto con alta precisión en español
- **Claude (Anthropic)** interpreta lo que dijiste y decide qué hacer
- **Tool use** permite a Claude llamar a funcionalidades reales del sistema
- **edge-tts** convierte la respuesta en voz natural y la reproduce

---

## Funcionalidades actuales

**Conversación general**
Mipo puede responder cualquier pregunta, hacer cálculos, explicar conceptos o simplemente charlar. Claude actúa como cerebro sin limitaciones temáticas.

**Temporizadores**
Corre en segundo plano — puedes seguir usando el asistente mientras cuenta.

**Notas y recordatorios**
Guardadas en disco, persisten entre sesiones. Puedes consultarlas en cualquier momento.

**Correo electrónico**
Envía emails por voz a contactos de tu agenda personal. También lee y resume los correos recibidos durante el día, extrayendo lo esencial para escucharlo en segundos.

**Agenda de contactos**
Resuelve nombres a emails automáticamente — dices "manda un mail a mamá" y Mipo sabe a quién escribir.

**Historial**
Registro persistente de todos los comandos con fecha y hora exacta.

---

## Stack tecnológico

| Capa | Tecnología | Motivo |
|---|---|---|
| Cerebro IA | Claude Haiku (Anthropic) | Rápido, económico, tool use nativo |
| Wake word | OpenWakeWord | Open source, corre en local |
| Voz a texto | Whisper small (local) | Alta precisión en español |
| Texto a voz | edge-tts (Microsoft) | Voces naturales, gratuito |
| Correos | SMTP + Gmail API | Envío y lectura sin depender de terceros |
| Audio | sounddevice + pygame | Control bajo nivel del hardware |
| Persistencia | JSON | Simple, legible, sin dependencias |

---

## Arquitectura del proyecto

El proyecto está organizado en módulos independientes — cada funcionalidad vive en su propio archivo dentro de `skills/`. Añadir una nueva capacidad es tan simple como crear un nuevo módulo y registrarlo en el cerebro.

```
mipo.py          → núcleo: sesiones, wake word, bucle principal
skills/
  cerebro.py     → integración con Claude y tool use
  voz.py         → todo lo relacionado con audio
  emails.py      → correo entrante y saliente
  notas.py       → sistema de notas
  historial.py   → registro de actividad
  temporizador.py → timers en segundo plano
  configuracion.py → configuración persistente
```

---

## Estado actual

El proyecto está en desarrollo activo. Actualmente corre en un ordenador de sobremesa o portátil con Ubuntu. La siguiente fase es la migración al hardware físico definitivo.

**Lo que ya funciona**
- Pipeline completo de voz end-to-end
- Detección de wake word con memoria limpia entre sesiones
- Gestión de sesiones con timeout inteligente — el timeout se pausa mientras Mipo habla
- Integración con Gmail API para lectura de correos
- Envío de emails con resolución automática de contactos
- Cerebro con tool use — Claude llama a funcionalidades reales, no simula

**Lo que está en progreso**
- Migración a Raspberry Pi 3 como primer prototipo físico
- Optimización de latencia end-to-end

---

## Roadmap

**Hardware**
- [ ] Primer prototipo en Raspberry Pi 2
- [ ] Migración a Raspberry Pi Zero para mayor portabilidad
- [ ] Diseño de carcasa impresa en 3D — clip o gancho para llevar encima
- [ ] Gestión de batería LiPo
- [ ] LED de estado — dormido, escuchando, procesando

**Voz e interacción**
- [ ] Wake word personalizado "Hey Mipo" en lugar de "Alexa"
- [ ] Whisper API para reducir latencia de 3s a menos de 1s
- [ ] Voces más naturales y expresivas
- [ ] Detección de idioma automática
- [ ] Modo susurro — respuestas más cortas en entornos silenciosos

**Integraciones**
- [ ] Google Calendar — consultar agenda, crear eventos, recordatorios
- [ ] Spotify — reproducir música, controlar reproducción por voz
- [ ] Domótica — control de luces, temperatura y dispositivos del hogar (Home Assistant)
- [ ] Clima — previsión del tiempo en tiempo real
- [ ] Noticias — resumen de titulares del día
- [ ] WhatsApp Business — lectura y envío de mensajes

**Sistema**
- [ ] App web de administración — gestionar contactos, notas y configuración desde el móvil
- [ ] Base de datos en lugar de JSON para mayor escalabilidad
- [ ] App móvil para administración remota

---

## Origen del proyecto

Mipo empezó como una pregunta: ¿se puede construir un Alexa propio desde cero, aprendiendo a programar al mismo tiempo?

La respuesta es sí. Este repositorio es el resultado de ese proceso — cada funcionalidad construida entendiéndola antes de escribirla, sin copiar soluciones sin comprenderlas.

El objetivo a largo plazo es un gadget físico compacto que quepa en un bolsillo, se enganche a la ropa, y sea tan útil como cualquier asistente comercial — pero completamente personalizable y privado.
