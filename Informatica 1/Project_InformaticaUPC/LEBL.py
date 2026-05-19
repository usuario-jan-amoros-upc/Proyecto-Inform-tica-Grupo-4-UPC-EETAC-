from Airport import IsSchengenAirport


class Gate:
    def __init__(self, name):
        self.name = name
        self.occupied = False
        self.aircraft_id = ""


class BoardingArea:
    def __init__(self, name, area_type):
        self.name = name
        self.type = area_type
        self.gates = []  # each element is a Gate


class Terminal:
    def __init__(self, name):
        self.name = name
        self.boarding_areas = []  # each element is a BoardingArea
        self.airlines = []  # each element is an airline ICAO code


terminal = Terminal


class BarcelonaAP:
    def __init__(self, code):
        self.code = code
        self.terminals = []  # each element is a Terminal


def SetGates(area, init_gate, end_gate, prefix):
    if end_gate <= init_gate:
        return -1

    area.gates = []
    i = init_gate
    while i <= end_gate:
        area.gates.append(Gate(prefix + str(i)))
        i = i + 1
    return 0


def LoadAirlines(terminal, terminal_name):
    filename = terminal_name + "_Airlines.txt"

    try:
        f = open(filename, "r")
        lines = f.readlines()
        f.close()
    except:
        return -1

    terminal.airlines = []
    i = 0
    while i < len(lines):
        parts = lines[i].strip().split("\t")
        if len(parts) == 2:
            terminal.airlines.append(parts[1])
        i = i + 1
    return 0


def LoadAirportStructure(filename):
    try:
        f = open(filename, "r")
        lines = f.readlines()
        f.close()
    except:
        return -1

    if len(lines) == 0:
        return -1

    first_line = lines[0].split()
    if len(first_line) < 1:
        return -1

    bcn = BarcelonaAP(first_line[0])
    current_terminal = ""
    i = 1

    while i < len(lines):
        parts = lines[i].split()

        if len(parts) > 0 and parts[0] == "Terminal":
            current_terminal = Terminal(parts[1])
            LoadAirlines(current_terminal, parts[1])
            bcn.terminals.append(current_terminal)

        elif len(parts) >= 7 and parts[0] == "Area" and current_terminal != "":
            area = BoardingArea(parts[1], parts[2])
            prefix = current_terminal.name + area.name + "G"
            SetGates(area, int(parts[4]), int(parts[6]), prefix)
            current_terminal.boarding_areas.append(area)

        i = i + 1

    return bcn


LoadAirportsStructure = LoadAirportStructure


def GateOccupancy(bcn):
    occupancy = []
    t = 0

    while t < len(bcn.terminals):
        term = bcn.terminals[t]
        a = 0

        while a < len(term.boarding_areas):
            area = term.boarding_areas[a]
            g = 0

            while g < len(area.gates):
                gate = area.gates[g]
                occupancy.append([term.name, area.name, gate.name, gate.occupied, gate.aircraft_id])
                g = g + 1

            a = a + 1

        t = t + 1

    return occupancy


def IsAirlineInTerminal(terminal, name):
    if name == "" or len(terminal.airlines) == 0:
        return False

    i = 0
    while i < len(terminal.airlines):
        if terminal.airlines[i] == name:
            return True
        i = i + 1

    return False


def SearchTerminal(bcn, name):
    t = 0
    while t < len(bcn.terminals):
        if IsAirlineInTerminal(bcn.terminals[t], name) == True:
            return bcn.terminals[t].name
        t = t + 1

    return ""


def AssignGate(bcn, aircraft):
    terminal_name = SearchTerminal(bcn, aircraft.airline)
    if terminal_name == "":
        return -1

    is_schengen = IsSchengenAirport(aircraft.origin)
    t = 0

    while t < len(bcn.terminals):
        term = bcn.terminals[t]

        if term.name == terminal_name:
            a = 0
            while a < len(term.boarding_areas):
                area = term.boarding_areas[a]

                if (is_schengen == True and area.type == "Schengen") or (is_schengen == False and area.type == "non-Schengen"):
                    g = 0
                    while g < len(area.gates):
                        gate = area.gates[g]
                        if gate.occupied == False:
                            gate.occupied = True
                            gate.aircraft_id = aircraft.aircraft_id
                            return 0
                        g = g + 1

                a = a + 1

        t = t + 1

    return -2


def ResetGates(bcn):
    t = 0
    while t < len(bcn.terminals):
        a = 0
        while a < len(bcn.terminals[t].boarding_areas):
            g = 0
            while g < len(bcn.terminals[t].boarding_areas[a].gates):
                gate = bcn.terminals[t].boarding_areas[a].gates[g]
                gate.occupied = False
                gate.aircraft_id = ""
                g = g + 1
            a = a + 1
        t = t + 1
    return 0


if __name__ == "__main__":
    from Aircraft import LoadArrivals

    bcn = LoadAirportStructure("LEBL.txt")
    aircrafts = LoadArrivals("Arrivals.txt")

    if bcn != -1:
        i = 0
        assigned = 0
        while i < len(aircrafts):
            if AssignGate(bcn, aircrafts[i]) == 0:
                assigned = assigned + 1
            i = i + 1
        print("Puertas asignadas:", assigned)
        print("Total puertas:", len(GateOccupancy(bcn)))
