import argparse
import urllib.request
import shutil
import sqlite3
import os
import ssl
import fitz

first_column = 52.560001373291016
second_column = 150.86000061035156
third_column = 229.82000732421875
fourth_column = 423.19000244140625
fifth_column = 623.8599853515625


def main(url):
    # it cleans the resource folder to avoid exception
    check_and_remove_resource_folder()

    path = "docs/downloaded_file.pdf"

    # Download data
    fetchincidents(url)

    # Extract data
    incidents = extractincidents(path)

    # Create new database
    db = createdb()

    # Insert data
    populatedb(db, incidents)

    # Print incident counts
    status(db)


def check_and_remove_resource_folder():
    if os.path.exists("resources"):
        shutil.rmtree("resources")
    if os.path.exists("docs"):
        shutil.rmtree("docs")


def fetchincidents(url):
    try:

        incident_data = urllib.request.urlopen(url)
        docs_dir = 'docs'
        if not os.path.exists(docs_dir):
            os.makedirs(docs_dir)
        path = os.path.join(docs_dir, "downloaded_file.pdf")
        with open(path, 'wb') as local_file:
            local_file.write(incident_data.read())
    except Exception as e:
        print(f"An error occurred while calling normanpd URL: {e}")


def extractincidents(path):
    try:
        doc = fitz.open(path)
        incidents = []
        incident = [''] * 5
        group_number = 0
        for page in doc:
            tuples = page.get_text('words')
            for data in tuples:
                current_number = data[5]
                if current_number == group_number:
                    add_data(incident, data)
                else:
                    text = incident[2]
                    if text.find("NORMAN POLICE DEPARTMENT") == -1 and text.find("Daily Incident Summary") == -1:
                        incidents.append(tuple(incident))
                    incident = [''] * 5
                    add_data(incident, data)
                    group_number = current_number
        if len(incidents) > 0:
            incidents.pop(0)
        return incidents
    except Exception as e:
        print(f"An error occurred while parsing PDF: {e}")


def add_data(incident, data):
    coordinate = data[0]
    text = data[4]
    if coordinate == first_column or coordinate < second_column:
        incident[0] = incident[0] + " " + text if incident[0] else text
    elif coordinate == second_column or coordinate < third_column:
        incident[1] = incident[1] + " " + text if incident[1] else text
    elif coordinate == third_column or coordinate < fourth_column:
        incident[2] = incident[2] + " " + text if incident[2] else text
    elif coordinate == fourth_column or coordinate < fifth_column:
        incident[3] = incident[3] + " " + text if incident[3] else text
    else:
        incident[4] = incident[4] + " " + text if incident[4] else text


# def extract_incidents_using_layout_mode(path):
#     reader = PdfReader(path)
#     pages = reader.pages
#     incidents = []
#     for page in pages:
#         data = page.extract_text(extraction_mode="layout")
#         for line in data.splitlines():
#             line = line.strip()
#             if line and line.find("Incident Number") == -1 and line.find("NORMAN POLICE DEPARTMENT") == -1 and line.find("Daily Incident Summary") == -1:
#                 res = re.split(r'\s{3,}', line)
#                 if len(res) == 1 and len(incidents) > 0 and res[0].isupper():
#                     last_tuple = incidents[-1]
#                     new_list = list(last_tuple)
#                     new_list[2] = new_list[2] + " " + res[0]
#                     incidents.pop()
#                     incidents.append(tuple(new_list))
#                 if len(res) == 5:
#                     incidents.append(tuple(res))
#     return incidents


def createdb():
    try:
        resources_dir = 'resources'
        if not os.path.exists(resources_dir):
            os.makedirs(resources_dir)
        con = sqlite3.connect(os.path.join(resources_dir, "normanpd.db"))
        return con
    except Exception as e:
        print("Exception Occurred while connecting to SQLLite ", e)


def populatedb(db, incident_data):
    cur = db.cursor()
    db.execute(
        "CREATE TABLE incidents (incident_time TEXT, incident_number TEXT, incident_location TEXT, nature TEXT, incident_ori TEXT);")
    cur.executemany("INSERT INTO incidents VALUES(?, ?, ?, ?, ?)", incident_data)
    db.commit()
    return


def status(db):
    cursor = db.cursor()
    cursor.execute(
        "SELECT nature, COUNT(*) as occurrence FROM incidents GROUP BY nature ORDER BY occurrence DESC, nature;")
    results = cursor.fetchall()
    is_empty = False
    empty_count = 0
    for nature, occurrence in results:
        if len(nature) == 0:
            empty_count = occurrence
            is_empty = True
            continue
        if is_empty and empty_count > occurrence:
            print(f"|{empty_count}")
            is_empty = False
        print(f"{nature}|{occurrence}")
    if is_empty:
        print(f"|{empty_count}")
    db.close()
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True,
                        help="Incident summary url.")

    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)
