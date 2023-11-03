import pygame, sys
from pygame.locals import *
from funciones import *
from config import *
from sound import *

pygame.init()

# configuro fuente del contador de monedas
score = 0
font = pygame.font.Font(None, 50) # fuente del texto
text_score = font.render(f"Level: 1   Score : {score}", True, CYAN)
text_rect = text_score.get_rect()

# Lista para almacenar las posiciones de los segmentos de la serpiente
snake_segments = [get_rectangulo(x, y, rect_width, rect_height, GREEN)]

# Inicializa la posición de los segmentos de la serpiente
for _ in range(snake_length - 1):
    snake_segments.append(get_rectangulo(x, y, rect_width, rect_height, GREEN))
    x += rect_width   # Aumenta la posición en X para el próximo segmento
 

count_comer = 0
coin_dict = {
    "x" : 300,
    "y" : 300
    }


# Bucle principal
run = True
clock = pygame.time.Clock()

while run:
    sound.play()
    #detectar los eventos
    for event in pygame.event.get():
                
        if event.type == QUIT:  #Evento de cierre de ventana del juego
            run = False
        keys = pygame.key.get_pressed()
        if keys[K_UP] and snake_direction != 1:
            snake_direction = 0  # Cambia la dirección hacia arriba
        elif keys[K_DOWN] and snake_direction != 0:
            snake_direction = 1  # Cambia la dirección hacia abajo
        elif keys[K_LEFT] and snake_direction != 3:
            snake_direction = 2  # Cambia la dirección hacia la izquierda
        elif keys[K_RIGHT] and snake_direction != 2:
            snake_direction = 3

    # Obtén la cabeza de la serpiente
    
    snake_head = snake_segments[0]["rect"]

 # Actualiza la posición de la serpiente
    if snake_direction == 0:
        new_head = {
            "rect": pygame.Rect(
                snake_segments[0]["rect"].left,
                snake_segments[0]["rect"].top - (snake_speed + segment_spacing),
                rect_width,
                rect_height,
            ),
            "dir": snake_direction,
        }
    elif snake_direction == 1:
        new_head = {
            "rect": pygame.Rect(
                snake_segments[0]["rect"].left,
                snake_segments[0]["rect"].top + (snake_speed + segment_spacing),
                rect_width,
                rect_height,
            ),
            "dir": snake_direction,
        }
    elif snake_direction == 2:
        new_head = {
            "rect": pygame.Rect(
                snake_segments[0]["rect"].left - (snake_speed + segment_spacing),
                snake_segments[0]["rect"].top,
                rect_width,
                rect_height,
            ),
            "dir": snake_direction,
        }
    elif snake_direction == 3:
        new_head = {
            "rect": pygame.Rect(
                snake_segments[0]["rect"].left + (snake_speed + segment_spacing),
                snake_segments[0]["rect"].top,
                rect_width,
                rect_height,
            ),
            "dir": snake_direction,
        }
    snake_segments[0] = new_head 
    
    # Verificar colisión con la pared

    if (
        new_head["rect"].left < 0
        or new_head["rect"].right > WIDTH
        or new_head["rect"].top < 0
        or new_head["rect"].bottom > HEIGHT
    ):
        run = False
    
    coin_rect = pygame.Rect(coin_dict['x'], coin_dict['y'], 25, 25)  # Rectángulo de la moneda actual

    if ( colision_2_rect(coin_rect,new_head["rect"])):

        score += 1
        text_score = font.render(f"Level:  1  Score = {score}", True, CYAN)
        coin_dict['x'] = random.randint(0, WIDTH - 25)  # Mueve la moneda a una nueva ubicación
        coin_dict['y'] = random.randint(0, HEIGHT - 25)  # Mueve la moneda a una nueva ubicación
        snake_length += 1  # Aumenta la longitud de la serpiente
    
    current_time = pygame.time.get_ticks()
   
    if current_time > colision:
        for segment in snake_segments[1:]:  # Comenzamos desde el segundo segmento ya que la cabeza no puede chocar consigo misma
            if colision_2_rect(segment["rect"], snake_segments[0]["rect"]):
                run = False
                break

    
    # Agrega el nuevo segmento de cabeza
    
    snake_segments.insert(0, {"rect": pygame.Rect(new_head["rect"]), "dir": snake_direction})

    # Elimina el último segmento de la serpiente
    
    if len(snake_segments) > snake_length:
        del snake_segments[-1]
    
    text_rect.center = (WIDTH // 2, 15) 
    
    #screen.fill(BLACK)
    screen.blit(wallpaper, (0, 0))

    for segment in snake_segments:
        pygame.draw.rect(screen, GREEN, segment["rect"], 0)
    
    screen.blit(text_score, text_rect)
    
    screen.blit(coin_images, (coin_dict['x'], coin_dict['y'])) # dibuja los coins
    
    # Dibuja la serpiente
    for i, segment in enumerate(snake_segments):
        if i == 0:
            # Dibuja la cabeza de la serpiente
            screen.blit(cabeza_imagen, segment["rect"])
     
    pygame.display.flip()
    clock.tick(10)

    
pygame.quit()
sys.exit()