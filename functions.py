import pygame

def carregar_personagem(arquivo, altura, virar):
    imagem = pygame.image.load("personagens/" + arquivo).convert_alpha()

    #corta o espaço vazio em volta da imagem:
    imagem = imagem.subsurface(imagem.get_bounding_rect()).copy()

    #vira o personagem de lado:
    if virar:
        imagem = pygame.transform.flip(imagem, True, False)

    #muda o tamanho da imagem
    largura = int(imagem.get_width() * altura / imagem.get_height())
    imagem = pygame.transform.smoothscale(imagem, (largura, altura))
    return imagem

def carregar_icone(arquivo, tamanho):
    imagem = pygame.image.load("imagens_botoes_tela_inicial/" + arquivo).convert_alpha()

    #corta o espaço vazio:
    imagem = imagem.subsurface(imagem.get_bounding_rect()).copy()

    #muda o tamanho sem deformar:
    proporcao = tamanho / max(imagem.get_width(), imagem.get_height())
    nova_largura = int(imagem.get_width() * proporcao)
    nova_altura = int(imagem.get_height() * proporcao)
    imagem = pygame.transform.smoothscale(imagem, (nova_largura, nova_altura))
    return imagem