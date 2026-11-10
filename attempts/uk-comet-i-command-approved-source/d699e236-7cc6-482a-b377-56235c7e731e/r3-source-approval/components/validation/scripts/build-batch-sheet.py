from pathlib import Path
from PIL import Image
p=Path('/Users/georgele/Developer/Projects/tools/dev/formseed/projects/uk-comet-i-conversions/delivery/review')
s=Image.new('RGB',(3600,3150),'#eee')
for i,k in enumerate(['command','observation','crocodile']):
 im=Image.open(p/f'{k}-condition-sheet.png');assert im.size==(1200,3150);s.paste(im,(i*1200,0))
s.save(p/'batch-artwork-review-r3-fit2.png')
