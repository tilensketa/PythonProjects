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
volumen_nazaj = volumen_valja(povrsina_bata - povrsina_batnice, L)

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

# Parametri in meritve
volumetricni_izkoristek = 85 # %
obrati = 60 # min-1

iztisnina_hidravlicnega_motorja = izracun_iztisnine_hidravlicnega_motorja(meritev0.pretok(), volumetricni_izkoristek / 100, obrati)

print("4.")
print(f"Iztisnina hidravlicnega motorja : {iztisnina_hidravlicnega_motorja} cm3/vrt")

# 2. Laboratorijska vaja : Meritve čistoče in termografija

# 1.1

class ISO4406():
    def __init__(self, x1: float, x2: float, x3: float):
        self.x1 = x1
        self.x2 = x2
        self.x3 = x3

class SAEAS4059():
    def __init__(self, A: int, B: int, C: int, D: int):
        self.A = A
        self.B = B
        self.C = C
        self.D = D

class MeritevCistoce():
    def __init__(self, cas: int, iso: ISO4406, sae: SAEAS4059, temp: float, voda: float):
        """
        cas [s] \n
        iso [x1,x2,x3] \n
        sae [A,B,C,D] \n
        temp [°C] \n
        voda [%]
        """
        self.cas = cas
        self.iso = iso
        self.sae = sae
        self.temp = temp
        self.voda = voda

meritev5_iso = ISO4406(0,0,0)
meritev10_iso = ISO4406(0,0,0)
meritev15_iso = ISO4406(0,0,0)

meritev5_sae = SAEAS4059(0,0,0,0)
meritev10_sae = SAEAS4059(0,0,0,0)
meritev15_sae = SAEAS4059(0,0,0,0)

meritev5 = MeritevCistoce(5, meritev5_iso, meritev5_sae, 5, 5)
meritev10 = MeritevCistoce(10, meritev10_iso, meritev10_sae, 5, 5)
meritev15 = MeritevCistoce(15, meritev15_iso, meritev15_sae, 5, 5)

# 1.2

def izracun_povrsine_filtra(r: float, h: float):
    """
    Input: \n
    r ... polmer filtra [m] \n
    h ... visina filtra [m] \n
    Output: \n
    A ... povrsina filtra [m2]
    """
    A = 2 * pi * r * h + 2 * pi * pow(r, 2)
    return A

# Parametri
specificna_prevzemnost_filtra = 90.83 # [g/m2]
stevilo_prepogibov_filtra = 93
r = 0.1 # polmer filtra [m]
h = 0.1 # visina filtra [m]

povrsina_filtra = izracun_povrsine_filtra(r, h)
prevzemnost_filtra = specificna_prevzemnost_filtra * povrsina_filtra

# ISO 16 14 10
# Povprečna teža delcev od 4µm do 6 µm = 1 × 10−9g
# Povprečna teža delcev od 6µm do 14 µm = 5 × 10−9g
# Povprečna teža delcev 𝑛𝑎𝑑 14 µm = 69 × 10−9g

masa_4 = 1 * pow(10, -9)
masa_6 = 5 * pow(10, -9)
masa_14 = 69 * pow(10, -9)
st_delcev_4 = (320 + 640) / 2
st_delcev_6 = (80 + 160) / 2
st_delcev_14 = (5 + 10) / 2

masa = masa_4 * st_delcev_4 + masa_6 * st_delcev_6 + masa_14 * st_delcev_14

preciscenih_litrov = prevzemnost_filtra / masa

print("1.2")
print(f"Povrsina filtra : {povrsina_filtra} m2")
print(f"Prevzemnost filtra : {prevzemnost_filtra} g")
print(f"Stevilo delcev > 4 : {st_delcev_4}")
print(f"Stevilo delcev > 6 : {st_delcev_6}")
print(f"Stevilo delcev > 14 : {st_delcev_14}")
print(f"Masa delcev na 1ml : {masa} g")
print(f"Precistimo lahko : {preciscenih_litrov} l")

# 2.

# Parametri
specificna_toplota_olja = 1670 # J/kgK
gostota_olja = 860 # kg/m3
sprememba_tlaka = 3 # Pa

def izracun_sprememba_temperature(deltap: float, rho: float, c: float):
    """
    Input: \n
    deltap ... sprememba tlaka [Pa] \n
    rho ... gostota olja [kg/m3] \n
    c ... specificna toplota olja [J/kgK] \n
    Output: \n
    deltaT ... sprememba temperature [°C]
    """
    deltaT = deltap / (rho * c)
    return deltaT

sprememba_temperature = izracun_sprememba_temperature(sprememba_tlaka, gostota_olja, specificna_toplota_olja)
print(f"Sprememba temperature : {sprememba_temperature} °C")