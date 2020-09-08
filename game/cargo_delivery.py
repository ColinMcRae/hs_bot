from game.config import WARP_PLANETS, HUBS, ARTIFACT_STORAGE
import libs.utils as utils
import time

class CargoDelivery:
    def __init__(self, solarsystem):
        self.sol = solarsystem
        self.transports = solarsystem.transports[:2]
        self.planets = solarsystem.planets
        self.tradestations = solarsystem.tradestations

    def move_cargo_to_warp(self):
        exit_condition = True
        it = 300

        while exit_condition:
            it -= 1
            if it < 0:
                break

            for transport in self.transports:
                if transport.status == 0:
                    station = self.__find_full_tradestation()
                    if station:
                        transport.send_to_dest(station)
                        station.status = 2
                        print(station.__hash__(), 'set as busy')
                        continue

                    planet = self.__find_full_external_planet()
                    if planet:
                        transport.send_to_dest(planet)
                        planet.status = 2
                        continue

                    transport.status = 4

                if transport.status == 1:
                    if transport.is_docked():
                        transport.status = 2

                if transport.status == 2:
                    if transport.is_empty():
                        transport.load_all()
                        transport.destination.status = 2
                    else:
                        transport.unload()
                        # transport.destination.status = 3 #TODO remove
                        self.__transport_redirect(transport)

                if transport.status == 3:
                    self.__transport_redirect(transport)

                if transport.status == 8:
                    # try to unload to hub
                    pass

                if transport.status == 9:
                    #find another planet to unload
                    pass

            exit_condition = False
            for transport in self.transports:
                if transport.status != 4:
                    exit_condition = True

    def sort_cargo(self):
        exit_condition = True
        it = 300

        while exit_condition:
            it -= 1
            if it < 0:
                break

            for transport in self.transports:
                transport.select()
                time.sleep(0.3)

                if transport.status == 0:
                    hub = self.__find_hub()

                    if not hub:
                        continue

                    transport.hub = hub
                    print('transport', transport.__hash__(), 'has hub', hub.name)

                    dest = self.__find_unvisited_planet(transport)
                    if not dest:
                        transport.finish()
                        continue

                    transport.send_to_dest(dest)

                if transport.status in [1, 2]:
                    if not transport.is_docked():
                        continue

                    transport.status = 3
                    transport.load_for_hub()

                    print('checking transport')
                    if transport.is_full():
                        print('full - sending to hub')
                        transport.send_to_hub()

                    else:
                        print('not full - find next planet')
                        transport.visited.append(transport.destination.name)
                        dest = self.__find_unvisited_planet(transport)
                        if not dest:
                            transport.send_to_hub()
                        else:
                            transport.send_to_dest(dest)

                if transport.status == 3:
                    print('status 3. We should not be here')
                    dest = self.__find_unvisited_planet(transport)
                    if not dest:
                        transport.send_to_hub()
                    else:
                        transport.send_to_dest(dest)

                if transport.status == 8:
                    if not transport.is_docked():
                        continue

                    transport.unload()
                    if transport.is_empty:
                        transport.finish()

            exit_condition = False
            for transport in self.transports:
                if transport.status not in [0, 4]:
                    exit_condition = True

    def __find_free_transport(self):
        for tr in self.transports:
            if tr.status == 0:
                return tr
        return None

    def __find_full_tradestation(self):
        for station in self.tradestations:
            if station.status == 0:
                return station

    def __find_full_external_planet(self):
        for planet in self.planets:
            if planet.name in ARTIFACT_STORAGE:
                continue
            if planet.name not in WARP_PLANETS and planet.status == 0:
                return planet

    def __find_hub(self):
        hubs = HUBS.keys()
        hub = None
        for planet in self.planets:
            if planet.name in hubs and planet.status == 0:
                hub = planet
                planet.status = 3
                break

        return hub

    def __find_planet_for_unload(self, transport):
        min_dist = 2000
        pl = None
        for planet in self.planets:
            if planet.name in ARTIFACT_STORAGE:
                continue
            #TODO - find transport current position
            distance_to_planet = utils.distance(transport.destination.coords, planet.coords)
            if planet.name in WARP_PLANETS and planet.status != 3 and distance_to_planet < min_dist:
                pl = planet
                min_dist = distance_to_planet
        return pl

    def __find_unvisited_planet(self, transport):
        min_dist = 2000
        pl = None
        for planet in self.planets:
            if planet.name in transport.visited or planet.status in [1, 2]:
                continue

            if transport.destination:
                distance_to_planet = utils.distance(transport.destination.coords, planet.coords)
                if distance_to_planet > min_dist:
                    continue
                min_dist = distance_to_planet
                pl = planet
            else:
                return planet
        if planet:
            print('planet found', pl.name)
        else:
            print('no planets left')
        return pl

    def __find_planet_by_name(self, name):
        for planet in self.planets:
            if planet.name == name:
                return planet

    #TODO - think about name
    def __transport_redirect(self, transport):
        if transport.is_empty():
            transport.reset_task()
        else:
            planet = self.__find_planet_for_unload(transport)
            if planet:
                transport.send_to_dest(planet)
