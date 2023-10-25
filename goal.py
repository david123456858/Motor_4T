import pygame
import sys
import math

pygame.init()

# Configuración de la pantalla
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Motor de 4 tiempos")
# Carga de las imagenes 
piston_image = pygame.image.load('piston.png')
cylinder_image = pygame.image.load('cilindro.png')
cuerpo_image = pygame.image.load('cuerpo.png')
valve_admission_image = pygame.image.load('derecha.png')
valve_exhaust_image = pygame.image.load('valvulaizq.png')
polea_image = pygame.image.load('polea.png')

new_width = 500  # Ancho deseado
new_height = 500  # Alto deseado

piston_image = pygame.transform.scale(piston_image, (130, 150))
cylinder_image = pygame.transform.scale(cylinder_image, (200, 200))
cuerpo_image = pygame.transform.scale(cuerpo_image, (new_width, new_height))
polea_image = pygame.transform.scale(polea_image, (100, 100))
valve_admission_image=pygame.transform.scale(valve_admission_image, (100, 100))
valve_exhaust_image=pygame.transform.scale(valve_exhaust_image, (100, 100))

# Colores personalizados
background_color = (255, 255, 255)
cylinder_color = (0, 0, 0)
piston_color = (0, 0, 0)
connecting_rod_color = (0, 0, 255)  # Color de la biela
valve_color = (255, 0, 0)  # Color de la válvula de admisión
exhaust_valve_color = (0, 255, 0)  # Color de la válvula de escape

# Inicialización del motor
running = True
rpm = 0
piston_position = 0
stroke = 0

# Ángulos para el cigüeñal
crankshaft_angle = 0
piston_speed = 0.2  # Velocidad de movimiento del pistón más lenta
crankshaft_length = 100
piston_length = 100

# Posición de la biela
connecting_rod_length = 200  # Longitud de la biela

# Estados de los tiempos del motor
ADMISSION = 1
COMPRESSION = 2
COMBUSTION = 3
EXHAUST = 4
current_state = ADMISSION

# Duración de cada tiempo en frames
state_duration = 400  # Ahora más lento
frame_count = 0

# Estado de las válvulas
valve_admission_open = True
valve_exhaust_open = False
#valvula izquierda
def valvula_izq():
    screen.blit(valve_exhaust_image, (515, 187))  # Cilindro
    pygame.draw.rect(screen, background_color, (365, 205, 70, 340))  # Interior del cilindro
#valvula derecha
def valvula_der():
    screen.blit(valve_admission_image, (630, 190))  # Cilindro
    pygame.draw.rect(screen, background_color, (365, 205, 70, 340))  # Interior del cilindro   
#caja del motor
def draw_cuerpo():
    # Dibuja un pistón en la posición y
    # Dibuja la biela conectada al pistón
    screen.blit(cuerpo_image, (360, 150))  # Cilindro
    pygame.draw.rect(screen, background_color, (365, 205, 70, 340))  # Interior del cilindro
#valvula cuerpo del piston    
def calcular_inclinacion_piston(angulo_ciguenal):
    amplitud_maxima = 12
    inclinacion_maxima = amplitud_maxima * math.sin(angulo_ciguenal)
    return inclinacion_maxima
def draw_cilindro(x, y, crankshaft_angle):
    amplitud_x = 50
    amplitud_y = 25
    velocidad_inclinacion = 1.0  # Ajusta la velocidad de cambio de inclinación

    # Calcula la inclinación en función del ángulo del cigüeñal
    x_cilindro = 0  # En el punto muerto superior
    y_cilindro = -amplitud_y * math.sin(crankshaft_angle)
    inclinacion_maxima = calcular_inclinacion_piston(crankshaft_angle)

    rotated_cylinder = pygame.transform.rotate(cylinder_image, inclinacion_maxima)
    screen.blit(rotated_cylinder, (x + x_cilindro, y + y_cilindro))
    pygame.draw.rect(screen, background_color, (365, 205, 70, 340))

    # Ajusta el ángulo del cigüeñal para un cambio más suave
    crankshaft_angle += velocidad_inclinacion * 0.01  # 0.01 es un valor de ajuste

    if crankshaft_angle >= 2 * math.pi:
        crankshaft_angle = 0

    return crankshaft_angle
#cabeza del piston
def draw_piston():
    screen.blit(piston_image, (560, 299))  
    pygame.draw.rect(screen, background_color, (365, 205, 70, 340))
#cigueñal    
def draw_polea():
    screen.blit(polea_image, (575, 510))  # Cilindro
    pygame.draw.rect(screen, background_color, (365, 205, 70, 340))
    
def draw_valves():
    # Dibuja el cilindro con las válvulas de admisión y escape en las esquinas superiores
    pygame.draw.rect(screen, cylinder_color, (360, 200, 80, 350))  # Cilindro
    pygame.draw.rect(screen, background_color, (365, 205, 70, 340))  # Interior del cilindro

    # Dibuja las válvulas de admisión en la esquina superior izquierda
    pygame.draw.circle(screen, valve_color if valve_admission_open else background_color, (550, 220), 10)  # Válvula de admisión

    # Dibuja las válvulas de escape en la esquina superior derecha
    pygame.draw.circle(screen, exhaust_valve_color if valve_exhaust_open else background_color, (435, 205), 10)  # Válvula de escape
def calcular_posicion_piston(angulo_ciguenal):
    # Calcula la posición del pistón en x y en y
    x = 520  # Posición inicial en x
    y = 350 + 200 * math.sin(angulo_ciguenal)  # Posición inicial en y y desplazamiento lateral

    return x, y
# Parámetros para la oscilación del cuerpo del pistón
amplitude = 50  # Amplitud del movimiento (cambia según tus necesidades)
frequency = 0.01  # Frecuencia de oscilación (cambia según tus necesidades)
time = 0

crankshaft_angle = 0
piston_speed = 0.2  # Velocidad de movimiento del pistón más lenta
crankshaft_length = 100
piston_length = 100
amplitude = 20
angle = math.pi / 4  # Ángulo inicial (45 grados)
angular_velocity = 0.1
running = True

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(background_color)
    
    time += 1
    
    piston_position_x = 560 + 50 * math.sin(angle)
    piston_position_y = 300 + amplitude * math.sin(frequency * time)

    # Calcula la posición del pistón
    piston_position = 300 - crankshaft_length * math.sin(crankshaft_angle)
    x, y = calcular_posicion_piston(crankshaft_angle)

    # Calcula la inclinación en función de la dirección del movimiento
    if piston_position_y > 300:
        # Si el pistón está bajando, inclínalo hacia la derecha
        inclinacion_maxima = -angle * (180 / math.pi)  # Inclinación negativa hacia la derecha
    else:
        # Si el pistón está subiendo, inclínalo hacia la izquierda
        inclinacion_maxima = angle * (180 / math.pi)  # Inclinación positiva hacia la izquierda
    
    angle += angular_velocity
    rotated_cylinder = pygame.transform.rotate(cylinder_image, inclinacion_maxima)
    screen.blit(rotated_cylinder, (x, y))
    piston_position_x = 560 + 50 * math.sin(angle)

    # Actualiza el ángulo del cigüeñal
    crankshaft_angle += math.radians(piston_speed)
    if crankshaft_angle >= 2 * math.pi:
        crankshaft_angle = 0
        
    piston_position_y = 300 + amplitude * math.sin(frequency * time)
    # Calcula la posición del pistón
    piston_position = 300 - crankshaft_length * math.sin(crankshaft_angle)
    x, y = calcular_posicion_piston(crankshaft_angle)
    # Dibuja las válvulas de admisión y escape
    draw_valves()

    # Actualizar el estado del motor
    frame_count += 1
    if frame_count > state_duration:
        frame_count = 0
        if current_state == ADMISSION:
            current_state = COMPRESSION
            valve_admission_open = False  # Cierra la válvula de admisión
            valve_exhaust_open = True  # Abre la válvula de escape
        elif current_state == COMPRESSION:
            current_state = COMBUSTION
        elif current_state == COMBUSTION:
            current_state = EXHAUST
            valve_admission_open = True  # Abre la válvula de admisión
            valve_exhaust_open = False  # Cierra la válvula de escape
        else:
            current_state = ADMISSION

    # Dibuja el pistón y la biela en los cilindros
    
    draw_piston()
    draw_valves()
    draw_cuerpo()
    crankshaft_angle=draw_cilindro(520, 350,crankshaft_angle)
    draw_polea()
    valvula_der()
    valvula_izq()
    pygame.display.update()
pygame.quit()
sys.exit()