from __future__ import division, unicode_literals
from collections import defaultdict
from bs4 import BeautifulSoup
import codecs
import os

output_dir = "Output"
messages = []


for file in os.listdir("Data"):
    print("Processing: " + file)
    html = codecs.open("Data/" + file, 'r', 'utf-8')
    soup = BeautifulSoup(html.read(), 'html.parser')

    all_messages = soup.find_all('div', {'class': ['from_name', 'text']})

    for message in all_messages:
        msg = message.text.replace("\n", "")
        msg = msg.strip()
        messages.append(msg)

names = [""]
chatter = ""
parsed_data = defaultdict(list)

for message in messages:
    if message in names:
        chatter = message
    else:
        parsed_data[chatter].append(message)

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

for key in parsed_data.keys():
    texts = ""
    for message in parsed_data[key]:
        message = "".join(i for i in message if ord(i)<128)
        texts += message + "\n"
    f = open(output_dir + "/" + key + ".txt", "w+")
    f.write(texts)
    f.close()
