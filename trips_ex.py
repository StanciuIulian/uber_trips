import sys
import click
import csv
import pprint
from collections import Counter
from datetime import datetime


class Calatorie:

    def __init__(
        self,
        calatorie,
    ):

        self.calatorie = calatorie
        self.elemente = []

    def csv_to_dict_list(self, csv_file):
        try:
            with open(csv_file, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.elemente.append(row)
        except SyntaxError:
            sys.exit("Could not format CSV")

    def trip_cost(self):
        cost_ron = [
            float(cost["Fare Amount"])
            for cost in self.elemente
            if isinstance(cost, dict)
            and cost.get("Fare Currency") == "RON"
            and cost.get("Fare Amount") is not None
            and isinstance(cost["Fare Amount"], (int, float, str))
        ]

        cost_euro = [
            float(cost["Fare Amount"])
            for cost in self.elemente
            if isinstance(cost, dict)
            and cost.get("Fare Currency") == "EUR"
            and cost.get("Fare Amount") is not None
            and isinstance(cost["Fare Amount"], (int, float, str))
        ]

        cost_total = sum(cost_ron) + sum(cost_euro) * 5
        return cost_total

    def trip_canceled(self):
        curse_anulate = len(
            [
                curse
                for curse in self.elemente
                if isinstance(curse, dict)
                and curse.get("Trip or Order Status") == "CANCELED"
            ]
        )
        return curse_anulate

    def trip_completed(self):
        curse_complete = len(
            [
                curse
                for curse in self.elemente
                if isinstance(curse, dict)
                and curse.get("Trip or Order Status") == "COMPLETED"
            ]
        )
        return curse_complete

    def total_trips(self):
        curse_anulate = self.trip_canceled()
        curse_complete = self.trip_completed()
        curse_totale = curse_anulate + curse_complete
        return curse_totale

    def city_trips(self):
        curse_orase = list(
            Counter(
                curse["City"]
                for curse in self.elemente
                if isinstance(curse, dict) and "City" in curse
            ).items()
        )
        return curse_orase

    def total_diatance(self):
        distanta_mile = [
            float(curse["Distance (miles)"])
            for curse in self.elemente
            if isinstance(curse, dict)
            and curse.get("Trip or Order Status") == "COMPLETED"
            and curse.get("Distance (miles)") is not None
            and isinstance(curse["Distance (miles)"], (int, float, str))
        ]
        distanta_totala = sum(distanta_mile) * 1.6
        return distanta_totala

    def product_type(self):
        curse_produs = list(
            Counter(
                curse["Product Type"]
                for curse in self.elemente
                if isinstance(curse, dict) and "Product Type" in curse
            ).items()
        )
        return curse_produs

    def begin_trip_time(self):
        inceput_cursa = [
            curse["Begin Trip Time"]
            for curse in self.elemente
            if isinstance(curse, dict)
        ]
        timp_inceput_cursa = []
        for timp in inceput_cursa:
            if timp == "2023-04-10 10:11:31 +0000 UTC":
                continue
            dt = datetime.strptime(timp, "%Y-%m-%d %H:%M:%S %z %Z")
            if dt.year == 1970:
                continue
            timestamp_in_seconds = int(dt.timestamp())
            timp_inceput_cursa.append(timestamp_in_seconds)
        return timp_inceput_cursa

    def dropoff_trip_time(self):
        sfarsit_cursa = [
            curse["Dropoff Time"] for curse in self.elemente if isinstance(curse, dict)
        ]
        timp_sfarsit_cursa = []
        curse_by_year = {}

        for curse, timp in zip(self.elemente, sfarsit_cursa):
            dt = datetime.strptime(timp, "%Y-%m-%d %H:%M:%S %z %Z")
            if dt.year == 1970:
                continue
            timestamp_in_seconds = int(dt.timestamp())
            timp_sfarsit_cursa.append(timestamp_in_seconds)

            year = dt.year
            if year not in curse_by_year:
                curse_by_year[year] = []
            curse_by_year[year].append(curse)

        return timp_sfarsit_cursa, curse_by_year

    def time_spent_trips(self):
        timp_inceput_cursa = self.begin_trip_time()
        timp_sfarsit_cursa, _ = self.dropoff_trip_time()
        timp_petrecut_calatorii = [
            val1 - val2 for val1, val2 in zip(timp_sfarsit_cursa, timp_inceput_cursa)
        ]
        return timp_petrecut_calatorii

    def time_spent_seconds(self):
        timp_petrecut_calatorii = self.time_spent_trips()
        timp_petrecut_in_secunde = sum(timp_petrecut_calatorii)
        return timp_petrecut_in_secunde

    def time_spent_minutes(self):
        timp_petrecut_in_secunde = self.time_spent_seconds()
        timp_petrecut_in_minute = timp_petrecut_in_secunde / 60
        return timp_petrecut_in_minute

    def time_spent_hours(self):
        timp_petrecut_in_minute = self.time_spent_minutes()
        timp_petrecut_in_ore = round((timp_petrecut_in_minute / 60), 2)
        return timp_petrecut_in_ore

    def time_spent_days(self):
        timp_petrecut_in_ore = self.time_spent_hours()
        timp_petrecut_in_zile = round((timp_petrecut_in_ore / 24), 2)
        return timp_petrecut_in_zile

    def shortest_trip(self):
        timp_petrecut_calatorii = self.time_spent_trips()
        cea_mai_scurta_cursa = min(timp_petrecut_calatorii) / 60
        return cea_mai_scurta_cursa

    def longest_trip(self):
        timp_petrecut_calatorii = self.time_spent_trips()
        cea_mai_lunga_cursa = round((max(timp_petrecut_calatorii) / 60), 2)
        return cea_mai_lunga_cursa

    def years_trip(self):
        _, curse_by_year = self.dropoff_trip_time()
        curse_pe_an = {year: len(curse) for year, curse in curse_by_year.items()}
        return curse_pe_an


@click.command()
@click.argument("csv_file", type=click.Path(exists=True))
def main(csv_file):
    calatorie = Calatorie(csv_file)
    calatorie.csv_to_dict_list(csv_file)
    cost_total = calatorie.trip_cost()
    curse_anulate = calatorie.trip_canceled()
    curse_complete = calatorie.trip_completed()
    curse_totale = calatorie.total_trips()
    curse_orase = calatorie.city_trips()
    distanta_totala = calatorie.total_diatance()
    curse_produs = calatorie.product_type()
    timp_inceput_cursa = calatorie.begin_trip_time()
    timp_sfarsit_cursa = calatorie.dropoff_trip_time()
    timp_petrecut_calatorii = calatorie.time_spent_trips()
    timp_petrecut_in_secunde = calatorie.time_spent_seconds()
    timp_petrecut_in_minute = calatorie.time_spent_minutes()
    timp_petrecut_in_ore = calatorie.time_spent_hours()
    timp_petrecut_in_zile = calatorie.time_spent_days()
    cea_mai_scurta_cursa = calatorie.shortest_trip()
    cea_mai_lunga_cursa = calatorie.longest_trip()
    curse_pe_an = calatorie.years_trip()

    print("STATISTICI")
    print("*" * 32)
    print(f"Cost total curse {cost_total} RON")
    print(f"Total curse anulate {curse_anulate}")
    print(f"Total curse complete {curse_complete}")
    print(f"Total curse {curse_totale}")
    print(f"Curse anuale {curse_pe_an}")
    print(f"Curse pe oras {curse_orase}")
    print(f"Distanta totala parcursa {distanta_totala} km")
    print(f"Curse produs {curse_produs}")
    print(f"Perioada totala petrecuta {timp_petrecut_in_secunde} secunde")
    print(f"Perioada totala petrecuta {timp_petrecut_in_minute} minute")
    print(f"Perioada totala petrecuta {timp_petrecut_in_ore} ore")
    print(f"Perioada totala petrecuta {timp_petrecut_in_zile} zile")
    print(f"Cea mai scurta cursa {cea_mai_scurta_cursa} minute")
    print(f"Cea mai lunga cursa {cea_mai_lunga_cursa} minute")


if __name__ == "__main__":
    main()
