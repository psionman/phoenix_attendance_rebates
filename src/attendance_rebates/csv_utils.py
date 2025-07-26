import csv
from collections import defaultdict


def get_dict_from_csv_file(csv_path, key_field) -> tuple[dict, list]:
    """ Return a csv file as a dict (keyed on the value of key field,
        where the item is a dict of fields: values)."""
    csv_list = _get_csv_file_as_list(csv_path)
    (db_fields, fieldnames) = _get_csv_fields(csv_list, key_field)
    data_dict = defaultdict(dict)
    for row in csv_list:
        if not row:
            continue  # put in to trap extra empty row in Windows
        key = row[db_fields[key_field]]
        if key:
            for index, item in enumerate(row):
                data_dict[key][db_fields[index]] = item
    return (data_dict, fieldnames)


def _get_csv_fields(csv_list, key_field):
    """Return a dict of text: column and  column: text from the title row."""
    db_fields = {}
    fieldnames = []
    for row in csv_list:
        if key_field in row:
            for index, item in enumerate(row):
                db_fields[item] = index
                db_fields[index] = item
                fieldnames.append(item)
            break
    return (db_fields, fieldnames)


def _get_csv_file_as_list(path) -> list[list]:
    """Return csv file as a list of lists."""
    try:
        with open(path, 'r', newline='') as f_csv:
            return _list_from_csv(csv.reader(f_csv))
    except UnicodeDecodeError:
        with open(path, 'r', newline='', encoding='Windows-1252') as f_csv:
            return _list_from_csv(csv.reader(f_csv))
    except FileNotFoundError:
        print(f'File not found: {path}')
    return []


def _list_from_csv(items: csv.reader) -> list[list]:
    csv_list = []
    for row in items:
        for index, field in enumerate(row):
            if ',' in field:
                row[index] = row[index].replace(',', '')
        csv_list.append(row)
    return csv_list


def write_csv_file(path, fieldnames, items):
    with open(path, 'w', newline='') as f_csv:
        writer = csv.DictWriter(f_csv, fieldnames=fieldnames)
        writer.writeheader()
        for value in items.values():
            writer.writerow(value)
