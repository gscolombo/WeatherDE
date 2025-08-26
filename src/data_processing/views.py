
views = {
    ("last_records_dt", "weather-ts"): [
        {"$sort": {"dt": 1}},
        {
            "$group": {
                "_id": {
                    "lat": {"$trunc": ["$coord.lat", 2]}, "lon": {"$trunc": ["$coord.lon", 2]}
                },
                "dt": {"$last": "$dt"},
                "main": {"$last": "$main"},
                "wind": {"$last": "$wind"},
                "weather": {"$last": "$weather"}
            }
        }
    ]
}
