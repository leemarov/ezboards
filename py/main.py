import sys
import json

import bs4
import argparse

soup: bs4.BeautifulSoup = None
parsed_briefing = {}
json_airfields = {}
json_threats = {}


def edit_html(html_file, briefing_file, airfield_json_file, threats_json_file):
    global soup
    global json_airfields, json_threats
    with open(briefing_file, "r") as f:
        briefing_lines = f.readlines()
        parse_briefing(briefing_lines)
    with open(airfield_json_file, "r") as f:
        json_airfields = json.load(f)
    with open(threats_json_file, "r") as f:
        json_threats = json.load(f)
    with open(html_file, "r") as f:
        html_str = f.read()
        soup = bs4.BeautifulSoup(html_str, 'html.parser')
        pg1 = soup.div
        pg2 = pg1.next_sibling.next_sibling
        left_bottom = soup.new_tag("div", **{'class': 'bottom'})
        left_bottom.append(get_page_1_bottom_contents())
        right_bottom = get_page_2_bottom_contents()
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
            threat = threat.split('-')[0:2]
            second_part = ''
            for c in threat[1]:
                if not str.isdigit(c):
                    break
                second_part += c
            threat = threat[0] + '-' + second_part
            pb['threats'] = pb.get('threats', []) + [threat]
    pb['threats'] = set(pb.get('threats', []))
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

    table_title = soup.new_tag("tr")
    table_title.append(create_tag("th", string="Airfields", colspan=8, **{'class': 'title'}))
    table_body.append(table_title)

    table_header = soup.new_tag("tr")
    table_header['class'] = 'header'
    table_header.append(create_tag("th", string="Airfield"))
    table_header.append(create_tag("th", string="TACAN"))
    table_header.append(create_tag("th", string="Elev"))
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
        rwy_items = []
        for rwy, d in af_dict.get("Rwy", {}).items():
            rwy_str = f"{rwy} [{d.get('hdg', '')}°"
            ils = d.get('ils', None)
            if ils:
                rwy_str += f" {ils}"
            rwy_str += "]"
            rwy_items.append(rwy_str)
        tr_af.append(create_tag("td", string=airfield_name))
        tr_af.append(create_tag("td", string=af_dict.get("TCN", "")))
        tr_af.append(create_tag("td", string=af_dict.get("Elev", "")))
        tr_af.append(create_tag("td", string=" ".join(rwy_items)))
        table_body.append(tr_af)

    for af in {parsed_briefing.get('field_departure', ''), parsed_briefing.get('field_arrival', '')}:
        create_airfield_row(af, bold=True)
    create_airfield_row(parsed_briefing.get('field_alternate', ''))
    return table


def get_page_2_bottom_contents():
    global soup, parsed_briefing
    bottom = soup.new_tag("div", **{'class': 'bottom2'})
    table = soup.new_tag("table")

    table_body = soup.new_tag("tbody")
    table.append(table_body)

    table_title = soup.new_tag("tr")
    table_title.append(create_tag("th", string="Threats", colspan=8, **{'class': 'title'}))
    table_body.append(table_title)

    table_header = soup.new_tag("tr")
    table_header['class'] = 'header'
    table_header.append(create_tag("th", string="Threat"))
    table_header.append(create_tag("th", string="Name"))
    table_header.append(create_tag("th", string="RWR"))
    table_header.append(create_tag("th", string="Type"))
    table_header.append(create_tag("th", string="Track"))
    table_header.append(create_tag("th", string="Engage"))
    table_header.append(create_tag("th", string="Max"))
    table_header.append(create_tag("th", string="Search"))
    table_body.append(table_header)

    alt_class = "odd"

    def create_threat_row(threat_name: str):
        nonlocal alt_class
        if threat_name not in json_threats:
            return
        json_threats.get(threat_name)
        threat_dict = json_threats[threat_name]
        tr_af = soup.new_tag("tr")
        tr_af['class'] = alt_class
        alt_class = "odd" if alt_class == "even" else "even"
        tr_af.append(create_tag("td", string=threat_name))
        tr_af.append(create_tag("td", string=threat_dict.get("name", "")))
        rwr = threat_dict.get("rwr", "")
        if rwr:
            rwr = f"[ {rwr} ]"
        tr_af.append(create_tag("td", string=rwr))
        tr_af.append(
            create_tag("td", string=threat_dict.get("type", "").replace('-fixed', '').replace('-mobile', ' Mobile')))
        tr_af.append(create_tag("td", string=threat_dict.get("tracking", "").capitalize()))
        tr_af.append(create_tag("td", string=threat_dict.get("range_engage", "").replace("/", " / ")))
        tr_af.append(create_tag("td", string=threat_dict.get("range_max", "").replace("/", " / ")))
        tr_af.append(create_tag("td", string=threat_dict.get("radar_sa", "")))
        table_body.append(tr_af)

    threats = parsed_briefing.get("threats", [])
    for threat_name in sorted(threats):
        create_threat_row(threat_name)
    if threats:
        bottom_height = 2 * len(threats) + 4
        bottom['style'] = f"top:{100 - bottom_height}%;height:{bottom_height}%"
        bottom.append(table)
    return bottom


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-f", "--file", type=str, default="../briefing.html")
    arg_parser.add_argument("-b", "--briefing", type=str, default="briefing_test.txt")
    arg_parser.add_argument("-j", "--airfields", type=str, default="../airfields.json")
    arg_parser.add_argument("-t", "--threats", type=str, default="../threats.json")
    args = arg_parser.parse_args(sys.argv[1:])
    edit_html(args.file, args.briefing, args.airfields, args.threats)


if __name__ == "__main__":
    main()
