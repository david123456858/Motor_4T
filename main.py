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
cylinder_image = pygame.image.load('cilindro.png').convert()
cylinder_image = pygame.transform.scale(cylinder_image, (80, 350))
cuerpo_image = pygame.image.load('cuerpo.png')
valve_admission_image = pygame.image.load('valdulader.png')
valve_exhaust_image = pygame.image.load('valvulaizq.png')

new_width = 500  # Ancho deseado
new_height = 500  # Alto deseado

piston_image = pygame.transform.scale(piston_image, (new_width, new_height))
cylinder_image = pygame.transform.scale(cylinder_image, (new_width, new_height))
cuerpo_image = pygame.transform.scale(cuerpo_image, (new_width, new_height))
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

def draw_piston_and_connecting_rod(piston_y):
    # Dibuja un pistón en la posición y
    # Dibuja la biela conectada al pistón
    screen.blit(cuerpo_image, (360, 150))  # Cilindro
    pygame.draw.rect(screen, background_color, (365, 205, 70, 340))  # Interior del cilindro

    # Ajusta la posición de la biela en función de piston_position
    
    
    # Dibuja la biela conectada al pistón
    

def draw_valves():
    # Dibuja el cilindro con las válvulas de admisión y escape en las esquinas superiores
    pygame.draw.rect(screen, cylinder_color, (360, 200, 80, 350))  # Cilindro
    pygame.draw.rect(screen, background_color, (365, 205, 70, 340))  # Interior del cilindro

    # Dibuja las válvulas de admisión en la esquina superior izquierda
    pygame.draw.circle(screen, valve_color if valve_admission_open else background_color, (365, 205), 10)  # Válvula de admisión

    # Dibuja las válvulas de escape en la esquina superior derecha
    pygame.draw.circle(screen, exhaust_valve_color if valve_exhaust_open else background_color, (435, 205), 10)  # Válvula de escape

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(background_color)
 
    # Actualiza el ángulo del cigüeñal
    crankshaft_angle += math.radians(piston_speed)
    if crankshaft_angle >= 2 * math.pi:
        crankshaft_angle = 0

    # Calcula la posición del pistón
    piston_position = 300 - crankshaft_length * math.sin(crankshaft_angle)
    
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
    
    draw_piston_and_connecting_rod(piston_position)
    
    pygame.display.update()

pygame.quit()
sys.exit()
