# CONTAGEM DO TEMPO DO JOGO

import time

def Iniciar_Jogo():

    Jogo_finalizado = False
    
    for segundos in range(90, -1, -1):  # Começando de 90s até 0

        # O '\r' faz o contador atualizar na mesma linha do terminal
        print(f"\rTempo restante: {segundos:02d}s ", end="", flush=True)
        
        if segundos > 0:
            time.sleep(1)
            
    print("\nFIm do tempo")
    Jogo_finalizado = True

# Função Iniciar jogo
Iniciar_Jogo()