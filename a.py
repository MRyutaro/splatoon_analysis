from PIL import Image
import pytesseract
img = Image.open("./data/image/an.png", "r")
number = pytesseract.image_to_string(img)
print(number)
