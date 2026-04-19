import sqlalchemy as sa
from app.database import SessionLocal
from app.models import Weather, CelestialEvents
from datetime import datetime

def get_weather_info():
    db = SessionLocal()
    print("--- Пошук погодних та астрономічних даних ---")
    
    country = input("Введіть назву країни (напр., Ukraine): ").strip()
    date_str = input("Введіть дату (YYYY-MM-DD, або натисніть Enter для останніх даних): ").strip()

    query = db.query(Weather).filter(Weather.country.ilike(country))

    if date_str:
        try:
            search_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            query = query.filter(sa.func.date(Weather.last_updated) == search_date)
        except ValueError:
            print("Неправильний формат дати. Використовуємо пошук лише за країною.")

    results = query.all()

    if not results:
        print(f"Пошук для '{country}' не дав результатів.")
    else:
        for item in results:
            print("-" * 40)
            print(f"КРАЇНА: {item.country}")
            print(f"Останнє оновлення: {item.last_updated}")
            print(f"Погода: Вітер {item.wind_kph} км/год, Напрямок: {item.wind_direction.value if item.wind_direction else 'N/A'}")
            
            c = item.celestial
            if c:
                print(f"Сонце: Схід {c.sunrise}, Захід {c.sunset}")
                print(f"Місяць: Фаза {c.moon_phase}, Освітленість {c.moon_illumination}%")
                
                recommendation = "Так, умови сприятливі" if c.should_go_outside else "Ні, краще залишитись вдома"
                print(f"Чи варто виходити: {recommendation}")
            print("-" * 40)

    db.close()

if __name__ == "__main__":
    get_weather_info()