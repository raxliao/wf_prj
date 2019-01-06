def getcmd(file_name,wkey):
    icmd=0
    for line in open(file_name):
       if wkey in line:
           a=''.join(line.split())
           #print(a)
           index = a.find(':')

           wcmd=[a[index+1:]]
           #print(wcmd)

           return wcmd

    return