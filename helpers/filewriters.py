import json, csv

def write_to_json(full_data, loc):
    with open(loc, 'w') as out:
        out.write(json.dumps(full_data, indent=4))

def write_to_csv(full_data,loc):
    with open(loc, 'w') as csvfile:
        csv_columns = list(full_data[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for parcel in full_data:
            writer.writerow(parcel)


