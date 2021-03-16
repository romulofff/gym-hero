import itertools as it
import random


chart_filename = 'temp.chart'

offset = 0
resolution = 192
bpm = 120
max_resolution = 1920

difficulty = 'Expert'
difficulty = difficulty.title()


def print_chart_header(chart):
    print('[Song]', file=chart)
    print('{', file=chart)
    print('  Offset = {}'.format(offset), file=chart)
    print('  Resolution = {}'.format(resolution), file=chart)
    print('  Player2 = bass', file=chart)
    print('  Difficulty = 0', file=chart)
    print('  PreviewStart = 0', file=chart)
    print('  PreviewEnd = 0', file=chart)
    print('  Genre = "rock"', file=chart)
    print('  MediaType = "cd"', file=chart)
    print('}', file=chart)
    print('[SyncTrack]', file=chart)
    print('{', file=chart)
    print('  0 = TS 4', file=chart)
    print('  0 = B {}000'.format(bpm), file=chart)
    print('}', file=chart)
    print('[Events]', file=chart)
    print('{', file=chart)
    print('}', file=chart)
    print('[{}Single]'.format(difficulty), file=chart)
    print('{', file=chart)
    return


if __name__ == '__main__':
    
    chart = open(chart_filename, 'w')
    
    print_chart_header(chart)
    
    difficulties = ['Easy', 'Medium', 'Hard', 'Expert']
    

    num_actions = min(difficulties.index(difficulty) + 3, 5)
    actions = [list(i) for i in it.product([0, 1], repeat=num_actions)]

    step = resolution // 4

    for i in range(0, max_resolution+1, step):
        a = random.choice(actions)
        for j in range(len(a)):
            if a[j]:
                print('  {} = N {} 0'.format(i, j), file=chart)


    print('}', file=chart)

    chart.close()
