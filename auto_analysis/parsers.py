import csv
import json
import logging

from pathlib import Path


def parse_generic_csv(csv_path: Path, delimiter=',', fieldname_translation={}, int_fields=[], float_fields=[]):
    """
    Parse a csv file to a list of dicts. Optionally cast int and float fields to those types.
    Optionally translate fieldnames via a lookup table. Translation is done after casting, so
    fields listed in the `int_fields` and `float_fields` args should reflect the fieldnames
    in the original file (pre-translation, if applicable).

    `fieldname_translation` is a dict from original fieldname to translated fieldname.
    """
    parsed_rows = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        for row in reader:
            parsed_row = {}
            for field, value in row.items():
                if field in int_fields:
                    try:
                        parsed_row[field] = int(value)
                    except ValueError as e:
                        parsed_row[field] = None
                elif field in float_fields:
                    try:
                        parsed_row[field] = float(value)
                    except ValueError as e:
                        parsed_row[field] = None
                else:
                    parsed_row[field] = value

            for original_fieldname, translated_fieldname in fieldname_translation.items():
                if original_fieldname in parsed_row:
                    value = parsed_row.pop(original_fieldname)
                    parsed_row[translated_fieldname] = value

            parsed_rows.append(parsed_row)

    return parsed_rows
