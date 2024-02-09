from ipdb import set_trace
from json import loads
from commonmark import Parser, dumpJSON
from frontmatter import load

ast = Parser().parse(load("file-configuration.md").content)

json_str = dumpJSON(ast)

with open("file-configuration.json", "w") as file_configuration_json_file:
    file_configuration_json_file.write(json_str)

json = loads(json_str)

set_trace()

for paragraph_node in [
    node for node in (
        Parser().parse(load("file-configuration.md").content).walker()
    ) if node[0].t == "paragraph"
][::2]:

    nodes = [node for node in paragraph_node[0].walker()]
    set_trace

    if nodes[1][0].t != "text":
        continue

    if (
        nodes[1][0].literal is not None and
        "File config" in nodes[1][0].literal
    ):
        set_trace

    paragraph = []

    for node in nodes:
        if node[0].t == "text":
            paragraph.append(node[0].literal)
        elif node[0].t == "softbreak":
            paragraph.append(" ")
        elif node[0].t == "code":
            paragraph.append(f"`{node[0].literal}`")

    result = "".join(paragraph)

    if "  " in result:
        set_trace()

    print(result)
    print()
