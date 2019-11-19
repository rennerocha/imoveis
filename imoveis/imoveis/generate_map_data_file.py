import json
import rows


feature_collection = {"type": "FeatureCollection", "features": []}
properties = rows.import_from_csv("properties_of_interest.csv")


for result in properties:
    feature_collection["features"].append(
        {
            "properties": {
                "latitude": result.latitude,
                "longitude": result.longitude,
                "code": result.code,
                "url": result.url,
                "rent_price": result.rent_price,
            },
            "geometry": {
                "type": "Point",
                "coordinates": [result.longitude, result.latitude],
            },
            "type": "Feature",
        }
    )

with open("gui/data.js", "w") as data:
    data.write(json.dumps(feature_collection))
