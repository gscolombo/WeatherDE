from typing import TypedDict, List


class Coordinates(TypedDict):
    lat: int
    lon: int


class Weather(TypedDict):
    id: int
    main: str
    description: str
    icon: str


class Main(TypedDict):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int
    sea_level: int
    grnd_level: int


class Wind(TypedDict):
    speed: float
    deg: int
    gust: float


class Clouds(TypedDict):
    all: int


Rain = TypedDict("Rain", {"1h": str})
Snow = TypedDict("Snow", {"1h": str})


class Sys(TypedDict):
    type: int
    id: int
    country: str
    sunrise: int
    sunset: int


class FullWeatherData(TypedDict):
    coord: Coordinates
    weather: List[Weather]
    base: str
    main: Main
    visibility: int
    wind: Wind
    clouds: Clouds
    rain: Rain
    Snow: Snow
    dt: int
    sys: Sys
    timezone: int
    id: int
    name: str
    cod: int
