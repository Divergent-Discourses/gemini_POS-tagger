import vertexai
import vertexai.preview.generative_models as generative_models
from vertexai.generative_models import GenerativeModel

class VertexAI:
    generation_config = {
        "max_output_tokens": 2048,
        "temperature": 0,
        "top_p": 0.25,
    }

    safety_settings = {
        generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }

    # prompt = "In the following, there are segmented tokens of a Tibetan passage. Assign POS tags to each Tibetan segmented token according to Universal Dependency POS tags and display them in CoNLL-U format in which entries are separated by tabs (token number\ttoken\tEnglish translation\tPOS-Tag). Note that the following Tibetan passage may not necessarily be a complete sentence:\n"
    prompt = "In the following, there a Tibetan passage in which tokens are segmented by white spaces. Assign POS tags to each Tibetan segmented token according to Universal Dependency POS tags and display them in CoNLL-U format in which entries are separated by tabs (token number\ttoken\tEnglish translation\tPOS-Tag). Note that the following Tibetan passage may not necessarily be a complete sentence:\n"

    def __init__(self, model='gemini-1.5-pro-preview-0409', location='us-central1', prompt=prompt, generation_config=generation_config, safety_settings=safety_settings, project='tibetan-postagging'):
    # def __init__(self, model='gemini-1.0-pro-002', location='us-central1', prompt=prompt, generation_config=generation_config, safety_settings=safety_settings, project='tibetan-postagging'):
        self.model = model
        self.location = location
        self.prompt = prompt
        self.project = project
        self.generation_config = generation_config
        self.safety_settings = safety_settings

    def generate_prompts(self, text_list):
        prompt = self.prompt
        prompts = []
        for tokens in text_list:
            text = ''
            for token in tokens:
                text = text + token + ' '
            prompts.append(prompt + text)
        return prompts

    def send_prompt(self, prompt, location, model):
        vertexai.init(project=self.project, location=self.location)
        model = GenerativeModel(self.model)
        responses = model.generate_content(
            [prompt],
            generation_config=self.generation_config,
            safety_settings=self.safety_settings,
        )
        return responses.candidates[0].content.parts[0].text

    def get_response(self, prompt):
        response = []
        for p in prompt:
            split_p = p.split('\n')
            tibetan_passage = split_p[len(split_p) -1]
            print(tibetan_passage)
            try:
                res = self.send_prompt(p, self.location, self.model)
                response.append(res)
            except Exception as error:
                print('An error occurred:', error)

        return response