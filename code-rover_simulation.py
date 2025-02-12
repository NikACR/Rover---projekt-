import time
from dronekit import connect, VehicleMode, LocationGlobalRelative
import math


class Prekazka:
    def __init__(self, lat, lon, radius):
        self.lat = lat
        self.lon = lon
        self.radius = radius


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Vypočítá vzdálenost mezi dvěma GPS souřadnicemi v metrech.
    """
    R = 6371000  # Poloměr Země v metrech
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def detect_obstacle(current_location, prekazky):
    """
    Detekuje překážky na trase a vrací překážku, pokud se rover nachází v jejím okruhu.
    """
    for prekazka in prekazky:
        vzdalenost = calculate_distance(current_location.lat, current_location.lon, prekazka.lat, prekazka.lon)
        if vzdalenost < prekazka.radius:
            return prekazka
    return None


def navigate_to_waypoint(vehicle, lat, lon, prekazky):
    """
    Navigace k waypointu s detekcí překážek a objížděním.
    """
    NORMALNI_RYCHLOST = 5  # m/s
    SNIZENA_RYCHLOST = 2   # m/s
    UHYBACI_VZDALENOST = 0.0002  # Vzdálenost pro objetí
    
    target_location = LocationGlobalRelative(lat, lon, 10)
    vehicle.groundspeed = NORMALNI_RYCHLOST
    vehicle.simple_goto(target_location)
    print(f"Navigace na waypoint: ({lat}, {lon})")

    while True:
        current_location = vehicle.location.global_relative_frame
        vzdalenost = calculate_distance(current_location.lat, current_location.lon, lat, lon)
        rychlost = vehicle.groundspeed

        print(f"  Aktuální pozice: ({current_location.lat}, {current_location.lon})")
        print(f"  Zbývá vzdálenost: {vzdalenost:.2f} m")
        print(f"  Rychlost: {rychlost:.2f} m/s")

        if vzdalenost < 1.0:
            print("Waypoint dosažen.")
            break

        prekazka = detect_obstacle(current_location, prekazky)
        if prekazka:
            print(f"Detekována překážka na pozici ({prekazka.lat}, {prekazka.lon})!")
            print("Snižuji rychlost a objíždím...")
            
            # Snížení rychlosti
            vehicle.groundspeed = SNIZENA_RYCHLOST
            
            # Určení směru objetí
            if current_location.lon < prekazka.lon:
                print("Objíždím překážku ZPRAVA.")
                new_location = LocationGlobalRelative(
                    current_location.lat,
                    current_location.lon + UHYBACI_VZDALENOST,
                    10
                )
            else:
                print("Objíždím překážku ZLEVA.")
                new_location = LocationGlobalRelative(
                    current_location.lat,
                    current_location.lon - UHYBACI_VZDALENOST,
                    10
                )
            
            vehicle.simple_goto(new_location)
            time.sleep(2)  # Počkáme, než se rover posune
            vehicle.simple_goto(target_location)  # Pokračujeme k cíli
        else:
            vehicle.groundspeed = NORMALNI_RYCHLOST
            
        time.sleep(1)


def main():
    connection_string = "tcp:127.0.0.1:5762"
    
    print("Připojuji se k vozidlu...")
    vehicle = connect(connection_string, wait_ready=True)
    
    # Získání skutečné startovní pozice
    start_location = vehicle.location.global_relative_frame
    start_position = (start_location.lat, start_location.lon)
    print(f"Startovní pozice: {start_position}")

    # Seznam překážek na trase
    prekazky = [
        Prekazka(-35.3619, 149.1665, 5),
        Prekazka(-35.3621, 149.1663, 5),
    ]

    print("Čekám na inicializaci vozidla...")
    while not vehicle.is_armable:
        print("  Vozidlo není připraveno. Čekám...")
        time.sleep(1)

    print("Armování motorů...")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print("  Čekám na armování...")
        time.sleep(1)

    print("Motory armovány! Připraven k navigaci.")

    # Seznam waypointů - cesta, kterou má rover projet
    waypoints = [
        (-35.3622, 149.1662),
        (-35.3620, 149.1664),
        (-35.3618, 149.1666),
        (-35.3616, 149.1664),
        (-35.3614, 149.1670),
    ]

    # Navigace přes všechny waypointy
    for i, waypoint in enumerate(waypoints, 1):
        print(f"\nNavigace k waypointu {i} z {len(waypoints)}")
        navigate_to_waypoint(vehicle, waypoint[0], waypoint[1], prekazky)

    # Návrat na startovní pozici
    print("\nNávrat na startovní pozici...")
    navigate_to_waypoint(vehicle, start_position[0], start_position[1], prekazky)

    print("Zastavuji rover...")
    vehicle.mode = VehicleMode("HOLD")
    print("Mise dokončena! Rover zastaven.")


if __name__ == "__main__":
    main()