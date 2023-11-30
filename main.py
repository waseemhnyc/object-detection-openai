from openai import OpenAI
from dotenv import load_dotenv
from utils import draw_circle, encode_image

import json

load_dotenv()

client = OpenAI()


def ask_gpt4_vision(system_instrutions, question, image_path):
    base64_image = encode_image(image_path)

    try:
        response = client.chat.completions.create(
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
        content = response.choices[0].message.content
        json_str = content.strip('`json\n') # Extract the JSON part from the string (remove the ```json and ``` at both ends)
        coordinates = json.loads(json_str) # Convert the JSON string into a Python dictionary

        print("Details:", coordinates["details"])

    except Exception as e:
        print(e)
        coordinates = {"x": 0, "y": 0, "details": ""}
    
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
draw_circle(image_path, coordinates)
