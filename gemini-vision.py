import pathlib
import textwrap

import google.generativeai as genai
import PIL.Image
from pathlib import Path
import os

GOOGLE_API_KEY = 'AIzaSyAGvP2HuK1HNtrf96eARkUhjFP-YgfLwtU'

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro-vision')

# img = PIL.Image.open('Screenshot 2024-02-29 at 6.26.25 PM.png')

prompt = """Explain the image in less than 10 wprds and Categorise the image as NSFW (Not Safe For Work) or not."""

safety_settings=[
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    }
]

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
            safety_settings=safety_settings, 
            stream=True
        )

        try:
            print("prompt_feedback\n", response.prompt_feedback)
            ratings = response.prompt_feedback.safety_ratings
            for element in ratings:
                if element.category > 6 and element.probability > 6:
                    print("Image does not comply with our Community guidelines")
                    nsfw = True

            response.resolve()
            classes = response.parts
            print(classes)
            if len(classes) > 0:
                for ele in classes:
                    try:
                        text = ele.text
                    except:
                        text = ''
                if text.lower().find('nsfw') != -1 and text.lower().find('not') != -1:
                    print('Image does not contains NSFW characters1')
                    nsfw = False
                elif text.lower().find('nsfw') != -1 or text.lower().find('not safe for work') != -1:
                    print('Warning: Image contains NSFW characters')
                    nsfw = True
                else:
                    print('Image does not contains NSFW characters2')
                    nsfw = False

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