# This Python file uses the following encoding: utf-8
import random
import math
import json
import csv
import logging
import argparse
from configparser import ConfigParser


class Sheep:
    def __init__(self, init_pos_limit):
        #wspolrzednie owcy w obszarze (-10,10)
        self.init_pos_limit=random.uniform(0, 1)*init_pos_limit
        self.x = -(self.init_pos_limit)
        self.y = self.init_pos_limit
        self.status = "alive"
        log = "sheep initialization function called"
        logging.debug(log)
        log_info = "sheep inizialize position: " + str(self.x) + ", " + str(self.y)
        logging.info(log_info)
    def move_sheep(self, sheep_move_dist):
        directions = ["north", "west", "east", "south"]
        random.shuffle(directions)
        random_direction = directions[0]
        log_info = "move_sheep, position before: " + str(self.x) + ", " + str(self.y)
        logging.info(log_info)
        if random_direction == "north":
            #print("to jest polnoc")
            self.y += sheep_move_dist
        elif random_direction == "west":
            #print("to jest zachod")
            self.x -= sheep_move_dist
        elif random_direction == "east":
            #print("to jest wschod")
            self.x += sheep_move_dist
        else:
            #print("to jest poludnie")
            self.y -= sheep_move_dist
        log = "sheep move method called"
        logging.debug(log)
        log_info = "move_sheep, position after: " + str(self.x) + ", " + str(self.y)
        logging.info(log_info)

    def get_eaten(self):
        self.status = 'eaten'
        log = "get_eaten function called"
        logging.debug(log)

    def sheep_info(self):
        log = 'sheep_info function called'
        if(self.status == "alive"):
            log = "sheep_info function called, returned values: " + str(self.x) + ", " + str(self.y)
            logging.debug(log)
            return str(self.x) + ', ' + str(self.y)
        else:
            log = "sheep_info function called, returned values: " + "null"
            logging.debug(log)
            return 'null'

    def get_sheep_coordinates(self):
        print(self.x)
        print(self.y)
        log = "get_sheep_coordinates function called"
        logging.debug(log)

class Wolf:
    def __init__(self):
        self.x=0.0
        self.y=0.0
    def move_wolf(self, wolf_move_dist, nearest_sheep_index, nearest_sheep_distance, sheep):
        log_info = "move_wolf, position before: " + str(self.x) + ", " + str(self.y)
        logging.info(log_info)
        self.x += wolf_move_dist * ((sheep[nearest_sheep_index].x - self.x) / nearest_sheep_distance)
        self.y += wolf_move_dist * ((sheep[nearest_sheep_index].y - self.y) / nearest_sheep_distance)
        log_info = "move_wolf, position after: " + str(self.x) + ", " + str(self.y)
        logging.info(log_info)
        log = "move_wolf method called"
        logging.debug(log)
    def get_wolf_coordinates(self):
        #"{:.3f}" sluzy do wyswietlenia wspolrzednych wilka z trzema miejscami po przecinku
        print("{:.3f}".format(self.x))
        print("{:.3f}".format(self.y))
        log = "get_wolf_coordinates method called"
        logging.debug(log)


def round(number_rounds, wolf, sheep, wolf_move_dist, j, sheep_move_dist):
    #wszystkie zyjace owce wykonuja ruch
    for single_sheep in sheep:
        if single_sheep.status == "alive":
            single_sheep.move_sheep(sheep_move_dist)

    #liczenie dystansu miedzy wilkiem i owcami
    distances_wolf_sheep = []

    for single_sheep in sheep:
        if single_sheep.status == "alive":
            distances_wolf_sheep.append(math.sqrt(((single_sheep.x - wolf.x) ** 2) + ((single_sheep.y - wolf.y) ** 2)))

    #wybor najblizszej owcy, znalezienie jej indeksu
    nearest_sheep_distance = min(distances_wolf_sheep)
    nearest_sheep_index = distances_wolf_sheep.index(min(distances_wolf_sheep))
    #sprawdzenie czy wilk moze pozreć najblizszą owcę
    if nearest_sheep_distance < wolf_move_dist:
        print("wilk zjada owcę!")
        #  del sheep[nearest_sheep_index]
        sheep[nearest_sheep_index].get_eaten()
        print("byla to owca o indeksie: ")
        print(nearest_sheep_index)
        log_info = "wolf has eaten sheep, sheep number: " + str(nearest_sheep_index)
        logging.info(log_info)
    else:
        wolf.move_wolf(wolf_move_dist, nearest_sheep_index, nearest_sheep_distance, sheep)
    toJSON(j, wolf, sheep)
    log = "round function called"
    logging.debug(log)



def toJSON(j, wolf, sheep):
    data = {"round_no": j, "wolf_pos": str("{:.3f}".format(wolf.x))+", "+str("{:.3f}".format(wolf.y))}
    positions = []
    for s in sheep:
        #if sheep_position != "Null":
        # positions.append(str(s.x)+", "+str(s.y))
        positions.append(s.sheep_info())
    #  if sheep_position == "Null":
    #     positions.append("None/null")
    data['sheep_pos'] = positions
    file = open("pos.json", "a+")
    file.write(json.dumps(data, indent=4))
    file.close()
    log = "round toJSON called"
    logging.debug(log)


def count_alive(sheep):
    count = 0
    for s in sheep:
        if s.status == 'alive':
            count += 1
    log = "round count_alive called, returned: " + str(count)
    logging.debug(log)
    return count


def toCSV(j, sheep):
    with open('alive.csv', 'a+') as csvfile:
        csvwriter = csv.writer(csvfile)
        # csvwriter.writerow([j, len(sheep)])
        csvwriter.writerow([j, count_alive(sheep)])
    log = "toCSV called"
    logging.debug(log)


def parse_args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-c', '--config', metavar='FILE',
                        help='config file')
    parser.add_argument('-d', '--dir', metavar='DIR',
                        help='directory name')
  #  parser.add_argument('-h', '--help')
    parser.add_argument('-l', '--log', metavar='LEVEL',
                        help='save to the journal')
    parser.add_argument('-r', '--rounds', type=int,
                        help='number of rounds to simulate')
    parser.add_argument('-s', '--sheep', type=int,
                        help='number of sheeps')
    parser.add_argument('-w', '--wait', action='store_true', help='Wait for user input')

    args = parser.parse_args()
    return args
    log = "parse_args called"
    logging.debug(log)


def config_parser(file_name):
    config = ConfigParser()
    config.read(file_name)

    init_pos_limit = config['Terrain']['InitPosLimit']
    sheep_move_dist = config['Movement']['SheepMoveDist']
    wolf_move_dist = config['Movement']['WolfMoveDist']

    if float(init_pos_limit) < 0:
        raise ValueError("init_pos_limi is not positive value")
        log_error = "init_pos_limi is not positive value"
        logging.error(log_error)
    if float(sheep_move_dist) < 0:
        raise ValueError("sheep_move_dist is not positive value")
        log_error = "sheep_move_dist is not positive value"
        logging.error(log_error)
    if float(wolf_move_dist) < 0:
        raise ValueError("wolf_move_dist is not positive value")
        log_error = "wolf_move_dist is not positive value"
        logging.error(log_error)

    log = "config_parser called, returned: " + str(init_pos_limit) + ", " + str(sheep_move_dist) + ", " + str(wolf_move_dist)
    logging.debug(log)
    return float(init_pos_limit), float(sheep_move_dist), float(wolf_move_dist)


def main():

    args = parse_args()

    sheep_move_dist = 0.5
    number_sheep = 15
    wolf_move_dist = 1
    number_rounds = 50
    init_pos_limit = 10.0

    wait = False
    if args.rounds:
        number_rounds = args.rounds
    if args.sheep:
        number_sheep = args.sheep
    if args.wait:
       wait = args.wait
    if args.config:
        init_pos_limit, sheep_move_dist, wolf_move_dist = config_parser(args.config)
    if args.log:
        if args.log == "10":
            log_level = logging.DEBUG
        elif args.log == "20":
            log_level = logging.INFO
        elif args.log == "30":
            log_level = logging.WARNING
        elif args.log == "40":
            log_level = logging.ERROR
        elif args.log == "50":
            log_level = logging.CRITICAL
        else:
            raise ValueError("Invalid log level!")
        logging.basicConfig(level=log_level, filename="chase.log", filemode="w")

    wolf = Wolf()
    #dodawanie owiec do tablicy sheep
    sheep = []
    i = 0
    while i < number_sheep:
        sheep.append(Sheep(init_pos_limit))
        i += 1

    #rozgrywka
    print("informacje o rundzie:")
    j = 0

    #zapis nagłówka pliku csv
    with open('alive.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Round_no", "Alive_no"])

    #czyszczenie pliku json przed nowym zapisem
    open("pos.json", "w").close()

    while j < number_rounds:
        round(number_rounds, wolf, sheep, wolf_move_dist, j, sheep_move_dist)
        toCSV(j, sheep)
        print("numer tury: ")
        print(j)
        print("wspolrzedne wilka: ")
        wolf.get_wolf_coordinates()
        print("ilosc owiec, ktore zyja:")
        print(count_alive(sheep))
        if(count_alive(sheep)) == 0:
            break
        if wait:
            input("Press key to continue simulation")
        j += 1


if __name__ == '__main__':
    main()