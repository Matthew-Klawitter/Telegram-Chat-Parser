from bs4 import BeautifulSoup
import codecs
import json
import os

input_dir = "html"
output_dir = "output"
output_file = "data.json"


def create_dirs():
    if not os.path.exists(input_dir):
        print("Input directory does not exist. Recreating")
        os.makedirs(input_dir)

    if not os.path.exists(output_dir):
        print("Creating output directory...")
        os.makedirs(output_dir)

def parse_html():
    messages = []

    # Find all the data and organize it correctly
    for file in os.listdir(input_dir):
        print("Processing: " + file)
        html = codecs.open(input_dir + "/" + file, 'r', 'utf-8')
        soup = BeautifulSoup(html.read(), 'html.parser')

        chat_room = soup.find('div', {'class': ['page_header']}).text.replace("\n", "").strip()
        all_messages = soup.find_all('div', {'class': ['message default clearfix', 'message default clearfix joined']})

        last_message = None

        for msg in all_messages:
            date = None
            name = None
            text = None

            children = msg.findChildren('div', {'class': ['pull_right date details', 'from_name', 'text']})

            if (len(children) == 3): # At this length we have a new message
                date = children[0].get("title")
                name = children[1].text.replace("\n", "").strip() # Name
                text = children[2].text.replace("\n", "").strip() # Text
            elif (len(children) == 2): # Message continuation
                date = children[0].get("title")
                text = children[1].text.replace("\n", "").strip() # Text

            if name is None: # The text is for the previous message by the same person
                if not last_message is None:
                    if not text is None:
                        last_message["text"] += "\n" + text

                if all_messages.index(msg) == len(all_messages): # Ensures the very last message parsed is added to our list, even if its just additional text
                    messages.append(last_message)

            else: # The text is for a new message by a new person
                if last_message is None: # Essentially checking if this is the first message
                    m = {"chat": chat_room, "date": date, "name": name, "text": text}
                    last_message = m
                else:
                    messages.append(last_message)
                    m = {"chat": chat_room, "date": date, "name": name, "text": text}
                    last_message = m
    return messages

def write_json(data):
    with open(output_dir + "/" + output_file, 'a+', encoding='utf-8') as f:
        data = json.dumps(data)
        f.write(data)
        f.close()


create_dirs()
write_json(parse_html())
print("Done! Your json data should be found at: " + output_dir + "/" + output_file)