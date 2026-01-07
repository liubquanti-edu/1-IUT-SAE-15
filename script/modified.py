#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modified on Wed Jan  7 08:53:43 2026

@author: liubquanti
"""
import sys
from datetime import datetime
from icalendar import Calendar
import csv
import re

# CONFIG

ICS_FILE_LOCATION = sys.argv[1]
CSV_FILE_LOCATION = sys.argv[2]

# ICAL2CSV

class Convert2CSV():
    def __init__(self):
        self.csv_data = []

    def read_ical(self, ical_file_location):
        with open(ical_file_location, 'r', encoding='utf-8') as ical_file:
            data = ical_file.read()
        self.cal = Calendar.from_ical(data)
        return self.cal

    def make_csv(self):
        for event in self.cal.subcomponents:
            if event.name != 'VEVENT':
                continue
            row = [
                # Date
                event.get('DTSTART').dt.strftime("%Y-%m-%d"),
                # HStart
                event.get('DTSTART').dt.strftime("%H:%M:%S"),
                # HEnd 
                event.get('DTEND').dt.strftime("%H:%M:%S"),
                # Summary
                ' : '.join(str(event.get('SUMMARY')).splitlines()),
                # Location
                str(event.get('LOCATION')),
                # Description
                ' : '.join(str(event.get('DESCRIPTION')).splitlines()),
            ]
            row = [x.strip() for x in row]
            self.csv_data.append(row)

    def process_summary_column(self):
        for row in self.csv_data:
            # Replace occurrences of -TD, -TP, -Cours with :TD, :TP, :Cours
            row[3] = re.sub(r'-(TD|TP|Cours)', r':\1', row[3])
            # Replace underscores and spaces with colons
            row[3] = re.sub(r'[_\s]+', ':', row[3])

    def split_column(self, column_index, delimiter):
        new_data = []
        for row in self.csv_data:
            # Split the column value by the delimiter
            split_values = row[column_index].split(delimiter)
            # Ensure the split values are added correctly
            if len(split_values) > 1:
                # Take the first part as Summary and the last part as Group
                summary = delimiter.join(split_values[:-1]).strip()
                group = split_values[-1].strip()
                # Remove trailing colons from Summary
                summary = re.sub(r':+$', '', summary)
                new_row = row[:column_index] + [summary, group] + row[column_index + 1:]
            else:
                # If no delimiter is found, keep the original value in Summary and leave Group empty
                summary = re.sub(r':+$', '', row[column_index].strip())
                new_row = row[:column_index] + [summary, ""] + row[column_index + 1:]
            new_data.append(new_row)
        self.csv_data = new_data

    def process_description_column(self):
        new_data = []
        for row in self.csv_data:
            description = row[-1]  # Assuming Description is the last column
            # Extract Year, Prof, and Updated using regex
            year_match = re.search(r'(\d+[A-Z]+\d*)', description)
            prof_match = re.search(r'([A-ZÉÀÈÙÂÊÎÔÛÄËÏÖÜÇ]+(?:\s[A-ZÉÀÈÙÂÊÎÔÛÄËÏÖÜÇ]+)+)', description)
            updated_match = re.search(r'Updated\s*:\s*(\d{2}/\d{2}/\d{4}\s\d{2}:\d{2})', description)

            year = year_match.group(1) if year_match else ''
            prof = prof_match.group(1) if prof_match else 'Intervenant à préciser'
            updated = updated_match.group(1) if updated_match else ''

            # Replace the Description column with Year, Prof, and Updated
            new_row = row[:-1] + [year, prof, updated]
            new_data.append(new_row)
        self.csv_data = new_data

    def save_csv(self, csv_location):  # type: (str) -> None
        schema = ["Date", "HStart", "HEnd", "Summary", "Group", "Location", "Year", "Prof", "Updated"]
        with open(csv_location, 'w', encoding='utf-8') as csv_handle:
            writer = csv.writer(csv_handle)
            writer.writerow(schema)
            for row in self.csv_data:
                # Ensure all rows match the schema length
                if len(row) == len(schema):
                    writer.writerow([r.strip() for r in row])
                else:
                    print(f"Skipping row due to mismatched columns: {row}")


Convert2CSV = Convert2CSV()
Convert2CSV.ICS_FILE_LOCATION = ICS_FILE_LOCATION
Convert2CSV.CSV_FILE_LOCATION = CSV_FILE_LOCATION

Convert2CSV.read_ical(Convert2CSV.ICS_FILE_LOCATION)
Convert2CSV.make_csv()
Convert2CSV.process_summary_column()
Convert2CSV.split_column(3, ':')  # Split the Summary column into Summary and Group
Convert2CSV.process_description_column()
Convert2CSV.save_csv(Convert2CSV.CSV_FILE_LOCATION)

