from typing import Final

H1: Final = 'H1'
H2: Final = 'H2'
H3: Final = 'H3'
H4: Final = 'H4'
H5: Final = 'H5'
H6: Final = 'H6'
PARAGRAPH: Final = 'PARAGRAPH'
BREAKLINE: Final = 'BREAKLINE'
LINK: Final = 'LINK'
TEXT: Final = 'TEXT'

def high_level_tokenizer(sentences: list) -> list:
    tokens = []
    for sentence in sentences:
        if sentence == '\n':
            tokens.append([BREAKLINE, '\n'])
            continue
        token_tuple = []
        position = 0
        for c in sentence:
            if c == '#':
                maybe_tittle = ''.join(sentence[position:])
                print(maybe_tittle)
                token_tuple = identify_header_size(maybe_tittle)
                break 
            position += 1
        if len(token_tuple) == 0:
            tokens.append([PARAGRAPH, sentence])
        else:
            tokens.append(token_tuple)

    return tokens

def calculate_index_from_links(sentence: str) -> list:
    stack = []
    indexes_boundaries = []
    L_BRACKET = '['
    R_BRACKET = ']'
    L_PARENTHESIS = '('
    R_PARENTHESIS = ')'
    i = 0
    for c in sentence:
        if c == L_BRACKET:
            if len(stack) == 0:
                stack.append(i)
        elif c == R_BRACKET:
            if len(stack) > 0:
                if i+1 < len(sentence) and sentence[i+1] == L_PARENTHESIS and len(stack) != 0:
                    j = i+1
                    for c in sentence[i+1:]:
                        if c == R_PARENTHESIS:
                            indexes_boundaries.append([stack.pop(), i, i+1, j])
                            break
                        j += 1

        i += 1
    return indexes_boundaries

def get_links_from_text(title_index_list: list, sentence: str) -> list:
    assert len(title_index_list) == 4
    stack = [LINK]
    link = title_index_list[1] - title_index_list[0]
    name = title_index_list[3] - title_index_list[2]
    if name > 0:
        stack.append(sentence[title_index_list[2]+1:title_index_list[3]])
    else:
        stack.append('')
    if link > 0:
        stack.append(sentence[title_index_list[0]+1:title_index_list[1]])
    else:
        stack.append('')
    return stack

def parse_links(sentence: str) -> list:
    LINK_BOUNDARY_SIZE = 4
    links_index_list = calculate_index_from_links(sentence)
    if len(links_index_list) == 0:
        return [[TEXT, sentence]]
    
    assert len(links_index_list[0]) == LINK_BOUNDARY_SIZE and len(links_index_list[-1]) == LINK_BOUNDARY_SIZE

    text_links_list = []

    first_chars = links_index_list[0][0] - 0
    if first_chars > 0:
        text_links_list.append([TEXT, sentence[0:links_index_list[0][0]]])

    for i in range(len(links_index_list)-1):
        assert len(links_index_list[i]) == LINK_BOUNDARY_SIZE and len(links_index_list[i+1]) == LINK_BOUNDARY_SIZE
        curr, next = links_index_list[i], links_index_list[i+1]
        h = get_links_from_text(curr, sentence)
        text_links_list.append(h)
        if next[0] - curr[3] > 1:
            in_between = sentence[curr[3]+1:next[0]]
            text_links_list.append([TEXT, in_between])

    last_boundary = links_index_list[-1]
    last_element = get_links_from_text(last_boundary, sentence)
    text_links_list.append(last_element)

    remainder_chars = len(sentence) - links_index_list[-1][3]
    if remainder_chars > 0:
        text_links_list.append([TEXT, sentence[links_index_list[-1][3]+1:len(sentence)]])
    return text_links_list


def identify_header_size(sentence: str) -> list:
    tuples = sentence.split(' ')
    if '#' == tuples[0]:
        return [H1, ' '.join(tuples[1:])]
    elif '##' == tuples[0]:
        return [H2, ' '.join(tuples[1:])]
    elif '###' == tuples[0]:
        return [H3, ' '.join(tuples[1:])]
    elif '####' == tuples[0]:
        return [H4, ' '.join(tuples[1:])]
    elif '#####' == tuples[0]:
        return [H5, ' '.join(tuples[1:])]
    elif '######' == tuples[0]:
        return [H6, ' '.join(tuples[1:])]
    else:
        return []

def merge_tokens_paragraph(tokens: list) -> list:
    merged_tokens = []
    for token in tokens:
        if token[0] == PARAGRAPH:
            if len(merged_tokens) > 0 and merged_tokens[-1][0] == PARAGRAPH:
                merged_tokens[-1][1] += token[1]
            else:
                merged_tokens.append(token)
        else:
            merged_tokens.append(token)
    return merged_tokens

def html_mapper(token: list) -> str:
    assert (2 <= len(token) <= 3)
    IDENTIFIER = token[0]
    if IDENTIFIER == H1:
        return f'<h1>{token[1]}</h1>'
    elif IDENTIFIER == H2:
        return f'<h2>{token[1]}</h2>'
    elif IDENTIFIER == H3:
       return f'<h3>{token[1]}</h3>'
    elif IDENTIFIER == H4:
        return f'<h4>{token[1]}</h4>'
    elif IDENTIFIER == H5:
        return f'<h5>{token[1]}</h5>'
    elif IDENTIFIER == H6:
        return f'<h6>{token[1]}</h6>'
    elif IDENTIFIER == PARAGRAPH:
        return f'<p>{token[1]}</p>'
    elif IDENTIFIER == BREAKLINE:
        return ''
    elif IDENTIFIER == TEXT:
        return token[1]
    elif IDENTIFIER == LINK:
        link, name = token[1], token[2]
        return f'<a href="{link}">{name}</a>'
    raise ValueError('Invalid token')

def parse_tokens(tokens: list) -> list:
    all_tokens = []
    IDENTIFIER = 0
    ELEMENTS = 1
    for token in tokens:
        links = parse_links(token[ELEMENTS])
        new_token = []
        new_token.append(token[IDENTIFIER])
        new_token.append(links)
        all_tokens.append(new_token)
    return all_tokens

def tokenizer(lines: list) -> list:
    first_pass_tokens = high_level_tokenizer(lines)
    optimized_paragraph = merge_tokens_paragraph(first_pass_tokens)
    tokens = parse_tokens(optimized_paragraph)
    return tokens


def html_generator(tokens: list) -> str:
    html = ''
    for token in tokens:
        html_inner = ''
        inner_tokens = token[1]
        for inner_token in inner_tokens:
            html_inner += html_mapper(inner_token)
        root = [token[0], html_inner]
        html += html_mapper(root)
    return html
