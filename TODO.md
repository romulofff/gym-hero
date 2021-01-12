# TODO:

### MÚSICA:
Preciso ler um 'chart' correspondente a alguma música e reproduzir as notas e os sons.
- Ler os charts [FEITO]
- As notas são renderizadas no tempo certo de acordo com o chart [FEITO]
- Falta colocar a música pra tocar junto

<!-- - [Subreddit do Clone Hero](https://www.reddit.com/r/CloneHero/comments/7caylm/how_to_install_clone_hero_and_all_the_files_you/) -->
<!-- - [Lista de músicas para download](https://docs.google.com/spreadsheets/d/13B823ukxdVMocowo1s5XnT3tzciOfruhUVePENKc01o/htmlview?usp=drive_web) -->

### DETECÇÃO DE COLISÃO [FEITO]:
Preciso detectar quando a nota colidir com o botão. Isso deve acontecer, caso o jogador clique no botão correto quando a nota estiver passando pelo botão.
- Reconhecer as teclas ('a', 's', 'd', 'f', 'g') referentes aos botões FEITO 
- Detectar a colisão FEITO

### SCORE POINTS:
- Melhorias gerais
- Atualizar valor quando houver colisão

### JANELA DESLIZANTE:
- Criar imagem de track
- Criar janela delizante
- Transformar perspectiva
    - Retânagulo --> Trapézio

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


### Lógica de Colisão (Sugestão Hyuan)
Para cada nota e Para cada traste
No intervalo de tempo em que a nota e o traste estão colidindo (bouding boxes cruzando) ativar varíavel de estado booleana. 
- Se a variável de estado E a tecla pressionada: HIT OK
- Se a variável de estado E não a tecla pressionada: HIT MISS
- Se não a variável de estado E a tecla pressionada: HIT MISS
- Se não a variável de estado E não a tecla pressionada: PASS