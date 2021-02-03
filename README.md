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
After cloning the repository, enter the project folder and type the following commands on the terminal
```
virtualenv venv --python=python3

source venv/bin/activate

pip install -r requirements.txt
```

When the installation is done, enter the src folder and on the terminal run:
```
python game.py ../charts/temp3.chart
```
Or any chart of your choice!

## References and helpful links:
- [List of songs to download](https://docs.google.com/spreadsheets/d/13B823ukxdVMocowo1s5XnT3tzciOfruhUVePENKc01o/htmlview?usp=drive_web)
- [Parsing Chart Files](https://www.reddit.com/r/CloneHero/comments/9acegu/question_parsing_chart_files_time_signatures_and/)
- [Forced Notes](https://www.reddit.com/r/CloneHero/comments/bnvu5i/what_are_forced_notes/)
- [Custom Charts](https://www.reddit.com/r/CloneHero/comments/8bkb0n/a_brief_history_of_custom_guitar_hero_chart/)
- [Format of Chart files](https://www.reddit.com/r/GuitarHero/comments/5zfyad/question_about_the_format_of_chart_files/)
- [Understanding Charts](https://www.reddit.com/r/CloneHero/comments/8pf0lj/help_interpreting_the_chart_files/)
