#!/usr/bin/env python3

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import httpx

app = FastAPI()

API_KEY = "5e44a2d73bf8b12ceb6134503cd93e77"


@app.get("/")
async def funcname(request: Request):

    client_ip = request.headers['x-client-ip']
    geolocation = httpx.get(f"http://ip-api.com/json/{client_ip}").json()

    #  return (request.method, request.url, request.headers, request.query_params, request.client, request.cookies, body)

    country = geolocation['country']
    region = geolocation['regionName']
    city = geolocation['city']
    lat = geolocation['lat']
    lon = geolocation['lon']

    # https://openweathermap.org/current
    weather = httpx.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}").json()

    temp = weather['main']['temp']
    feels_like = weather['main']['feels_like']
    humidity = weather['main']['humidity']

    html_content = f"""
    <html>
        <head>
            <title>Welcome</title>
        </head>
        <body>
        <div style="display:flex;justify-content:center;align-items:center;flex-direction:column;">
            <div>
                <h1>It seems like your ip is {client_ip}</h1>
            </div>
            <div>
                <h1>Based on that, it seems like you live in {country}, {region}, {city}</h1>
            </div>
            <div>
                <h1>lon: {lon}° lat: {lat}°</h1>
            </div>
            <div>
                <h1>🌤 It is currently {temp}°C with a humidity of {humidity} and it feels like {feels_like}°C</h1>
            </div>
        </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
