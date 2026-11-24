import pygame
import functions
from functions import carregar_personagem, carregar_icone
from button import criar_botoes_iniciais

#cores - RGB
branco = (255, 255, 255)
azul_escuro = (25, 25, 100)
dourado = (240, 190, 50)
cinza_claro = (240, 240, 250)
cinza_escuro = (160, 160, 187)

#imagem de fundo
arquivo_fundo = "cenarios/imagem_fundo_tela_inicial.png"

#personagens que aparecerão na tela inicial:
lista_personagens = [
    # lado esquerdo
    ("claude.png", 292, 464, 185, False),
    ("duque.png", 202, 528, 266, False),
    ("bolsonaro.png", 89, 640, 336, False),
    ("manuel_gomes.png", 0, 729, 342, False),
    # lado direito
    ("lalo.png", 816, 548, 306, True),
    ("elon_musk.png", 905, 604, 294, True),
    ("lula.png", 982, 673, 286, True),
    ("personagem_base_1.png", 1099, 757, 342, True),
]

def tela_inicial(tela):
    """Mostra a tela inicial"""
    largura = tela.get_width()
    altura = tela.get_height()
    relogio = pygame.time.Clock()   #define o fps da tela

    # Fontes
    fonte_titulo = pygame.font.SysFont("arial", 80, bold=True)
    fonte_botao = pygame.font.SysFont("arial", 30, bold=True)

    # Botões define o (x,y,largura, altura)
    botao_jogar, botao_loja, botao_som = criar_botoes_iniciais(largura)

    #Fundo
    fundo = pygame.image.load(arquivo_fundo).convert()
    fundo = pygame.transform.smoothscale(fundo, (largura, altura))

    #Personagens:
    personagens = []
    for arquivo, x, pes, alt, virar in lista_personagens:       #definindo lugar de cada personagem
        imagem = carregar_personagem(arquivo, alt, virar)
        y = pes - imagem.get_height()
        personagens.append((imagem, x, y))

    #Icones dos botoes:
    icone_jogar = carregar_icone("jogar.png", 85)
    icone_loja = carregar_icone("loja.png", 70)
    icone_som_ligado = carregar_icone("audio_ligado.png", 50)
    icone_som_desligado = carregar_icone("audio_desligado.png", 50)

    # Música de fundo
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load("music/musica_menu.mp3")
        pygame.mixer.music.play(-1)
    functions.aplicar_volume()

    while True:     #manterá a tela para sempre rodando
        mouse = pygame.mouse.get_pos()  #mostrara o mouse

        # Eventos
        for evento in pygame.event.get():       #se for clicado em fechar a aba, o jogo sai
            if evento.type == pygame.QUIT:
                return "sair"

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_jogar.collidepoint(evento.pos):    #clicou em jogar isso sera retornado para o nosso main.py
                    return "jogar"
                
                if botao_loja.collidepoint(evento.pos):     #clicou em loja isso sera retornado para o nosso main.py
                    return "loja"

                if botao_som.collidepoint(evento.pos):      #quer tirar o som do jogo
                    functions.alternar_musica()

        #Fundo
        tela.blit(fundo, (0, 0))    #definindo fundo quando inicia a tela

        #Personagem:
        for imagem, x, y in personagens:    #definindo personagens quando a tela é criada
            tela.blit(imagem, (x, y))

        #desenho do título:
        pygame.draw.rect(tela, dourado, (350, 35, 580, 110), border_radius=15)
        pygame.draw.rect(tela, azul_escuro, (350, 35, 580, 110), 5, border_radius=15)
        texto_titulo = fonte_titulo.render("CinCabeçada!", True, branco)
        tela.blit(texto_titulo, texto_titulo.get_rect(center=(largura // 2, 90)))

        #animação do botão jogar e desenho
        if botao_jogar.collidepoint(mouse):
            cor = cinza_escuro
        else:
            cor = cinza_claro
        pygame.draw.rect(tela, cor, botao_jogar, border_radius=20)
        tela.blit(icone_jogar, icone_jogar.get_rect(center=(botao_jogar.centerx, botao_jogar.centery - 18)))
        texto = fonte_botao.render("JOGAR", True, azul_escuro)
        tela.blit(texto, texto.get_rect(center=(botao_jogar.centerx, botao_jogar.bottom - 30)))

        #animação do botão loja e desenho
        if botao_loja.collidepoint(mouse):
            cor = cinza_escuro
        else:
            cor = cinza_claro
        pygame.draw.rect(tela, cor, botao_loja, border_radius=20)
        tela.blit(icone_loja, icone_loja.get_rect(center=(botao_loja.centerx, botao_loja.centery - 18)))
        texto = fonte_botao.render("LOJA", True, azul_escuro)
        tela.blit(texto, texto.get_rect(center=(botao_loja.centerx, botao_loja.bottom - 30)))

        #animação do botão silenciar e desenho dele
        if botao_som.collidepoint(mouse):
            cor = cinza_escuro
        else:
            cor = cinza_claro
        pygame.draw.rect(tela, cor, botao_som, border_radius=15)
        if functions.musica_ligada:
            icone = icone_som_ligado
        else:
            icone = icone_som_desligado
        tela.blit(icone, icone.get_rect(center=botao_som.center))

        pygame.display.update()
        relogio.tick(60)
