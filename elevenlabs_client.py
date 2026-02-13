import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
BASE_URL = "https://api.elevenlabs.io/v1"

HEADERS = {
    "xi-api-key": ELEVENLABS_API_KEY
}

def get_conversation_history():
    """ Obtener historial de conversaciones de ElevenLabs """
    
    url = f"{BASE_URL}/convai/conversations"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        conversations = data.get("conversations", [])
        print(f"✅ Se obtuvieron {len(conversations)} conversaciones")
        return conversations
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al obtener conversaciones: {e}")
        return []

def get_conversation_details(conversation_id):
    """ Obtener detalles completos de una conversación específica """
    
    url = f"{BASE_URL}/convai/conversations/{conversation_id}"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al obtener conversación {conversation_id}: {e}")
        return None

def extraer_dato_collection(data_collection, key):
    """ Extrae el valor limpio del JSON de Data Collection """
    
    item = data_collection.get(key)
    if isinstance(item, dict):
        return item.get('value')
    return item

def parse_conversation(conv_data):
    """ Extraer datos relevantes incluyendo forma, Tiempo y Lugar """
    
    metadata = conv_data.get("metadata", {})
    analysis = conv_data.get("analysis", {})
    collected = analysis.get("data_collection_results", {})
    
    # Construir transcripción
    transcript_parts = []
    if "transcript" in conv_data:
        for turn in conv_data["transcript"]:
            speaker = turn.get("role", "unknown")
            text = turn.get("message", "")
            time = turn.get("time_in_call_secs", 0)
            transcript_parts.append(f"[{time:.1f}s] {speaker.upper()}: {text}")
    
    full_transcript = "\n".join(transcript_parts)
    
    conversation_parsed = {
        "id_eleven": conv_data.get("conversation_id"),
        "id_agente": conv_data.get("agent_id"),
        "fecha": None,
        "hora_inicio": None,
        "hora_fin": None,
        "duracion": None,
        "transcripcion": full_transcript,
        "forma": extraer_dato_collection(collected, 'forma'), 
        "lugar": extraer_dato_collection(collected, 'lugar'),
        "tiempo": extraer_dato_collection(collected, 'tiempo'),
        "id_extorsion": extraer_dato_collection(collected, 'id_extorsion')
    }
    
    # Extraer timestamps
    start_timestamp = metadata.get("start_time_unix_secs")
    if start_timestamp:
        start_dt = datetime.fromtimestamp(start_timestamp)
        conversation_parsed["fecha"] = start_dt.date()
        conversation_parsed["hora_inicio"] = start_dt.time()
    
    duration_secs = metadata.get("call_duration_secs")
    if duration_secs:
        conversation_parsed["duracion"] = f"{duration_secs} seconds"
        if start_timestamp:
            end_dt = start_dt + timedelta(seconds=duration_secs)
            conversation_parsed["hora_fin"] = end_dt.time()
    
    return conversation_parsed


def get_agent_details(agent_id):
    """ Obtener detalles completos de un agente específico """
    
    url = f"{BASE_URL}/convai/agents/{agent_id}"
    
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al obtener agente {agent_id}: {e}")
        return None

def parse_agent(agent_data):
    """ Extraer datos relevantes del agente """
    
    if not agent_data:
        return {"id_agente": None, "nombre_agente": "Desconocido"}
        
    return {
        "id_agente": agent_data.get("agent_id"),
        "nombre_agente": agent_data.get("name")
    }

# ----- DESCOMENTAR SI SOLO QUIERES PRBAR EL ARCHIVO -----

# if __name__ == "__main__":
#     print("🔍 Probando conexión y extracción completa...")
#     conversations = get_conversation_history()
    
#     if conversations:
#         conv = conversations[0]
#         details = get_conversation_details(conv.get('conversation_id'))
        
#         if details:
#             parsed = parse_conversation(details)
#             print(f"\n✅ Datos de Situación Extraídos:")
#             print(f"forma: {parsed['forma']}")
#             print(f"Lugar: {parsed['lugar']}")
#             print(f"Tiempo: {parsed['tiempo']}")
#             print(f"ID Extorsión: {parsed['id_extorsion']}")
#             print("-" * 30)
#             print(f"Fecha: {parsed['fecha']} | Inicio: {parsed['hora_inicio']}")