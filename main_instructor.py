from utils import draw_circle, encode_image
import instructor
from openai import OpenAI
from pydantic import BaseModel, Field

from dotenv import load_dotenv

load_dotenv()

client = instructor.patch(OpenAI())

class ObjectDetectionFound(BaseModel):
    x: int  = Field(default=0)
    y: int = Field(default=0)
    details: str = Field(default='')

def ask_gpt4_vision(system_instrutions, question, image_path):
    base64_image = encode_image(image_path)

    object_found = client.chat.completions.create(
        response_model=ObjectDetectionFound,
        model="gpt-4-vision-preview",
        max_tokens=100,
        messages=[
            {
                "role": "system", 
                "content": system_instrutions
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        },
                    },
                ],
            }
        ],
    )
    print(object_found)
    coordinates = object_found.x, object_found.y
    
    return coordinates

image_path = "assets/kitten-and-puppy.webp"
# image_path = "assets/puppy.jpg"

system_instructions = """
As an image recognition expert, your task is to analyze images and provide 
output in JSON format with the following keys only: 'x', 'y', and 'details'.

- 'x' and 'y' should represent the coordinates of the center of the detected 
object within the image, with the reference point [0,0] at the top left corner.
- 'details' should provide a brief description of the object identified in the image.

For cases involving the identification of people or animals, focus on locating and 
identifying the face of the person or animal. Ensure that the given 'x' and 'y' 
coordinates correspond to the center of the identified face.

Please adhere strictly to this output structure:
{
  "x": value,
  "y": value,
  "details": "Description"
}

Note: Do not include any additional data or keys outside of what has been specified.
"""

question = "Detect Dog"

coordinates = ask_gpt4_vision(system_instructions, question, image_path)
# draw_circle(image_path, coordinates)
