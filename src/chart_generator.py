import itertools as it
import random
import argparse


parser = argparse.ArgumentParser(
    description='Generate random charts.')

parser.add_argument(
    '-f', '--chart-filename',
    metavar='N',
    help='Chart filename. [Default="temp.chart"]',
    default='temp.chart')
parser.add_argument(
    '-o', '--offset',
    type=int,
    metavar='N',
    help='Song offset. [Default=0]',
    default=0)
parser.add_argument(
    '-r', '--resolution',
    type=int,
    metavar='N',
    help='Song resolution. [Default=192]',
    default=192)
parser.add_argument(
    '-b', '--bpm',
    type=int,
    metavar='N',
    help='Song resolution. [Default=120]',
    default=120)
parser.add_argument(
    '-m', '--max-ticks',
    type=int,
    metavar='N',
    help='Maximum allowed number of ticks (exclusive). [Default=1921]',
    default=1921)
parser.add_argument(
    '-d', '--difficulty',
    metavar='DIFF',
    help='Song difficulty. Also defines the number of possible notes. [Default="Easy"].',
    default='Easy')


args = parser.parse_args()


difficulty = args.difficulty.title()


def print_chart_header(chart):
    print('[Song]', file=chart)
    print('{', file=chart)
    print('  Offset = {}'.format(args.offset), file=chart)
    print('  Resolution = {}'.format(args.resolution), file=chart)
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
    print('  0 = B {}000'.format(args.bpm), file=chart)
    print('}', file=chart)
    print('[Events]', file=chart)
    print('{', file=chart)
    print('}', file=chart)
    print('[{}Single]'.format(difficulty), file=chart)
    print('{', file=chart)
    return


if __name__ == '__main__':
    
    chart = open(args.chart_filename, 'w')
    
    print_chart_header(chart)
    
    difficulties = ['Easy', 'Medium', 'Hard', 'Expert']
    

    num_actions = min(difficulties.index(args.difficulty) + 3, 5)
    actions = [list(i) for i in it.product([0, 1], repeat=num_actions)]

    step = args.resolution // 4

    for i in range(0, args.max_ticks+1, step):
        a = random.choice(actions)
        for j in range(len(a)):
            if a[j]:
                print('  {} = N {} 0'.format(i, j), file=chart)


    print('}', file=chart)

    chart.close()
