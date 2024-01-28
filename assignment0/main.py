import argparse
import urllib.request
import ssl
import sqlite3
import re

from pypdf import PdfReader


def main(url):

    # Download data
    fetchincidents(url)

    # Extract data
    incidents = extractincidents()

    # Create new database
    db = createdb()

    # Insert data
    populatedb(db, incidents)

    # Print incident counts
    status(db)

# make sure the to remove the SSL
def fetchincidents(url):
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    try:
        incident_data = urllib.request.urlopen(url, context=ssl_context)
        path = "docs/downloaded_file.pdf"
        with open(path, 'wb') as local_file:
            local_file.write(incident_data.read())
    except Exception as e:
        print(f"An error occurred: {e}")

def extractincidents():
    reader = PdfReader("docs/downloaded_file.pdf")
    pages = reader.pages
    incidents = []
    for page in pages:
        data = page.extract_text(extraction_mode="layout")
        for line in data.splitlines():
            line = line.strip()
            if line and line.find("Incident Number") == -1:
                res = re.split(r'\s{2,}', line)
                if len(res) == 5:
                    incidents.append(tuple(res))
    return incidents


def createdb():
    try:
        con = sqlite3.connect("resources/normanpd.db")
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
    cursor.execute("SELECT nature, COUNT(*) as occurrence FROM incidents GROUP BY nature ORDER BY occurrence DESC, nature")

    results = cursor.fetchall()
    for nature, occurrence in results:
        print(f"{nature}|{occurrence}")
    db.close()
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True,
                        help="Incident summary url.")

    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)
