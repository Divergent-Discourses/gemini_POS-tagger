from botok.config import Config
from botok import WordTokenizer
import os
from conllu import parse
from module import load_conllu, check_tags, modify_pos_tag, add_lemmas, generate_conllu, add_entries, export_conllu

def main():
    base_dir = os.getcwd()
    output_conllu = base_dir + '/output/'
    output_dir = base_dir + '/conllu/'
    file_names = [file for file in os.listdir(output_conllu) if file.endswith('.conllu')]

    # load Botok
    config = Config(dialect_name="custom")
    wt = WordTokenizer(config=config)

    for file_name in file_names:
        print(file_name)
        conllu_path = output_conllu + file_name

        # load conllu
        conllu = load_conllu(conllu_path)
        sentences = parse(conllu)

        # modifications
        # sentences = check_pos_tags(sentences)
        sentences = check_tags(sentences, wt)
        sentences = modify_pos_tag(sentences)
        sentences = add_lemmas(sentences, wt)

        # modifications in string
        conllu = generate_conllu(sentences)
        conllu = add_entries(conllu)

        # export conllu file
        output_file = output_dir + file_name
        export_conllu(conllu, output_file)

if __name__ == '__main__':
    main()