import re
import json
import openai
from time import time,sleep


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


def load_info():
    info = open_file('my_info.json')
    info = json.loads(info)
    return info


openai.api_key = open_file('openaiapikey.txt')  # update this - create the file if needed


def gpt3_completion(prompt, engine='text-davinci-002', temp=0.7, top_p=1.0, tokens=1000, freq_pen=0.0, pres_pen=0.0, stop=['asdfasdf', 'asdasdf']):
    max_retry = 5
    retry = 0
    prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()  # force it to fix any unicode errors
    while True:
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop)
            text = response['choices'][0]['text'].strip()
            #text = re.sub('\s+', ' ', text)
            filename = '%s_gpt3.txt' % time()
            save_file('gpt3_logs/%s' % filename, prompt + '\n\n==========\n\n' + text)
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % oops
            print('Error communicating with OpenAI:', oops)
            sleep(1)


if __name__ == '__main__':
    info = load_info()
    #print(info)
    text_block = ''
    for i in info:
        text_block += '%s: %s\n' % (i['label'], i['answer'])
    #print(text_block)
    prompt = open_file('prompt_cover_letter.txt').replace('<<INFO>>', text_block)
    #print(prompt)
    completion = gpt3_completion(prompt)
    print('\n\nCOVER LETTER:', completion)
    save_file('cover_letter_%s.txt' % time(), completion)
    ### get professional objective
    prompt = open_file('prompt_professional_objective.txt').replace('<<INFO>>', text_block)
    #print(prompt)
    completion = gpt3_completion(prompt)
    print('\n\nPROFESSIONAL OBJECTIVE:', completion)
    save_file('professional_objective_%s.txt' % time(), completion)
    