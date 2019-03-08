import json

def save_file(content):
    out_path = "D:/projects//gitpages//numlocked//Pickledtezcat.github.io//saved_data.js"

    with open(out_path, "w") as outfile:
        converted_content = json.dumps(content, sort_keys=True)
        outfile.write("my_data ={}".format(converted_content))

def load_file():
    in_path = "D:/projects//gitpages//numlocked//Pickledtezcat.github.io//saved_data.js"

    with open(in_path, "r") as infile:
        loaded_content = infile.read()
        if len(loaded_content) > 0:
            converted_content = loaded_content.split("=")[1]
            content = json.loads(converted_content)
            return content
        else:
            return None