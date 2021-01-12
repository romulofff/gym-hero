# GH-PyGame
## Artigos / TCC
### Breve descrição:

Criar um clone de guitar hero (tipo flash hero, clone hero, etc). A ideia é que ele funcione com os arquivos das músicas que já tem disponíveis na internet (isso vai ser provavelmente a parte mais difícil de fazer). 

Em cima desse clone desenvolver um "Ambiente de Aprendizagem por Reforço" que é uma forma de extrair e enviar informações pro jogo.

Informações para serem retornadas:


+ Nota Acertada
+ Quantas notas em seguida
+ Pontuação total

Tendo esse ambiente, desenvolver um agente de aprendizagem por reforço que aprenda a jogar guitar hero :)


## How to run it:
Após clonar o repositório, entre na pasta do projeto usando um terminal e digite os seguintes comandos:
```
virtualenv venv --python=python3

source venv/bin/activate

pip install -r requirements.txt
```

Em seguida entre na pasta src e digite:
```
python game.py
```

## References:
- [List of songs to download](https://docs.google.com/spreadsheets/d/13B823ukxdVMocowo1s5XnT3tzciOfruhUVePENKc01o/htmlview?usp=drive_web)
