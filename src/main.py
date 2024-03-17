from marker import tokenizer, html_generator
import argparse
from utils import file_reader, file_writer, printTokens, printHtml

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="the markdown filename to be converted to html", type=str)
    parser.add_argument("--tokens", help="print the tokens",
                    action="store_true")
    parser.add_argument("--html", help="print the html", action="store_true")
    parser.add_argument("--output", help="output file", type=str)
    args = parser.parse_args()
    lines = file_reader(args.filename)
    tokens = tokenizer(lines)
    html = html_generator(tokens)
    if args.tokens:
        printTokens(tokens)
    if args.html:
        printHtml(html)
    if args.output:
        file_writer(args.output, html)