

# input: <p>Software engineer</p>
# output: "p", "Software engineer"
def extract_tag_and_text(html_string):
    start_tag_index = html_string.find("<") + 1
    end_tag_index = html_string.find(">")
    tag = html_string[start_tag_index:end_tag_index]

    closing_tag = f"</{tag}>"
    closing_tag_index = html_string.find(closing_tag)
    text = html_string[end_tag_index + 1:closing_tag_index]

    return tag, text


tag, text = extract_tag_and_text("<h1>Hello World</h1>")
print(f"Tag: {tag}, Text: {text}")
