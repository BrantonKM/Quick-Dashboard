from io import BytesIO, StringIO
import csv

def generate_csv(rows):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Section", "Content", "Fetched At"])
    for row in rows:
        writer.writerow(row)
    byte_stream = BytesIO()
    byte_stream.write(output.getvalue().encode("utf-8"))
    byte_stream.seek(0)
    return byte_stream
