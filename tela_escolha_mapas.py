import pygame
import functions
from functions import carregar_fundo, carregar_icone, criar_carta_mapa, desenhar_carta_mapa
from button import criar_botoes_mapas, desenhar_botao_seta, desenhar_botao_dourado
import random

#cores
branco = (255, 255, 255)
azul_escuro = (25, 25, 100)
dourado = (240, 190, 50)

#IMAGENS
arquivo_fundo = "cenarios/imagem_fundo_tela_inicial.png"
arquivo_seta_voltar = "voltar.png"
arquivo_seta_avancar = "avancar.png"
arquivo_som_ligado = "audio_ligado.png"
arquivo_som_desligado = "audio_desligado.png"

lista_mapas = [
    ("aflitos", "Estádio dos Aflitos", "cenarios/mapa_nautico.png"),
    ("cin", "Centro de Informática", "cenarios/mapa_cin.png"),
    ("raiz", "Futebol Raiz", "cenarios/mapa_rua.png"),
]

def tela_mapas(tela):
    largura = tela.get_width()
    altura = tela.get_height()
    relogio = pygame.time.Clock()

    #fontes
    fonte_titulo = pygame.font.SysFont("arial", 70, bold=True)
    fonte_nome = pygame.font.SysFont("arial", 30, bold=True)
    fonte_aleatorio = pygame.font.SysFont("arial", 32, bold=True)

    #botoes
    botao_voltar, botao_som, botao_aleatorio, botao_avancar = criar_botoes_mapas(largura, altura)

    #imagens
    fundo = carregar_fundo(arquivo_fundo, largura, altura)
    seta_voltar = carregar_icone(arquivo_seta_voltar, 45)
    seta_avancar = carregar_icone(arquivo_seta_avancar, 45)
    icone_som_ligado = carregar_icone(arquivo_som_ligado, 50)
    icone_som_desligado = carregar_icone(arquivo_som_desligado, 50)

    #titulo e texto do botao aleatorio
    retangulo_titulo = pygame.Rect(290, 66, 700, 110)
    texto_titulo = fonte_titulo.render("ESCOLHA O MAPA", True, branco)
    texto_aleatorio = fonte_aleatorio.render("MAPA ALEATÓRIO", True, branco)

    #cria uma "carta" para cada mapa - ira servir ppara podermos armazenar as informacoes de cada mapa e saber quando foi escolhido
    cartas = []
    for numero in range(len(lista_mapas)):
        id_mapa = lista_mapas[numero][0]
        nome = lista_mapas[numero][1]
        arquivo = lista_mapas[numero][2]
        cartas.append(criar_carta_mapa(numero, id_mapa, nome, arquivo, fonte_nome))

    escolhido = None

    while True:     #sempre se repetir ate clicar para sair
        mouse = pygame.mouse.get_pos()

        #eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:  #clicar para fechar o jogo
                return "sair", None

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_som.collidepoint(evento.pos):
                    functions.alternar_musica()

                elif botao_voltar.collidepoint(evento.pos):
                    return "voltar", None

                elif botao_aleatorio.collidepoint(evento.pos):
                    escolhido = random.randint(0, len(cartas) - 1)  #sorteia um mapa dos 3 disponiveis

                elif escolhido != None and botao_avancar.collidepoint(evento.pos):
                    return "pronto", cartas[escolhido]["id"]

                else:
                    for numero in range(len(cartas)):
                        if cartas[numero]["moldura"].collidepoint(evento.pos) or cartas[numero]["rotulo"].collidepoint(evento.pos):
                            escolhido = numero

        #fundo e titulo
        tela.blit(fundo, (0, 0))
        pygame.draw.rect(tela, dourado, retangulo_titulo, border_radius=15)
        pygame.draw.rect(tela, azul_escuro, retangulo_titulo, 5, border_radius=15)
        tela.blit(texto_titulo, texto_titulo.get_rect(center=retangulo_titulo.center))

        #botao de voltar
        desenhar_botao_seta(tela, botao_voltar, mouse, seta_voltar)

        #botao de som
        if functions.musica_ligada:
            icone_som = icone_som_ligado
        else:
            icone_som = icone_som_desligado
        desenhar_botao_seta(tela, botao_som, mouse, icone_som)

        #mapas
        for numero in range(len(cartas)):
            desenhar_carta_mapa(tela, cartas[numero], numero == escolhido, mouse)

        #botao mapa aleatorio
        desenhar_botao_dourado(tela, botao_aleatorio, mouse, texto_aleatorio)

        #seta para continuar (so aparece depois de escolher um mapa)
        if escolhido != None:
            desenhar_botao_seta(tela, botao_avancar, mouse, seta_avancar)

        pygame.display.update()
        relogio.tick(60)
            
