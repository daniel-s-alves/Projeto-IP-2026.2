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

def carregar_personagem(arquivo, altura, virar, alpha_minimo=1):
    imagem = pygame.image.load("personagens/" + arquivo).convert_alpha()

    #corta o espaço vazio em volta da imagem:
    imagem = imagem.subsurface(imagem.get_bounding_rect(alpha_minimo)).copy()

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

#-------------FUNCOES TELA 3--------------------
#carta dos mapas
branco = (255, 255, 255)
azul_escuro = (25, 25, 100)
dourado = (240, 190, 50)
cinza_claro = (240, 240, 250)
cinza_hover = (140, 140, 170)

#carta sera usada para termos as informações de cada mapa, como imagem, texto, moldura e rotulo
def criar_carta_mapa(numero, id_mapa, nome, arquivo, fonte):
    x = 52 + 400 * numero
    moldura = pygame.Rect(x, 262, 376, 220) #imagem
    rotulo = pygame.Rect(x, 494, 376, 54)   #nome do mapa

    #imagem do mapa
    imagem = carregar_fundo(arquivo, 364, 208)
    texto = fonte.render(nome, True, azul_escuro)

    #versao mais escura da imagem (usada quando o mouse esta em cima)
    imagem_escura = imagem.copy()
    imagem_escura.fill((150, 150, 150), special_flags=pygame.BLEND_RGB_MULT)

    carta = {
        "id": id_mapa,
        "imagem": imagem,
        "imagem_escura": imagem_escura,
        "texto": texto,
        "moldura": moldura,
        "rotulo": rotulo,
    }
    return carta

#e a desenhar_carta_mapa ira servir para desenharmos na tela um do lado do outro
def desenhar_carta_mapa(tela, carta, escolhido, mouse):
    imagem = carta["imagem"]
    if escolhido:
        cor_moldura = dourado
        cor_rotulo = dourado
    elif carta["moldura"].collidepoint(mouse) or carta["rotulo"].collidepoint(mouse):
        cor_moldura = cinza_hover
        cor_rotulo = cinza_hover
        imagem = carta["imagem_escura"]
    else:
        cor_moldura = branco
        cor_rotulo = cinza_claro

    #imagem do mapa
    pygame.draw.rect(tela, cor_moldura, carta["moldura"], border_radius=15)
    tela.blit(imagem, imagem.get_rect(center=carta["moldura"].center))
    pygame.draw.rect(tela, azul_escuro, carta["moldura"], 5, border_radius=15)

    #nome do mapa
    pygame.draw.rect(tela, cor_rotulo, carta["rotulo"], border_radius=15)
    pygame.draw.rect(tela, azul_escuro, carta["rotulo"], 4, border_radius=15)
    tela.blit(carta["texto"], carta["texto"].get_rect(center=carta["rotulo"].center))

#---------------SOM------------------
musica_ligada = True
VOLUME_MUSICA = 0.5

def aplicar_volume():
    if musica_ligada:
        pygame.mixer.music.set_volume(VOLUME_MUSICA)
    else:
        pygame.mixer.music.set_volume(0)

def alternar_musica():
    global musica_ligada
    musica_ligada = not musica_ligada
    aplicar_volume()
