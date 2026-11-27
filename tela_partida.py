from collections import deque
from random import choice, randint, randrange, shuffle

import pygame

from counters import DURACAO_PARTIDA, criar_placar
from functions import CONTROLES_JOGADOR_1, CONTROLES_JOGADOR_2, carregar_fundo, carregar_personagem


GRAVIDADE = 1300
VELOCIDADE_JOGADOR = 340
VELOCIDADE_PULO = 620
RESTITUICAO_BOLA = 0.45
VELOCIDADE_MINIMA_QUIQUE = 65
TAMANHO_COLECIONAVEL = 52

# A posição do piso acompanha a linha da frente do campo em cada imagem.
CENARIOS_PARTIDA = {
    "aflitos": ("objetos_partida/mapa_nautico_jogo.png", 612 / 768),
    "cin": ("objetos_partida/mapa_cin_jogo.png", 739 / 941),
    "raiz": ("objetos_partida/mapa_rua_jogo.png", 605 / 768),
}


class Jogador:
    def __init__(self, nome, controles, x, piso, virar):
        self.imagem = carregar_personagem(nome + ".png", 128, virar, alpha_minimo=128)
        self.imagem_agachada = pygame.transform.smoothscale(
            self.imagem, (self.imagem.get_width(), 84)
        )
        self.controles = controles
        self.x = x
        self.y = piso
        self.velocidade_y = 0
        self.agachado = False

    def pular(self, tecla, piso):
        if tecla == self.controles["pular"] and self.y == piso:
            self.velocidade_y = -VELOCIDADE_PULO

    def atualizar(self, teclas, dt, largura, piso):
        direcao = int(teclas[self.controles["direita"]]) - int(teclas[self.controles["esquerda"]])
        margem = self.imagem.get_width() // 2
        self.x = max(margem, min(largura - margem, self.x + direcao * VELOCIDADE_JOGADOR * dt))

        self.velocidade_y += GRAVIDADE * dt
        self.y += self.velocidade_y * dt
        if self.y >= piso:
            self.y = piso
            self.velocidade_y = 0
        self.agachado = self.y == piso and teclas[self.controles["baixo"]]

    @property
    def imagem_atual(self):
        return self.imagem_agachada if self.agachado else self.imagem

    def retangulo(self):
        return self.imagem_atual.get_rect(midbottom=(round(self.x), round(self.y)))

    def desenhar(self, tela):
        tela.blit(self.imagem_atual, self.retangulo())


class Bola:
    def __init__(self, x, y):
        imagem = pygame.image.load("objetos_partida/bola_jogo.png").convert_alpha()
        imagem = imagem.subsurface(imagem.get_bounding_rect())
        self.imagem = pygame.transform.smoothscale(imagem, (48, 48))
        self.x = x
        self.y = y
        self.velocidade_y = 0

    def atualizar(self, dt, piso):
        if self.y == piso and self.velocidade_y == 0:
            return

        self.velocidade_y += GRAVIDADE * dt
        self.y += self.velocidade_y * dt
        if self.y >= piso:
            self.y = piso
            quique = self.velocidade_y * RESTITUICAO_BOLA
            self.velocidade_y = -quique if quique >= VELOCIDADE_MINIMA_QUIQUE else 0

    def desenhar(self, tela):
        tela.blit(self.imagem, self.imagem.get_rect(midbottom=(self.x, round(self.y))))


class ColecionaveisPartida:
    def __init__(self, contadores, largura, piso, altura_jogador):
        self.contadores = contadores
        self.ativos = []
        self.agendados = deque()

        tipos = list(contadores)
        imagens = {tipo: self.carregar_imagem(tipo) for tipo in tipos}
        if randint(3, 4) == 4:
            tipos.append(choice(tipos))
        shuffle(tipos)

        altura_pulo = int(VELOCIDADE_PULO ** 2 / (2 * GRAVIDADE))
        limite_superior = max(0, piso - altura_jogador - altura_pulo)
        faixa = (DURACAO_PARTIDA - 10) // len(tipos)

        for indice, tipo in enumerate(tipos):
            segundo = randrange(5 + indice * faixa, 5 + (indice + 1) * faixa)
            imagem = imagens[tipo]
            area = imagem.get_rect(
                x=randint(0, largura - imagem.get_width()),
                y=randint(limite_superior, piso - imagem.get_height()),
            )
            self.agendados.append((segundo, tipo, imagem, area))

    @staticmethod
    def carregar_imagem(tipo):
        imagem = pygame.image.load(f"colecionaveis/imagens/{tipo}.png").convert_alpha()
        imagem = imagem.subsurface(imagem.get_bounding_rect(128))
        escala = TAMANHO_COLECIONAVEL / max(imagem.get_size())
        return pygame.transform.scale_by(imagem, escala)

    def atualizar(self, segundos_decorridos, jogadores):
        while self.agendados and self.agendados[0][0] <= segundos_decorridos:
            _, tipo, imagem, area = self.agendados.popleft()
            self.ativos.append((tipo, imagem, area))

        areas_jogadores = [jogador.retangulo() for jogador in jogadores]
        restantes = []
        for tipo, imagem, area in self.ativos:
            if area.collidelist(areas_jogadores) >= 0:
                self.contadores[tipo] += 1
            else:
                restantes.append((tipo, imagem, area))
        self.ativos = restantes

    def desenhar(self, tela):
        for _, imagem, area in self.ativos:
            tela.blit(imagem, area)


def tela_partida(tela, jogador1, jogador2, mapa_escolhido, contadores_colecionaveis):
    largura, altura = tela.get_size()
    arquivo_fundo, altura_relativa_piso = CENARIOS_PARTIDA[mapa_escolhido]
    fundo = carregar_fundo(arquivo_fundo, largura, altura)
    piso = round(altura * altura_relativa_piso)
    relogio = pygame.time.Clock()

    jogadores = (
        Jogador(jogador1, CONTROLES_JOGADOR_1, largura // 4, piso, virar=False),
        Jogador(jogador2, CONTROLES_JOGADOR_2, 3 * largura // 4, piso, virar=True),
    )
    bola = Bola(largura // 2, altura // 3)
    itens = ColecionaveisPartida(contadores_colecionaveis, largura, piso, jogadores[0].imagem.get_height())
    placar = criar_placar()
    fonte_placar = pygame.font.Font(None, 54)
    fonte_tempo = pygame.font.Font(None, 38)
    texto_placar = fonte_placar.render(
        f"{placar['jogador_1']} a {placar['jogador_2']}", True, (255, 255, 255)
    )
    fundo_placar = pygame.Rect(0, 0, 152, 88)
    fundo_placar.midtop = (largura // 2, 18)
    posicao_placar = texto_placar.get_rect(midtop=(fundo_placar.centerx, fundo_placar.top + 8))
    inicio = pygame.time.get_ticks()

    while True:
        dt = min(relogio.tick(60) / 1000, 1 / 30)
        segundos_decorridos = (pygame.time.get_ticks() - inicio) // 1000
        tempo_restante = max(0, DURACAO_PARTIDA - segundos_decorridos)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return "mapas"
                if tempo_restante > 0:
                    for jogador in jogadores:
                        jogador.pular(evento.key, piso)

        if tempo_restante > 0:
            teclas = pygame.key.get_pressed()
            for jogador in jogadores:
                jogador.atualizar(teclas, dt, largura, piso)
            bola.atualizar(dt, piso)
            itens.atualizar(segundos_decorridos, jogadores)

        tela.blit(fundo, (0, 0))
        pygame.draw.rect(tela, (25, 25, 25), fundo_placar, border_radius=8)
        tela.blit(texto_placar, posicao_placar)
        texto_tempo = fonte_tempo.render(f"{tempo_restante:02d}s", True, (255, 210, 90))
        posicao_tempo = texto_tempo.get_rect(midbottom=(fundo_placar.centerx, fundo_placar.bottom - 8))
        tela.blit(texto_tempo, posicao_tempo)
        for jogador in jogadores:
            jogador.desenhar(tela)
        bola.desenhar(tela)
        itens.desenhar(tela)
        pygame.display.flip()
