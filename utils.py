def write_to_file(html, json, filename):
    if html != None:
        with open(f"{filename}.html", "w", encoding='utf-8') as file:
                file.write(str(html.text))
    if json != None:
        with open(f"{filename}.json", "w", encoding='utf-8') as file:
            file.write(str(json))