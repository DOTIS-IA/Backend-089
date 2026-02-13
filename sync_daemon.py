import time
import logging
from datetime import datetime
from sync import sync_all_conversations
from elevenlabs_client import get_conversation_history

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/doti-ia/logs/sync_daemon.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Variable global para tracking
last_conversation_id = None

def check_for_new_conversations():
    """
    Verifica si hay conversaciones nuevas SIN procesarlas todas.
    Retorna True si detecta conversaciones nuevas.
    """
    global last_conversation_id
    
    try:
        # Obtener solo las conversaciones más recientes
        conversations = get_conversation_history()
        
        if not conversations:
            logger.debug("ℹ️  No hay conversaciones disponibles")
            return False
        
        # Obtener el ID de la conversación más reciente
        latest_conv_id = conversations[0].get('conversation_id')
        
        # Si es diferente a la última que procesamos, hay nuevas
        if latest_conv_id != last_conversation_id:
            logger.info(f"🆕 Nueva conversación detectada: {latest_conv_id}")
            last_conversation_id = latest_conv_id
            return True
        else:
            logger.debug("✓ No hay conversaciones nuevas desde la última verificación")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error verificando conversaciones: {e}")
        return False

def run_sync_cycle():
    """Ejecuta sincronización completa de conversaciones nuevas"""
    try:
        logger.info("="*70)
        logger.info("🔄 INICIANDO SINCRONIZACIÓN DE CONVERSACIONES NUEVAS")
        logger.info("="*70)
        
        sync_all_conversations()
        
        logger.info("="*70)
        logger.info("✅ SINCRONIZACIÓN COMPLETADA EXITOSAMENTE")
        logger.info("="*70)
        
    except Exception as e:
        logger.error(f"❌ Error en ciclo de sincronización: {e}", exc_info=True)

def main():
    """
    Daemon optimizado - verifica cada minuto y solo sincroniza cuando 
    detecta conversaciones nuevas
    """
    
    # Intervalo de verificación en segundos
    CHECK_INTERVAL = 60  # 1 minuto
    
    logger.info("="*70)
    logger.info("🚀 DAEMON DE SINCRONIZACIÓN INTELIGENTE INICIADO")
    logger.info("="*70)
    logger.info(f"⏰ Intervalo de verificación: {CHECK_INTERVAL} segundos (1 minuto)")
    logger.info(f"💡 Solo sincroniza cuando detecta conversaciones nuevas")
    logger.info(f"📅 Fecha de inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("="*70 + "\n")
    
    # Contador de ciclos
    cycle_count = 0
    
    while True:
        try:
            cycle_count += 1
            logger.info(f"🔍 Ciclo #{cycle_count} - Verificando conversaciones...")
            
            # Verificación ligera
            if check_for_new_conversations():
                # Solo si hay nuevas, hacer sync completo
                run_sync_cycle()
            else:
                logger.info("😴 Sin cambios detectados")
            
            logger.info(f"⏸️  Esperando {CHECK_INTERVAL} segundos hasta próxima verificación...\n")
            time.sleep(CHECK_INTERVAL)
            
        except KeyboardInterrupt:
            logger.info("\n" + "="*70)
            logger.info("👋 DAEMON DETENIDO POR EL USUARIO")
            logger.info(f"📊 Total de ciclos ejecutados: {cycle_count}")
            logger.info("="*70)
            break
            
        except Exception as e:
            logger.error(f"❌ Error crítico en el daemon: {e}", exc_info=True)
            logger.info("⏸️  Esperando 60 segundos antes de reintentar...")
            time.sleep(60)

if __name__ == "__main__":
    main()