import os
import re
from symbol_list import pos_tags, stop_words, symbol_list

def load_texts(text_dir):
    texts = []
    for filename in os.listdir(text_dir):
        if filename.endswith(".txt"):
            file_path = os.path.join(text_dir, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()
                texts.append((filename, text))
    return texts

def remove_signs(text):
    removed_text = text
    signs = [' ', '\n']
    for sign in signs:
        removed_text = removed_text.replace(sign, '')
    return removed_text

def divide_texts(texts):
    split_texts = {}
    for text in texts:
        snippets = re.split(r'\s+', text[1])
        name = text[0].split('.')[0]
        split_texts[name] = [snippet for snippet in snippets if snippet.count('་') > 1]

    return split_texts

def botok_segment(wt, text):
    segmented_text = []
    for sent in text:
        tokens = wt.tokenize(sent, split_affixes=True)
        temp = []
        for token in tokens:
            t = remove_signs(token['text'])
            temp.append(t)
        segmented_text.append(temp)
    return segmented_text

def extract_conllu(res):
    conllu = ''
#    stop_words = ['token', 'Token', '#']
    i = 1  # sent_id
    for conllu_temp in res:
        lines = conllu_temp.split('\n')
        sent = temp = ''
        j = 1 # token_id
        for l in lines:
            c_split = l.split('\t')
            if len(c_split) > 3:
                token = c_split[1]
                if token in stop_words:
                    continue
                pos_tag = c_split[3].strip()
                sent = sent + token
                temp = temp + '\t'.join([str(j), token, '_', pos_tag]) + '\t_'*6 + '\n'
                j = j + 1
        if sent != '':
            conllu = conllu + '# sent_id = ' + str(i) + '\n# text = ' + sent + '\n' + temp + '\n'
            i = i + 1

    return conllu

def export_conllu(conllu, conllu_name):
    with open(conllu_name, 'w', encoding="utf-8") as file:
        file.write(conllu)

def delete_file(file_path):
    try:
        os.remove(file_path)
    except Exception as e:
        print(f"An error occurred: {e}")

def None_replacement(token):
    for key, value in token.items():
        if value is None:
            token[key] = '_'
    return token

def generate_conllu(sentences):
    conllu_str = ''
    for sentence in sentences:
        sent_id = sentence.metadata['sent_id']
        text = sentence.metadata['text']
        content = ''
        for token in sentence:
            token = None_replacement(token)
            content = content + '\t'.join([str(token[key]) for key in token.keys()]) + '\n'
        conllu_str = conllu_str + '# sent_id = ' + sent_id + '\n' + '# text = ' + text + '\n' + content + '\n'

    return conllu_str

#################################
# post-processing
#################################
def load_conllu(conllu_path):
    with open(conllu_path, 'r', encoding='utf-8') as file:
        conllu = file.read()
    return conllu

def modify_pos_tag(sentences):
    for sentence in sentences:
        for token in sentence:
            for symbol in symbol_list:
                if token['form'] in symbol[0]:
                    if symbol[1] == '*':
                        token['upos'] = symbol[2]
                    elif token['upos'] == symbol[1]:
                        token['upos'] = symbol[2]

    return sentences

def check_tags(sentences, wt):
    filtered_sentences = []
    cnt = 1
    for sentence in sentences:
        text = sentence.metadata['text']
        tokens = wt.tokenize(text, split_affixes=True)
        prediction = [token.text for token in tokens]
        ref = []
        for token in sentence:
            ref.append(token['form'])
        flag_token = ref == prediction
        flag_pos = all(token['upos'] in pos_tags for token in sentence)
        # if all(token['upos'] in pos_tags for token in sentence):
        if flag_token and flag_pos:
            sentence.metadata['sent_id'] = str(cnt)
            filtered_sentences.append(sentence)
            cnt = cnt + 1
    return filtered_sentences

def add_lemmas(sentences, wt):
    for sentence in sentences:
        for token in sentence:
            analyzed_token = wt.tokenize(token['form'], split_affixes=True)
            try:
                if analyzed_token[0]['lemma'] != '':
                    token['lemma'] = analyzed_token[0]['lemma']
                else:
                    token['lemma'] = token['form']
            except Exception as e:
                print(e)
                token['lemma'] = token['form']

    return sentences

# add dummy entries to HEAD, DEPREL and MISC in conllu
def add_entries(input_conllu):
    lines = input_conllu.split('\n')
    modified_lines = []
    for line in lines:
        if line.startswith("#") or line.strip() == "":
            # Add comment lines and empty lines as is
            modified_lines.append(line)
            continue

        columns = line.split('\t')
        if len(columns) == 10:  # Ensure the line has all necessary columns
            if columns[6].strip() == "_":  # Check if HEAD column is "_"
                columns[6] = '0'  # Replace with 0
            if columns[7].strip() == "_":  # Check if DEPREL column is "_"
                columns[7] = 'root'  # Replace with root
            if columns[9].strip() == "_":  # Check if MISC column is "_"
                columns[9] = "SpaceAfter=No"  # Replace with "SpaceAfter=No"
            modified_line = '\t'.join(columns)
            modified_lines.append(modified_line)
        else:
            modified_lines.append(line)  # If columns are not complete, add line as is

    output_conllu = str()
    for line in modified_lines:
        output_conllu = output_conllu + line + '\n'
    return output_conllu