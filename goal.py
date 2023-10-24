import pygame
import sys

pygame.init()

# Configuración de la pantalla
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Motor de 4 tiempos")

# Carga de las imágenes
piston_image = pygame.image.load('piston.png')
cylinder_image = pygame.image.load('cilindro.png')
cuerpo_image = pygame.image.load('cuerpo.png')

new_width = 200  # Ancho deseado
new_height = 200  # Alto deseado

piston_image = pygame.transform.scale(piston_image, (new_width, new_height))
cylinder_image = pygame.transform.scale(cylinder_image, (new_width, new_height))
cuerpo_image = pygame.transform.scale(cuerpo_image, (new_width, new_height))

# Inicialización del motor
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((255, 255, 255))

    # Dibuja las imágenes en la pantalla
    screen.blit(piston_image, (100, 100))  # Ejemplo de ubicación
    screen.blit(cylinder_image, (300, 100))  # Ejemplo de ubicación
    screen.blit(cuerpo_image, (500, 100))  # Ejemplo de ubicación

    
    pygame.display.update()

pygame.quit()
sys.exit()