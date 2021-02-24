# TODO:

### MÚSICA:
Preciso ler um 'chart' correspondente a alguma música e reproduzir as notas e os sons.
- Ler os charts [FEITO]
- Criar e Renderizar notas de acordo com o chart [FEITO]
- Separar a lista de colisão da lista de notas renderizadas
- Música deve tocar junto [FEITO]
- Implementar notas longas
- Implementar notas estrela
- Implementar o TS
- Ajustar o BPM

### DETECÇÃO DE COLISÃO [FEITO]:
Preciso detectar quando a nota colidir com o botão. Isso deve acontecer, caso o jogador clique no botão correto quando a nota estiver passando pelo botão.
- Reconhecer as teclas ('a', 's', 'd', 'f', 'g') referentes aos botões [FEITO] 
- Detectar a colisão [FEITO]

### SCORE POINTS:
- Atualizar valor quando houver colisão [FEITO]
- Opção para diminuir caso o jogador erre
- Implementar multiplicador (a cada 10 notas aumenta em 1, máximo x4) [FEITO]

### PÚBLICO:
A torcida no Guitar Hero original era a sua "vida", se o jogador errar muito, o público fica insatisfeito e te expulsa do palco (com vaias e xingamentos)
- Implementar Torcida [FEITO]

### AMBIENTE GYM:
- Implementar ambiente GYM

### TESTE DE FEATURES
- Poder retornar o array de screen buffer, label buffer e depth buffer (se tiver)
    - Screen buffer --> **OK**
    - Label buffer --> ?
- Vários tipos de label buffer (só foreground/background, 1 valor pra cada traste, 1 valor pra cada elemento na tela, ...)
- Desligar a renderização (com duas oopções: 1. mantém o buffer mas não mostra na tela e 2. sequer cria o buffer)
    - Mantendo buffer --> **OK**
- Modo jogador (usando input do teclado/controle) e modo COM --> **OK**
- Modificar o visual do jogo facilmente
- Mudar os valores de recompensa, score multiplicador, ..., facilmente (arquivo de configs, por ex)
- Resolução custom --> **OK**
- Renderização em vários modos de imagem (rgb, bgr, grayscale, ...)
- Instalação via pip
- Modo multiplayer


<!-- - [Subreddit do Clone Hero](https://www.reddit.com/r/CloneHero/comments/7caylm/how_to_install_clone_hero_and_all_the_files_you/) -->
