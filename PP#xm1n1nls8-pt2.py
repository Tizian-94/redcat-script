import csv
import math

#unjeti Koordinate u A i B ili A, B i C redove coordinates.csv datoteke (prvih 5 redaka)
#primjer koordinata za testiranje:

#2D Koordinate - trokut, X je unutar oblika
# (0.0,0.0)
# (5.0,0.0)
# (0.0,5.0)
# (2.0,2.0)

#2D Koordinate - trokut, X je izvan oblika
# (0.0,0.0)
# (5.0,0.0)
# (0.0,5.0)
# (2.0,6.0)

###################################################

#2D Koordinate, X je unutar oblika, kvadrad
# (0.0,0.0)
# (2.0,0.0)
# (0.0,2.0)
# (2.0,2.0)
# (1.0,1.0)

#2D Koordinate, X je izvan oblika, kvadrad
# (0.0,0.0)
# (2.0,0.0)
# (0.0,2.0)
# (2.0,2.0)
# (4.0,1.0)

#2D Koordinate, X je izvnan oblika, nije kvadrad
# (5.0,1.0)
# (2.0,0.0)
# (1.0,2.0)
# (2.0,3.0)
# (1.0,1.0)

###################################################

#3D Koordinate, X je unutar oblika, kutevi potencijalno stvaraju kvadratni 3d objekt <- radi ali nije dobro, preciznost je losa, trebao bih se pozabavit s time
# (0.0,0.0,0.0)
# (3.0,0.0,0.0)
# (3.0,3.0,0.0)
# (0.0,3.0,0.0)
# (2.0,0.0,0.0)

#3D Koordinate, X je izvan oblika, kutevi potencijalno stvaraju kvadratni 3d objekt
# (0.0,0.0,0.0)
# (3.0,0.0,0.0)
# (3.0,3.0,0.0)
# (0.0,3.0,0.0)
# (0.0,2.9,0.0)

#3D Koordinate, X je izvan oblika, kutevi ne stvaraju kvadratni 3d objekt
# (0.0,2.0,0.0)
# (1.0,0.0,2.0)
# (4.0,4.0,0.0)
# (0.0,2.0,1.0)
# (5.0,6.0,2.0)

def read_coordinates(file_path):

    #ucitavanje csv datoteke, dodjeljivanje konvencijonalnih imena i svrstavanje u dict

    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            coordinates = []
            for row_number, row in enumerate(reader, start=1):
                #dopusta 2 ili 3, reda u csv, ovisno ako se zeli unjet xy ili xyz
                if len(row) != 2 and len(row) != 3:
                    raise ValueError(f"Red {row_number} mora sadrzavati izricito dvije (x, y) ili tri (x, y, z) Koordinate.")
                try:
                    coordinates.append(tuple(map(float, row)))
                except ValueError:
                    raise ValueError(f"nevazeci format kordinata u redu: {row_number} u .csv dokumentu")

            #stavljeno kao primjer limit na 5 reda, na bazi prilozenog u zadatku

            if len(coordinates) == 4:
                # ako su samo 4 Koordinate tretira se kao trokut A, B, C i X
                coordinates.append(coordinates[3])  #dodaje zadnju stavku kao X

                # dodjeljivanje slova kordinatama abcx
                designations = ['A', 'B', 'C', 'X']
                assigned_coordinates = {designation: coordinate for designation, coordinate in zip(designations, coordinates)}
            elif len(coordinates) == 5:
                # ako csv ako ima tocno 5 redova kordinata, dodaje se i A,B,C,D i X, tretira se ili kao 2d ili 3d cetverokutni
                # dodjeljivanje slova kordinatama abcdx
                designations = ['A', 'B', 'C', 'D', 'X']
                assigned_coordinates = {designation: coordinate for designation, coordinate in zip(designations, coordinates)}
            else:
                raise ValueError("Csv dokument mora imati tocno 4 ili 5 redaka kordinata")

            # sortiranje na bazi slova u abecednom redosljedu ako vec nisu
            assigned_coordinates = {k: assigned_coordinates[k] for k in sorted(assigned_coordinates)}

            # pregled ako su 3d Koordinate (xyz)
            is_3d = len(coordinates[0]) == 3

            return assigned_coordinates, is_3d
    except FileNotFoundError:
        raise FileNotFoundError("Datoteka nije pronadena.")
    

def check_unique_coordinates(coordinates):
    unique_coordinates = set(coordinates.values())
    if len(unique_coordinates) != len(coordinates):
        raise ValueError("Koordinate MORAJU BITI UNIKATNE!")


def distance(point1, point2):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(point1, point2))) #euklidarna formula

def calculate_diagonal_distance(coordinates):
    # Diagonalna distanca oblika projektiranog sa ABC i D
    max_distance = 0
    keys = list(coordinates.keys())[:-1]  # Iskljucivanje "X" iz racunice
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            distance_ij = distance(coordinates[keys[i]], coordinates[keys[j]])
            max_distance = max(max_distance, distance_ij)
    return max_distance


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
    

def is_inside_3d_object(A, B, C, D, X):

    if 'D' not in (A, B, C, X):
        return is_inside_triangle(A, B, C, X)  #ako nema D, tocke projektiraju trokut
    else:
            # racunaj sve vektore od A-X, B-X,C-X, D-X, ako se x nalazi unutar projektiranog oblika koristeci se metodom tetraedarskih volumena <- sve chatgpt
        # prvi izbor mi je bio koristiti plotly, al kad sam vec cijeli kod napisao bez koristenja librarya osim math i csv htio sam i da ovo bude inline

        # Calculate vectors from A to X, B to X, C to X, and D to X
        AX = (X[0] - A[0], X[1] - A[1], X[2] - A[2])
        BX = (X[0] - B[0], X[1] - B[1], X[2] - B[2])
        CX = (X[0] - C[0], X[1] - C[1], X[2] - C[2])
        DX = (X[0] - D[0], X[1] - D[1], X[2] - D[2])

        # Calculate the vectors AB, AC, AD, BC, BD, CD, CA, DA, and DB
        AB = (B[0] - A[0], B[1] - A[1], B[2] - A[2])
        AC = (C[0] - A[0], C[1] - A[1], C[2] - A[2])
        AD = (D[0] - A[0], D[1] - A[1], D[2] - A[2])
        BC = (C[0] - B[0], C[1] - B[1], C[2] - B[2])
        BD = (D[0] - B[0], D[1] - B[1], D[2] - B[2])
        CD = (D[0] - C[0], D[1] - C[1], D[2] - C[2])
        CA = (A[0] - C[0], A[1] - C[1], A[2] - C[2])
        DA = (A[0] - D[0], A[1] - D[1], A[2] - D[2])
        DB = (B[0] - D[0], B[1] - D[1], B[2] - D[2])

        # Calculate the tetrahedral volumes formed by each combination of A, B, C, D, and X
        volume_ABCX = abs(dot_product(cross_product(AB, AC), AX)) / 6
        volume_BCDX = abs(dot_product(cross_product(BC, BD), BX)) / 6
        volume_CDAX = abs(dot_product(cross_product(CD, CA), CX)) / 6
        volume_DABX = abs(dot_product(cross_product(DA, DB), DX)) / 6

        # Calculate the total volume of the tetrahedron ABCD
        volume_ABCD = abs(dot_product(cross_product(AB, AC), AD)) / 6

        # Check if the sum of volumes formed by X and each face is approximately equal to the volume of the tetrahedron
        return math.isclose(volume_ABCX + volume_BCDX + volume_CDAX + volume_DABX, volume_ABCD)

# skalarna projekcija iz prijasnje verzije, samo prilagodena za 3d objekt
#prvo tockasto oznacavanje = da se jedan vektor projektira na drugi 
def dot_product(vector1, vector2):
    return sum(i * j for i, j in zip(vector1, vector2))

#zatim krizno (xyz) = da se kroz jedan vektor projektiraju 2 okomita "input" vektora
def cross_product(vector1, vector2):
    x = vector1[1] * vector2[2] - vector1[2] * vector2[1]
    y = vector1[2] * vector2[0] - vector1[0] * vector2[2]
    z = vector1[0] * vector2[1] - vector1[1] * vector2[0]
    return x, y, z

def is_inside_triangle(A, B, C, X):
    #Necu se ni pravit da znam ovo, skinuto sa stacka nakon 3 sata kopanja: https://gamedev.stackexchange.com/questions/23743/whats-the-most-efficient-way-to-find-barycentric-coordinates
    denominator = ((B[1] - C[1]) * (A[0] - C[0]) + (C[0] - B[0]) * (A[1] - C[1]))
    alpha = ((B[1] - C[1]) * (X[0] - C[0]) + (C[0] - B[0]) * (X[1] - C[1])) / denominator
    beta = ((C[1] - A[1]) * (X[0] - C[0]) + (A[0] - C[0]) * (X[1] - C[1])) / denominator
    gamma = 1 - alpha - beta

    return 0 <= alpha <= 1 and 0 <= beta <= 1 and 0 <= gamma <= 1

def calculate_diagonal_distance_3d(coordinates):
    # racuna diagonalnu distancu 3d objekta
    max_distance = 0
    keys = list(coordinates.keys())[:-1]  # Iskljucivanje "X" iz racunice
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            distance_ij = distance(coordinates[keys[i]], coordinates[keys[j]])
            max_distance = max(max_distance, distance_ij)
    return max_distance


def is_rectangle(coordinates, is_3d):
    if 'D' not in coordinates:
        return False  # ako nema D je trokut
    
    elif is_3d:
        # distanca suprotnih rubova u 3d prostoru
        AB_length = distance(coordinates['A'], coordinates['B'])
        CD_length = distance(coordinates['C'], coordinates['D'])
        BC_length = distance(coordinates['B'], coordinates['C'])
        DA_length = distance(coordinates['D'], coordinates['A'])
        AC_length = distance(coordinates['A'], coordinates['C'])
        BD_length = distance(coordinates['B'], coordinates['D'])

        # provjera ako ikoji imaju jednake duzine
        return math.isclose(AB_length, CD_length) and \
               math.isclose(BC_length, DA_length) and \
               math.isclose(AC_length, BD_length)
    else:
        # distanca suprrotnih rubova u 2d prostorru
        AB_length = distance(coordinates['A'], coordinates['B'])
        CD_length = distance(coordinates['C'], coordinates['D'])
        BC_length = distance(coordinates['B'], coordinates['C'])
        DA_length = distance(coordinates['D'], coordinates['A'])

        # provjera ako ikoji imaju jednake duzine
        return math.isclose(AB_length, CD_length) and \
               math.isclose(BC_length, DA_length)


# _main_
file_path = "coordinates.csv"  #promjenit ako treba
assigned_coordinates, is_3d = read_coordinates(file_path)
check_unique_coordinates(assigned_coordinates)
print("Koordinate:", assigned_coordinates)

if is_3d:
    print("Prepoznane su 3D Koordinate.")

    diagonal_distance = calculate_diagonal_distance_3d(assigned_coordinates)
    print("Dijagonalna duzina 3D oblika:", diagonal_distance)

    A = assigned_coordinates['A']
    B = assigned_coordinates['B']
    C = assigned_coordinates['C']
    D = assigned_coordinates.get('D', None)  # Ako 'D' ne postoji, uzvraca None
    X = assigned_coordinates['X']

    if is_inside_3d_object(A, B, C, D, X):
        print("Koordinata 'X' se nalazi unutar 3D objekta kojeg cine A, B, C i D.")
    else:
        print("Koordinata 'X' se ne nalazi unutar 3D objekta koji cine A, B, C i D.")

    if is_rectangle(assigned_coordinates, is_3d):
        print("Tocke A, B, C i D su vrlo vjerojatno cine pravokut")
    else:
        print("Tocke A, B, C i D ne cine pravokut")

else:
    print("Prepoznane su 2D Koordinate.")

    diagonal_distance_2d = calculate_diagonal_distance(assigned_coordinates)
    print("Dijagonalna duzina 2D oblika:", diagonal_distance_2d)

    A = assigned_coordinates['A']
    B = assigned_coordinates['B']
    C = assigned_coordinates['C']
    D = assigned_coordinates.get('D', None)  # Ako 'D' ne postoji, uzvraca None
    X = assigned_coordinates['X']

    if is_inside_triangle(A, B, C, X):
        print("Koordinata 'X' se nalazi unutar 2D objekta kojeg cine A, B, C i D.")
    else:
        print("Koordinata 'X' se ne nalazi unutar 2D objekta kojeg cine A, B, C i D.")

    if is_rectangle(assigned_coordinates, is_3d):
        print("Tocke A, B, C i D su vrlo vjerojatno cine pravokut")
    else:
        print("Tocke A, B, C i D ne cine pravokut")
