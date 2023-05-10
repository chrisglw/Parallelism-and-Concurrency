"""
Course: CSE 251 
Lesson Week: 02
File: assignment.py 
Author: Brother Comeau

I followed the hints that the professor gave in class, plus the study material 
in order to fulfill all the requirements for this assignment. 

Purpose: Retrieve Star Wars details from a server

Instructions:

- Each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- Run the server.py program from a terminal/console program.  Simply type
  "python server.py"
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information from the
  server.
- You need to match the output outlined in the description of the assignment.
  Note that the names are sorted.
- You are required to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the server. You can
  define your class within this Python file (ie., no need to have a separate
  file for the class)
- Do not add any global variables except for the ones included in this program.

The call to TOP_API_URL will return the following Dictionary(JSON).  Do NOT have
this dictionary hard coded - use the API call to get this.  Then you can use
this dictionary to make other API calls for data.

{
   "people": "http://127.0.0.1:8790/people/", 
   "planets": "http://127.0.0.1:8790/planets/",
   "films": "http://127.0.0.1:8790/films/",
   "species": "http://127.0.0.1:8790/species/", 
   "vehicles": "http://127.0.0.1:8790/vehicles/", 
   "starships": "http://127.0.0.1:8790/starships/"
}
"""

from datetime import datetime, timedelta
import requests
import json
import threading

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0


# TODO Add your threaded class definition here
class Request_thread(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url
        self.response = {}

    def run(self):
        response = requests.get(self.url)
        global call_count
        call_count += 1
        if response.status_code == 200:
            self.response = response.json()
        else:
            print('RESPONSE = ', response.status_code)

# TODO Add any functions you need here
def get_top_api_urls():
    req = Request_thread(TOP_API_URL)
    req.start()
    req.join()
    return req.response


def get_film_details(film_url):
    req = Request_thread(film_url)
    req.start()
    req.join()
    return req.response

def main():
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')

    # TODO Retrieve Top API urls
    top_urls = get_top_api_urls()

    # TODO Retrieve Details on film 6
    film_url = top_urls['films'] + '6/'
    film_data = get_film_details(film_url)

    # TODO Display results
    character_list = []
    for url in film_data['characters']:
        req = Request_thread(url)
        req.start()
        character_list.append(req)
    for thread in character_list:
        thread.join()
    characters = sorted([char.response['name'] for char in character_list])

    planet_list = []
    for url in film_data['planets']:
        req = Request_thread(url)
        req.start()
        planet_list.append(req)
    for thread in planet_list:
        thread.join()
    planets = sorted([planet.response['name'] for planet in planet_list])

    species_list = []
    for url in film_data['species']:
        req = Request_thread(url)
        req.start()
        species_list.append(req)
    for thread in species_list:
        thread.join()
    species = sorted([specie.response['name'] for specie in species_list])

    starship_list = []
    for url in film_data['starships']:
        req = Request_thread(url)
        req.start()
        starship_list.append(req)
    for thread in starship_list:
        thread.join()
    starships = sorted([starship.response['name'] for starship in starship_list])

    vehicle_list = []
    for url in film_data['vehicles']:
        req = Request_thread(url)
        req.start()
        vehicle_list.append(req)
    for thread in vehicle_list:
        thread.join()
    vehicles = sorted([vehicle.response['name'] for vehicle in vehicle_list])

    log.write(f'{"-"*40}')
    log.write(f'{"Title":<7} : {film_data["title"]}')
    log.write(f'{"Director:"} {film_data["director"]}')
    log.write(f'{"Producer:"} {film_data["producer"]}')
    log.write(f'{"Released:"} {film_data["release_date"]}')
    log.write('')
    log.write(f'{"Characters:"} {len(characters)}')
    charactersClean = str(characters)
    log.write(charactersClean[1:-1].replace("'", ""))
    log.write('')
    log.write(f'{"Planets:"} {len(planets)}')
    PlanetsClean = str(planets)
    log.write(PlanetsClean[1:-1].replace("'", ""))
    log.write('')
    log.write(f'{"Starships:"} {len(starships)}')
    starshipsClean = str(starships)
    log.write(starshipsClean[1:-1].replace("'", "")) # starships
    log.write('')
    log.write(f'{"Vehicles:"} {len(vehicles)}')
    vehiclesClean = str(vehicles)
    log.write(vehiclesClean[1:-1].replace("'", "")) # vehicles
    log.write('')
    log.write(f'{"Species:"} {len(species)}')
    speciesClean = str(species)
    log.write(speciesClean[1:-1].replace("'", "")) # species
    log.write('')
    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to swapi server')

if __name__ == "__main__":
    main()