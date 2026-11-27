import pygame
from counters import criar_contadores
from tela_inicial import tela_inicial
from tela_escolha_personagens import tela_personagem
from tela_escolha_mapas import tela_mapas
from tela_partida import tela_partida

pygame.init()
pygame.mixer.init()

#janela do jogo
largura = 1280
altura = 800

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("CinCabeçada")

tela_atual = "inicial"
colecionaveis = criar_contadores()

#personagens escolhidos na tela de seleção
jogador1 = None
jogador2 = None
mapa_escolhido = None

while tela_atual != "sair":
    if tela_atual == "inicial":
        tela_atual = tela_inicial(tela)

    elif tela_atual == "jogar":
        """ATENÇÃO AQUI FICARÁ A TELA DE SELECIONAR OS PERSONAGENS QUE APARECERA DEPOIS DE CLICAR EM JOGAR"""
        resposta, personagens = tela_personagem(tela)
        if resposta == "sair":
            tela_atual = "sair"
        elif resposta == "voltar":
            tela_atual = "inicial"
        elif resposta == "pronto":
            jogador1 = personagens[0]
            jogador2 = personagens[1]
            tela_atual = "mapas"

    elif tela_atual == "mapas":
        """ATENCAO AQUI FICARA A TELA DE ESCOLHA DE MAPAS"""
        resposta, mapa = tela_mapas(tela)
        if resposta == "sair":
            tela_atual = "sair"
        elif resposta == "voltar":
            tela_atual = "jogar"
        elif resposta == "pronto":
            mapa_escolhido = mapa
            tela_atual = "partida"

    elif tela_atual == "partida":
        tela_atual = tela_partida(tela, jogador1, jogador2, mapa_escolhido, colecionaveis)

    elif tela_atual == "loja":
        """ATENÇÃO AQUI FICARÁ A TELA DA LOJA, DE COMPRAR AS SKINS COM OS COLECIONAVEIS"""

pygame.quit()
