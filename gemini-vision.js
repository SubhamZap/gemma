const { GoogleGenerativeAI } = require("@google/generative-ai");
const { HarmBlockThreshold, HarmCategory } = require("@google/generative-ai");
const fs = require("fs");

const genAI = new GoogleGenerativeAI('AIzaSyAGvP2HuK1HNtrf96eARkUhjFP-YgfLwtU');

const safetySettings = [
    {
        category: HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold: HarmBlockThreshold.BLOCK_NONE,
    },
    {
        category: HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold: HarmBlockThreshold.BLOCK_NONE,
    },
    {
        category: HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold: HarmBlockThreshold.BLOCK_NONE
    },
    {
        category: HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold: HarmBlockThreshold.BLOCK_NONE
    },
];

const model = genAI.getGenerativeModel(
    { 
        model: "gemini-pro-vision",
        safetySettings: safetySettings,
        generationConfig: {
            temperature: 0
        } 
    }
);

console.log(model);

const prompt = `You have to categorize the image into 3 top-level category.
The top-level categories are 'Explicit Nudity', 'Non Explicity Nudity' and 'Violence'.
These top-level categories are divided into multiple second-level category.
For 'Explicit Nudity', second-level categories are 'Exposed Male Genitalia', 'Exposed Female Genitalia',
'Exposed Buttocks or Anus', 'Exposed Female Nipple', 'Explicit Sexual Activity', 'Sex Toys'.
For 'Non Explicity Nudity', second-level categories are 'Bare Back', 'Exposed Male Nipple', 'Partially Exposed Buttocks', 
'Partially Exposed Female Breast', 'Implied Nudity', 'Obstructed Female Nipple', 'Obstructed Male Genitalia', 
'Kissing on the Lips', 'Swimwear or Underwear'.
For 'Violence', second-level categories are 'Weapon', 'Violence', 'Self-Harm', 'Blood & Gore', 'Explosions and Blasts'.
If the image falls in any of the above second-level category, only return the result in json format:
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
}`;

function fileToGenerativePart(path, mimeType) {
    return {
      inlineData: {
            data: Buffer.from(fs.readFileSync(path)).toString("base64"),
            mimeType
        },
    };
}

async function run() {
  
    const imageParts = [
        fileToGenerativePart("Screenshot 2024-03-01 at 12.08.42 PM.png", "image/png"),
    ];
  
    const result = await model.generateContent([prompt, ...imageParts]);
    console.log({result});

    const response = await result.response;
    console.log({response});

    console.log(response.promptFeedback);
    console.log("blockReason" in response.promptFeedback);

    const text = response.text();

    return text
}

async function processMessage() {
    const text = await run();
    const image_response = JSON.parse(text)
    console.log(image_response);
    const topLevelCategory = image_response.topLevelCategory
    
    console.log(topLevelCategory);
}

processMessage();