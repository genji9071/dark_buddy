from fontTools.ttLib import TTFont

font = TTFont('/Users/tianhaozhang/Downloads/字由芳华体.otf')
font_code = str(font.get('name').__dict__.get('names')[6])
print(font_code)
