import os
import codecs

filename = './chat.txt'
foldername = ''

gotNames = False
un1 = ''
un2 = ''

chatraw = []

def main():
    while True:
        global filename; global foldername
        
        inp = input('Default file name is "chat.txt" press enter to confirm or type new file name: ')
        if inp: filename = inp

        inp = input('Provide a name for the folder to store the results on: ')
        foldername = inp

        if makeChecks(): transform()

def transform():
    global chatraw

    os.mkdir(foldername)
    
    with codecs.open(filename, encoding='utf-8') as f:
        chatraw = f.readlines()

    print(f'chatraw has {len(chatraw)} elements')
    
    i = 1
    for l in chatraw:
        try:
            chatraw[i] = fixLine(chatraw[i])
        except:
            print('past chat by a line')
        i += 1

    with codecs.open(foldername+'/fixedChat.txt', encoding='utf-8', mode='w') as f:
        f.writelines(chatraw)

    print('----  Done with fixing chat  ----')

    calculate()

def calculate():
    msgs = getPercs()
    totalmsgs = msgs[0] + msgs[1]

    stats = [
        f'Total number of messages sent: {totalmsgs}.',
        f'{f"{un1}:":<20} {msgs[0]:>10} msgs |||  {int(100*(msgs[0]/totalmsgs))}%',
        f'{f"{un2}:":<20} {msgs[1]:>10} msgs |||  {int(100*(msgs[1]/totalmsgs))}%',
        f'Number of exceptions: {msgs[2]}'
    ]

    print('\n'+'\n'.join(stats)+'\n')

    with codecs.open(foldername+'/results.txt', encoding='utf-8', mode='w') as f:
        f.write('\n'.join(stats))

    print(f'Results successfully written to {foldername}/results.txt')
    input('Press Enter to Exit.')
    exit()


## HELPER FUNCTIONS

def makeChecks():
    okflag = True
    
    if not os.path.isfile(filename):
        okflag = False
        print(f'"{filename}" does not exist, make sure you type the name with the extension.')
    if os.path.isdir(foldername):
        okflag = False
        print(f'Folder with name "{foldername}" already exists.')
        
    print('\n\n')
    return okflag

def fixLine(line):
    global gotNames; global un1; global un2;
    newline = ''

    try:
        newline = line.split(' - ')[1]
        if not gotNames:
            name = newline.split(':')[0]
            if not un1:
                un1 = name
                print(f'first name: {un1}')
            if name != un1:
                un2 = name
                print(f'second name: {un2}')
                gotNames = True
    except IndexError:
        return line
    
    return newline

def getPercs():
    global chatraw
    
    count = 0
    count2 = 0
    exceptions = 0
    
    for l in chatraw:
        if l.startswith(un1):
            count += 1
        elif l.startswith(un2):
            count2 += 1
        else:
            exceptions += 1

    return [count, count2, exceptions]

main()
