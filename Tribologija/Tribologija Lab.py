from math import log10, pow, pi, e, sqrt
import numpy as np
import matplotlib.pyplot as plt

# 1. , 2. Vaja : Hrapavost

class Merjenec():
    def __init__(self, Ra: float, Sa: float, Sq: float, Hv: float):
        """
        Ra hrapavost [μm] \n
        Sa [nm] \n
        Sq [nm] \n
        Hv [HV]
        """
        self.Ra = Ra
        self.Sa = Sa
        self.Sq = Sq
        self.HV = Hv

# Dobljene meritve hrapavosti, Sa, Sq in trdote za mali in veliki merjenec
merjenec_mali = Merjenec(0.25, 230.33, 302, 926.2)
merjenec_veliki = Merjenec(0.05275, 109.25, 143.20, 0)


# 3. Vaja : Viskoznost

class MeritveNaViskozimetru():
    def __init__(self, temperatura: int, dinamicna_viskoznost: float, kinematicna_viskoznost: float, gostota: float):
        """
        temperatura [°C] \n
        dinamicna_viskoznost [mPa s] \n
        kinematicna_viskoznost [mm2/s] \n
        gostota [g/cm3]
        """
        self.temperatura = temperatura
        self.dinamicna_viskoznost = dinamicna_viskoznost
        self.kinematicna_viskoznost = kinematicna_viskoznost
        self.gostota = gostota

# Dobljene meritve na avtomatskem rotacijskem viskozimetru Anton Paar SVM 3001
meritev_25 = MeritveNaViskozimetru(25, 340.44, 382.76, 0.8894)
meritev_40 = MeritveNaViskozimetru(40, 132.62, 150.69, 0.8801)
meritev_60 = MeritveNaViskozimetru(60, 48.644, 56.051, 0.8679)
meritev_80 = MeritveNaViskozimetru(80, 22.142, 25.875, 0.8557)
meritev_100 = MeritveNaViskozimetru(100, 11.956, 14.173, 0.8436)

def izracun_L(Y: float):
    """
    Input: \n
    Y ... izmerjena kinematicna viskoznost opazovanega olja pri 100 °C [mm2/s] \n
    Output: \n
    L ... kinematicna viskoznost pri 40 °C mineralnega olja z VI = 0, ki ima pri 100 °C enako kinematicno viskoznost kot olje, ki ga merimo [mm2/s]
    """
    L = 0.8353 * pow(Y, 2) + 14.67 * Y - 216
    return L

def izracun_H(Y: float):
    """
    Input: \n
    Y ... izmerjena kinematicna viskoznost opazovanega olja pri 100 °C [mm2/s] \n
    Output: \n
    H ... kinematicna viskoznost pri 40 °C mineralnega olja z VI = 100, ki ima pri 100 °C enako kinematicno viskoznost kot olje, ki ga merimo [mm2/s]
    """
    H = 0.1684 * pow(Y, 2) + 11.85 * Y - 97
    return H

def podatki_iz_txt(txt_file: str):
    """
    Input: \n
    txt_file ... tekstovna datoteka \n
    Output: \n
    final_data ... lista tuplov za vsako kinematično viskoznost (kinematicna viskoznost, L, H)
    """
    string_data = []
    with open(txt_file, "r") as f1:
        lines = f1.readlines()
        for line in lines:
            new_line = line.rstrip("\n")
            string_data.append(new_line)
    data = []
    for string in string_data:
        new_string = string.split(" ")
        data.append(new_string)
    final_data = []
    for dat in data:
        new_data = (float(dat[0]), float(dat[1]), float(dat[2]))
        final_data.append(new_data)
    return final_data

def tabela_L_H(kinematicna_viskoznost: float):
    """
    Input: \n
    kinematicna_viskoznost ... kinematicna viskoznost za izracun L in H \n
    Output: \n
    L ... kinematicna viskoznost pri 40 °C mineralnega olja z VI = 0, ki ima pri 100 °C enako kinematicno viskoznost kot olje, ki ga merimo [mm2/s] \n
    H ... kinematicna viskoznost pri 40 °C mineralnega olja z VI = 100, ki ima pri 100 °C enako kinematicno viskoznost kot olje, ki ga merimo [mm2/s]
    """
    spodnja_meja = data[0][0]
    index = 0
    for i in range(len(data)):
        kv = data[i][0]
        if kv < kinematicna_viskoznost and kv > spodnja_meja:
            spodnja_meja = kv
            index = i
    zgornja_meja = data[index + 1][0]

    L0 = data[index][1]
    H0 = data[index][2]
    L1 = data[index + 1][1]
    H1 = data[index + 1][2]

    L = L0 + (kinematicna_viskoznost - spodnja_meja) * ((L1- L0)/(zgornja_meja - spodnja_meja))
    H = H0 + (kinematicna_viskoznost - spodnja_meja) * ((H1- H0)/(zgornja_meja - spodnja_meja))

    return(L, H)

def izracun_indeks_viskoznosti(L: float, H: float, U: float):
    """
    Input: \n
    L ... kinematicna viskoznost pri 40 °C mineralnega olja z VI = 0, ki ima pri 100 °C enako kinematicno viskoznost kot olje, ki ga merimo [mm2/s] \n
    H ... kinematicna viskoznost pri 40 °C mineralnega olja z VI = 100, ki ima pri 100 °C enako kinematicno viskoznost kot olje, ki ga merimo [mm2/s] \n
    U ... izmerjena kinematicna viskoznost opazovanega olja pri 40 °C [mm2/s] \n
    Output: \n
    indeks_viskoznosti ... Indeks viskoznosti VI opisuje vpliv temperature na spreminjanje viskoznosti: višji VI pomeni manjši vpliv T na viskoznost
    """
    indeks_viskoznosti = ((L - U)/(L - H)) * 100
    return indeks_viskoznosti

Y = meritev_100.kinematicna_viskoznost
if Y <= 70:
    data = podatki_iz_txt("Tabela_L_H.txt")
    L, H = tabela_L_H(meritev_100.kinematicna_viskoznost)
elif Y > 70:
    L = izracun_L(Y)
    H = izracun_H(Y)
indeks_viskoznosti = izracun_indeks_viskoznosti(L, H, meritev_40.kinematicna_viskoznost)

print(f"L = {L}")
print(f"H = {H}")
print(f"Indeks viskoznosti VI = {indeks_viskoznosti}")

def izracun_koeficienta_tlaka_in_viskoznosti_alpha(T1:float, T2: float, v_t1: float, v_t2: float, v_0: float, rho_0: float):
    """
    Input: \n
    T1 je obicajno 40°C\n
    T2 je obicajno 100°C\n
    v_t1 je kinematicna viskoznost pri temperaturi T1\n
    v_t2 je kinematicna viskoznost pri temperaturi T2\n
    v_0 ... kinematicna viskoznost maziva pri doloceni temepraturi [mm2/s]\n
    rho_0 ... gostota maziva pri atmosferskem tlaku in doloceni temperaturi [kg/m3] \n
    Output: \n
    alpha ... koeficient tlaka in viskoznosti
    """
    A1 = log10(log10(v_t1 + 0.8))
    A2 = log10(log10(v_t2 + 0.8))
    C1 = log10(T1 + 273)
    C2 = log10(T2 + 273)
    # b ... parameter temperature in viskoznosti [/]
    b = (A1 - A2)/(C2 - C1)
    alpha = (1.216 + 4.143 * (pow(log10(v_0), 3.0627)) + 2.848 * pow(10, -4) * pow(b, 5.1903) * pow(log10(v_0), 1.5976) - 3.999 * pow(log10(v_0), 3.0975) * pow((rho_0 * 0.001), 0.1162)) * pow(10, -8)
    return alpha

alpha_25 = izracun_koeficienta_tlaka_in_viskoznosti_alpha(40, 100, meritev_40.kinematicna_viskoznost, meritev_100.kinematicna_viskoznost, meritev_25.kinematicna_viskoznost, meritev_25.gostota * 1000)
alpha_40 = izracun_koeficienta_tlaka_in_viskoznosti_alpha(40, 100, meritev_40.kinematicna_viskoznost, meritev_100.kinematicna_viskoznost, meritev_40.kinematicna_viskoznost, meritev_40.gostota * 1000)
alpha_60 = izracun_koeficienta_tlaka_in_viskoznosti_alpha(40, 100, meritev_40.kinematicna_viskoznost, meritev_100.kinematicna_viskoznost, meritev_60.kinematicna_viskoznost, meritev_60.gostota * 1000)
alpha_80 = izracun_koeficienta_tlaka_in_viskoznosti_alpha(40, 100, meritev_40.kinematicna_viskoznost, meritev_100.kinematicna_viskoznost, meritev_80.kinematicna_viskoznost, meritev_80.gostota * 1000)
alpha_100 = izracun_koeficienta_tlaka_in_viskoznosti_alpha(40, 100, meritev_40.kinematicna_viskoznost, meritev_100.kinematicna_viskoznost, meritev_100.kinematicna_viskoznost, meritev_100.gostota * 1000)

print(f"Alpha 25 : {alpha_25} 1/Pa")
print(f"Alpha 40 : {alpha_40} 1/Pa")
print(f"Alpha 60 : {alpha_60} 1/Pa")
print(f"Alpha 80 : {alpha_80} 1/Pa")
print(f"Alpha 100 : {alpha_100} 1/Pa")



# 4. Vaja : Four Ball test

# Doloci parametre
X = [2,2,5,3,6,7,5,7,8,1] # Dobljene vrednosti premera kalote [mm] (10 vrednosti)

L = [6, 8, 10, 13, 16, 20, 24, 32, 40, 50, 63, 80, 100, 126, 160, 200, 250, 315, 400, 500, 620, 800]
L_Dh = [0.95, 1.40, 1.88, 2.67, 3.52, 4.74, 6.05, 8.87, 11.96, 16.10, 21.86, 30.08, 40.5, 55.2, 75.8, 102.2, 137.5, 187.1, 258, 347, 462, 649]

L_Dh_10 = L_Dh[7:17]
L_10 = L[7:17]

def izracun_LDhX(LDh: float, X: float):
    """
    Input: \n
    LDh ... L*Dh faktor iz tabele \n
    X ... izmerjen premer kalote [mm] \n
    Output: \n
    LDh/X ... popravljena obremenitev [kg]
    """
    return LDh / X

LDhX_rezultati = []
for i in range(len(X)):
    LDhX_rezultati.append(izracun_LDhX(L_Dh_10[i], X[i]))

LWI = np.average(LDhX_rezultati)

print(f"LDh * X rezultati : {LDhX_rezultati} kg")
print(f"LWI = {LWI} kg")

plt.xscale("log")
plt.yscale("log")
plt.xlabel("log L [kg]")
plt.ylabel("log X [mm]")
plt.plot(L_10, X, "-go")
#plt.show()
plt.savefig("LX")
plt.close()

# 5. Vaja : Analiza s SEM




# 6. Vaja : Merjenje trenja in obrabe

def izracun_obrabni_volumen(d_pravokotni: float, d_vzporedni: float, R: float):
    """
    Input: \n
    d_pravokotni ... pravokotni premer [mm] \n
    d_vzporedni ... vzporedni premer [mm] \n
    R ... polmer [mm] \n
    Output: \n
    V_obr ... obrabni volumen [mm3]
    """
    d_sr = (d_pravokotni + d_vzporedni) / 2
    V_obr = (pi * pow(d_sr, 4)) / (64 * R)
    return V_obr

def izracun_koeficienta_obrabe(V_obr: float, F: float, s: float):
    """
    Input: \n
    V_obr ... obrabni volumen [mm3] \n
    F ... pritisna normalna sila [N] \n
    s ... drsna razdalja [m] \n
    Output: \n
    k ... koeficient obrabe [mm3/Nm]
    """
    k = V_obr / (F * s)
    return k

def izracun_ekvivalentni_radij_ukrivljenosti(R_x: float, R_y: float):
    """
    Input: \n
    R_x ... radij ukrivljenosti kroglice [mm] \n
    R_y ... radij ukrivljenosti kroglice [mm] \n
    Output: \n
    R_ ... ekvivalentni radij ukrivljenosti [mm]
    """
    R_ = pow((1 / R_x + 1 / R_y), -1)
    return R_

def izracun_ekvivalentni_modul_elasticnosti(E_A: float, E_B: float, v_A: float, v_B: float):
    """
    Input: \n
    E_A ... modul elasticnosti kroglice [MPa] \n
    E_B ... modul elasticnosti ploscice [MPa] \n
    v_A ... Poissonov kolicnik kroglice [/] \n
    v_B ... Poissonov kolicnik ploscice [/] \n
    Output: \n
    E_ ... ekvivalentni modul elasticnosti [MPa]
    """
    E_ = pow((1/2 * (((1 - pow(v_A, 2)) / E_A) + ((1 - pow(v_B, 2)) / E_B))), -1)
    return E_

def izracun_Hertzov_kontaktni_radij(F_N: float, R_: float, E_: float):
    """
    Input: \n
    F_N ... normalna obremenitvena sila [N] \n
    R_ ... ekvivalentni radij ukrivljensti [mm] \n
    E_ ... ekvivalentni modul elasticnosti [MPa] \n
    Output: \n
    a ... Hertzov kontaktni radij [mm]
    """
    a = pow(((3 * F_N * R_) / E_), 1/3)
    return a

def izracun_Hertzov_maksimalni_tlak(F_N: float, a: float):
    """
    Input: \n
    F_N ... pritisna normalna sila [N] \n
    a ... Hertzov kontaktni radij [mm] \n
    Output: \n
    p_0 ... Hertzov maksimalni kontaktni tlak [MPa]
    """
    p_0 = (3 * F_N)/(2 * pi * pow(a, 2))
    return p_0

def izracun_Hertzov_srednji_tlak(F_N: float, a: float):
    """
    Input: \n
    F_N ... pritisna normalna sila [N] \n
    a ... Hertzov kontaktni radij [mm] \n
    Output: \n
    p_sr ... Hertzov srednji kontaktni tlak [MPa]
    """
    p_sr = F_N / (pi * pow(a, 2))
    return p_sr

# Izberi parametre
d_pravokotni = 3 # pravokotni premer [mm]
d_vzporedni = 3 # vzporedni premer [mm]
R = 5 # polmer [mm]
F = 150 # pritisna sila [N]
s = 100 # drsna razdalja [m]
R_x = 5 # radij ukrivljenosti kroglice [mm]
R_y = 5 # radij ukrivljenosti kroglice [mm]
E_A = 210000 # modul elasticnosti za kroglico [MPa]
E_B = 210000 # modul elasticnosti za ploscico [MPa]
v_A = 0.3 # Poissonov kolicnik za kroglico [/]
v_B = 0.3 # Poissonov kolicnik za ploscico [/]
F_N = 150 # normalna obremenitvena sila [N]


obrabni_volumen_na_kroglici = izracun_obrabni_volumen(d_pravokotni, d_vzporedni, R)
obrabni_volumen_na_disku = izracun_obrabni_volumen(d_pravokotni, d_vzporedni, R)
koeficient_obrabe_na_kroglici = izracun_koeficienta_obrabe(obrabni_volumen_na_kroglici, F, s)
koeficient_obrabe_na_disku = izracun_koeficienta_obrabe(obrabni_volumen_na_disku, F, s)

print(f"Obrabni volumen na kroglici V_obr = {obrabni_volumen_na_kroglici}")
print(f"Obrabni volumen na disku V_obr = {obrabni_volumen_na_disku}")
print(f"Koeficient obrabe na kroglici k = {koeficient_obrabe_na_kroglici}")
print(f"Koeficient obrabe na disku k = {koeficient_obrabe_na_disku}")

ekvivalentni_radij_ukrivljenosti = izracun_ekvivalentni_radij_ukrivljenosti(R_x, R_y)
ekvivalentni_modul_elasticnosti = izracun_ekvivalentni_modul_elasticnosti(E_A, E_B, v_A, v_B)
Hertzov_kontaktni_radij = izracun_Hertzov_kontaktni_radij(F_N, ekvivalentni_radij_ukrivljenosti, ekvivalentni_modul_elasticnosti)

print(f"Ekvivalentni radij ukrivlenosti R' = {ekvivalentni_radij_ukrivljenosti} mm")
print(f"Ekvivalentni modul elasticnosti E' = {ekvivalentni_modul_elasticnosti} MPa")
print(f"Hertzov kontaktni radij a = {Hertzov_kontaktni_radij} mm")



# 7. Vaja : EHD film in trenje

def izracun_minimalna_debelina_filma(R_: float, U_p: float, G_p: float, W_p: float, k: float):
    """
    Input: \n
    R_ ... ekvivalentni radij ukrivljenosti [mm] \n
    U_p ... parameter hitrosti [/] \n
    G_p ... parameter materiala [/] \n
    W_p ... parameter obremenitve [/] \n
    k ... parameter elipticnosti [/] \n
    Output: \n
    h_0 ... minimalna debelina filma [mm]
    """
    h_0 = R_ * 3.63 * pow(U_p, 0.68) * pow(G_p, 0.49) * pow(W_p, -0.073) * (1 - pow(e, -0.68 * k))
    return h_0

def izracun_centralne_debeline_filma(R_: float, U_p: float, G_p: float, W_p: float, k: float):
    """
    Input: \n
    R_ ... ekvivalentni radij ukrivljenosti [mm] \n
    U_p ... parameter hitrosti [/] \n
    G_p ... parameter materiala [/] \n
    W_p ... parameter obremenitve [/] \n
    k ... parameter elipticnosti [/] \n
    Output: \n
    h_c ... centralna debelina filma [mm]
    """
    h_c = R_ * 2.69 * pow(U_p, 0.67) * pow(G_p, 0.53) * pow(W_p, -0.067) * (1 - 0.61 * pow(e, -0.73 * k))
    return h_c

def izracun_G_p(alpha: float, E_: float):
    """
    Input: \n
    alpha ... koeficient tlaka in viskoznosti [m2/N] \n
    E_ ... ekvivalentni modul elastičnosti kontakta [Pa] \n
    Output: \n
    G_p ... parameter materiala [/]
    """
    G_p = alpha * E_
    return G_p

def izracun_U_p(U: float, eta_0: float, R_: float, E_: float):
    """
    Input: \n
    U ... srednja hitrost kontakta [m/s] \n
    eta_0 ... dinamična viskoznost maziva pri atmosferskem tlaku in delovni temperaturi [kg/m s] \n
    R_ ... ekvivalentni radij ukrivljenosti [m] \n
    E_ ... ekvivalentni modul elastičnosti kontakta [Pa] \n
    Output: \n
    U_p ... parameter hitrosti [/]

    """
    U_p = (U * eta_0)/(E_ * R_)
    return U_p

def izracun_srednja_hitrost_kontakta(U1: float, U2: float):
    """
    Input: \n
    U1 ... hitrost telesa 1 v kontaktu [m/s] \n
    U2 ... hitrost telesa 2 v kontaktu [m/s] \n
    Output: \n
    U ... srednja hitrost kontakta [m/s]
    """
    U = (U1 + U2)/2
    return U

def izracun_W_p(F_N: float, R_: float, E_:float):
    """
    Input: \n
    F_N ... normalna obremenitev kontakta [N] \n
    R_ ... ekvivalentni radij ukrivljenosti [m] \n
    E_ ... ekvivalentni modul elastičnosti kontakta [Pa] \n
    Output: \n
    W_p ... parameter obremenitve [/]
    """
    W_p = F_N / (E_ * pow(R_, 2))
    return W_p

def izracun_parametra_elipticnosti(a: float, b: float):
    """
    Input: \n
    Za kontakt kroglica-ploscica velja, da je a = b \n
    Output: \n
    k ... parameter elipticnosti
    """
    k = a / b
    return k

def izracun_Tallianov_parameter(h_0: float, R_qA: float, R_qB: float):
    """
    Input: \n
    h_0 ... minimalna debelina mazalnega filma [mm] \n
    R_qA ... standardna deviacija hrapavosti kontaktne povrsine A [mm] \n
    R_qB ... standardna deviacija hrapavosti kontaktne povrsine B [mm] \n
    Output: \n
    lambdaa ... Tallianov parameter [/]
    """
    lambdaa = h_0 / (sqrt(pow(R_qA, 2) + pow(R_qB, 2)))
    return lambdaa

# Izberi parametre in skupino
skupina = 4
R_x = 9.525 # radij ukrivljenosti kroglice [mm]
R_y = 9.525 # radij ukrivljenosti kroglice [mm]
U = 2.5 # srednja hitrost kontakta [m/s]
F_N = 35 # normalna obremenitev kontakta
E_A = 210000 # modul elasticnosti za kroglico [MPa]
E_B = 210000 # modul elasticnosti za ploscico [MPa]
v_A = 0.3 # Poissonov kolicnik za kroglico [/]
v_B = 0.3 # Poissonov kolicnik za ploscico [/]
R_qA = 0.025 # standardna deviacija kontaktne povrsine kroglice [μm]
k_list = [2,4,5,6,7,6,6,3,4,2,9,2,7,0,4] # koeficienti trenja


ekvivalentni_modul_elasticnosti = izracun_ekvivalentni_modul_elasticnosti(E_A, E_B, v_A, v_B)
ekvivalentni_radij_ukrivljenosti = izracun_ekvivalentni_radij_ukrivljenosti(R_x, R_y)

print(f"Ekvivalentni modul elasticnosti E' = {ekvivalentni_modul_elasticnosti} MPa")
print(f"Ekvivalentni radij ukrivljenosti R' = {ekvivalentni_radij_ukrivljenosti} mm")

if skupina == 4 or 15:
    G_p = izracun_G_p(alpha_25, ekvivalentni_modul_elasticnosti * pow(10, 5))
    U_p = izracun_U_p(U, meritev_25.dinamicna_viskoznost * pow(10, -3), ekvivalentni_radij_ukrivljenosti * pow(10, -3), ekvivalentni_modul_elasticnosti * pow(10, 5))
elif skupina == 3 or 5 or 7 or 10 or 11:
    G_p = izracun_G_p(alpha_40, ekvivalentni_modul_elasticnosti * pow(10, 5))
    U_p = izracun_U_p(U, meritev_40.dinamicna_viskoznost * pow(10, -3), ekvivalentni_radij_ukrivljenosti * pow(10, -3), ekvivalentni_modul_elasticnosti * pow(10, 5))
elif skupina == 1 or 2 or 6 or 9 or 13 or 14 or 16:
    G_p = izracun_G_p(alpha_60, ekvivalentni_modul_elasticnosti * pow(10, 5))
    U_p = izracun_U_p(U, meritev_60.dinamicna_viskoznost * pow(10, -3), ekvivalentni_radij_ukrivljenosti * pow(10, -3), ekvivalentni_modul_elasticnosti * pow(10, 5))
elif skupina == 8 or 12:
    G_p = izracun_G_p(alpha_80, ekvivalentni_modul_elasticnosti * pow(10, 5))
    U_p = izracun_U_p(U, meritev_80.dinamicna_viskoznost * pow(10, -3), ekvivalentni_radij_ukrivljenosti * pow(10, -3), ekvivalentni_modul_elasticnosti * pow(10, 5))

W_p = izracun_W_p(F_N, ekvivalentni_radij_ukrivljenosti * pow(10, -3), ekvivalentni_modul_elasticnosti * pow(10, 5))
k = izracun_parametra_elipticnosti(1, 1)

print(f"G_p = {G_p}")
print(f"U_p = {U_p}")
print(f"W_p = {W_p}")
print(f"k = {k}")

minimalna_debelina_mazalnega_filma = izracun_minimalna_debelina_filma(ekvivalentni_radij_ukrivljenosti, U_p, G_p, W_p, k)
centralna_debelina_mazalnega_filma = izracun_centralne_debeline_filma(ekvivalentni_radij_ukrivljenosti, U_p, G_p, W_p, k)
Tallianov_parameter = izracun_Tallianov_parameter(minimalna_debelina_mazalnega_filma, R_qA * pow(10, -3), merjenec_veliki.Sq * pow(10, -6))

print(f"Minimalna debelina mazalnega filma h_0 = {minimalna_debelina_mazalnega_filma} mm")
print(f"Centralna debelina mazalnega filma h_c = {centralna_debelina_mazalnega_filma} mm")
print(f"Tallianov parameter = {Tallianov_parameter}")

U_list = np.logspace(log10(0.05 * pow(10, 3)), log10(2.5 * pow(10, 3)), 15)
plt.xlabel("Srednja hitrost U [mm/s]")
plt.ylabel("Koeficient trenja")
plt.plot(U_list, k_list, "-yo")
#plt.show()
plt.savefig("Uk")
plt.close()


def izracun_strizne_napetosti(mi: float, p: float):
    """
    Input: \n
    mi ... koeficient trenja \n
    p ... povprecni Hertzov tlak [MPa] \n
    Output: \n
    tau ... strizna napetost [MPa]
    """
    tau = mi * p
    return tau

def izracun_povprecni_Hertzov_tlak(p_0: float):
    """
    Input: \n
    p_0 ... maksimalni Hertzov tlak [MPa] \n
    Output: \n
    p ... povprecni Hertzov tlak [MPa] \n
    """
    p = (2 / 3) * p_0
    return p

# Izberi parametre
F_N = 35 # pritisna normalna sila [N]
U = 2.5 # srednja hitrost kontakta [m/s]

maksimalni_Hertzov_tlak = izracun_Hertzov_maksimalni_tlak(F_N, Hertzov_kontaktni_radij)
srednji_Hertzov_tlak = izracun_Hertzov_srednji_tlak(F_N, Hertzov_kontaktni_radij)
povprecni_Hertzov_tlak = izracun_povprecni_Hertzov_tlak(maksimalni_Hertzov_tlak)
strizna_napetost = izracun_strizne_napetosti(k_list[0], povprecni_Hertzov_tlak)

print(f"Maksimalni Hertzov tlak p_0 = {maksimalni_Hertzov_tlak} MPa")
print(f"Srednji Hertzov tlak p_sr = {srednji_Hertzov_tlak} MPa")
print(f"Povprecni Hertzov tlak p = {povprecni_Hertzov_tlak} MPa")
print(f"Strizna napetost tau = {strizna_napetost} MPa")

def izracun_dinamicna_viskoznost(h_c: float, R_: float, G_p: float, W_p: float, k: float, E_: float, U: float):
    """
    Input: \n
    h_c ... centralna debelina filma [mm] \n
    R_ ... ekvivalentni radij ukrivljenosti [mm] \n
    G_p ... parameter materiala [/] \n
    W_p ... parameter obremenitve [/] \n
    k ... parameter elipticnosti [/] \n
    E_ ... ekvivalentni modul elastičnosti kontakta [Pa] \n
    U ... srednja hitrost kontakta [m/s] \n
    Output: \n
    eta_0 ... dinamična viskoznost maziva pri atmosferskem tlaku in delovni temperaturi [kg/m s]
    """
    eta_0 = (pow(h_c / (R_ * 2.69 * pow(G_p, 0.53) * pow(W_p, -0.067) * (1 - 0.61 * pow(e, -0.73 * k))), -0.67) * E_ * R_) / U
    return eta_0

dinamicna_viskoznost = izracun_dinamicna_viskoznost(centralna_debelina_mazalnega_filma, ekvivalentni_radij_ukrivljenosti, G_p, W_p, k, ekvivalentni_modul_elasticnosti * pow(10, 5), U)
print(f"Dinamicna viskoznost eta_0 = {dinamicna_viskoznost} kg/m s")