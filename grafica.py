import numpy as np
import matplotlib.pyplot as plt

# Parámetros del motor
volumen_cilindro = 1000  # Volumen del cilindro en cm^3
presion_inicial = 1.0  # Presión inicial en atmósferas
temperatura_inicial = 300  # Temperatura inicial en Kelvin
relacion_compresion = 10  # Relación de compresión

# Simulación del motor de 4 tiempos
def motor_4_tiempos():
    # 1. Admisión
    volumen_admision = volumen_cilindro
    presion_admision = presion_inicial
    temperatura_admision = temperatura_inicial

    # 2. Compresión
    volumen_compresion = volumen_cilindro / relacion_compresion
    presion_compresion = presion_admision * relacion_compresion
    temperatura_compresion = (temperatura_admision * presion_compresion) / (presion_admision)

    # 3. Explosión
    volumen_explosion = volumen_cilindro
    presion_explosion = presion_compresion * 20  # Ejemplo de aumento de presión en la explosión
    temperatura_explosion = (temperatura_compresion * presion_explosion) / (presion_compresion)

    # 4. Escape
    volumen_escape = volumen_cilindro
    presion_escape = presion_explosion / 10  # Ejemplo de reducción de presión en el escape
    temperatura_escape = (temperatura_explosion * presion_escape) / (presion_explosion)

    return [volumen_admision, presion_admision, temperatura_admision], \
           [volumen_compresion, presion_compresion, temperatura_compresion], \
           [volumen_explosion, presion_explosion, temperatura_explosion], \
           [volumen_escape, presion_escape, temperatura_escape]

# Realizar la simulación
estado_admision, estado_compresion, estado_explosion, estado_escape = motor_4_tiempos()

# Extraer datos
volumen = [estado_admision[0], estado_compresion[0], estado_explosion[0], estado_escape[0]]
presion = [estado_admision[1], estado_compresion[1], estado_explosion[1], estado_escape[1]]
temperatura = [estado_admision[2], estado_compresion[2], estado_explosion[2], estado_escape[2]]
tiempos = np.arange(4)

# Etiquetas para cada tiempo del ciclo
nombres_tiempos = ["Admisión", "Compresión", "Explosión", "Escape"]

# Visualizar los resultados con etiquetas
plt.figure(figsize=(10, 5))
plt.subplot(121)
plt.plot(tiempos, presion, marker='o')
plt.title('Presión en el Cilindro')
plt.xlabel('Tiempo (Tiempo de Ciclo)')
plt.ylabel('Presión (atm)')
plt.xticks(tiempos, nombres_tiempos)

plt.subplot(122)
plt.plot(tiempos, temperatura, marker='o')
plt.title('Temperatura en el Cilindro')
plt.xlabel('Tiempo (Tiempo de Ciclo)')
plt.ylabel('Temperatura (K)')
plt.xticks(tiempos, nombres_tiempos)

plt.tight_layout()
plt.show()
