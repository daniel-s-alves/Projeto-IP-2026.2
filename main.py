import pygame
from tela_inicial import tela_inicial

pygame.init()
pygame.mixer.init()

#janela do jogo
largura = 1280
altura = 800

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("CinCabeçada")

tela_atual = "inicial"

while tela_atual != "sair":
    if tela_atual == "inicial":
        tela_atual = tela_inicial(tela)

    elif tela_atual == "jogar":
        """ATENÇÃO AQUI FICARÁ A TELA DE SELECIONAR OS PERSONAGENS QUE APARECERA DEPOIS DE CLICAR EM JOGAR"""

    elif tela_atual == "loja":
        """ATENÇÃO AQUI FICARÁ A TELA DA LOJA, DE COMPRAR AS SKINS COM OS COLECIONAVEIS"""

pygame.quit()