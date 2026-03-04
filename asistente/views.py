import json
import os
import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .models import Conversacion, Mensaje
from .tools import TOOLS_GROQ, FUNCIONES

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL   = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """Eres un asistente inteligente del restaurante Q'Chicharron. 
Tienes acceso a herramientas para consultar y gestionar datos reales del restaurante.

Puedes:
- Consultar el stock de productos
- Ver qué productos están por agotarse
- Ver pedidos activos (pendientes y en preparación)
- Crear nuevos pedidos
- Ver el resumen de ventas del día

REGLAS IMPORTANTES:
- NUNCA inventes datos, cifras, pedidos o productos. Solo usa lo que retornen las herramientas.
- Si una herramienta retorna lista vacía o total 0, dilo claramente: "No hay datos registrados".
- Si no encuentras un producto o mesa, infórmalo sin inventar alternativas.
- Las ventas del día solo incluyen ventas marcadas como pagadas en el sistema.
- Responde siempre en español, de forma clara y amigable.
- Cuando muestres listas, usa formato ordenado con los datos exactos retornados.
- Si vas a crear un pedido, confirma mesa e items antes de ejecutar."""


def es_autorizado(usuario):
    return usuario.cargo in ('administrador', 'mesero') or usuario.is_superuser


@login_required
def chat_view(request):
    if not es_autorizado(request.user):
        return redirect('apl:dashboard')

    # Obtener o crear conversación activa
    conversacion_id = request.session.get('conversacion_id')
    conversacion = None

    if conversacion_id:
        try:
            conversacion = Conversacion.objects.get(id=conversacion_id, usuario=request.user)
        except Conversacion.DoesNotExist:
            conversacion = None

    if not conversacion:
        conversacion = Conversacion.objects.create(usuario=request.user)
        request.session['conversacion_id'] = conversacion.id

    mensajes = conversacion.mensajes.all()

    return render(request, 'modulos/chat.html', {
        'mensajes': mensajes,
        'conversacion': conversacion,
    })


@login_required
@require_POST
def enviar_mensaje(request):
    if not es_autorizado(request.user):
        return JsonResponse({'error': 'No autorizado'}, status=403)

    try:
        data = json.loads(request.body)
        texto_usuario = data.get('mensaje', '').strip()
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    if not texto_usuario:
        return JsonResponse({'error': 'Mensaje vacío'}, status=400)

    # Obtener conversación
    conversacion_id = request.session.get('conversacion_id')
    try:
        conversacion = Conversacion.objects.get(id=conversacion_id, usuario=request.user)
    except Conversacion.DoesNotExist:
        conversacion = Conversacion.objects.create(usuario=request.user)
        request.session['conversacion_id'] = conversacion.id

    # Guardar mensaje del usuario
    Mensaje.objects.create(
        conversacion=conversacion,
        rol='user',
        contenido=texto_usuario,
    )

    # Construir historial para Groq
    historial = [{'role': 'system', 'content': SYSTEM_PROMPT}]
    for m in conversacion.mensajes.all():
        historial.append({'role': m.rol, 'content': m.contenido})

    # Llamar a Groq
    api_key = os.environ.get('GROQ_API_KEY', '')
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }

    payload = {
        'model': GROQ_MODEL,
        'messages': historial,
        'tools': TOOLS_GROQ,
        'tool_choice': 'auto',
        'max_tokens': 1024,
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
    except requests.exceptions.Timeout:
        return JsonResponse({'error': 'El asistente tardó demasiado en responder. Intenta de nuevo.'}, status=504)
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': f'Error de conexión con Groq: {str(e)}'}, status=502)

    choice = result['choices'][0]
    message = choice['message']

    # Si el modelo quiere usar una herramienta
    if choice.get('finish_reason') == 'tool_calls' and message.get('tool_calls'):
        tool_calls = message['tool_calls']

        # Agregar respuesta del asistente con tool_calls al historial
        historial.append(message)

        # Ejecutar cada tool call
        for tc in tool_calls:
            fn_name   = tc['function']['name']
            fn_args   = json.loads(tc['function']['arguments'] or '{}')
            tc_id     = tc['id']

            funcion = FUNCIONES.get(fn_name)
            if funcion:
                try:
                    # Inyectar usuario_id automáticamente en crear_pedido
                    if fn_name == 'crear_pedido':
                        fn_args['usuario_id'] = request.user.id
                    resultado = funcion(**fn_args)
                except Exception as e:
                    resultado = {'error': str(e)}
            else:
                resultado = {'error': f'Función {fn_name} no encontrada'}

            historial.append({
                'role': 'tool',
                'tool_call_id': tc_id,
                'content': json.dumps(resultado, ensure_ascii=False, default=str),
            })

        # Segunda llamada a Groq con los resultados
        payload2 = {
            'model': GROQ_MODEL,
            'messages': historial,
            'max_tokens': 1024,
        }

        try:
            response2 = requests.post(GROQ_API_URL, headers=headers, json=payload2, timeout=30)
            response2.raise_for_status()
            result2 = response2.json()
            respuesta_final = result2['choices'][0]['message']['content']
        except Exception as e:
            respuesta_final = f'Error al procesar la respuesta: {str(e)}'

    else:
        respuesta_final = message.get('content', 'No pude generar una respuesta.')

    # Guardar respuesta del asistente
    Mensaje.objects.create(
        conversacion=conversacion,
        rol='assistant',
        contenido=respuesta_final,
    )

    return JsonResponse({'respuesta': respuesta_final})


@login_required
@require_POST
def nueva_conversacion(request):
    if not es_autorizado(request.user):
        return JsonResponse({'error': 'No autorizado'}, status=403)

    conversacion = Conversacion.objects.create(usuario=request.user)
    request.session['conversacion_id'] = conversacion.id

    return JsonResponse({'ok': True, 'conversacion_id': conversacion.id})