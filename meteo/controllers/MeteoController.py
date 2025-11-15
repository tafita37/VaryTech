import requests
from django.views.decorators.http import require_GET
from django.shortcuts import render

API_KEY = "bd6e5a5b4a934bb8b9c90042251511"   # Mets ta vraie clé ici
BASE_URL = "https://api.weatherapi.com/v1/forecast.json"  # Exemple WeatherAPI

@require_GET
def meteo_prediction_page(request):
    city = "Antananarivo"   # Tu peux rendre ça dynamique plus tard
    days = 14                 # Nombre de jours de prévision

    try:
        response = requests.get(
            BASE_URL,
            params={
                "key": API_KEY,
                "q": city,
                "days": days,
                # "aqi": "no",
                # "alerts": "no"
            },
            timeout=5
        )

        response.raise_for_status()
        data = response.json()
        print(data["forecast"]["forecastday"][0]['day']['condition'])

    except Exception as e:
        data = None
        print("Erreur API météo :", e)

    context = {
        "titre_inner": "Prévisions Météo",
        "forecast": data["forecast"]["forecastday"] if data else [],
        "location": data["location"] if data else None,
    }

    return render(request, "views/meteo_prevision.html", context)