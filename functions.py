import pygame

CONTROLES_JOGADOR_1 = {
    "pular": pygame.K_w,
    "esquerda": pygame.K_a,
    "direita": pygame.K_d,
    "baixo": pygame.K_s,
}

CONTROLES_JOGADOR_2 = {
    "pular": pygame.K_UP,
    "esquerda": pygame.K_LEFT,
    "direita": pygame.K_RIGHT,
    "baixo": pygame.K_DOWN,
}

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
    imagem = pygame.image.load("icones_telas/" + arquivo).convert_alpha()

    #corta o espaço vazio:
    imagem = imagem.subsurface(imagem.get_bounding_rect()).copy()

    #muda o tamanho sem deformar:
    proporcao = tamanho / max(imagem.get_width(), imagem.get_height())
    nova_largura = int(imagem.get_width() * proporcao)
    nova_altura = int(imagem.get_height() * proporcao)
    imagem = pygame.transform.smoothscale(imagem, (nova_largura, nova_altura))
    return imagem

#-------------- FUNCOES TELA 2-----------------------
def carregar_cabeca(arquivo, parte_de_cima, largura_caixa, altura_caixa):
    imagem = pygame.image.load("personagens/" + arquivo).convert_alpha()

    #corta o espaço vazio
    imagem = imagem.subsurface(imagem.get_bounding_rect(128)).copy()

    #fica so com a cabeca
    corte = int(imagem.get_height() * parte_de_cima)
    imagem = imagem.subsurface((0, 0, imagem.get_width(), corte)).copy()
    imagem = imagem.subsurface(imagem.get_bounding_rect(128)).copy()

    #muda o tamanho sem deformar:
    proporcao = min(largura_caixa / imagem.get_width(), altura_caixa / imagem.get_height())
    nova_largura = int(imagem.get_width() * proporcao)
    nova_altura = int(imagem.get_height() * proporcao)
    imagem = pygame.transform.smoothscale(imagem, (nova_largura, nova_altura))
    return imagem

#serve para personagens ainda nao desbloqueados
def criar_silhueta(imagem):
    # pinta de preto tudo o que não é transparente  
    mascara = pygame.mask.from_surface(imagem)
    silhueta = mascara.to_surface(setcolor=(0, 0, 0, 255), unsetcolor=(0, 0, 0, 0))
    return silhueta

def carregar_fundo(caminho, largura, altura):
    imagem = pygame.image.load(caminho).convert()

    # ajusta a imagem para o tamanho da tela
    imagem = pygame.transform.smoothscale(imagem, (largura, altura))
    return imagem

def carregar_cadeado(caminho, altura):
    imagem = pygame.image.load(caminho).convert_alpha()

    # corta o espaço vazio em volta
    imagem = imagem.subsurface(imagem.get_bounding_rect()).copy()

    # muda o tamanho sem deformar
    largura = int(imagem.get_width() * altura / imagem.get_height())
    imagem = pygame.transform.smoothscale(imagem, (largura, altura))
    return imagem

#---------------SOM------------------
musica_ligada = True

def alternar_musica():
    #liga ou desliga a musica
    global musica_ligada
    if musica_ligada:
        pygame.mixer.music.pause()
        musica_ligada = False
    else:
        pygame.mixer.music.unpause()
        musica_ligada = True