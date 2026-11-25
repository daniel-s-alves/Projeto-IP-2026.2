import pygame

#cores
azul_escuro = (25, 25, 100)
dourado = (240, 190, 50)
dourado_escuro = (180, 130, 20)
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

def criar_botoes_mapas(largura, altura):
    """Retornara os botoes necessarios para a escolha dos mapas, voltar, avancar, aleatorio, som"""
    botao_voltar = pygame.Rect(30, 24, 80, 80)
    botao_som = pygame.Rect(largura - 110, 24, 80, 80)

    botao_aleatorio = pygame.Rect(0, 0, 300, 70)
    botao_aleatorio.center = (largura // 2, 631)

    botao_avancar = pygame.Rect(0, 0, 80, 80)
    botao_avancar.center = (largura // 2, altura - 60)

    return botao_voltar, botao_som, botao_aleatorio, botao_avancar

def desenhar_botao_dourado(tela, botao, mouse, texto):
    if botao.collidepoint(mouse):
        cor = dourado_escuro
    else:
        cor = dourado
    pygame.draw.rect(tela, cor, botao, border_radius=15)
    pygame.draw.rect(tela, azul_escuro, botao, 5, border_radius=15)
    tela.blit(texto, texto.get_rect(center=botao.center))