class Note:
    def __init__(self):
        self.start = 0
        self.type = 0 # 0 = normal note, 1 = star
        self.color = 0
        self.duration = 0
        
    def __repr__(self):
        return f'<Note start:{self.start} type:{self.type} color:{self.color} duration:{self.duration}>'
        
    def __str__(self):
        return f'Note: start={self.start}, type={self.type}, color={self.color}, duration={self.duration}'
        
        

# read file
f = open('../charts/temp.chart', 'r')
chart_data = f.read().replace('  ', '')
f.close()

search_string = '[ExpertSingle]\n{\n'
inf = chart_data.find(search_string)
sup = chart_data[inf:].find('}')

sup += inf
inf += len(search_string)

notes_data = chart_data[inf:sup]

notes = []

for line in notes_data.splitlines():
    n = line.split()
    
    if (n[2] == 'N'):
        note = Note()
        note.start = int(n[0])
        note.color = int(n[3])
        note.duration = int(n[4])
        notes.append(note)

for n in notes:
    print(n)

