import os
import rows


properties_of_interest = []

for result in os.listdir("results"):
    results = rows.import_from_csv("results/" + result)
    properties = [
        p._asdict()
        for p in results
        if p.for_rent
        and p.property_type == "casa"
        and p.rent_price <= 1500
        and "campinas" in p.city.lower()
    ]
    properties_of_interest.extend(properties)

table = rows.import_from_dicts(properties_of_interest)
rows.export_to_csv(table, "properties_of_interest_2.csv")
