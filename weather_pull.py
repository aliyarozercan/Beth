# weather_pull.py

import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import matplotlib
matplotlib.use("Agg")  # Safe backend for headless systems
import matplotlib.pyplot as plt
from datetime import datetime
import os

def get_weather_forecast():
    # Setup Open-Meteo API with cache and retry
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 0.0,  # <-- Replace with your location or configure via env var
        "longitude": 0.0,
        "hourly": [
            "temperature_2m",
            "precipitation_probability",
            "cloud_cover"
        ],
        "forecast_days": 1
    }

    response = openmeteo.weather_api(url, params=params)[0]
    hourly = response.Hourly()

    # Create DataFrame
    times = pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    ).tz_convert("America/Los_Angeles")  # <-- Optional: customize your timezone

    df = pd.DataFrame({
        "time": times, 
        "temperature": hourly.Variables(0).ValuesAsNumpy(),
        "rain_chance": hourly.Variables(1).ValuesAsNumpy(),
        "cloud_cover": hourly.Variables(2).ValuesAsNumpy(),
    })
    
    # Filter 8am–10pm
    today = datetime.now().astimezone()
    start = today.replace(hour=8, minute=0, second=0, microsecond=0)
    end = today.replace(hour=22, minute=0, second=0, microsecond=0)
    df_filtered = df[(df["time"] >= start) & (df["time"] <= end)]
            
    # 🌡️ Summary
    min_temp = df_filtered["temperature"].min()
    max_temp = df_filtered["temperature"].max()
     
    rain_over_5 = df_filtered[df_filtered["rain_chance"] > 5]
    if not rain_over_5.empty:
        max_rain = rain_over_5["rain_chance"].max()
        earliest_rain_time = rain_over_5.iloc[0]["time"].strftime("%I:%M %p")
        rain_summary = f"☔ Rain chance up to {max_rain:.0f}% starting around {earliest_rain_time}"
    else:
        rain_summary = "☀️ No significant rain expected today."

    # 📈 Plots directory
    os.makedirs("plots", exist_ok=True)

    df_plot = df_filtered.set_index("time").resample("2h").mean()

    # Temperature plot
    plt.figure()
    df_plot["temperature"].plot(marker="o")
    plt.title("Temperature (°C)")
    plt.ylabel("°C")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("plots/beth_temp_plot.png")
    plt.close()

    # Cloud cover plot
    plt.figure()
    df_plot["cloud_cover"].plot(marker="o", color="gray")
    plt.title("Cloud Cover (%)")
    plt.ylabel("%")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("plots/beth_cloud_plot.png")
    plt.close()

    # Rain plot (only if relevant)
    if not rain_over_5.empty:
        plt.figure()
        df_plot["rain_chance"].plot(marker="o", color="blue")
        plt.title("Rain Chance (%)")
        plt.ylabel("%")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("plots/beth_rain_plot.png")
        plt.close()

    # Final weather summary text
    summary = (
        f"🌡️ Temp range: {min_temp:.1f}°C - {max_temp:.1f}°C\n"
        f"{rain_summary}"
    )

    return summary

if __name__ == "__main__":
    print(get_weather_forecast())
