def printTokens(tokens: list):
    print('*** TOKENS ***')
    for token in tokens:
        print(token)
    print('*** TOKENS END ***')

def printHtml(html: str):
    print('*** HTML ***')
    print(html)
    print('*** HTML END ***')


def file_reader(filename: str) -> list:
    lines = []
    with open(filename) as f:
        for line in f:
            if line != '\n':
                lines.append(line)
            else:
                lines.append('\n')
    return lines

def file_writer(filename: str, content: str) -> None:
    file = filename + '.html'
    with open(file, 'w') as f:
        f.write(content)