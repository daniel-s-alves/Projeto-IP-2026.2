import pygame

#cores
cinza_claro = (240, 240, 250)
cinza_escuro = (160, 160, 185)

def criar_botoes_iniciais(largura):
    """Retorna os botoes jogar, loja e som"""
    botao_jogar = pygame.Rect(0, 0, 150, 150)
    botao_jogar.center = (largura // 2, 385)
    
    botao_loja = pygame.Rect(0, 0, 150, 150)
    botao_loja.center = (largura // 2, 556)
    
    botao_som = pygame.Rect(largura - 120, 30, 85, 85)

    return botao_jogar, botao_loja, botao_som

def desenhar_botao_seta(tela, botao, mouse, icone):
    if botao.collidepoint(mouse):
        cor = cinza_escuro
    else:
        cor = cinza_claro
    pygame.draw.rect(tela, cor, botao, border_radius=16)
    tela.blit(icone, icone.get_rect(center=botao.center))