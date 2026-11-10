from pathlib import Path
from PIL import Image,ImageDraw
import json
p=Path('/Users/georgele/Developer/Projects/tools/dev/formseed/projects/uk-comet-i-conversions/delivery/review')
for package in ['command','observation','crocodile']:
 sheet=Image.new('RGB',(1200,7*450),'#eee');d=ImageDraw.Draw(sheet)
 for i,condition in enumerate(['clean','D01','D02','D03','W01','W02','W03']):
  for j,view in enumerate(['front-left','rear-right']):
   im=Image.open(p/f'{package}-{condition}-{view}.png');im.thumbnail((600,425));sheet.paste(im,(j*600,i*450));d.text((j*600+10,i*450+429),f'{package} {condition} | {view}',fill='#111')
 sheet.save(p/f'{package}-condition-sheet.png')
