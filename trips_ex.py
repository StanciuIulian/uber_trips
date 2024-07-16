import click
import csv
import pprint
from collections import Counter
from datetime import datetime


@click.command()
@click.argument('csv_file', type=click.Path(exists=True))
def csv_to_dict_list(csv_file):
    elemente = []
    try:
        with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                elemente.append(dict(row))
        click.echo(elemente)
    except SyntaxError:
        return click.echo(elemente)


class Calatorie:

    def __init__(self, cost_total, curse_anulate, curse_complete, curse_totale, curse_orase, distanta_totala,
                 curse_produs, extragere_date, timp_inceput_cursa, timp_sfarsit_cursa, total_timp_petrecut,
                 total_timp_secunde, timp_petrecut_in_minute, timp_petrecut_in_ore, timp_petrecut_in_zile,
                 cea_mai_scurta_cursa, cea_mai_lunga_cursa, curse_an ):
        self.cost_total = cost_total
        self.curse_anulate = curse_anulate
        self.curse_complete = curse_complete
        self.curse_totale = curse_totale
        self.curse_orase = curse_orase
        self.distanta_totala = distanta_totala
        self.curse_produs = curse_produs
        self.extragere_date = extragere_date
        self.timp_inceput_cursa = timp_inceput_cursa
        self.timp_sfarsit_cursa = timp_sfarsit_cursa
        self.total_timp_petrecut = total_timp_petrecut
        self.total_timp_secunde = total_timp_secunde
        self.timp_petrecut_in_minute = timp_petrecut_in_minute
        self.timp_petrecut_in_ore = timp_petrecut_in_ore
        self.timp_petrecut_in_zile = timp_petrecut_in_zile
        self.cea_mai_scurta_cursa = cea_mai_scurta_cursa
        self.cea_mai_lunga_cursa = cea_mai_lunga_cursa
        self.curse_an = curse_an


    def trip_cost(self):
        cost_ron = list(cost['Fare Amount'] for cost in elemente if cost['Fare Currency'] == 'RON')
        cost_euro = list(cost['Fare Amount'] for cost in elemente if cost['Fare Currency'] == 'EUR')
        cost_total_ron = sum(cost_ron)
        cost_total_euro = sum(cost_euro) * 5
        cost_total = cost_total_ron + cost_total_euro
        return cost_total

    def trip_canceled(self):
        curse_anulate = Counter(curse['Trip or Order Status'] for curse in elemente if
                                curse['Trip or Order Status'] == 'CANCELED')
        curse_anulate = curse_anulate['CANCELED']
        return curse_anulate

    def trip_completed(self):
        curse_complete = Counter(curse['Trip or Order Status'] for curse in elemente if
            curse['Trip or Order Status'] == 'COMPLETED')
        curse_complete = curse_complete['COMPLETED']
        return curse_complete

    def total_trips(self):
        curse_complete = calatorie.trip_completed()
        curse_anulate = calatorie.trip_canceled()
        curse_totale = curse_complete + curse_anulate
        return curse_totale

    def city_trips(self):
        curse_orase = list(Counter(curse['City'] for curse in elemente if curse['City'] == str(curse['City'])).items())
        return curse_orase

    def total_diatance(self):
        distanta_mile = list(curse['Distance (miles)'] for curse in elemente if
                             curse['Trip or Order Status'] == 'COMPLETED' for curse in elemente)
        distanta_mile = [elem for elem in distanta_mile if elem != '']
        distanta_totala = sum(distanta_mile) * 1.6
        return distanta_totala

    def product_type(self):
        curse_produs = list(Counter(curse['Product Type'] for curse in elemente).items())
        return curse_produs

    def begin_trip_time(self):
        inceput_cursa = list(curse['Begin Trip Time'] for curse in elemente)
        timp_inceput_cursa = []
        for timp in inceput_cursa:
            # aici am avut o cursa care incepea in data de 2023-04-10 si se termina in 1970-01-01
            if timp == '2023-04-10 10:11:31 +0000 UTC':
                continue
            dt = datetime.strptime(timp, '%Y-%m-%d %H:%M:%S %z %Z')
            if dt.year == 1970:
                continue
            timestamp = dt.strftime('%Y-%m-%d %H:%M:%S')
            timestamp_in_seconds = int(dt.timestamp())
            timp_inceput_cursa.append({dt.year: timestamp, 'seconds': timestamp_in_seconds})
        return timp_inceput_cursa

    def dropoff_trip_time(self):
        sfarsit_cursa = list(curse['Dropoff Time'] for curse in elemente)
        timp_sfarsit_cursa = []
        for timp in sfarsit_cursa:
            dt = datetime.strptime(timp, '%Y-%m-%d %H:%M:%S %z %Z')
            if dt.year == 1970:
                continue
            timestamp = dt.strftime('%Y-%m-%d %H:%M:%S')
            timestamp_in_seconds = int(dt.timestamp())
            timp_sfarsit_cursa.append({dt.year: timestamp, 'seconds': timestamp_in_seconds})
        return timp_sfarsit_cursa

    def time_spent_trips(self):
        timp_inceput_cursa = calatorie.begin_trip_time()
        timp_sfarsit_cursa = calatorie.dropoff_trip_time()
        timp_inceput = [cursa['seconds'] for cursa in timp_inceput_cursa]
        timp_sfarsit = [cursa['seconds'] for cursa in timp_sfarsit_cursa]
        timp_petrecut_calatorii = [val1 - val2 for val1, val2 in zip(timp_sfarsit, timp_inceput)]
        return timp_petrecut_calatorii

    def time_spent_seconds(self):
        timp_petrecut_calatorii = calatorie.time_spent_trips()
        timp_petrecut_in_secunde = sum(timp_petrecut_calatorii)
        return timp_petrecut_in_secunde

    def time_spent_minutes(self):
        timp_petrecut_in_secunde = calatorie.time_spent_seconds()
        timp_petrecut_in_minute = timp_petrecut_in_secunde / 60
        return timp_petrecut_in_minute

    def time_spent_hours(self):
        timp_petrecut_in_minute = calatorie.time_spent_minutes()
        timp_petrecut_in_ore = round((timp_petrecut_in_minute / 60), 2)
        return timp_petrecut_in_ore

    def time_spent_days(self):
        timp_petrecut_in_ore = calatorie.time_spent_hours()
        timp_petrecut_in_zile = round((timp_petrecut_in_ore / 24), 2)
        return timp_petrecut_in_zile

    def shortest_trip(self):
        timp_petrecut_calatorii = calatorie.time_spent_trips()
        cea_mai_scurta_cursa = min(timp_petrecut_calatorii) / 60
        return cea_mai_scurta_cursa

    def longest_trip(self):
        timp_petrecut_calatorii = calatorie.time_spent_trips()
        cea_mai_lunga_cursa = round((max(timp_petrecut_calatorii) / 60), 2)
        return cea_mai_lunga_cursa

    def yeas_trip(self):
        timp_sfarsit_cursa = calatorie.dropoff_trip_time()
        curse_an = {}
        for item in timp_sfarsit_cursa:
            for key in item:
                if isinstance(key, int):
                    if key in curse_an:
                        curse_an[key] += 1
                    else:
                        curse_an[key] = 1
        return curse_an


elemente = csv_to_dict_list()
calatorie = Calatorie('cost_total', 'curse_anulate', 'curse_complete',
                      'curse_totale', 'curse_orase', 'distanta_totala',
                      'curse_produs','extragere_date', 'timp_inceput_cursa',
                      'timp_sfarsit_cursa','total_timp_petrecut',
                      'total_timp_secunde', 'timp_petrecut_in_minute',
                      'timp_petrecut_in_ore', 'timp_petrecut_in_zile',
                      'cea_mai_scurta_cursa', 'cea_mai_lunga_cursa',
                      'curse_an' )
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
curse_an = calatorie.yeas_trip()

print("STATISTICI")
print("*" * 32)
print(f"Cost total curse {cost_total} RON")
print(f"Total curse anulate {curse_anulate}")
print(f"Total curse complete {curse_complete}")
print(f"Total curse {curse_totale}")
print(f"Curse anuale {curse_an}")
print(f"Curse pe oras {curse_orase}")
print(f"Distanta totala parcursa {distanta_totala} km")
print(f"Curse produs {curse_produs}")
print(f"Perioada totala petrecuta {timp_petrecut_in_secunde} secunde")
print(f"Perioada totala petrecuta {timp_petrecut_in_minute} minute")
print(f"Perioada totala petrecuta {timp_petrecut_in_ore} ore")
print(f"Perioada totala petrecuta {timp_petrecut_in_zile} zile")
print(f"Cea mai scurta cursa {cea_mai_scurta_cursa} minute")
print(f"Cea mai lunga cursa {cea_mai_lunga_cursa} minute")


if __name__ == '__main__':
    csv_to_dict_list()

