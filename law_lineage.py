import os
from pdfminer.high_level import extract_text

inputs = os.listdir('input')

for i in inputs:
    text = extract_text('input/'+i)
    with open('output/'+i.replace('.pdf', '.txt'), 'w', encoding = 'utf-8') as f:
        f.write(text)