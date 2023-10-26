import pygame
import sys
import math
import random 
pygame.init()

# Configuración de la pantalla
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
air_inflow = 0.1  # Cantidad de aire (por ejemplo, en litros)
fuel_inflow = 0.05  # Cantidad de gasolina (por ejemplo, en litros)
pygame.display.set_caption("Motor de 4 tiempos")
# Antes del bucle principal
piston_background = pygame.image.load("pis.png")
valvula_img = pygame.image.load("valvula.png")
caja_image = pygame.image.load('cuerpo.png')
caja_image= pygame.transform.scale(caja_image, (600, 700))
# Colores personalizados
background_color = (255, 255, 255)
cylinder_color = (0, 0, 0)
piston_color = (0, 0, 0)
connecting_rod_color = (68, 70, 84)  # Color de la biela
valve_color = (0, 255, 0)  # Color de la válvula de admisión (verde)
exhaust_valve_color = (255, 0, 0)  # Color de la válvula de escape(rojo)

# Inicialización del motor
running = True
rpm = 0
piston_position = 0
stroke = 0

# Ángulos para el cigüeñal
crankshaft_angle = 0
piston_speed = 0.5  # Velocidad de movimiento del pistón más lenta
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
state_duration = 572   # Ahora más lento
frame_count = 0

# Estado de las válvulas
valve_admission_open = True
valve_exhaust_open = False
def draw_caja():
    # Dibuja un pistón en la posición y
    # Dibuja la biela conectada al pistón
    screen.blit(caja_image, (80, 50))  # Cilindro
    pygame.draw.rect(screen, background_color, (365, 205, 70, 340))

def draw_piston_and_connecting_rod(piston_x, piston_y, circle_center_x, circle_center_y):
    # Dibuja un pistón en la posición (x, y)

    piston_background2 = pygame.transform.scale(piston_background, (100, 110))


    # pygame.draw.rect(screen, background_color, (piston_x + 10, piston_y + 10, 20, 10))

    # Dibuja la biela conectada al pistón
    piston_center = (piston_x + 20, piston_y + 70)
    pygame.draw.line(screen, connecting_rod_color, piston_center, (circle_center_x, circle_center_y), 10)
    pygame.draw.rect(screen, background_color, (370, piston_y, 60, 90))
    screen.blit(piston_background2, (350, piston_y))

    # Dibuja el círculo en la biela
    pygame.draw.circle(screen, (68, 70, 84) , (circle_center_x, circle_center_y), 10)
    pygame.draw.circle(screen, (205, 203, 204), (circle_center_x, circle_center_y),5)

def draw_valves():
    # Dibuja el cilindro con las válvulas de admisión y escape en las esquinas superiores
    pygame.draw.rect(screen, (144, 144, 144), (340, 200, 120, 350))  # Cilindro
    pygame.draw.rect(screen, (255,255,255), (345, 205, 110, 340))  # Interior del cilindro
    valvula_img2= pygame.transform.scale(valvula_img, (60, 90))

    # Dibuja un círculo estático dentro del cilindro
    circle_color = (0, 0, 0)  # Color del círculo
    circle_center = (400, 605)  # Posición del círculo
    circle_radius = 50  # Radio del círculo
    pygame.draw.circle(screen, (144, 144, 144) , circle_center, 100)
    pygame.draw.circle(screen, (110, 110, 110), circle_center, circle_radius)

    # Dibuja las válvulas de admisión en la esquina superior izquierda
    pygame.draw.circle(screen,(255,255,255) if valve_admission_open else background_color, (365, 205), 10)  # Válvula de admisión
    pygame.draw.circle(screen, (255,255,255) if valve_exhaust_open else background_color, (435, 205), 10) 
    # Dibuja las válvulas de escape en la esquina superior derecha
    if current_state==ADMISSION:
        screen.blit(valvula_img2, (335, 105))
    else:
        screen.blit(valvula_img2, (335, 120))
    if current_state==EXHAUST:
        screen.blit(valvula_img2, (405, 105))
    else:
        screen.blit(valvula_img2, (405, 120))
    
     # Válvula de escape
font = pygame.font.Font(None, 36)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(background_color)
    #draw_caja()
    # Actualiza el ángulo del cigüeñal
    crankshaft_angle += math.radians(piston_speed)
    if crankshaft_angle >= 2 * math.pi:
        crankshaft_angle = 0

    # Calcula la posición del pistón (movimiento vertical)
    piston_position_x = 380
    piston_position_y = 330 + 70 * math.sin(crankshaft_angle)  # Movimiento vertical

    # Calcula la posición del círculo de la biela
    circle_center_x = 400 + 50 * math.cos(crankshaft_angle)
    circle_center_y = 605 + 50 * math.sin(crankshaft_angle)

    # Dibuja las válvulas de admisión y escape
    draw_valves()
    #draw_caja()
    # Actualizar el estado del motor
    frame_count += 1.0
    if frame_count > state_duration:
        frame_count = 0
        valve_exhaust_open = False
        if current_state==COMBUSTION or current_state==COMPRESSION:
            valve_admission_open=False
        if current_state == ADMISSION:
            current_state = COMPRESSION
            valve_admission_open = False  # Cierra la válvula de admisión
            
        elif current_state == COMPRESSION:
            current_state = COMBUSTION
        elif current_state == COMBUSTION:
            current_state = EXHAUST
            # Abre la válvula de escape solo cuando el pistón está en su punto más bajo (punto muerto inferior)
            valve_admission_open = False  # Abre la válvula de admisión
            valve_exhaust_open = True  # Cierra la válvula de escape
        else:
            current_state = ADMISSION
    
    # Dibuja el pistón y la biela en los cilindros
    draw_piston_and_connecting_rod(piston_position_x, piston_position_y, circle_center_x, circle_center_y)
    
    text = font.render(f"Estado: {'Admisión' if current_state == ADMISSION else 'Compresión' if current_state == COMPRESSION else 'Combustión' if current_state == COMBUSTION else 'Escape'}", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (screen_width // 2, 20)
    particles = []

    if current_state == ADMISSION or current_state==COMPRESSION or current_state==COMBUSTION:
        # Abre la válvula de admisión
        valve_admission_open = True

        # Simula la entrada de aire y gasolina
        for _ in range(10):  # Agregar 10 partículas en cada ciclo de admisión
            # Generar partículas de diferentes colores para representar aire y gasolina
            particle_color = (0, 0, 255)  # Azul para aire
            if random.random() < 0.7:  # 70% de probabilidad de que sea gasolina
                particle_color = (255, 0, 0)  # Rojo para gasolina

            # Agregar una partícula en una posición aleatoria dentro del cilindro
            particle_x = 365 + random.randint(5, 65)
            particle_y = 205 + random.randint(5, 135)
            particles.append((particle_x, particle_y, particle_color))
    elif current_state == EXHAUST:
        # Cierra la válvula de admisión
        valve_admission_open = False

        # Eliminar las partículas que representan aire y gasolina
        particles = []

# Dibujar las partículas en el cilindro
    for particle in particles:
        particle_x, particle_y, particle_color = particle
        pygame.draw.circle(screen, particle_color, (particle_x, particle_y), 2)
    # Dibuja el texto en la ventana
    screen.blit(text, text_rect)
    
    pygame.display.update()

pygame.quit()
sys.exit()
