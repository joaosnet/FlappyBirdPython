import pygame  # Importa a biblioteca pygame
import os  # Importa a biblioteca os
import random  # Importa a biblioteca random

TELA_LARGURA = 500  # Define a largura da tela
TELA_ALTURA = 800  # Define a altura da tela

IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))  # Carrega a imagem do cano e redimensiona
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))  # Carrega a imagem do chão e redimensiona
IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))  # Carrega a imagem do fundo e redimensiona
IMAGENS_PASSARO = [  # Carrega as imagens do pássaro e redimensiona
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png'))),
]

pygame.font.init()  # Inicializa a biblioteca de fontes do pygame
FONTE_PONTOS = pygame.font.SysFont('arial', 50)  # Define a fonte para exibir os pontos

class Passaro:
    IMGS = IMAGENS_PASSARO  # Define as imagens do pássaro
    ROTACAO_MAXIMA = 25  # Define o ângulo máximo de rotação do pássaro
    VELOCIDADE_ROTACAO = 20  # Define a velocidade de rotação do pássaro
    TEMPO_ANIMACAO = 5  # Define o tempo de animação do pássaro

    def __init__(self, x, y):  # Inicializa a classe Passaro
        self.x = x  # Define a posição x do pássaro
        self.y = y  # Define a posição y do pássaro
        self.angulo = 0  # Define o ângulo de rotação do pássaro
        self.velocidade = 0  # Define a velocidade do pássaro
        self.altura = self.y  # Define a altura inicial do pássaro
        self.tempo = 0  # Define o tempo de animação do pássaro
        self.contagem_imagem = 0  # Define a contagem de imagens do pássaro
        self.imagem = self.IMGS[0]  # Define a imagem inicial do pássaro

    def pular(self):  # Método para fazer o pássaro pular
        self.velocidade = -10.5  # Define a velocidade de pulo do pássaro
        self.tempo = 0  # Reinicia o tempo de animação do pássaro
        self.altura = self.y  # Define a altura inicial do pássaro

    def mover(self):  # Método para mover o pássaro
        self.tempo += 1  # Incrementa o tempo de animação do pássaro
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo  # Calcula o deslocamento do pássaro

        if deslocamento > 16:  # Restringe o deslocamento máximo do pássaro
            deslocamento = 16
        elif deslocamento < 0:  # Restringe o deslocamento mínimo do pássaro
            deslocamento -= 2

        self.y += deslocamento  # Atualiza a posição y do pássaro

        if deslocamento < 0 or self.y < (self.altura + 50):  # Verifica se o pássaro está subindo
            if self.angulo < self.ROTACAO_MAXIMA:  # Verifica se o ângulo de rotação está abaixo do máximo
                self.angulo = self.ROTACAO_MAXIMA  # Define o ângulo de rotação máximo
        else:
            if self.angulo > -90:  # Verifica se o ângulo de rotação está acima do mínimo
                self.angulo -= self.VELOCIDADE_ROTACAO  # Atualiza o ângulo de rotação

    def desenhar(self, tela):  # Método para desenhar o pássaro na tela
        self.contagem_imagem += 1  # Incrementa a contagem de imagens do pássaro

        if self.contagem_imagem < self.TEMPO_ANIMACAO:  # Define a imagem do pássaro de acordo com a contagem de imagens
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO*4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0

        if self.angulo <= -80:  # Verifica se o pássaro está caindo
            self.imagem = self.IMGS[1]  # Define a imagem do pássaro em queda
            self.contagem_imagem = self.TEMPO_ANIMACAO*2  # Define a contagem de imagens para a imagem em queda

        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)  # Rotaciona a imagem do pássaro
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center  # Obtém o centro da imagem
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)  # Obtém o retângulo da imagem rotacionada
        tela.blit(imagem_rotacionada, retangulo.topleft)  # Desenha a imagem rotacionada na tela

    def get_mask(self):  # Método para obter a máscara de colisão do pássaro
        return pygame.mask.from_surface(self.imagem)  # Retorna a máscara de colisão da imagem do pássaro


class Cano:
    DISTANCIA = 200  # Define a distância entre os canos
    VELOCIDADE = 5  # Define a velocidade de movimento dos canos

    def __init__(self, x):  # Inicializa a classe Cano
        self.x = x  # Define a posição x do cano
        self.altura = 0  # Define a altura do cano
        self.pos_topo = 0  # Define a posição do topo do cano
        self.pos_base = 0  # Define a posição da base do cano
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)  # Inverte a imagem do cano para o topo
        self.CANO_BASE = IMAGEM_CANO  # Define a imagem do cano para a base
        self.passou = False  # Define se o pássaro já passou pelo cano
        self.definir_altura()  # Define a altura do cano

    def definir_altura(self):  # Método para definir a altura do cano
        self.altura = random.randrange(50, 450)  # Define uma altura aleatória para o cano
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()  # Define a posição do topo do cano
        self.pos_base = self.altura + self.DISTANCIA  # Define a posição da base do cano

    def mover(self):  # Método para mover o cano
        self.x -= self.VELOCIDADE  # Move o cano para a esquerda

    def desenhar(self, tela):  # Método para desenhar o cano na tela
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))  # Desenha o cano topo na tela
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))  # Desenha o cano base na tela

    def colidir(self, passaro):  # Método para verificar colisão entre o cano e o pássaro
        passaro_mask = passaro.get_mask()  # Obtém a máscara de colisão do pássaro
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)  # Obtém a máscara de colisão do cano topo
        base_mask = pygame.mask.from_surface(self.CANO_BASE)  # Obtém a máscara de colisão do cano base

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))  # Calcula a distância entre o topo do cano e o pássaro
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))  # Calcula a distância entre a base do cano e o pássaro

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)  # Verifica se houve colisão entre o topo do cano e o pássaro
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)  # Verifica se houve colisão entre a base do cano e o pássaro

        if base_ponto or topo_ponto:  # Verifica se houve colisão entre o pássaro e o cano
            return True  # Retorna True se houve colisão
        else:
            return False  # Retorna False se não houve colisão


class Chao:
    VELOCIDADE = 5  # Define a velocidade de movimento do chão
    LARGURA = IMAGEM_CHAO.get_width()  # Obtém a largura da imagem do chão
    IMAGEM = IMAGEM_CHAO  # Define a imagem do chão

    def __init__(self, y):  # Inicializa a classe Chao
        self.y = y  # Define a posição y do chão
        self.x1 = 0  # Define a posição x1 do chão
        self.x2 = self.LARGURA  # Define a posição x2 do chão

    def mover(self):  # Método para mover o chão
        self.x1 -= self.VELOCIDADE  # Move o chão para a esquerda
        self.x2 -= self.VELOCIDADE  # Move o chão para a esquerda

        if self.x1 + self.LARGURA < 0:  # Verifica se o chão saiu da tela
            self.x1 = self.x2 + self.LARGURA  # Reposiciona o chão para a direita da tela
        if self.x2 + self.LARGURA < 0:  # Verifica se o chão saiu da tela
            self.x2 = self.x1 + self.LARGURA  # Reposiciona o chão para a direita da tela

    def desenhar(self, tela):  # Método para desenhar o chão na tela
        tela.blit(self.IMAGEM, (self.x1, self.y))  # Desenha a imagem do chão na tela
        tela.blit(self.IMAGEM, (self.x2, self.y))  # Desenha a imagem do chão na tela


def desenhar_tela(tela, passaros, canos, chao, pontos):  # Função para desenhar a tela do jogo
    tela.blit(IMAGEM_BACKGROUND, (0, 0))  # Desenha a imagem de fundo na tela
    for passaro in passaros:  # Desenha os pássaros na tela
        passaro.desenhar(tela)
    for cano in canos:  # Desenha os canos na tela
        cano.desenhar(tela)

    texto = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255, 255, 255))  # Renderiza o texto de pontuação
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))  # Desenha o texto de pontuação na tela
    chao.desenhar(tela)  # Desenha o chão na tela
    pygame.display.update()  # Atualiza a tela


def desenhar_tela_game_over(tela, pontos):
    tela.blit(IMAGEM_BACKGROUND, (0, 0))  # Desenha a imagem de fundo na tela

    # Texto "Game Over"
    texto_game_over = FONTE_PONTOS.render("Game Over", 1, (255, 255, 255))
    pos_x_game_over = TELA_LARGURA / 2 - texto_game_over.get_width() / 2
    pos_y_game_over = TELA_ALTURA / 3 - texto_game_over.get_height() / 2
    tela.blit(texto_game_over, (pos_x_game_over, pos_y_game_over))

    # Pontuação final
    texto_pontos_final = FONTE_PONTOS.render(f"Pontuação final: {pontos}", 1, (255, 255, 255))
    pos_x_pontos = TELA_LARGURA / 2 - texto_pontos_final.get_width() / 2
    pos_y_pontos = TELA_ALTURA / 2 - texto_pontos_final.get_height() / 2
    tela.blit(texto_pontos_final, (pos_x_pontos, pos_y_pontos))

    # Instruções para reiniciar ou sair
    fonte_instrucoes = pygame.font.SysFont('arial', 30) # Fonte menor para instruções
    texto_instrucoes = fonte_instrucoes.render("Pressione 'R' para reiniciar ou 'Q' para sair", 1, (255, 255, 255))
    pos_x_instrucoes = TELA_LARGURA / 2 - texto_instrucoes.get_width() / 2
    pos_y_instrucoes = TELA_ALTURA * 2/3 - texto_instrucoes.get_height() / 2
    tela.blit(texto_instrucoes, (pos_x_instrucoes, pos_y_instrucoes))

    pygame.display.update()  # Atualiza a tela


def main():  # Função principal do jogo
    passaros = [Passaro(230, 350)]  # Cria uma lista de pássaros
    chao = Chao(730)  # Cria o chão
    canos = [Cano(700)]  # Cria uma lista de canos
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))  # Cria a tela do jogo
    pontos = 0  # Inicializa a pontuação
    relogio = pygame.time.Clock()  # Inicializa o relógio do jogo
    game_over = False  # Variável para controlar o estado de game over

    rodando = True  # Variável para controlar o loop principal do jogo
    while rodando:
        relogio.tick(30)  # Define a taxa de atualização da tela

        for evento in pygame.event.get():  # Verifica os eventos do jogo
            if evento.type == pygame.QUIT:  # Verifica se o evento é de fechar a janela
                rodando = False  # Encerra o loop principal do jogo
                pygame.quit()  # Encerra o pygame
                quit()  # Encerra o programa
            if evento.type == pygame.KEYDOWN:  # Verifica se o evento é de pressionar uma tecla
                if not game_over and evento.key == pygame.K_SPACE:  # Verifica se a tecla pressionada é a barra de espaço
                    for passaro in passaros:  # Faz cada pássaro pular
                        passaro.pular()
                elif game_over:
                    if evento.key == pygame.K_r:
                        # Reiniciar o jogo
                        passaros = [Passaro(230, 350)]
                        chao = Chao(730)
                        canos = [Cano(700)]
                        pontos = 0
                        game_over = False
                    elif evento.key == pygame.K_q:
                        # Sair do jogo
                        rodando = False
                        pygame.quit()
                        quit()

        if not game_over:
            # Lógica de movimento e colisão do jogo
            for passaro in passaros:  # Move os pássaros
                passaro.mover()
            chao.mover()  # Move o chão

            adicionar_cano = False  # Variável para controlar a adição de novos canos
            remover_canos = []  # Lista para armazenar os canos que serão removidos
            for cano in canos:  # Verifica a colisão dos pássaros com os canos
                for i, passaro in enumerate(passaros):
                    if cano.colidir(passaro):  # Verifica se houve colisão entre o pássaro e o cano
                        passaros.pop(i)  # Remove o pássaro da lista
                    if not cano.passou and passaro.x > cano.x:  # Verifica se o pássaro passou pelo cano
                        cano.passou = True  # Marca o cano como passado
                        adicionar_cano = True  # Habilita a adição de um novo cano
                cano.mover()  # Move o cano
                if cano.x + cano.CANO_TOPO.get_width() < 0:  # Verifica se o cano saiu da tela
                    remover_canos.append(cano)  # Adiciona o cano à lista de remoção

            if adicionar_cano:  # Verifica se deve adicionar um novo cano
                pontos += 1  # Incrementa a pontuação
                canos.append(Cano(600))  # Adiciona um novo cano à lista
            for cano in remover_canos:  # Remove os canos que saíram da tela
                canos.remove(cano)

            for i, passaro in enumerate(passaros):  # Verifica se os pássaros colidiram com o chão
                if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                    passaros.pop(i)

            if not passaros: # Se a lista de pássaros está vazia
                game_over = True

            desenhar_tela(tela, passaros, canos, chao, pontos)  # Desenha a tela do jogo
        else:
            # Lógica da tela de Game Over
            desenhar_tela_game_over(tela, pontos) # Função a ser criada

if __name__ == '__main__':
    main()  # Chama a função principal do jogo
