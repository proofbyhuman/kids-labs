"""Punto de entrada principal para KidsLab.

Gestiona el bucle asíncrono y aplica degradación elegante para hardware ausente.
"""

import asyncio
import logging
import sys
from typing import Final

import pygame

SCREEN_WIDTH: Final[int] = 800
SCREEN_HEIGHT: Final[int] = 600
FPS: Final[int] = 60
C64_BLACK: Final[tuple[int, int, int]] = (0, 0, 0)


def procesar_eventos() -> bool:
    """Procesa la entrada del usuario usando Early Return."""
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return False
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            return False
    return True


async def main() -> None:
    """Bucle principal asíncrono compatible con WASM/Pygbag."""
    pygame.init()
    
    # Degradación Elegante: Previene crasheos en la nube sin hardware de audio
    try:
        pygame.mixer.init()
    except pygame.error as e:
        logging.warning(f"Hardware de audio no detectado ({e}). Modo silencioso activado.")

    # Inicialización de pantalla
    pantalla: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("🧪 KidsLab · Oracle Kids")
    
    reloj: pygame.time.Clock = pygame.time.Clock()
    esta_corriendo: bool = True

    while esta_corriendo:
        esta_corriendo = procesar_eventos()
        if not esta_corriendo:
            break

        pantalla.fill(C64_BLACK)
        pygame.display.flip()
        
        reloj.tick(FPS)
        await asyncio.sleep(0)

    # Limpieza de recursos al salir
    if pygame.mixer.get_init():
        pygame.mixer.quit()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    # Configuración del nivel de logging para ver las advertencias en terminal
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())