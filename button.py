import pygame

def criar_botoes_iniciais(largura):
    """Retorna os botoes jogar, loja e som"""
    botao_jogar = pygame.Rect(0, 0, 150, 150)
    botao_jogar.center = (largura // 2, 385)
    
    botao_loja = pygame.Rect(0, 0, 150, 150)
    botao_loja.center = (largura // 2, 556)
    
    botao_som = pygame.Rect(largura - 120, 30, 85, 85)

    return botao_jogar, botao_loja, botao_som