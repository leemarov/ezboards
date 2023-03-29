import sys

import bs4
import argparse


def edit_html(html_file, briefing_file):
    with open(briefing_file, "r") as f:
        briefing_lines = f.readlines()
    with open(html_file, "r") as f:
        html_str = f.read()
        soup = bs4.BeautifulSoup(html_str, 'html.parser')
        pg1 = soup.div
        pg2 = pg1.next_sibling.next_sibling
        pg1.append(u'<div class="bottom">{get_page_1_bottom_contents()}</div>')
        pg2.append(u'<div class="bottom">{get_page_2_bottom_contents()}</div>')
    with open(html_file, "w") as f:
        f.write(soup.prettify())


def get_page_1_bottom_contents():
    pass


def get_page_2_bottom_contents():
    pass


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-f", "--file", type=str, default="../briefing.html")
    arg_parser.add_argument("-b", "--briefing", type=str, default="briefing_test.txt")
    args = arg_parser.parse_args(sys.argv[1:])
    edit_html(args.file, args.briefing)


if __name__ == "__main__":
    main()
