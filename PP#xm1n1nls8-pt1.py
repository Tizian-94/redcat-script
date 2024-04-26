import csv
import math


#unjeti koordinate u A i B redove coordinates.csv datoteke (prva 4 reda)
#primjer koordinata za testiranje:

#koordinate NE prave pravokutni trokut:
# (1.0,1.0)
# (2.0,2.0)
# (3.0,3.0)
# (0.0,0.0)

#koordinate prave pravokutni trokut ali X je izvan nacrtanog oblika:
# (0.0,0.0)
# (2.0,0.0)
# (0.0,3.0)
# (1.0,2.0)

#koordinate prave pravokutni trokut i X je unutar nacrtanog oblika:
# (0.0,0.0)
# (3.0,0.0)
# (1.0,2.0)
# (1.0,1.5)

def read_coordinates(file_path):

    #ucitavanje csv datoteke, dodjeljivanje konvencijonalnih imena i svrstavanje u dict

    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            coordinates = []
            for row_number, row in enumerate(reader, start=1):
                if len(row) != 2:
                    raise ValueError(f"Red {row_number} mora sadrzavati izricito dvije kordinate (x, y).")
                try:
                    x, y = map(float, row)
                    coordinates.append((x, y))
                except ValueError:
                    raise ValueError(f"nevazeci format kordinata u redu: {row_number} u .csv dokumentu")

            #stavljeno kao primjer limit na 4 reda, na bazi prilozenog u zadatku

            if len(coordinates) != 4:
                raise ValueError("Csv dokument morrra imati tocno 4 reda kordinata")

            # dodjeljivanje slova kordinatama
            designations = ['A', 'B', 'C', 'X']
            assigned_coordinates = {designation: coordinate for designation, coordinate in zip(designations, coordinates)}

            # sortiranje na bazi slova u abecednom redosljedu ako vec nisu
            assigned_coordinates = {k: assigned_coordinates[k] for k in sorted(assigned_coordinates)}

            # iteracija kroz listu kordinata, razdjela na x1 i y1 za svaku kordinatu, zaokruzuje "visak" u proracunu distance i svrstava u listu
            distances = []
            for i in range(len(coordinates)):
                x1, y1 = coordinates[i]
                x2, y2 = coordinates[(i + 1) % len(coordinates)]
                distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                distances.append(distance)

            return assigned_coordinates, distances  # vraca dictionary i izracunate distance
    except FileNotFoundError:
        raise FileNotFoundError("Datoteka nije pronadena.")


def distance(point1, point2):
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2) #euklidarna formula

def form_shape(coordinates):
    # racunanje duzine spojenih tocaka
    AB_length = distance(coordinates['A'], coordinates['B'])
    BC_length = distance(coordinates['B'], coordinates['C'])
    CA_length = distance(coordinates['C'], coordinates['A'])

    # gleda ako bilo koje 2 duzine imaju otprilike istu duzinu, ili su 2 tocke bilzu sebi dovoljno da bi se moglo kasificirat kao jednakokracan trokut
    # nb: probao sam ne koristit math.isclose radi preciznosti ali je bilo pre ubagirano, pogotovo kod cudnih input kordinata
    if math.isclose(AB_length, BC_length) or math.isclose(BC_length, CA_length) or math.isclose(CA_length, AB_length):
        return "jednakokracan trokut"
    else:
        return "razmjerni trokut"


def is_inside_triangle(A, B, C, X):
    
    #Necu se ni pravit da znam ovo, skinuto sa stacka nakon 3 sata kopanja: https://gamedev.stackexchange.com/questions/23743/whats-the-most-efficient-way-to-find-barycentric-coordinates
    denominator = ((B[1] - C[1]) * (A[0] - C[0]) + (C[0] - B[0]) * (A[1] - C[1]))
    alpha = ((B[1] - C[1]) * (X[0] - C[0]) + (C[0] - B[0]) * (X[1] - C[1])) / denominator
    beta = ((C[1] - A[1]) * (X[0] - C[0]) + (A[0] - C[0]) * (X[1] - C[1])) / denominator
    gamma = 1 - alpha - beta

    return 0 <= alpha <= 1 and 0 <= beta <= 1 and 0 <= gamma <= 1


# _main_
file_path = "coordinates.csv" #promjenit ako treba
assigned_coordinates, distances = read_coordinates(file_path)
shape = form_shape(assigned_coordinates)
print("Kordinate:", assigned_coordinates)

if shape == "razmjerni trokut":
    print(f"Kordinate stvaraju oblik: {shape}.")

    A = assigned_coordinates['A']
    B = assigned_coordinates['B']
    C = assigned_coordinates['C']
    X = assigned_coordinates['X']

    if is_inside_triangle(A, B, C, X):
        print("tocka 'X' se nalazi unutar oblika nacrtanog s kordinatama")
    else:
        print("tocka 'X' se NE nalazi unutar oblika nacrtanog s kordinatama")
else:
    print("Kordinate ne cine pravilan razmjerni trokut.")
