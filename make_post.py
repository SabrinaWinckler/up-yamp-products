from Quote2Image import Convert, GenerateColors, ImgObject
import cv2 
import numpy as np
import requests
import pandas as pd
from PIL import ImageFont, ImageDraw, Image  


infos_csv = pd.read_csv('infos1.csv')
data = pd.read_excel('saldo_tudo.xlsx')


width=1080
height=1080

print(f"{len(data)} Products")
for i in range(len(data)):
	isbn = data.loc[i]['ISBN']
	infos = infos_csv.loc[(infos_csv['ISBN'])==isbn]
	url = infos['image'].values[0]
	if(infos.empty):
		break
	if ("Not Found" in url):
		continue
	r = requests.get(url)
	with open(f'notes/{url.split("/")[-1]}','wb') as output:
		output.write(r.content)

	img = np.zeros((height,width,3), np.uint8)

	src = cv2.imread(f'notes/{url.split("/")[-1]}')
	dim = (width//2, height//2)

	resized = cv2.resize(src, dim, interpolation = cv2.INTER_AREA)

	img[:,:] = (255,255,255)
	position_x = 200
	position_y = 260
	img[position_x:height//2+position_x,position_y:width//2+position_y] = resized

	cv2.imwrite("temp.jpg", img=img)

	image = Image.open("temp.jpg")  

	draw = ImageDraw.Draw(image)  
	shape = [(40, 40), (width - 400, height - 10)]

	# use a truetype font  
	font = ImageFont.truetype("arial.ttf", 70)  

	draw.text((250, 100), "Livro Disponível", font=font,fill="black",align="center")  
	draw.line(shape, fill ="#FFC600", width = 10)
	font = ImageFont.truetype("arial.ttf", 55)  
	draw.text((580, 780), "Saiba mais", font=font,fill="#FFC600",align="left")  


	image.save(f"books/{url.split('/')[-1]}")  


	text  = F" {infos['description'].values[0]}"	
	author = data.loc[i]['AUTOR']
	# Generate Fg and Bg Color
	fg = 'white' 

	bg=ImgObject(image=f'notes/{url.split("/")[-1]}', brightness=80, blur=80)

	img=Convert(
		quote=text,
		author=author,
		fg=fg,
		bg=bg,
		font_size=40,
		font_type="arial.ttf",
		font_size_author=30,
		width=1080,
		height=1080,
			watermark_text="@adrianolivross",
			watermark_font_size=30
	)

	# Save The Image as a Png file
	img.save(f"posts/description-{url.split('/')[-1]}")