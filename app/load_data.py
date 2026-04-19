import pandas as pd
from datetime import datetime
from app.database import SessionLocal
from app.models import Weather, CelestialEvents, WindDirection

def parse_time(time_str):
    if not isinstance(time_str, str) or time_str.strip() == "":
        return None
    try:
        # Обробка формату "06:15 AM"
        return datetime.strptime(time_str.strip(), "%I:%M %p").time()
    except ValueError:
        return None

def run_seed():
    db = SessionLocal()
    df = pd.read_csv('global_weather_repository.csv')
    
    print("Починаю завантаження даних...")
    
    for _, row in df.head(100).iterrows():
        wind_speed = float(row['wind_kph'])
        illumination = int(row['moon_illumination'])
        
        is_worth_going_out = (wind_speed < 30.0) and (illumination > 30)

        celestial = CelestialEvents(
            sunrise=parse_time(row['sunrise']),
            sunset=parse_time(row['sunset']),
            moonrise=parse_time(row['moonrise']),
            moonset=parse_time(row['moonset']),
            moon_phase=row['moon_phase'],
            moon_illumination=illumination,
            should_go_outside=is_worth_going_out
        )
        db.add(celestial)
        db.flush()

        w_direction = row['wind_direction']
        if w_direction not in WindDirection.__members__:
            w_direction = None 

        weather = Weather(
            country=row['country'],
            last_updated=pd.to_datetime(row['last_updated']),
            wind_degree=int(row['wind_degree']),
            wind_kph=wind_speed,
            wind_direction=w_direction,
            celestial_id=celestial.id
        )
        db.add(weather)

    try:
        db.commit()
        print("Успіх: 100 записів додано до бази!")
    except Exception as e:
        db.rollback()
        print(f"Помилка при збереженні: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run_seed()