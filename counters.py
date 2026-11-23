# CONTAGEM DO TEMPO DO JOGO

import time

def criar_contadores():
    return {
        "redbull": 0,
        "lata_de_pitu": 0,
        "luva_de_boxe": 0,
    }

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
if __name__ == "__main__":
    Iniciar_Jogo()
