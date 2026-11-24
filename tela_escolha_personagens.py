import pygame
from functions import carregar_cabeca, carregar_cadeado, carregar_icone, carregar_fundo
from functions import criar_silhueta
from button import desenhar_botao_seta

#cores que serao utilizadas
branco = (255, 255, 255)
azul_escuro = (18, 35, 91)
cinza_nome = (192, 192, 200)
cores_jogadores = [(40, 110, 230), (220, 60, 60)] # cor vermelha para o jogador 1 e cor azul pro jogador 2

#IMAGENS
arquivo_fundo = "cenarios/fundo_escolha_personagens.png"
arquivo_cadeado = "icones_telas/cadeado.png"
arquivo_seta_voltar = "voltar.png"
arquivo_seta_avancar = "avancar.png"

aumento = 1.12     #efeito de a cabeça crescer quando o mouse passar em cima

#lista personagens
#cada personagem terá um numero no final que diz quantos % aparecera do personagem 
lista_personagens = [
    ("personagem_base_1", False, 0.70),
    ("personagem_base_2", False, 0.63),
    ("personagem_base_3", False, 0.62),
    ("personagem_base_4", False, 0.63),
    ("personagem_base_5", False, 0.63),
    ("bolsonaro", True, 0.74),
    ("claude", True, 0.73),
    ("duque", True, 0.73),
    ("elon_musk", True, 0.76),
    ("jane", True, 0.73),
    ("lalo", True, 0.73),
    ("lula", True, 0.80),
    ("manuel_gomes", True, 0.79),
    ("papai_noel", True, 0.73),
]

def tela_personagem(tela):
    largura = tela.get_width()
    altura = tela.get_height()
    relogio = pygame.time.Clock()

    #fontes
    fonte_titulo = pygame.font.SysFont("arial", 38, bold=True)
    fonte_nome = pygame.font.SysFont("arial", 16, bold=True)
    fonte_jogador = pygame.font.SysFont("arial", 18, bold=True)

    #botoes
    botao_voltar = pygame.Rect(23, 21, 80, 80)
    botao_avancar = pygame.Rect(0, 0, 80, 80)
    botao_avancar.center = (largura // 2, altura - 70)

    #IMAGENS:
    fundo = carregar_fundo(arquivo_fundo, largura, altura)
    cadeado = carregar_cadeado(arquivo_cadeado, 50)
    seta_voltar = carregar_icone(arquivo_seta_voltar, 45)
    seta_avancar = carregar_icone(arquivo_seta_avancar, 45)

    #titulos:
    titulos = [
        fonte_titulo.render("ESCOLHA PERSONAGEM 1", True, azul_escuro),
        fonte_titulo.render("ESCOLHA PERSONAGEM 2", True, azul_escuro),
        fonte_titulo.render("PRONTO PARA JOGAR!", True, azul_escuro),
    ]

    #etiqueta J1 e J2 na escolha de personagens:
    etiquetas = [
        fonte_jogador.render("J1", True, branco),
        fonte_jogador.render("J2", True, branco),
    ]

    # Cria uma "carta" para cada personagem - vai servoir para termos as informações daquela carta
    cartas = []
    for numero in range(len(lista_personagens)):
        nome = lista_personagens[numero][0]
        bloqueado = lista_personagens[numero][1]
        parte_de_cima = lista_personagens[numero][2]

        # Posição: 7 por linha para ficar centralizado na tela
        coluna = numero % 7
        linha = numero // 7
        x = 127 + 171 * coluna
        y = 282 + 274 * linha

        #imagem da cabeca e o nome - os bloqueados ficam pretos e com o nome cinza
        imagem = carregar_cabeca(nome + ".png", parte_de_cima, 170, 137)
        if bloqueado:
            imagem = criar_silhueta(imagem)
            texto = fonte_nome.render(nome, True, cinza_nome)
        else:
            texto = fonte_nome.render(nome, True, azul_escuro)

        # Cabeça um pouco maior, usada quando o mouse está em cima
        nova_largura = int(imagem.get_width() * aumento)
        nova_altura = int(imagem.get_height() * aumento)
        imagem_grande = pygame.transform.smoothscale(imagem, (nova_largura, nova_altura))

        # Área onde o mouse pode clicar
        area = pygame.Rect(0, 0, 170, 137)
        area.center = (x, y)

        carta = {
            "nome": nome,
            "bloqueado": bloqueado,
            "imagem": imagem,
            "imagem_grande": imagem_grande,
            "texto": texto,
            "area": area,
        }
        cartas.append(carta)

    escolhidos = []
    while True:     #sempre vai se repetir ate a pessoa sair do jogo
        mouse = pygame.mouse.get_pos()

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair", None

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_voltar.collidepoint(evento.pos):
                    # Se já escolheram alguém, desfaz a última escolha
                    if len(escolhidos) == 0:
                        return "voltar", None
                    escolhidos.pop()

                elif len(escolhidos) == 2:  #se os dois tiverem sido escolhidos
                    if botao_avancar.collidepoint(evento.pos):
                        return "pronto", (escolhidos[0], escolhidos[1])

                else:   #se ainda nao tiverem os dois sido escolhidos
                    for carta in cartas:
                        if carta["area"].collidepoint(evento.pos) and not carta["bloqueado"]:
                            escolhidos.append(carta["nome"])
                            break

        #fundo e titulo
        tela.blit(fundo, (0, 0))
        titulo = titulos[len(escolhidos)]
        tela.blit(titulo, titulo.get_rect(center=(largura // 2, 45)))

        # Botão de voltar
        desenhar_botao_seta(tela, botao_voltar, mouse, seta_voltar)

        #personagens:
        for carta in cartas:
            area = carta["area"]
            figura = carta["imagem"]    #usa a cebca maior se o mouse estiver em cima
            if area.collidepoint(mouse) and not carta["bloqueado"] and len(escolhidos) < 2:
                figura = carta["imagem_grande"]

            tela.blit(figura, figura.get_rect(center=area.center))

            # Cadeado e nome
            if carta["bloqueado"]:
                tela.blit(cadeado, cadeado.get_rect(center=(area.centerx, area.centery + 5)))
            tela.blit(carta["texto"], carta["texto"].get_rect(center=(area.centerx, area.centery + 103)))

            # Moldura colorida no personagem que cada jogador escolheu
            for jogador in range(len(escolhidos)):
                if escolhidos[jogador] == carta["nome"]:
                    moldura = area.inflate(-10 - 12 * jogador, -12 * jogador)
                    pygame.draw.rect(tela, cores_jogadores[jogador], moldura, 4, border_radius=14)

                    etiqueta = etiquetas[jogador]

                    fundo_etiqueta = etiqueta.get_rect(topleft=(moldura.left + 8 + jogador * 40, moldura.top + 6))
                    pygame.draw.rect(tela, cores_jogadores[jogador], fundo_etiqueta.inflate(10, 4), border_radius=6)
                    tela.blit(etiqueta, fundo_etiqueta)

        #Seta para continuar so aparecer depois de escolher dois personagens
        if len(escolhidos) == 2:
            desenhar_botao_seta(tela, botao_avancar, mouse, seta_avancar)

        pygame.display.update()
        relogio.tick(60)