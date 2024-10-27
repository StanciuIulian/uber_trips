# Uber Trips

## Descriere

Este o aplicație pentru statistica călătoriilor cu UBER folosind fișierul CSV cu propriile călătorii. 
Cu această aplicație utilizatorul poate afla:

1. Costul total al curselor
2. Total curse 
3. Total curse anulate
4. Total curse complete
5. Total curse efectuate în funcție de anul efectuării
6. Total curse efectuate în funcție de oraș
7. Distanța totală parcursă în km
8. Total curse efectuate cu un anumit tip de Uber
9. Perioada total în curse în:
   - secunde,
   - minute,
   - ore,
   - zile
10. Cea mai scurtă cursă
11. Cea mai lungă cursă

## Obținerea fișierului CSV

Pentru a obține fișierul CSV cu propriile călătorii, apasă [aici](https://help.uber.com/driving-and-delivering/article/download-your-uber-personaldata?nodeId=fbf08e68-65ba-456b-9bc6-1369eb9d2c44).

## Instalare

1. Clonează repository-ul într-un mediu virtual compatibil cu Python.
2. Instalează dependențele:

    ```bash
    pip install -r requirements.txt
    ```

## Utilizare

Pentru utilizare, fișierul CSV trebuie adăugat în proiect:

    ```bash
    python trips_ex.py <numefisier>.csv
    ```

