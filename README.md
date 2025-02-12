# Projekt: Autonomní Rover v SITL

## Obsah
- [O projektu](#o-projektu)
- [Funkce](#funkce)
- [Požadavky](#požadavky)
- [Instalace](#instalace)
- [Použití](#použití)
- [Struktura projektu](#struktura-projektu)
- [To-Do list](#to-do-list)

---

## O projektu
Tento projekt se zaměřuje na simulaci autonomního čtyřkolového roveru v SITL (Software In The Loop). Rover naviguje po předem definované trase s možnými dynamickými změnami waypointů a schopností detekovat a obcházet překážky.

---

## Funkce
- **Nastavení roveru**: Definice velikosti, rychlosti a typu pohonu vozidla.
- **Definice trasy**: Určení startovního a cílového bodu s waypointy mezi nimi.
- **Detekce překážek**: Rover rozpozná překážky na trase pomocí senzorů.
- **Vyhýbání se překážkám**: Automatické rozhodování, zda překážku objet zprava nebo zleva.
- **Dynamická změna waypointů**: Přidává nové waypointy při zablokované trase.
- **Zobrazení dat**: Během simulace se vypisuje aktuální pozice, rychlost, vzdálenost k překážkám a waypointům.
- **Zastavení u cíle**: Rover se zastaví po dosažení cílového bodu.

---

## Požadavky
Pro běž tohoto projektu je nutné mít nainstalované:
- **Ubuntu/Linux nebo Windows s WSL**
- **Python 3.8+**
- **ArduPilot SITL**
- **MAVProxy**
- **Mission Planner / APM Planner**
- **Knihovny Pythonu**: `pymavlink`, `matplotlib`, `numpy`, `pandas`, `dronekit`

---

## Instalace
1. **Nainstalujte ArduPilot SITL**
```bash
sudo apt update && sudo apt install git python3 python3-pip
git clone --recurse-submodules https://github.com/ArduPilot/ardupilot.git
cd ardupilot
Tools/environment_install/install-prereqs-ubuntu.sh -y
. ~/.profile
```
2. **Nainstalujte Python knihovny**
```bash
pip install pymavlink matplotlib numpy pandas dronekit
```
3. **Spuštění SITL simulace roveru**
```bash
cd ardupilot/ArduRover
sim_vehicle.py -v ArduRover -L KSFO
```

---

## Použití
1. **Spuštění simulace**
2. **Nastavení trasy a waypointů**
3. **Zapnutí detekce překážek**
4. **Monitorování dat během simulace**
5. **Ukončení roveru v cíli**

---

## Struktura projektu
```
/
├── rover_navigation.py  # Hlavní skript pro řízení roveru
├── sensors.py          # Modul pro senzorickou detekci
├── waypoints.py        # Modul pro správu waypointů
├── visualization.py    # Vykreslení trasy a pohybu roveru
├── README.md          # Dokumentace projektu
├── requirements.txt   # Požadované knihovny
```

---

## To-Do list
- [ ] Implementovat pokročilejší algoritmus pro vyhýbání se překážám a dle podmínek upravit algoritmus na vyhýbání překážkám
- [ ] Vytvořit úspěšnou komunikaci pro připojení k Mission Planneru, kde by se daly simulovat mise dle potřeb
- [ ] Zlepšit a vylepšit celkově pohyb Roveru, co se týče rychlosti
- [ ] Vytvořit řešení pro dynamickou změnu waypointů a aby se automaticky přidávaly a komunikovaly přes senzory.


