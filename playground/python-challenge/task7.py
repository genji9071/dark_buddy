import requests
from PIL import Image

file = open('oxygen.png', 'wb')
im_data = requests.get('http://www.pythonchallenge.com/pc/def/oxygen.png')
file.write(im_data.content)
file.close()

image = Image.open('oxygen.png')

message = []
for i in range(0, 608, 7):
    message.append(list(image.getpixel((i, 43)))[0])

answer = ''
for i in message:
    answer += chr(i)
print(answer)
