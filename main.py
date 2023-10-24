import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Animación de Motor de 4 Tiempos")

# Colores
white = (255, 255, 255)
black = (0, 0, 0)

# Posiciones de los pistones
piston_x = 400
top_piston_y = 300
bottom_piston_y = 450

# Velocidad de la animación
clock = pygame.time.Clock()

# Ciclo principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Lógica de animación (simulación de los tiempos del motor)
    # Aquí debes implementar la lógica para los tiempos de los pistones

    # Limpiar la pantalla
    screen.fill(white)

    # Dibuja los pistones (rectángulos)
    pygame.draw.rect(screen, black, (piston_x - 20, top_piston_y, 40, 10))  # Pistón superior
    pygame.draw.rect(screen, black, (piston_x - 20, bottom_piston_y, 40, 10))  # Pistón inferior

    # Actualizar la pantalla
    pygame.display.flip()

    # Control de velocidad
    clock.tick(60)

# Finalizar Pygame
pygame.quit()
sys.exit()
