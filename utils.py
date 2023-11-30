import base64
from PIL import Image, ImageDraw

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
def draw_circle(image_path, coordinates):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    radius = 5
    x = coordinates['x']
    y = coordinates['y']

    draw.ellipse(
        [(x - radius, y - radius), (x + radius, y + radius)], 
        outline='red', 
        width=4
    )

    new_image_path = image_path.split('.')[0] + '_detected.' + image_path.split('.')[1]

    image.save(new_image_path)
