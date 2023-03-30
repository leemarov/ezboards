import sys
import json

import bs4
import argparse

soup: bs4.BeautifulSoup = None
parsed_briefing = {}
json_airfields = {}


def edit_html(html_file, briefing_file, airfield_json_file):
    global soup
    global json_airfields
    with open(briefing_file, "r") as f:
        briefing_lines = f.readlines()
        parse_briefing(briefing_lines)
    with open(airfield_json_file, "r") as f:
        json_airfields = json.load(f)
    with open(html_file, "r") as f:
        html_str = f.read()
        soup = bs4.BeautifulSoup(html_str, 'html.parser')
        pg1 = soup.div
        pg2 = pg1.next_sibling.next_sibling
        left_bottom = soup.new_tag("div", **{'class': 'bottom'})
        left_bottom.append(get_page_1_bottom_contents())
        right_bottom = soup.new_tag("div", **{'class': 'bottom'})
        right_bottom.append(get_page_2_bottom_contents())
        pg1.append(left_bottom)
        pg2.append(right_bottom)
    with open(html_file, "w") as f:
        f.write(soup.prettify())


def parse_briefing(briefing_lines):
    global parsed_briefing
    pb = {}

    def lines_between(pt1, pt2):
        return briefing_lines[briefing_lines.index(pt1 + '\n') + 1:briefing_lines.index(pt2 + '\n')]

    lines_overview = lines_between("Mission Overview:", "Situation: ")
    lines_situation = lines_between("Situation: ", "Pilot Roster:")
    lines_roster = lines_between("Pilot Roster:", "Threat Analysis:")
    lines_threat = lines_between("Threat Analysis:", "Steerpoints:")
    lines_steerpoints = lines_between("Steerpoints:", "Comm Ladder:")
    lines_comms = lines_between("Comm Ladder:", "Iff")
    lines_iff = lines_between("Iff", "Ordnance:")
    lines_ordnance = lines_between("Ordnance:", "Weather:")
    lines_weather = lines_between("Weather:", "Support:")
    lines_support = lines_between("Support:", "Rules of Engagement:")
    lines_roe = lines_between("Rules of Engagement:", "Emergency Procedures:")
    lines_emergency = lines_between("Emergency Procedures:", "END_OF_BRIEFING")
    for line in lines_comms:
        if "Dep Atis:" in line:
            pb['field_departure'] = line.split('\t')[2].replace('ATIS', '').strip()
        if "Arr Atis:" in line:
            pb['field_arrival'] = line.split('\t')[2].replace('ATIS', '').strip()
        if "Alt Atis:" in line:
            pb['field_alternate'] = line.split('\t')[2].replace('ATIS', '').strip()
    for line in lines_threat:
        if "--" in line:
            threat = line.split('\t')[1].replace('--', '').strip()
            pb['threats'] = pb.get('threats', []) + [threat]
    parsed_briefing = pb


def create_tag(name, string="", attrs={}, **kwargs):
    global soup
    tag = soup.new_tag(name, attrs=attrs, **kwargs)
    tag.string = string
    return tag


def get_page_1_bottom_contents():
    global soup
    global parsed_briefing
    table = soup.new_tag("table")
    # table['height'] = "100%"
    table_body = soup.new_tag("tbody")
    table.append(table_body)
    table_header = soup.new_tag("tr")
    table_header['class'] = 'header'
    table_header.append(create_tag("th", string="Airfield"))
    table_header.append(create_tag("th", string="TACAN"))
    table_header.append(create_tag("th", string="ILS"))
    table_header.append(create_tag("th", string="Rwy"))
    table_body.append(table_header)
    alt_class = "odd"

    def create_airfield_row(airfield_name, bold=False):
        global json_airfields
        nonlocal alt_class
        if airfield_name not in json_airfields:
            print(f"af not found: {airfield_name}")
            return
        af_dict = json_airfields[airfield_name]
        tr_af = soup.new_tag("tr")
        tr_af['class'] = alt_class
        alt_class = "odd" if alt_class == "even" else "even"
        if bold:
            tr_af['class'] = "ownflight"
        tr_af.append(create_tag("td", string=airfield_name))
        tr_af.append(create_tag("td", string=af_dict.get("TCN", "")))
        tr_af.append(create_tag("td", string=af_dict.get("ILS", "").replace(";", " | ")))
        tr_af.append(create_tag("td", string=af_dict.get("Rwy", "").replace(";", " | ")))
        table_body.append(tr_af)

    for af in {parsed_briefing.get('field_departure', ''), parsed_briefing.get('field_arrival', '')}:
        create_airfield_row(af, bold=True)
    create_airfield_row(parsed_briefing.get('field_alternate', ''))
    return table


def get_page_2_bottom_contents():
    global soup
    return soup.new_tag("div")


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-f", "--file", type=str, default="../briefing.html")
    arg_parser.add_argument("-b", "--briefing", type=str, default="briefing_test.txt")
    arg_parser.add_argument("-j", "--airfields", type=str, default="../airfields.json")
    args = arg_parser.parse_args(sys.argv[1:])
    edit_html(args.file, args.briefing, args.airfields)


if __name__ == "__main__":
    main()
