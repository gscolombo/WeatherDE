
views = {
    ("last_main_records", "weather-ts"): [
        {"$sort": {"dt": 1}},
        {
            "$group": {
                "_id": {
                    "lat": {"$round": ["$coord.lat", 2]}, "lon": {"$round": ["$coord.lon", 2]}
                },
                "dt": {"$last": "$dt"},
                "main": {"$last": "$main"},
            }
        }
    ],

    ("last_wind_records", "weather-ts"): [
        {"$sort": {"dt": 1}},
        {
            "$group": {
                "_id": {
                    "lat": {"$round": ["$coord.lat", 2]}, "lon": {"$round": ["$coord.lon", 2]}
                },
                "dt": {"$last": "$dt"},
                "wind": {"$last": "$wind"},
            }
        }
    ],

    ("last_weather_records", "weather-ts"): [
        {"$sort": {"dt": 1}},
        {
            "$group": {
                "_id": {
                    "lat": {"$round": ["$coord.lat", 2]}, "lon": {"$round": ["$coord.lon", 2]}
                },
                "dt": {"$last": "$dt"},
                "weather": {"$last": "$weather"},
            }
        }
    ]
}
