import csv
import io

def export_csv(rows):
    output = io.StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(["name", "note"])
    writer.writerows(rows)
    return output.getvalue()
