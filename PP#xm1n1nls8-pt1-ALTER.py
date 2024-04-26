import csv
import math

#alternativna verzija programa iz prvog zadatka koji na bazi tocke A i C izracuna potencijalnu tocku "D", 
#ako je u mogucnosti napravi pravokutni oblik izracuna diagonalu oblika i pokusa izracunat ako se tocka X nalazi unutar oblika

#unjeti koordinate u A i B redove coordinates.csv datoteke (prva 4 reda)
#primjer koordinata za testiranje:

#koordinate NE prave pravokutnik
# (2.0,2.0)
# (3.0,3.0)
# (0.0,0.0)

#koordinate prave pravokutnik ali X je izvan nacrtanog oblika
# (0.0,0.0)
# (3.0,0.0)
# (0.0,3.0)
# (3.0,4.0)

#koordinate prave pravokutnik kvadrat te je X unutar nacrtanog oblika
# (0.0,0.0)
# (3.0,0.0)
# (0.0,3.0)
# (1.5,1.5)

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
                raise ValueError("Csv dokument mora imati tocno 4 reda kordinata")

            # dodjeljivanje slova kordinatama
            designations = ['A', 'B', 'C', 'X']
            assigned_coordinates = {designation: coordinate for designation, coordinate in zip(designations, coordinates)}

            # racunanje potencijalne kordinate "D"
            missing_coordinate = calculate_missing_coordinate(assigned_coordinates)
            assigned_coordinates['D'] = missing_coordinate

            # sortiranje na bazi slova u abecednom redosljedu ako vec nisu
            assigned_coordinates = {k: assigned_coordinates[k] for k in sorted(assigned_coordinates)}

            # iteracija kroz listu kordinata, razdjela na x1 i y1 za svaku kordinatu, zaokruzuje "visak" u proracunu distance i svrstava u listu
            distances = []
            for i in range(len(coordinates)):
                x1, y1 = coordinates[i]
                x2, y2 = coordinates[(i + 1) % len(coordinates)]  # zaokruzivanje na zadnjoj kordinati
                distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                distances.append(distance)

            # printa tocku "D"
            print("nepoznata kordinata 'D' je:", missing_coordinate)

            return assigned_coordinates, distances  # vraca dictionary i izracunate distance
    except FileNotFoundError:
        raise FileNotFoundError("Datoteka nije pronadena.")


def distance(point1, point2):
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2) #euklidarna formula


def calculate_diagonal_length(coordinates):
    # racunanje diagonale izmedu AC i BD
    AC_length = distance(coordinates['A'], coordinates['C'])
    BD_length = distance(coordinates['B'], coordinates['D'])
    return AC_length, BD_length


def form_shape(coordinates):
    # racunanje duzine svih 4 strana
    AB_length = distance(coordinates['A'], coordinates['B'])
    BC_length = distance(coordinates['B'], coordinates['C'])
    CD_length = distance(coordinates['C'], coordinates['D'])
    DA_length = distance(coordinates['D'], coordinates['A'])

    # racuna duzinu obije diagonale
    AC_length = distance(coordinates['A'], coordinates['C'])
    BD_length = distance(coordinates['B'], coordinates['D'])

    # provjerava ako suprotne strane imaju "jednake" duzine, ponovno math.isclose radi lakse aproksimacije
    #ako obije diagonale imaju "jednake" duzine, vraca kvadrat
    if math.isclose(AB_length, CD_length) and math.isclose(BC_length, DA_length):
        if math.isclose(AC_length, BD_length):
            return "kvadrat"
    return False




def calculate_missing_coordinate(coordinates):

    #uzima kordinate A, B i C i ako imaju prave kuteve, D = B+C-A
    A = coordinates['A']
    B = coordinates['B']
    C = coordinates['C']

    D = (B[0] + C[0] - A[0], B[1] + C[1] - A[1])

    return D


def is_inside_rectangle(A, B, C, D, X):

    #opet stack overflow spasava dan, ovaj put znatno manje sati: https://stackoverflow.com/questions/5919530/what-is-the-pythonic-way-to-calculate-dot-product
    #

    # stvara vektore koji sluze kao strane pravokuta
    AB = (B[0] - A[0], B[1] - A[1])
    BC = (C[0] - B[0], C[1] - B[1])
    CD = (D[0] - C[0], D[1] - C[1])
    DA = (A[0] - D[0], A[1] - D[1])

    # stvara vektore OD svakog kuta sve DO tocke X
    AX = (X[0] - A[0], X[1] - A[1])
    BX = (X[0] - B[0], X[1] - B[1])
    CX = (X[0] - C[0], X[1] - C[1])
    DX = (X[0] - D[0], X[1] - D[1])

    # skalarna projekcija od svih vanjskih vektora do potencijalno unutrasnjeg X vektora
    dot_product_AB_AX = AB[0] * AX[0] + AB[1] * AX[1]
    dot_product_BC_BX = BC[0] * BX[0] + BC[1] * BX[1]
    dot_product_CD_CX = CD[0] * CX[0] + CD[1] * CX[1]
    dot_product_DA_DX = DA[0] * DX[0] + DA[1] * DX[1]

    # ako su svi dot_product u + znaci da x mora biti unutar oblika, ako samo jedan nije znaci da je X van oblika
    return dot_product_AB_AX > 0 and dot_product_BC_BX > 0 and dot_product_CD_CX > 0 and dot_product_DA_DX > 0

# _main_
file_path = "coordinates.csv" #promjenit ako treba
assigned_coordinates, distances = read_coordinates(file_path)
shape = form_shape(assigned_coordinates)
print("Kordinate:", assigned_coordinates)

if form_shape(assigned_coordinates):
    print(f"kordinate stvaraju oblik: {shape}.")
    missing_coordinate = calculate_missing_coordinate(assigned_coordinates)
    print("nepoznata kordinata (D):", missing_coordinate)

    # print diagonale AC & BD
    # nb: obije su tu jer sam u jednom trenutku htio da kod prepozna ako je oblik npr. romb
    diagonal_AC_length, diagonal_BD_length = calculate_diagonal_length(assigned_coordinates)
    print("Duzina diagonale: AC:", diagonal_AC_length)
    print("Duzina diagonale: BD:", diagonal_BD_length)

    A = assigned_coordinates['A']
    B = assigned_coordinates['B']
    C = assigned_coordinates['C']
    D = assigned_coordinates['D']
    X = assigned_coordinates['X']

    if is_inside_rectangle(A, B, C, D, X):
        print("tocka 'X' se nalazi unutar oblika nacrtanog s kordinatama")
    else:
        print("tocka 'X' se NE nalazi unutar oblika nacrtanog s kordinatama")
else:
    print("Kvadrat nije moguce stvoriti sa zadanim kordinatama.")
