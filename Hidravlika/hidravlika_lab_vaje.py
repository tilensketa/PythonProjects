from math import pi, pow

# 1. Laboratorijska vaja : Zgradba, delovanje in meritve preprostega hidravličnega sistema

# Parametri bata
D = 40 # mm
d = 28 # mm
L = 525 # mm

def povrsina_kroga(d: float):
    """
    Input: \n
    d ... premer kroga [mm] \n
    Output: \n
    A ... povrsina kroga [mm2]
    """
    A = (pi * pow(d, 2))/4
    return A

def volumen_valja(A: float, L: float):
    """
    Input: \n
    A ... povrsina kroga [mm2] \n
    L ... dolzina valja [mm] \n
    Output: \n
    V ... volumen valja [mm3]
    """
    V = A * L
    return V

# 1.1

class MeritevPrimer1():
    def __init__(self, tlak: float, volumen: float, cas: float):
        """
        tlak [bar] \n
        volumen [ml] \n
        cas [s]
        """
        self.tlak = tlak
        self.volumen = volumen
        self.cas = cas
    
    def pretok(self):
        """
        Q ... pretok [l/min]
        """
        Q = (self.volumen / 1000)/(self.cas / 60)
        return Q

# Meritve
meritev0 = MeritevPrimer1(0, 2000, 40)
meritev100 = MeritevPrimer1(100, 2000, 41)

izkoristek_crpalke = (meritev100.pretok() / meritev0.pretok()) * 100

print("1.1")
print(f"Pretok pri 0 bar: {meritev0.pretok()} l/min")
print(f"Pretok pri 100 bar: {meritev100.pretok()} l/min")
print(f"Izkoristek črpalke: {izkoristek_crpalke} %")

# 1.2

class MeritevPrimer2():
    def __init__(self, pot: float, volumen: float, cas: float):
        """
        pot [mm] \n
        volumen [ml] \n
        cas [s]
        """
        self.pot = pot
        self.volumen = volumen
        self.cas = cas
    
    def pretok(self):
        """
        Q ... pretok [l/min]
        """
        Q = (2 * self.volumen / 1000) / (self.cas / 60)
        return Q

povrsina_bata = povrsina_kroga(D)
povrsina_batnice = povrsina_kroga(d)
volumen_naprej = volumen_valja(povrsina_bata, L)
volumen_nazaj = volumen_valja(povrsina_bata-povrsina_batnice, L)

# Meritve
meritev_naprej = MeritevPrimer2(L, volumen_naprej / 1000, 26)
meritev_nazaj = MeritevPrimer2(L, volumen_nazaj / 1000, 30)

print("1.2")
print(f"Volumen naprej : {volumen_naprej} ml")
print(f"Volumen nazaj : {volumen_nazaj} ml")
print(f"Pretok naprej: {meritev_naprej.pretok()} l/min")
print(f"Pretok nazaj: {meritev_nazaj.pretok()} l/min")

# 4.

def izracun_iztisnine_hidravlicnega_motorja(Q_HM: float, ni_VHM: float, n_HM: float):
    """
    Input: \n
    Q_HM ... pretok cez hidravlicni motor [l/min] \n
    n_HM ... obrati hidravlicnega motorja [min-1] \n
    ni_VHM ... volumetricni izkoristek [%] \n
    Output: \n
    q_HM ... iztisnina hidravlicnega motorja [cm3/vrt]
    """
    q_HM = (Q_HM * 1000 * ni_VHM) / n_HM
    return q_HM

iztisnina_hidravlicnega_motorja = izracun_iztisnine_hidravlicnega_motorja(meritev0.pretok(), 0.85, 60)

print("4.")
print(f"Iztisnina hidravlicnega motorja : {iztisnina_hidravlicnega_motorja} cm3/vrt")