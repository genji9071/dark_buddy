cipher=['o_o_ooo',
'oo_o___',
'oo__o_o',
'ooo__o_',
'oo__o_o',
'_o_____',
'ooo_o__',
'oo_o___',
'oo__o_o',
'ooo__o_',
'oo__o_o',
'_o_____',
'oo_o__o',
'ooo__oo',
'_o_____',
'oo____o',
'_o_____',
'ooo_ooo',
'oo_o__o',
'oo_oo__',
'oo_oo__',
'_o_oo__',
'ooo_o__',
'oo_o___',
'oo__o_o',
'ooo__o_',
'oo__o_o',
'_o_____',
'oo_o__o',
'ooo__oo',
'_o_____',
'oo____o',
'_o_____',
'ooo_ooo',
'oo____o',
'oooo__o',
'_o_ooo_']

answer=''

for char in cipher:
    char = char.replace('o','1')
    char = char.replace('_','0')
    answer+=chr(int(char, 2))

print(answer)