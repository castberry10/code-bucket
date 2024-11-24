from PIL import Image
import pytesseract

image_path = "./image.png"
image = Image.open(image_path)

extracted_text = pytesseract.image_to_string(image)

print(extracted_text)
