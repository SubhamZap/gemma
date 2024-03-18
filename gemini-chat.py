from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-pro-vision")


message = HumanMessage(
    content=[
        {
            "type": "text",
            "text": "What are the differences between the two images?",
        },
        {
            "type": "image_url",
            "image_url": "https://picsum.photos/seed/all/300/300"
        },
        {
            "type": "image_url",
            "image_url": "https://picsum.photos/seed/e/300/300"
        }
    ]
)


response = llm.invoke([message])
print(response.content)