import time
from datetime import datetime

def gerar_timestamp():
    """Retorna o horário atual formatado como [HH:MM:SS]."""
    return f"[{datetime.now().strftime('%H:%M:%S')}] "

def lento(texto):
    # Imprime o timestamp sem o efeito lento para agilidade
    timestamp = gerar_timestamp()
    print(timestamp, end='', flush=True)
    
    # Efeito de digitação para o texto original
    for letra in texto:
        print(letra, end ='', flush=True)
        time.sleep(0.03)
    print()

