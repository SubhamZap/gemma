import pathlib
import textwrap

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import PIL.Image
from pathlib import Path
import os
import json
from dotenv import load_dotenv
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_VISION_API")

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel(
    'gemini-pro-vision',
    generation_config={'temperature':0},
    safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }
    )
print(model)

# img = PIL.Image.open('Screenshot 2024-02-29 at 6.26.25 PM.png')

prompt = """You have to categorize the image into 3 top-level category.
The top-level categories are `Explicit Nudity`, `Non Explicity Nudity` and `Violence`.
These top-level categories are divided into multiple second-level category.
For `Explicit Nudity`, second-level categories are `Exposed Male Genitalia`, `Exposed Female Genitalia`,
`Exposed Buttocks or Anus`, `Exposed Female Nipple`, `Explicit Sexual Activity`, `Sex Toys`.
For `Non Explicity Nudity`, second-level categories are `Bare Back`, `Exposed Male Nipple`, `Partially Exposed Buttocks`, 
`Partially Exposed Female Breast`, `Implied Nudity`, `Obstructed Female Nipple`, `Obstructed Male Genitalia`, 
`Kissing on the Lips`, `Swimwear or Underwear`.
For `Violence`, second-level categories are `Weapon`, `Violence`, `Self-Harm`, `Blood & Gore`, `Explosions and Blasts`.
If the image falls in any of the above second-level category, then generate a json in the below format:
{
    "explanation": "Explan the image in less than 10 words.",
    "topLevelCategory": "Violence",
    "secondLevelCategory": "Self-Harm",
    "confidenceScore": 99.99
}
If the image does not fall in any of the above second-level category, then return the result in json format:
{
    "explanation": "Explan the image in less than 10 words.",
    "topLevelCategory": "Others",
    "secondLevelCategory": "Others",
    "confidenceScore": 99.99
}"""

# response = model.generate_content([prompt, img], stream=True)
# print(response.prompt_feedback)
# ratings = response.prompt_feedback.safety_ratings
# print(ratings)
# for element in ratings:
#     print(element)
#     print(element.category)
#     print(element.probability)
# response.resolve()

# try:
#     print(response.parts)

#     if len(response.parts) > 0:
#         for element in response.parts:
#             try:
#                 text = element.text
#             except:
#                 text = ''
#         if text.lower().find('nsfw') != -1 and text.lower().find('not') != -1:
#             print('Image does not contains NSFW characters')
#         elif text.lower().find('nsfw') != -1 or text.lower().find('not safe for work') != -1:
#             print('Warning: Image contains NSFW characters')

#     else:
#         print('Image does not contains NSFW characters')

# except response.prompt_feedback as e:
#     print(e)


def isNSFWImage(imagePathList):
    nsfw = False
    for imagePath in imagePathList:
        image = PIL.Image.open(imagePath)
        print(imagePath)

        response = model.generate_content(
            [prompt, image],  
            stream=True
        )

        try:
            print("prompt_feedback\n", response.prompt_feedback)

            # ratings = response.prompt_feedback.safety_ratings
            
            # for element in ratings:
            #     if element.category > 6 and element.probability > 1:
            #         nsfw = True
            #         print("Image does not comply with our Community guidelines")
            #         break

            response.resolve()
            classes = response.parts
            print(classes)
            if len(classes) > 0 and nsfw == False:
                for ele in classes:
                    try:
                        text = ele.text
                    except:
                        text = ''
                response = json.loads(text)
                print(response)
                for key, val in response.items():
                    print(key, val)

                if response['topLevelCategory'] == 'Explicit Nudity':
                    print('Image does not comply with our Community guidelines')
                
                elif response['topLevelCategory'] == 'Non Explicity Nudity':
                    print('Warning: Image might have sensitivity')
                
                else:
                    print('Image comply with our Community guidelines')

                # if text.lower().find('nsfw') != -1 and text.lower().find('not') != -1:
                #     print('Image does not contains NSFW characters1')
                #     nsfw = False
                # elif text.lower().find('nsfw') != -1 or text.lower().find('not safe for work') != -1:
                #     print('Warning: Image contains NSFW characters')
                #     nsfw = True
                # else:
                #     print('Image does not contains NSFW characters2')
                #     nsfw = False

            else:
                print('Image does not contains NSFW characters3')
                nsfw = False
            
        except Exception as e:
            print("Prompt feedback response error: ", e)
            print("Image might contain NSFW elements")
            nsfw = True

cwd = os.getcwd()
images = Path(cwd).glob("*.png")
isNSFWImage(imagePathList=images)