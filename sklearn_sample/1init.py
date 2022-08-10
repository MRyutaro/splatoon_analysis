import pytesseract
from PIL import Image

url_img = 'config/image/5.png'
img = Image.open(url_img)
number = pytesseract.image_to_string(img)
print(number)