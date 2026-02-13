import psycopg2

# Importación de los otros archivos
from db import get_db_connection
from elevenlabs_client import (
    get_conversation_history,
    get_conversation_details,
    get_agent_details,
    parse_agent,
    parse_conversation
)

def insert_agente(cursor, id_agente, nombre=None):
    cursor.execute("""
        INSERT INTO agentes (id_agente, nombre)
        VALUES (%s, %s)
        ON CONFLICT (id_agente) DO UPDATE SET
            nombre = COALESCE(EXCLUDED.nombre, agentes.nombre)
    """, (id_agente, nombre))
    
def insert_situacion(cursor, id_conversacion, conv_data):
    """ Inserta o actualiza los datos analizados de la conversación. 
        Si ya existe un reporte para esa conversación, lo actualiza. """
    
    cursor.execute('''
        INSERT INTO reportes (id_conversacion, id_extorsion, modo, tiempo, lugar)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (id_conversacion) DO UPDATE SET
            id_extorsion = EXCLUDED.id_extorsion,
            modo = EXCLUDED.modo,
            tiempo = EXCLUDED.tiempo,
            lugar = EXCLUDED.lugar
        RETURNING folio;
    ''', (
        id_conversacion, 
        conv_data.get("id_extorsion"),
        conv_data.get("forma"), 
        conv_data.get("tiempo"), 
        conv_data.get("lugar")
    ))
    
    result = cursor.fetchone()
    return result[0] if result else None

def insert_conversacion(cursor, conv_data):
    """ Insertar conversación en la base de datos y retornar el ID generado """
    
    cursor.execute("""
        INSERT INTO conversaciones
        (id_eleven, id_agente, fecha, hora_inicio, hora_fin, duracion, transcripcion)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id_eleven) DO UPDATE SET
            transcripcion = EXCLUDED.transcripcion,
            hora_fin = EXCLUDED.hora_fin,
            duracion = EXCLUDED.duracion
        RETURNING id_conversacion
    """, (
        conv_data["id_eleven"],
        conv_data["id_agente"],
        conv_data["fecha"],
        conv_data["hora_inicio"],
        conv_data["hora_fin"],
        conv_data["duracion"],
        conv_data["transcripcion"]
    ))
    
    result = cursor.fetchone()
    return result[0] if result else None

def sync_all_conversations():
    """ Sincronizar todas las conversaciones de ElevenLabs a PostgreSQL """
    
    print("🔄 Iniciando sincronización de conversaciones...")
    
    conversations = get_conversation_history()
    
    if not conversations:
        print("ℹ️  No se encontraron conversaciones")
        return
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        synced_count = 0
        error_count = 0
        
        for idx, conv_summary in enumerate(conversations, 1):
            conv_id = conv_summary.get("conversation_id")
            agent_id = conv_summary.get("agent_id")
            
            if not conv_id or not agent_id:
                print(f"⚠️  [{idx}] Conversación sin ID válido, omitiendo...")
                continue
            
            print(f"\n[{idx}/{len(conversations)}] Procesando: {conv_id}")
            
            try:
                # Obtener detalles
                conv_details = get_conversation_details(conv_id)
                agent_details = get_agent_details(agent_id)
                
                if not conv_details:
                    print(f"❌ No se pudieron obtener detalles")
                    error_count += 1
                    continue
                
                conv_data = parse_conversation(conv_details)
                agent_data = parse_agent(agent_details)
                
                # 1. Insertar/Actualizar Agente
                if conv_data.get("id_agente") and agent_data.get("nombre_agente"):
                    insert_agente(cursor, conv_data["id_agente"], agent_data["nombre_agente"])
                    print(f"  ✓ Agente: {agent_data['nombre_agente']}")
                
                # 2. Insertar Conversación
                id_conversacion = insert_conversacion(cursor, conv_data)
                print(f"  ✓ Conversación ID: {id_conversacion}")
                
                # 3. Insertar Reporte
                if id_conversacion:
                    folio = insert_situacion(cursor, id_conversacion, conv_data)
                    print(f"  ✓ Reporte generado: {folio}")
                    print(f"     - Modo: {conv_data.get('forma')}")
                    print(f"     - Lugar: {conv_data.get('lugar')}")
                    print(f"     - Tiempo: {conv_data.get('tiempo')}")
                    synced_count += 1
                
            except Exception as e:
                print(f"  ❌ Error: {e}")
                error_count += 1
                # No hacer rollback para que las anteriores se guarden
                continue
        
        print(f"\n{'='*60}")
        print(f"✅ Sincronización completada")
        print(f"   • Exitosas: {synced_count}")
        print(f"   • Errores: {error_count}")
        print(f"{'='*60}")
        
if __name__ == "__main__":
    sync_all_conversations()