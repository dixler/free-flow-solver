#!/usr/bin/env python

import sys

num_colors=int(sys.argv[1])
width=int(sys.argv[2])
print('vis')
is_sat=input()
if is_sat == 'sat':
    'satisfiable'
    sat=[(int(i)-1)%num_colors for i in input().split(' ') if i != '' and int(i) > 0]
    for i, val in enumerate(sat):
        if i % (width+2) == 0:
            print()
        print(val, end=' ')

else:
    'unsatisfiable'
