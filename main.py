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
    if angulo_ciguenal <= math.pi:
        inclinacion_maxima = (angulo_ciguenal / math.pi) * 12  # Aumenta la inclinación hacia la izquierda
    else:
        inclinacion_maxima = (2 * math.pi - angulo_ciguenal) / math.pi * 12  # Aumenta la inclinación hacia la derecha
    return inclinacion_maxima
def draw_cilindro(x, y, crankshaft_angle):
    amplitud_x = 50
    amplitud_y = 25
    velocidad_inclinacion = 1.4  # Ajusta la velocidad de cambio de inclinación

    # Calcula la inclinación en función del ángulo del cigüeñal
    if crankshaft_angle <= math.pi:
        x_cilindro = 0  # En el punto muerto superior
        y_cilindro = -amplitud_y * math.sin(crankshaft_angle)
        inclinacion_maxima = (crankshaft_angle / math.pi) * 10  # Aumenta la inclinación hacia la izquierda
    else:
        x_cilindro = 0  # No hay movimiento horizontal
        y_cilindro = -amplitud_y * math.sin(crankshaft_angle)
        inclinacion_maxima = (2 * math.pi - crankshaft_angle) / math.pi * 10  # Aumenta la inclinación hacia la derecha

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
    amplitud_y = 45  # Ajusta la amplitud vertical según tus necesidades
    

    # Calcula la posición vertical del pistón en función del ángulo del cigüeñal
    if head_angle <= math.pi:
        y_piston = amplitud_y * math.sin(head_angle)
    else:
        y_piston = -amplitud_y * math.sin(head_angle)

    screen.blit(piston_image, (560, 295 + y_piston))
    pygame.draw.rect(screen, background_color, (365, 205, 70, 340))
#cigueñal    
def draw_polea():
    screen.blit(polea_image, (575, 510))  # Cilindro
    pygame.draw.rect(screen, background_color, (365, 205, 70, 340))
def draw_polea_rotating(polea_image, polea_angle):
   # Obtiene el rectángulo que rodea la imagen de la polea
    polea_rect = polea_image.get_rect()
    
    # Calcula el centro de la polea
    polea_center = polea_rect.center
    
    # Rota la imagen de la polea alrededor de su centro
    polea_rotated = pygame.transform.rotate(polea_image, polea_angle)
    
    # Obtén el nuevo rectángulo que rodea la imagen rotada
    polea_rotated_rect = polea_rotated.get_rect()
    
    # Establece el centro del rectángulo rotado en el centro original
    polea_rotated_rect.center = polea_center
    
    # Dibuja la polea girando en su propio eje
    screen.blit(polea_rotated, polea_rotated_rect) 
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
amplitude = 20  # Amplitud del movimiento (cambia según tus necesidades)
frequency = 0.05  # Frecuencia de oscilación (cambia según tus necesidades)
time = 0
polea_angle = 0
crankshaft_angle = 0
piston_speed = 0.68  # Velocidad de movimiento del pistón más lenta
cabeza_speed= 1.4
crankshaft_length = 100
piston_length = 100
amplitude_cuerpo = 20  # Amplitud de movimiento del cuerpo
frequency_cuerpo = 0.05  # Frecuencia de oscilación del cuerpo
amplitude_cabeza = 40  # Amplitud de movimiento de la cabeza del pistón
frequency_cabeza = 0.05  
angle = math.pi / 4  # Ángulo inicial (45 grados)
angular_velocity = 0.1
head_angle= 0
running = True
head_pause = False
pause_time = 0
permitir_movimiento_cuerpo = True
clock = pygame.time.Clock()
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(background_color)
    
    time += 1
    
    cuerpo_position_y = 300 + amplitude_cuerpo * math.sin(frequency_cuerpo * angle)
    cabeza_position_y = 300 + amplitude_cabeza * math.sin(frequency_cabeza * angle)
    
    if permitir_movimiento_cuerpo and cuerpo_position_y <= 350:
        permitir_movimiento_cuerpo = False

    if not permitir_movimiento_cuerpo:
        # Cuando el cuerpo del pistón ha alcanzado su posición más alta, permite el movimiento de la cabeza
        cabeza_position_y = 350 - amplitude_cabeza * math.sin(frequency_cabeza * angle)

    piston_position = 300 - crankshaft_length * math.sin(crankshaft_angle)
    angle += angular_velocity
    
    piston_position_x = 560 + 50 * math.sin(angle)

    # Actualiza el ángulo del cigüeñal
    crankshaft_angle += math.radians(piston_speed)
    head_angle += math.radians(piston_speed)
    
    if head_angle >= 2 * math.pi:
        head_angle = 0
    
    if crankshaft_angle >= 2 * math.pi:
        crankshaft_angle = 0
    cuerpo_position_y = 300 + amplitude_cuerpo * math.sin(frequency_cuerpo * angle)
    cabeza_position_y = 300 + amplitude_cabeza * math.sin(frequency_cabeza * angle)    
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
    
    polea_angle += 0.02
    draw_valves()
    draw_cuerpo()
    crankshaft_angle=draw_cilindro(520, 350,crankshaft_angle)
    # Velocidad de rotación de la polea (ajusta según tus necesidades)
    draw_polea_rotating(polea_image, polea_angle)
    draw_piston()
    valvula_der()
    valvula_izq()
    
    pygame.display.update()
    clock.tick(60)
pygame.quit()
sys.exit()