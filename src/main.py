# reference
# https://www.youtube.com/watch?v=LRQH4JBUYC8
# https://console.cloud.google.com/vertex-ai/generative/language/create/text?hl=de&project=tibetan-postagging
# Cookbook: https://github.com/google-gemini/cookbook?tab=readme-ov-file
# Request a higher quota: https://console.cloud.google.com/iam-admin/quotas?walkthrough_id=bigquery--bigquery_quota_request&project=tibetan-postagging

# TODO: change the output_dir to '/output/' and empty the '/conllu/'
# TODO: modify export_conllu, so that it exports only files that are not empty.

from botok import WordTokenizer
from botok.config import Config
from gemini import VertexAI
from module import load_texts, divide_texts, botok_segment, extract_conllu, export_conllu, delete_file
import time
import os

base_dir = os.getcwd()
text_dir = base_dir + '/text/'
output_dir = base_dir + '/output/'

def main():
    texts = load_texts(text_dir)
    split_texts = divide_texts(texts)
    vertex = VertexAI()

    # load Botok
    config = Config(dialect_name="custom")
    wt = WordTokenizer(config=config)

    cnt = 1
    for text_name, text in split_texts.items():
        print(cnt, ':', text_name)
        segmented_text = botok_segment(wt, text)

        # get pos-tagged sentence
        start = time.time()
        prompts = vertex.generate_prompts(segmented_text)
        print('There are', len(prompts), 'prompts')
        res = vertex.get_response(prompt=prompts)

        # measure elapsed time
        end = time.time()
        print('elapsed time:', end - start)

        # extract conllu
        conllu = extract_conllu(res)

        # export conllu
        conllu_name = output_dir + text_name + '.conllu'
        export_conllu(conllu, conllu_name)

        # delete the text file that has been processed.
        file_path = text_dir + text_name + '.txt'
        delete_file(file_path)
        cnt = cnt + 1

if __name__ == '__main__':
    main()