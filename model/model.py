import pprint as prp
import numpy as np
from math import *

from report.report_builder import BuildDoc


def model(TPd, op):
    # Operational Parameters
    Nm, Nd, Nc, Na, Nsp = op
    # Nm = 1450  # output speed of the electric motor in rpm
    # Nd = 109  # Design speed of the digester shaft in rpm
    # Nc = 109  # Design speed of the cake breaker shaft in rpm
    # Na = 218  # speed of the auger shaft(Na) in rpm
    # Nsp = 60  # speed of the screw press shaft in rpm

    # Constant Parameters
    td = 180  # total time required to load, digest and discharge a batch of palm fruits from the digester, in secs.
    pd = 913  # density of digested palm fruit, kg/m^3
    pp = 913  # density of digested palm fruit pulp, kg/m^3
    ps = 7850  # density of mildsteel, kg/m^3
    pb = 1140  # density of belt material, kg/m^3
    pf = 625  # density of wet palm fruit fiber, kg/m^3
    g = 9.81  # acceleration due to gravity, m/s^2
    k1 = 0.8  # digester fill volume factor
    k2 = 0.7  # percentage of pulp contained in a unit mass of digested palm fruit
    k3 = 1.15  # ratio of outer diameter to the inner diameter of digester, cakebreake and auger membranes
    k4 = 0.5  # fill volume factor of the separator chamber
    k5 = 0.5  # Filling coeeficient of the screw section
    k6 = 0.4  # Material factor
    k7 = 12  # correction factor to determine the outer diameter of auger membrane
    k8 = 0.82  # correction factor to determine the diameter of auger membrane
    kb = 1.0  # combined shock and fatique factor for bending
    kt = 1.0  # combined shock and fatique factor for twisting
    sf = 1.4  # Service factor for belt selection
    P = 2.8  # maximum safe stress of belt material, Mpa=N/mm^2
    u = 0.35  # coefficient of friction between belt and pulley
    tau1 = 42  # maximum permissible shear stress on shaft,Mpa=N/mm^2
    q = 84  # maximum permissible working stress in tension or compression ,Mpa=N/mm^2
    do = 247  # yield stress of the shaft material (mild steel), in N/mm2
    B1 = 38  # groove angle on the V-Belt pulley
    Psp = 200  # Maximum squeezing pressure for oil extraction, in kPa
    c = 0.003  # clearance between digester beaters and the digester barrel, in m
    c1 = 0.01  # clearance between the cake breaker beaters and the separator top cover, in m
    c2 = 0.03  # clearance between the cake breaker beaters and auger/separator side walls, in m
    wa = 0.003  # width of the separator pulp discharge chute, in m
    wab = 0.0025  # width of the auger screw flight(i.e. depth of the auger screw), in m
    tab = 0.005  # thickness of the auger screw flight, in m



    # Standards
    # ==== Internal Diameters of auger membrane (Ai)in m ====
    Ai = np.array([0.015, 0.020, 0.025, 0.040, 0.050, 0.080, 0.10, 0.125, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40])

    # ==== External Diameters of auger membrane (Ao)in m ====
    Ao = np.array(
        [0.02134, 0.02667, 0.03340, 0.0483, 0.0603, 0.0889, 0.1143, 0.1413, 0.1683, 0.2191, 0.273, 0.3239, 0.3556, 0.4064])

    # ==== Internal Diameters of Digester Barrel (Pi)in m ====
    Pi = np.array([0.15, 0.20, 0.25, 0.30, 0.35, 0.40])

    # ==== External Diameters of Digester Membrane (Po)in m ====
    Po = np.array([0.0483, 0.0603, 0.0889, 0.1143, 0.1413, 0.1683])

    # = == == Standard diameters of Deformed / Twisted Steel Bar in m ===
    Ao1 = np.array([0.006, 0.008, 0.010, 0.0120, 0.0140, 0.0160, 0.0180, 0.020, 0.022, 0.025, 0.028, 0.032, 0.036, 0.040])

    # === Corresponding length of digester beaters, in m
    LB = np.array([0.04785, 0.06685, 0.07755, 0.08985, 0.10135, 0.11285])

    # === Corresponding number of rows of digester beaters
    dbr = np.array([0, 3, 4, 5, 6, 7])

    # ===== Standard Lengths of Types A, B, C, D and E V-Belts in mm ===
    A = np.array([645, 696, 747, 823, 848, 925, 950, 1001, 1026, 1051, 1102, 1128, 1204, 1255, 1331, 1433, 1458, 1509,
                  1560, 1636, 1661, 1687, 1763, 1814, 1941, 2017, 2068, 2093, 2195, 2322, 2474, 2703, 2880, 3084, 3287,
                  3693])

    B = np.array([932, 1008, 1059, 1110, 1212, 1262, 1339, 1415, 1440, 1466, 1567, 1694, 1770, 1821, 1948, 2024, 2101,
                  2202, 2329, 2507, 2583, 2710, 2888, 3091, 3294, 3701, 4056, 4158, 4437, 4615, 4996, 5377])

    C = np.array([1275, 1351, 1453, 1580, 1681, 1783, 1834, 1961, 2088, 2113, 2215, 2342, 2494, 2723, 2901, 3104,
                  3205, 3307, 3459, 3713, 4069, 4171, 4450, 4628, 5009, 5390, 6101, 6863, 7625, 8387, 9149])

    D = np.array(
        [3127, 3330, 3736, 4092, 4194, 4473, 4651, 5032, 5413, 6124, 6886, 7648, 8410, 9172, 9934, 10696, 12220, 13744,
         15268, 16792])

    E = np.array([5426, 6137, 6899, 7661, 8423, 9185, 9947, 10709, 12233, 13757, 15283, 16805])

    Bearings = {10: [0, [0.743, 0.846, 1.469]], 12: [1, [0.823, 0.979, 1.691]], 15: [2, [0.890, 1.157, 2.092]],
                17: [3, [0.952, 1.469, 2.492, 4.050]], 20: [4, [1.629, 1.780, 2.893, 6.141]],
                25: [5, [1.758, 2.225, 4.050, 7.165]], 30: [6, [2.420, 2.715, 5.296, 8.655]],
                35: [7, [3.013, 3.783, 6.675, 10.191]], 40: [8, [3.190, 4.450, 8.188, 11.704]],
                45: [9, [4.094, 4.940, 9.879, 13.662]], 50: [10, [4.325, 5.429, 11.080, 15.620]],
                55: [11, [5.874, 6.853, 13.083, 17.800]], 60: [12, [6.186, 7.298, 13.573, 20.070]],
                65: [13, [6.484, 8.411, 17.750, 22.475]], 70: [14, [8.188, 9.212, 19.080, 27.635]],
                75: [15, [8.566, 10.146, 21.360, 30.349]], 80: [16, [10.146, 11.081, 22.562, 33.242]],
                85: [17, [11.058, 13.083, 25.276, 36.179]], 90: [18, [12.238, 13.973, 27.590, 39.272]],
                95: [19, [12.816, 16.109, 30.705, 45.740]], 100: [20, [13.350, 17.444, 34.176, 52.620]],
                105: [21, [15.041, 18.334, 37.38]], 110: [22, [16.732, 20.025, 41.83]]}


    def bearings_selector(frs, bs, br, nd):
        """ Select radial ball bearings based on radial loads (frs) and bore of shaft bs"""
        V = 1  # Rotation Factor
        X = 1  # The radial factor
        Y = 1.5  # The thrust factor
        Ka = 1.5  # Application factor for uniform and steady load on ball bearings
        Kt = 1.05  # Temperature factor for temperatures of about 125 degrees
        Ld = 24000  # Desired life of bearing in hours
        Lc = 10000  # Catalogue life of bearing in hours
        Nd = nd  # Desired Rotational speed of bearing in rev/min
        Nc = 500  # Catalogue Rotational speed of bearing in rev/min
        bores = np.array([*br.keys()])  # create an array of standard bore sizes
        bore = min(bores[bores > bs])  # find the smallest standard bore greater than the given one

        def compute_cr(fr):
            p = V * fr  # Equivalent load on bearing

            # Accounting for temperature and application factors to compute the design load
            f = p * Ka * Kt

            # Computing Radial Load Rating
            kl = (Ld / Lc) ** (1 / 3)  # Life Factor
            ks = (Nd / Nc) ** (1 / 3)  # Speed factor
            cr = (f * kl * ks) / 1000  # Computed critical radial load capacity

            # Choose bearing from standards
            scr = np.array(br[bore][1])  # Create the array of standard critical radial load ratings
            Cr = min(scr[scr > cr])  # Standard critical radial load capacity
            bi = ((np.nonzero(scr == Cr)[0][0] + 1) * 100) + br[bore][0]  # Calculate bearing number
            return bi, cr, Cr

        results = [compute_cr(i) for i in frs]
        return [bore, *results]


    def BeltSelector(Pd):
        if Pd <= 3000:
            A1 = 104  # cross sectional area of belt
            T1 = P * A1
            Belt_Type = 'A'
            Belt = A
            e = 15
            f = 10
        elif 3001 <= Pd <= 15000:
            A1 = 187
            T1 = P * A1
            Belt_Type = 'B'
            Belt = B
            e = 19
            f = 12.5
        elif 15001 <= Pd <= 75000:
            A1 = 308
            T1 = P * A1
            Belt_Type = 'C'
            Belt = C
            e = 25.5
            f = 17
        elif 75001 <= Pd <= 150000:
            A1 = 608
            T1 = P * A1
            Belt_Type = 'D'
            Belt = D
            e = 37
            f = 24
        elif 150001 <= Pd <= 350000:
            A1 = 874
            T1 = P * A1
            Belt_Type = 'E'
            Belt = E
            e = 44.5
            f = 29

        return A1, T1, e, f, Belt_Type, Belt


    def select_throughput(TPd):
        # global TPd, A, B, C, D, E, P, Parameters
        # assert 280 <= TPd <= 5650

        if 280 <= TPd <= 2000:
            L2 = 1.2
            Dmps = 0.176

        elif 2001 <= TPd <= 3000:
            L2 = 1.4
            Dmps = 0.187

        elif 3001 <= TPd <= 4000:
            L2 = 1.6
            Dmps = 0.210

        elif 4001 <= TPd <= 5650:
            L2 = 1.8
            Dmps = 0.260
        else:
            raise ValueError('Invalid Input')

        return TPd, L2, Dmps

    BeltType = {}
    TPd, L2, Dmp = select_throughput(TPd)

    # Selection of Pulley Parameters and Associated Values for the Whole Machine.
    VR2 = round(Nm / Nd)  # speed ratio of digester speed reducer
    Nrp1 = Nd * VR2  # input speed of the digester speed reducer in rpm
    VR1 = Nm / Nrp1  # velocity ratio of electric motor/digester speed reducer drive
    VR3 = Nd / Nc  # velocity ratio of the digester/cake breaker drive
    VR4 = Nc / Na  # velocity ratio of the cake breaker/auger drive
    VR6 = round(Na / Nsp)  # speed ratio of screw press speed reducer
    Nrp2 = Nsp * VR6  # input speed of the screw press speed reducer, in rpm
    VR5 = Na / Nrp2  # velocity ratio of auger/screw press speed reducer drive
    Ddp1 = VR1 * Dmp  # Diameter of the pulley on the digester speed reducer in m
    Ddp2 = Dmp  # diameter of the digester driving pulley, in m
    Dcp = VR3 * Ddp2  # diameter of the cake breaker pulley, in m
    Dap = VR4 * Dcp  # Diameter of auger auger driven pulley, in m
    Drp = Dap  # Diameter of screw press speed reducer pulley, in m
    Drp1 = VR6 * Dap  # Diameter of screw press pulley(if speed reducer is not used), in m
    v1 = ((pi * Dmp * Nm) / 60)  # Peripherial velocity of electric motor/speed reducer belt, in m/s
    v2 = ((pi * Ddp2 * Nd) / 60)  # peripherial velocity of digester/cakebreaker drive belt/digester shaft, in m/s
    v3 = ((pi * Dcp * Nc) / 60)  # peripherial velocity of cakebreaker/auger drive belt/cakebreaker shaft, in m/s
    v4 = ((pi * Dap * Na) / 60)  # peripherial velocity of auger/speed reducer drive belt, in m/s

    # EVALUATING EQUATIONS FOR THE DIGESTER UNIT OF THE MACHINE
    L4 = L2 - 0.13  # Distance of discharge chute of the digester, in m
    Lam = L2 - 0.2  # length of auger membrane, in m
    L5 = L2 - Lam  # Length of nuts discharge chute, in m
    La = Lam - 0.08  # length of the separator pulp discharge chute, in m
    Lp = 0.25 * L2  # length of the barrel, in m
    nd = 3600 / td  # the number of batches for the digestion operation per hour
    md = TPd / nd  # maximum mass capacity of the digester barrel, in kg/batch
    Vd = (md / pd)  # Volume capacity of the digester barrel, m^3/batch
    Qd = (TPd / pd) / 3600  # volumetric discharge rate of the digester, in m^3/s.
    td2 = Vd / Qd  # time taken to empty the digester barrel, in secs.
    td1 = td - td2  # time taken required to load and digest sterilized palm fruits, in secs.
    Wd = md * g  # weight capacity of the digester barrel, in N
    P1 = Wd * v2  # Power required to digest the cooked palm fruits, in W
    P2 = 4.5 * TPd * L2 * g * k6  # Power required to convey digested mash out of the digester barrel, in W
    Pd = P1 + P2  # Overall power required to drive the digester unit,in W
    Tdi = (Pd * 60) / (2 * pi * Nd)  # Torque transmitted by the digester membrane, N-m
    Mdi = ((Wd / L2) * (L2 ** 2)) / 8  # Bending moment on the digester membrane due to (UDL), N-m
    Td1 = (((kb * Mdi ** 2) + (kt * Tdi ** 2)) ** (1 / 2)) * 1e3  # Equivalent twisting moment on the digester membrane, Nmm
    ddi = (((16 * Td1) / (pi * tau1)) ** (
                1 / 3)) / 1e3  # Calculated inner diameter of digester membrane/Bore diameter of digester Pulley, in m

    Di = min(Ai[Ai >= ddi])  # Standard inner diameter of digester membrane,in m
    ddo = Di * k3  # Estimated outer diameter of digester membrane, in m

    # Choose a standard shaft from the array of External Diameters of digester membrane (Po) in m
    Do = min(Po[Po >= ddo])  # Standard outer diameter of digester membrane,in m
    Ddi = Pi[list(Po).index(Do)]  # Standard inner diameter of digester barrel, in m
    Ldmp = Ddi  # pitch of the digester beaters, in m
    vd = ((Ldmp * Nd) / 60) / 8
    Ad = Qd / vd  # Area of digester discharge chutes, in m^2
    wd = sqrt(Ad)  # Length of digester discharge opening, in m
    Bd = wd  # Width of digester discharge opening, in m
    Ldb = LB[list(Po).index(Do)]  # Length of digester beaters, in m
    Lm = L2 - 0.0508  # Length of digester and cakebreaker membrane, in m
    Mdb = ((Wd / L2) * (
        Ldb)) * 1e3  # Maximum bending moment on each of the digester beater based on point load/cantilever support,in N
    Ddb = (((32 * Mdb) / (pi * q)) ** (1 / 3)) * 1e-3  # Calculated diameter of digester beaters, in m
    pdm = 0.2  # Distance btw each row of digester beaters
    nr = dbr[list(Po).index(Do)]  # number of rows of digester beaters on the digester membrane
    ndb = (Lm / Ldmp) * nr  # Number of digester beaters
    Do1 = min(Ao1[Ao1 >= Ddb])  # Standard diameter of digester beaters,in m
    Wdm = ps * g * (pi * (((Do / 2) ** 2) - ((Di / 2) ** 2)) * L2)  # weight of the digester membrane, in N

    Wdb = ps * g * (pi * ((Do1 / 2) ** 2) * Ldb) * ndb  # weight of the digester beaters, in N
    Wd1 = Wdm + Wdb  # Total weight of the digester membrane and beaters, N
    P3 = Wd1 * v2  # Power required to overcome the inertia of the digester membrane and beaters, in W
    Pd1b = (Pd + P3) / VR2  # Power required to drive the input shaft of the digester speed reducer, in W
    Pd1a = (Pd + P3) * sf  # Design power of the digester shaft, in W
    Pd1 = Pd1a / VR2  # Design power for electric motor/digester drive belt selection, in W
    A1, T1, e, f, Belt_Type, Belt = BeltSelector(Pd1)
    BeltType['Belt type for electric motor/digester drive'] = [Belt_Type, '']

    B2 = (B1 * 0.5) * pi / 180  # pulley groove angle in radians
    C1 = (1.5 * Ddp1) / ((VR1) ** (1 / 3))  # Theoretical centre distance between electric motor and digester shafts, in m
    O1 = (pi - (2 * (
        asin((Ddp1 - Dmp) / (2 * C1)))))  # angle of lap for the electric motor/digester speed reducer drive, in radians
    T2 = T1 / exp(
        (u * O1) / (sin(B2)))  # Tension on the slack side of electric motor/digester speed reducer drive belt, in N
    Ptb1 = (T1 - T2) * v1  # Power transmitted per belt of the electric motor/speed reducer drive, in W
    N1a = ceil(Pd1 / (Ptb1))  # Actual Number of belts for the electric motor/speed reducer drive
    T3 = P * A1  # Tension on the tight side of digester/cakebreaker drive belt, in N
    C2 = (1.5 * Ddi) / ((VR3) ** (1 / 3))  # Theoretical center distance between Digester and cake breaker shafts, in m.
    O2 = (pi - (2 * (
        asin((Ddp2 - Dcp) / (2 * C2)))))  # angle of lap on the Small pulley of digester/cakebreaker belt drive, in radians
    T4 = T3 / exp((u * O2) / (sin(B2)))  # Tension on the slack side of digester/cakebreaker drive belt, in N
    Lb1 = ((2 * C1) + ((pi / 2) * (Ddp1 + Dmp)) + (((Ddp1 - Dmp) ** 2)) / (
                4 * C1)) * 1000  # theorectical pitch length of electric motor/digester speed reducer drive belt, in m
    Lb1 = min(Belt[Belt >= Lb1])
    Mts = ((T1 - T2) * (Ddp1 / 2))  # input torque of the speed reducer, in N-m
    Mtd = Mts * VR2  # Output torque speed reducer, in N-m
    W1 = (T1 + T2)  # Load due to the tensions on the motor/digester drive belt, in N
    W2 = (Wd + Wd1)  # Load on the digester shaft due to the weight of membrane, beaters and sterilized palm fruits
    W3 = (T3 + T4)  # Load due to the tensions on the digester/cakebreaker drive belt, in N (weight of pulley is neglected)

    F = ((N1a - 1) * e) + (2 * f)  # Face  width of the belt pulley mounted on the digeser shaft, in mm
    L1 = (3 * F) * 1e-3  # Length of LHS Extension of digester shaft, in m
    L3 = L1  # Length of RHS Extension of digester shaft, in m
    Ld = L2 + 2 * L1  # Length of digester shaft, in m
    RD = (((-W1) * L1) + (W2 * (L2 / 2)) + (
                W3 * (L1 + L2))) / L2  # Axial load on the RHS support (Bearing 2) of the digester shaft, in N
    RB = (W1 + W2 + W3) - RD  # Axial load on the LHS support (Bearing 1) of the digester shaft, in N
    SA = -W1
    SB = -W1 + RB
    SC = -W1 + RB - W2
    SD = -W1 + RB - W2 + RD
    SE = -W1 + RB - W2 + RD - W3
    MA = 0
    MB = -W1 * L1
    MC = (-W1 * (L1 + (L2 / 2))) + (RB * ((L1 + (L2 / 2) - L1)))
    MD = (-W1 * (L1 + L2)) + (RB * ((L1 + L2) - L1)) - (W2 * ((L1 + L2) - (L1 + (L2 / 2))))
    ME = -W1 * Ld + (RB * (Ld - L1)) - (W2 * (Ld - (L1 + (L2 / 2)))) + (RD * (Ld - (L1 + L2)))
    Mbd = max(np.abs([MA, MB, MC, MD, ME]))  # Maximum bending Moment on the digester shaft, in N-m
    Td = (((Mbd * kb) ** 2 + (Tdi * kt) ** 2) ** (1 / 2)) * 1e3  # equivalent Twisting moment on the digester shaft, in N-mm
    Md = (1 / 2) * ((kb * (Mbd * 1e3)) + (Td))  # equivalent bending moment on the digester shaft
    dd = ((16 * Td) / (pi * tau1)) ** (1 / 3)  # Diameter of the digester shaft based on shear stress, in mm
    DD = ((Md * 32) / (pi * q)) ** (1 / 3)  # Diameter of the digester shaft based on bending stress, in mm
    bore = DD  # bore is the max of DD and dd

    dds, rd, rb = bearings_selector([RD, RB], bore, Bearings, Nd)  # Call the bearings selector function
    RDbn = rd[0]  # Bearing number of digester shaft right hand bearing
    RDcrlc = rd[1]  # Computed radial load capacity of digester shaft right hand bearing
    RDsrlc = rd[2]  # Standard radial load capacity of digester shaft right hand bearing
    RBbn = rb[0]  # Bearing number of digester shaft left hand bearing
    RBcrlc = rb[1]  # Computed radial load capacity of digester shaft left hand bearing
    RBsrlc = rb[2]  # Standard radial load capacity of digester shaft left hand bearing

    # EVALUATING EQUATIONS FOR THE SEPARATOR UNIT OF THE MACHINE
    Qp = Qd * k2  # volumetric discharge rate of pulp from the separator, in m^3/s.
    Qn = Qd - Qp  # volumetric discharge rate of nuts from the separator, in m^3/s.
    Aps = wa * La  # area of pulp discharge opening of the separator, in m^2
    v5 = (Qp / Aps) * k7  # peripherial velocity of the auger membrane multiplied by 10 , in m/s===
    Da1 = (60 * v5) / (pi * Na)  # Outer diameter of auger membrane membrane in m.
    dam = min(Ao[Ao >= Da1])  # Standard outer diameter of auger membrane,in m
    Dami = dam * k8  # internal diameter of the auger membrane, in m
    dami = min(Ai[Ai >= Dami])  # Standard internal diameter of auger membrane,in m
    pam = dam  # pitch of helix on the auger membrane, in m
    vn = (pam * Na) / 60  # flow velocity of palm nuts towards its discharge opening, m/s
    C3 = (dam / 2) + wa + c2 + Ldb + (Ddi / 2)  # Theoretical center distance between cake breaker and auger shafts, in m.
    Dco = Do  # External diameter of cake breaker membrane
    Lcb = C3 - (dam / 2) - (Dco / 2) - c2  # Length of the cake breaker beaters, in m
    ncb = ndb  # Number of cake breaker beaters
    Dcb = Do1  # Diameter of cake breaker beaters, in m
    Dci = Di  # Inner diameter of cake breaker membrane
    Vam = (pi * ((dam / 2) ** 2 * Lam))  # volume of the auger membrane membrane in m^3
    Vcm = pi * ((Dco / 2) ** 2 * L2)  # volume of the cake breaker membrane in m^3
    Vcb = pi * ((Dcb / 2) ** 2 * Lcb * ncb)  # Volume of the cake breaker beaters in m^3
    Vcmi = pi * (((Dco / 2) ** 2 * L2) - ((Dci / 2) ** 2 * L2))  # Volume of material in the cake breaker membrane in m^3
    a = (Lcb * 2) + Dco + c2  # effective length of the separator chamber top, in m
    b = dam + c2  # effective length of the separator chamber base, in m
    Vs = ((0.5 * (a + b) * C3) - Vam - Vcm - Vcb) * k4  # effective volume of the separator chamber, in m^3
    Wcm = (ps * Vcmi) * g  # Weight of cakebreaker membrane, in N
    Wcb = (ps * Vcb) * g  # Weight of cakebreaker beaters, in N
    Wc1 = Wcm + Wcb  # Total weight of the cakebreaker membrane and beaters, N
    P4 = (Wc1 * v3)  # Power required to overcome the inertia of the cakebreaker membrane and beaters, in Watts (W)
    msp = pd * Vs  # mass of digested palm fruit in the separator chamber, in kg
    Ws = msp * g  # Maximum weight capacity of the separator unit,in N
    P5 = (Ws * v3)  # Power required by the cakebreaker to loosen the digested palm fruits mash, in W (W)
    Pc = P4 + P5  # Power required to drive the cakebreaker shaft, in W
    Pc1 = Pc * sf  # Design Power for digester/cakebreaker drive belt selection, in
    A1, T1, e, f, Belt_Type, Belt = BeltSelector(Pc1)  # Calling the beltselector with the design power
    BeltType['Belt type for digester/cakebreaker drive'] = [Belt_Type, '']
    T5 = P * A1  # Tension on the tight side of cakebreaker/auger drive belt, in N
    O3 = (pi - (2 * (asin((Dcp - Dcp) / (2 * C3)))))  # angle of lap for the cakebreaker/auger drive, in radians
    T6 = T5 / exp((u * O3) / (sin(B2)))  # Tension on the slack side of cakebreaker/auger drive belt, in N
    Ptb2 = (T3 - T4) * v2  # Power transmitted per belt, in W
    N2a = ceil(Pc1 / Ptb2)  # Number of belts for the digester/cakebreaker drive
    Lb2 = (2 * C2) + ((pi / 2) * (Ddp2 + Dcp)) + (((Ddp2 - Dcp) ** 2)) / (
                4 * C2)  # theorectical pitch length of cakebreaker/digester drive belt, in m
    Lb2 = min(Belt[Belt >= Lb2])  # actual pitch length of cakebreaker/digester drive belt, in m

    Mtc = (T5 - T6) * (Dcp / 2)  # maximum twisting moment on the cakebreaker shaft
    hd = wd  # height of digester discharge chute, in m
    W5 = pd * g * (Ad * hd)  # Load on the digester shaft due to palm fruits beign discharged from the digester
    W4 = W5 + Wc1  # Load on the digester shaft due to the weight of cake breaker membrane, beaters and
    W6 = T5 + T6  # Load due to the tensions on the cake breaker/auger drive belt, in N (weight of pulley is neglected)
    RI = ((W6 * (L2 + L3)) + (W5 * L4) - (W4 * (L2 / 2))) / (
        L2)  # Axial load on the RHS support (Bearing 2) of the cakebreaker shaft, in N
    RF = W4 + W5 + W6 - RI  # Axial load on the LHS support (Bearing 1) of the cakebreaker shaft, in N
    SJ = -W6
    SI = -W6 + RI
    SH = -W6 + RI - W5
    SG = -W6 + RI - W5 - W4
    SF = -W6 + RI - W5 - W4 + RF
    MJ = 0
    MI = W6 * L3
    MH = ((W6) * (L3 + L4)) - (RI * L4)
    MG = ((W6) * (L3 + (L2 / 2))) - (RI * (L2 / 2)) + (W5 * ((L2 / 2) - L4))
    MF = ((W6) * (L3 + L2)) - (RI * L2) + (W5 * (L2 - L4)) + (W4 * (L2 / 2))
    Mbc = max(np.abs([MJ, MI, MH, MG, MF]))  # Maximum bending Moment on the cake breaker shaft, in N-m
    Tc = (((Mbc * kb) ** 2 + (Mtc * kt) ** 2) ** (
                1 / 2)) * 1e3  # equivalent Twisting moment on the cakebreaker shaft,in N-mm
    Mc = (1 / 2) * ((kb * (Mbc * 1e3)) + (Tc))  # equivalent bending moment on the cakebreaker shaft,in N-mm
    dc = (((16 * Tc) / (pi * tau1)) ** (1 / 3))  # Diameter of the cakebreaker shaft based on shear stress, in mm
    DC = (Mc / ((pi / 32) * q)) ** (1 / 3)  # Diameter of the cakebreaker shaft based on bending stress, in mm
    bore = max(DC, dc)  # bore of the shaft based on maximum ofshear and bending stress
    dcs, ri, rf = bearings_selector([RI, RF], bore, Bearings, Nc)

    RIbn = ri[0]  # Bearing number of cakebreaker shaft right hand bearing
    RIcrlc = ri[1]  # Computed radial load capacity of cakebreaker shaft right hand bearing
    RIsrlc = ri[2]  # Standard radial load capacity of cakebreaker shaft right hand bearing
    RFbn = rf[0]  # Bearing number of cakebreaker shaft left hand bearing
    RFcrlc = rf[1]  # Computed radial load capacity of cakebreaker shaft left hand bearing
    RFsrlc = rf[2]  # Standard radial load capacity of cakebreaker shaft left hand bearing

    Wam = ps * g * pi * (((dam / 2) ** 2 * Lam) - ((dami / 2) ** 2 * Lam))  # Weight of Auger Membrane, in N
    Lamp = ((pi * dam) ** 2 + (pam) ** 2) ** (1 / 2)  # Length of one complete spiral on the Auger Conveyor, in m
    nab = Lam / Lamp  # number helix on the auger conveyor membrane
    Wab = ((ps * g) * (wab * Lamp * tab)) * nab  # weight of the auger screw flight, in N
    Wa1 = Wam + Wab  # Total weight of the auger membrane and screw flight, N
    P6 = (Wa1 * v5)  # Power required to overcome the weight of the auger membrane and screw fliht, in W
    P7 = Ws * vn  # Power required to discharge nut and pulp from the separator, in W
    Pa = P6 + P7  # power required to drive the auger conveyor, in W
    Ps = Pc + Pa  # Overall power required to drive the separator, in W
    Pa1 = Pa * sf  # design power of auger shaft
    A1, T1, e, f, Belt_Type, Belt = BeltSelector(Pa1)  # Calling the belt selector function.
    BeltType['Belt type for auger/speed reducer drive'] = [Belt_Type, '']
    T7 = P * A1  # Tension on the tight side of auger/speed reducer drive belt, in N
    O5 = 60  # Angle of inclination of the pulp discharge chute, in degrees
    O6 = (90 - O5)
    C4 = (Lam / 2) / tan((O6) * (pi / 180))  # Theoretical center distance between auger and screw press shafts, in m
    O4 = (pi - (2 * (asin((Dap - Drp) / (2 * C4)))))  # angle of lap for the auger/speed reducer drive, in radians
    T8 = T7 / exp((u * O4) / (sin(B2)))  # Tension on the slack side of auger/speed reducer drive belt, in N
    Ptb3 = (T5 - T6) * v3  # Power transmitted per belt, in W
    N3a = ceil(Pa1 / Ptb3)  # Actual Number of belts for the cake breaker/auger drive
    Lb3 = (2 * C3) + ((pi / 2) * (Dap + Dcp)) + (((Dap - Dcp) ** 2)) / (
                4 * C3)  # theorectical pitch length of the cake breaker/auger drive belt, in m
    Lb3 = min(Belt[Belt >= Lb3])
    BeltType['Belt type for cake breaker/auger drive'] = [Belt_Type, '']

    Mta = (T7 - T8) * (Dap / 2)  # maximum twisting moment on the auger shaft
    W7 = Ws + Wa1
    W8 = T7 + T8
    RM = (((W7 * (Lam / 2) + L5)) + (W8 * (L2 + L3))) / (
        L2)  # Axial load on the RHS support (Bearing 2) of the auger shaft, in N
    RK = W7 + W8 - RM  # Axial load on the LHS support (Bearing 1) of the auger shaft, in N
    SN = -W8
    SM = -W8 + RM
    SL = -W8 + RM - W7
    SK = -W8 + RM - W7 + RK
    MN = 0
    MM = (-W8) * L3
    ML = (-W8 * (L3 + (Lam / 2))) + (RM * Lam) - (W7 * (Lam / 2))
    MK = (-W8 * (L3 + L2)) + (RM * L2) - (W7 * ((Lam / 2) + L5))
    Mba = max(np.abs([MN, MM, ML, MK]))  # Maximum bending Moment on the cake breaker shaft, in N-m
    Ta = (((Mba * kb) ** 2 + (Mta * kt) ** 2) ** (1 / 2)) * 10 ** 3  # equivalent Twisting moment on the cakebreaker shaft
    Ma = (1 / 2) * ((kb * (Mba * 10 ** 3)) + (Ta))  # equivalent bending moment on the cakebreaker shaft
    da = (((16 * Ta) / (pi * tau1)) ** (1 / 3))  # Diameter of the Auger shaft based on shear stress
    DA = (Ma / ((pi / 32) * q)) ** (1 / 3)  # Diameter of the Auger shaft based on bending stress
    bore = max(da, DA)  # bore of the shaft based on maximum ofshear and bending stress
    das, rm, rk = bearings_selector([RM, RK], bore, Bearings, Na)  # call the bearing selector function
    RMbn = rm[0]  # Bearing number of auger shaft right hand bearing
    RMcrlc = rm[1]  # Computed radial load capacity of auger shaft right hand bearing
    RMsrlc = rm[2]  # Standard radial load capacity of auger shaft right hand bearing
    RKbn = rk[0]  # Bearing number of auger shaft left hand bearing
    RKcrlc = rk[1]  # Computed radial load capacity of auger shaft left hand bearing
    RKsrlc = rk[2]  # Standard radial load capacity of auger shaft left hand bearing
    Mtp = ((T7 - T8) * (Drp / 2))  # input torque of the screw press speed reducer, in Nm
    Mtp1 = Mtp * VR6  # output torque of the screw press speed reducer, in Nm
    Lb4 = (2 * C4) + ((pi / 2) * (Dap + Drp)) + (((Dap - Drp) ** 2)) / (
                4 * C4)  # theorectical pitch length of the auger/screw press drive belt, in m
    Lb4 = min(Belt[Belt >= Lb4])  # actual pitch length of the auger/screw press drive belt, in m
    # BeltType['Belt type for cake auger/screw press drive'] = [Belt_Type, '']
    TPp = Qp * pd * 3600  # Throughput capacity of the screw press, in kg/hr.
    if 195 <= TPp <= 1400:
        Dsf = 0.2
    elif 1400 <= TPp <= 2100:
        Dsf = 0.3
    elif 2100 <= TPp <= 2800:
        Dsf = 0.35
    elif 2800 <= TPp <= 3960:
        Dsf = 0.4
    s = Dsf  # screw Pitch, in m
    dcs = Dsf / 3.624  # depth of the screw flight, in m
    ds = Dsf - (2 * dcs)  # diameter of the screw shaft, in m
    Dm = ds + dcs  # mean thread diameter
    Vps = pi * ((ds / 2) ** 2) * Lp  # Volume of the screw shaft, in m^3
    mps = ps * Vps  # Mass of the screw shaft, in kg
    Cs = pi * Dsf  # Circunference of screw flight, in m
    Ls = ((s * 2) + (Cs ** 2)) ** (1 / 2)  # Length of one helix, in m
    ns = Lp / s  # number of screw turns
    Af = atan(s / (pi * Dsf)) * (180 / pi)  # the helix angle of the screw, in degrees
    wc = pi * Dsf * (sin(Af * (pi / 180)))  # screw channel width, in m
    tf = s - ((wc) / (cos(Af * 180 / pi)))  # flight land width, in m

    Vsf = (Ls * dcs * tf) * ns  # Total volume of the screw flight, in m^3
    msf = ps * Vsf  # Mass of the screw flight, in kg
    ms = mps + msf  # Total mass of screw conveyor, in kg
    v7 = (s * Nsp) / 60  # peripherial velocity of the screw press shaft
    P8 = (ms * g) * v7  # Power to overcome the mass of the screw conveyor, in W
    P9 = 4.5 * TPp * Lp * g * k6  # Power required to convey the pulp in the press, in W
    Ap = pi * Dm * ns * dcs  # Pressing Area, in m^2
    F1 = Psp * Ap  # Force required to squeeze out oil from the pulp, in kN
    P10 = (F1 * v7) * 1000  # Power required to press out palm oil, in W
    Pp = P8 + P9 + P10  # power required to drive the screw press, in W9
    F2 = g * (((TPp / 3600) * Lp) / v7)  # Force due to the weight of the pulp, in kN
    F3 = ms * g  # Force due to the weight of the screw conveyor, in kN
    F4 = F2 + F3  # Total load acting at the centre of the screw shaft, in kN

    A1, T1, e, f, Belt_Type, Belt = BeltSelector(Pp)
    BeltType['Belt type for auger/speed reducer drive'] = [Belt_Type, '']
    T7 = P * A1
    T8 = T7 / exp((u * O4) / (sin(B2)))

    Ptb4 = (T7 - T8) * v4  # Power transmitted per belt, in W
    N4a = ceil(Pp / (Ptb4 * VR6))  # Actual Number of belts for the auger/speed reducer drive
    Mbs = (F4 * Lp) / 4  # Maximum bending moment on screw press shaft, in kN-m
    Ts = (((Mbs * kb) ** 2 + (Mtp1 * kt) ** 2) ** (
                1 / 2)) * 1e3  # equivalent Twisting moment on the screw press shaft, in kN-mm
    ds1 = ((16 * (Ts)) / (0.27 * pi * do)) ** (1 / 3)  # diameter of screw press shaft, in mm

    # SELECTION OF THE SPEED REDUCERS
    Pds = ((2 * pi * Nd * (
                Td1 / 1000)) / 60) / 746  # Capacity of the speed reducer required for the digester unit, in horse power
    Pps = Pp / 746  # Capacity of the speed reducer required for the digester unit, in horse power

    # SELECTION OF THE PRIME MOVER
    Pt = Pd1b + Ps + Pp  # Total power required to drive the integrated machine, in W
    PkW = Pt + (0.1 * Pt)  # Capacity of the required electric motor (accounting for 10% loss), in W
    Php = PkW / 746  # Capacity of the required electric motor, in horse power


    # Parameters for the various units and the belt drive are stored in a dictionary from where they can be accessed for
    # display.

    DigesterParameters = {'Number of batches for the digestion operation per hour': [nd, 'batch/hr'],
                          'Maximum mass capacity of the digester barrel, in kg/batch': [md, 'kg/batch'],
                          'Standard inner diameter of digester membrane': [Di, 'm'],
                          'Standard outer diameter of digester membrane': [Do, 'm'],
                          'Standard inner diameter of digester barrel': [Ddi, 'm'],
                          'Pitch of the digester beaters': [Ldmp, 'm'],
                          'Length of digester discharge opening': [wd, 'm'],
                          'Width of digester discharge opening': [Bd, 'm'],
                          'length of digester beaters': [Ldb, 'm'],
                          'Length of digester and cake breaker membrane': [Lm, 'm'],
                          'Number of digester beaters': [ndb, ''], 'Standard diameter of digester beaters': [Do1, 'm'],
                          'Length of LHS Extension of digester shaft': [L1, 'm'],
                          'Length of RHS Extension of digester shaft': [L3, 'm'],
                          'Length of digester shaft': [Ld, 'm'],
                          'Diameter of the digester shaft based on shear stress': [dd, 'mm'],
                          'Diameter of the digester shaft based on bending stress': [DD, 'mm'],
                          'Standard Diameter of Digester Shaft': [dds, 'mm'],
                          'Bearing number of digester shaft right hand bearing': [RDbn, ''],
                          'Computed radial load capacity of digester shaft right hand bearing': [RDcrlc, 'kN'],
                          'Standard radial load capacity of digester shaft right hand bearing': [RDsrlc, 'kN'],
                          'Bearing number of digester shaft left hand bearing': [RBbn, ''],
                          'Computed radial load capacity of digester shaft left hand bearing': [RBcrlc, 'kN'],
                          'Standard radial load capacity of digester shaft left hand bearing': [RBsrlc, 'kN']
                          }

    SeparatorParameters = {'length of auger membrane': [Lam, 'm'],
                           'length of the separator pulp discharge chute': [La, 'm'],
                           'Standard outer diameter of auger membrane': [dam, 'm'],
                           'Standard internal diameter of auger membrane': [dami, 'm'],
                           'Pitch of helix on the auger membrane': [pam, 'm'],
                           'Flow velocity of palm nuts towards its discharge opening': [vn, 'm/s'],
                           'External diameter of cake breaker membrane': [Dco, 'mm'],
                           'Length of the cake breaker beaters': [Lcb, 'm'],
                           'Number of cake breaker beaters': [ncb, ''],
                           'Diameter of cake breaker beaters': [Dcb, 'm'],
                           'Inner diameter of cake breaker membrane': [Dci, 'mm'],
                           'Effective length of the separator chamber top': [a, 'm'],
                           'Effective length of the separator chamber base': [b, 'm'],
                           'Height of digester discharge chute': [hd, 'm'],
                           'Distance of discharge chute of the digester': [L4, 'm'],
                           'Diameter of the cake breaker shaft based on shear stress': [dc, 'mm'],
                           'Diameter of the cake breaker shaft based on bending stress': [DC, 'mm'],
                           'Standard Diameter of the cakebreaker shaft': [dcs, 'mm'],
                           'Bearing number of cakebreaker shaft right hand bearing': [RIbn, ''],
                           'Computed radial load capacity of cakebreaker shaft right hand bearing': [RIcrlc, 'kN'],
                           'Standard radial load capacity of cakebreaker shaft right hand bearing': [RIsrlc, 'kN'],
                           'Bearing number of cakebreaker shaft left hand bearing': [RFbn, ''],
                           'Computed radial load capacity of cakebreaker shaft left hand bearing': [RFcrlc, 'kN'],
                           'Standard radial load capacity of cakebreaker shaft left hand bearing': [RFsrlc, 'kN'],
                           'number helix on the auger conveyor membrane': [nab, ''],
                           'Diameter of the Auger shaft based on shear stress': [da, 'mm'],
                           'Diameter of the Auger shaft based on bending stress': [DA, 'mm'],
                           'Standard Diameter of the auger shaft': [das, 'mm'],
                           'Bearing number of auger shaft right hand bearing': [RMbn, ''],
                           'Computed radial load capacity of auger shaft right hand bearing': [RMcrlc, 'kN'],
                           'Standard radial load capacity of auger shaft right hand bearing': [RMsrlc, 'kN'],
                           'Bearing number of auger shaft left hand bearing': [RKbn, ''],
                           'Computed radial load capacity of auger shaft left hand bearing': [RKcrlc, 'kN'],
                           'Standard radial load capacity of auger shaft left hand bearing': [RKsrlc, 'kN'],
                           }

    ScrewPressParameters = {'Internal diameter of screw press barrel': [Dsf, 'm'], 'Screw Pitch': [s, 'm'],
                            'depth of the screw flight': [dcs, 'm'], 'diameter of the screw shaft': [ds, 'm'],
                            'mean thread diameter': [Dm, 'm'], 'length of the barrel': [Lp, 'm'],
                            'number of screw turns': [ns, ''], 'helix angle of the screw': [Af, 'degrees'],
                            'screw channel width': [wc, 'm'], 'flight land width': [tf, 'm'],
                            'diameter of screw press shaft': [ds1, 'mm']}

    PulleyParameters = {'Diameter of the pulley on the digester speed reducer': [Ddp1, 'm'],
                        'Diameter of the digester driving pulley': [Ddp2, 'm'],
                        'Diameter of the cake breaker pulley': [Dcp, 'm'],
                        'Diameter of auger Auger driven pulley': [Dap, 'm'],
                        'Diameter of screw press speed reducer pulley': [Drp, 'm'],
                        'Diameter of screw press pulley (if speed reducer is not used)': [Drp1, 'm']}

    BeltParameters = {'Minimum center distance between electric motor and digester shafts': [C1, 'm'],
                      'Minimum center distance between Digester and cake breaker shafts': [C2, 'm'],
                      'Minimum center distance between cake breaker and auger shafts': [C3, 'm'],
                      'Minimum center distance between auger and screw press shafts': [C4, 'm'],
                      'pitch length of electric motor/digester speed reducer drive belt': [Lb1, 'm'],
                      'pitch length of the digester/cake breaker drive belt': [Lb2, 'm'],
                      'pitch length of the cake breaker/auger drive belt': [Lb3, 'm'],
                      'pitch length of the auger/screw press drive belt': [Lb4, 'm'],
                      'Actual Number of belts for the electric motor/speed reducer drive': [N1a, ''],
                      'Actual Number of belts for the digester/cake breaker drive': [N2a, ''],
                      'Actual Number of belts for the cake breaker/auger drive': [N3a, ''],
                      'Actual Number of belts for the auger/speed reducer drive': [N4a, '']}

    BeltParameters.update(BeltType)

    PowerRequirement = {'Capacity of the speed reducer required for the digester unit': [Pds, 'hp'],
                        'Capacity of the speed reducer required for the screw press': [Pps, 'hp'],
                        'Total power required to drive the integrated machine': [Pt, 'W'],
                        'Capacity of the required electric motor (accounting for 10%loss)': [PkW, 'W'],
                        'Capacity of the required electric motor, in horse power': [Php, 'hp']}

    """The data for each unit is contained in a dictionary. The dictionary contains two items 'parameters' and 'parts'. 
    The 'parameters' value is a dictionary containing the parameters of that unit in a dictionary. While 'parts' is the 
    key to an array containing drawings of that file. Each item in this array is a dictionary containing three items 
    'name' which is the name of that part, 'definition' which is a description of that file an 'files' which is an array 
    containing the image files. """
    duparts = [{'name': 'Component Drawings', 'definition': '', 'files': 'Digester Unit.jpg'}]
    suparts = [{'name': 'Component Drawings', 'definition': '', 'files': 'Separator Unit.jpg'}]
    prparts = [{'name': 'Component Drawings', 'definition': '', 'files': 'Press Unit.jpg'}]
    Parameters = {
        'Digester Unit': {'parameters': DigesterParameters, 'parts': duparts},
        'Separator Unit': {'parameters': SeparatorParameters, 'parts': suparts},
        'Screw Press Unit': {'parameters': ScrewPressParameters, 'parts': prparts},
        'Pulley System': {'parameters': PulleyParameters, 'parts': []},
        'Parameters of the Drive System': {'parameters': BeltParameters, 'parts': []},
        'Power Requirement of the Machine': {'parameters': PowerRequirement, 'parts': []}
    }

    return Parameters


fullparts = [{'name': 'Component Drawings', 'definition': '', 'files': 'Components 1.jpg'},
             {'name': 'Component Drawings', 'definition': '', 'files': 'Components 2.jpg'},
             {'name': 'Front View', 'definition': '', 'files': 'Digester Fiber Separator Press Machine Front View.jpg'},
             {'name': 'Top View', 'definition': '', 'files': 'Digester Fiber Separator Press Machine Top View.jpg'},
             {'name': 'Back View', 'definition': '', 'files': 'Digester Fiber Separator Press Machine Back View.jpg'},
             {'name': 'Bottom View', 'definition': '', 'files': 'Digester Fiber Separator Press Machine Bottom View.jpg'},
             {'name': 'Right View', 'definition': '', 'files': 'Digester Fiber Separator Press Machine Right View.jpg'},
             {'name': 'Left View', 'definition': '', 'files': 'Digester Fiber Separator Press Machine Left View.jpg'},
             {'name': 'Full Diagram', 'definition': '', 'files': 'Full Diagram 1.jpg'},
             {'name': 'Labeled Diagram', 'definition': '', 'files': 'Full Diagram.jpg'}]


def tabulate(unit):
    """Creates an array of arrays containing the parameters, units and value of each of each section of the machine """
    data = [["Parameter", "Value", "Units"]]
    for k, v in unit.items():
        val = round(v[0], 4) if isinstance(v[0], (float, int)) else v[0]
        data.append([k.title(), val, v[1]])
    return data


def format_results(units, capacity):
    """
    Formats the results of the model computation for easy dispaly by the GUI and easy pdf report generation
    :param units:
    :param capacity:
    :return: The output is a dictionary
    """
    output = {'sections': [{'title': 'Integrated Machine', 'drawings': fullparts, 'data': []}]}
    t = f'Design Manual for {capacity} Capacity Palm Oil Processing Machine'
    for unit in units:
        section = {'title': unit, 'data': tabulate(units[unit]['parameters']), 'drawings': units[unit]['parts']}
        # output[str(title)] = {data, title}
        output['sections'].append(section)
    output['cover'] = {'title': t, 'image': 'coverimage.jpg'}
    output['filename'] = f"{t}.pdf"

    return output


if __name__ == '__main__':
    p = model(4080, [1450, 109, 109, 218, 60])
    from report.report_builder import BuildDoc
    output = format_results(p, 4080)
    fname = output['filename']
    BuildDoc(output, fname)

