import numpy as np  
    #voor numerieken berekeningen zoals sinus, cosinus en vierkants wortel (np.sqrt)
from scipy.integrate import solve_ivp  
    #differentialvergelijkingen numeriek oplossen
from scipy.optimize import fsolve  
    #wiskundige vergelijkingen numeriek oplossen
    #numeriek oplossen betekent dat je de vergelijkingen opnieuw uitvoert totdat je de juiste waarden vindt

def formules(t, state, g, Cd, rho, A, m):
        #deel waar alle formules worden uitgeschreven
    x, y, vx, vy = state
        #stopt deze waarden in een tabel
    v = np.sqrt(vx**2 + vy**2)  
        #formule algemene snelheid
    if v == 0:
        v = 1e-6  
            # Vermijd deling door nul in de formules ax en ay
    Fd = 0.5 * Cd * rho * A * v**2  
        #formule luchtweerstand
    ax = -Fd * vx / (m * v)  
        #formule versnelling op de x-as
    ay = -g - (Fd * vy / (m * v))  
        #formule versnelling op de y-as 
    return [vx, vy, ax, ay]

def lanceerhoek(v0, x_doel, h_doel, g=9.81, Cd=0.47, rho=1.225, A=0.001, m=0.005):
        #deze waarden staan niet vast
    def zoek_hoek(theta):
        theta = theta[0]  
            #Zorg ervoor dat theta een scalaire waarde is
        vx0 = v0 * np.cos(theta) 
            #formule beginsnelheid op de x-as
        vy0 = v0 * np.sin(theta) 
            #formule beginsnelheid op de y-as
        sol = solve_ivp(formules, [0, 10], [0, 0, vx0, vy0], args=(g, Cd, rho, A, m), max_step=0.01)
        x_vals, y_vals = sol.y[0], sol.y[1]
        if x_doel < np.min(x_vals) or x_doel > np.max(x_vals):
            return np.inf  
                #Vermijd extrapolatie buiten de gesimuleerde waarden
        return np.interp(x_doel, x_vals, y_vals) - h_doel

    theta_oplossing = fsolve(zoek_hoek, [np.radians(45)])
    return np.degrees(theta_oplossing[0])

v0 = 10 #weten wij door de kinetische kracht van de servo/motor te berekenen
x = 4 #berekent de turret
h = 4 #berekent de turret

hoek = lanceerhoek(v0, x, h)
    #berekent de lanceerhoek
    #deze hoek geven we door aan de turret, die op die hoek gaat staan en op het doel schiet
print(f"Benodigde lanceerhoek: {hoek:.2f} graden")
