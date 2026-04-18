#!/usr/bin/env python3
from html.parser import HTMLParser
import csv
import json

class TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_cell = False
        self.current_cell = ""
        self.current_row = []
        self.current_table = []
        self.all_tables = []

    def handle_starttag(self, tag, attrs):
        if tag in ("td", "th"):
            self.in_cell = True
            self.current_cell = ""

    def handle_endtag(self, tag):
        if tag in ("td", "th"):
            self.in_cell = False
            self.current_row.append(self.current_cell.strip())
        elif tag == "tr":
            if self.current_row:
                self.current_table.append(self.current_row)
                self.current_row = []
        elif tag == "table":
            if self.current_table:
                self.all_tables.append(self.current_table)
                self.current_table = []

    def handle_data(self, data):
        if self.in_cell:
            self.current_cell += data

    def get_items(self):
        return self.all_tables

def main():
    # Load HTML file
    with open("superbowl.html", "r", encoding="utf-8") as file:
        html = file.read()

    parser = TableParser()
    parser.feed(html)
    all_tables = parser.get_items()

    if not all_tables:
        print("No tables found in the HTML.")
        return

    best_table = max(all_tables, key=lambda t: len(t))
    
    headers = best_table[0]
    data_rows = best_table[1:]

    data_dicts = []
    for row in data_rows:
        row_dict = {}
        for i, header in enumerate(headers):
            row_dict[header] = row[i] if i < len(row) else ""
        data_dicts.append(row_dict)

    # Save CSV
    with open("superbowl.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data_dicts)

    # Save JSON
    with open("superbowl.json", "w", encoding="utf-8") as f:
        json.dump(data_dicts, f, indent=2)

    print("Super Bowl CSV and JSON fully saved!")
 
if __name__ == "__main__":
    main()
