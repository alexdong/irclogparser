from irclogparser import LogParser

f = open('sample.log', 'r')
for time, what, info in LogParser(f):
    if len(info) != 2: continue
    who, msg = info
    print time, what, (who, msg)
