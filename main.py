"""Punto de entrada principal para KidsLab.
import l
Este módulo inicializa el motor de Pygame y gestiona el bucle principal
de la aplicación de forma asíncrona para permitir la compilación a
WebAssembly (WASM) mediante pygbag.
"""

import asyncio
import sys
import logging
from typing import Final

import pygame

# Importaciones locales (simuladas para la arquitectura)
# from src.config import SCREEN_SIZE, FPS, BG_COLOR
# from src.screens import ScreenManager

# Constantes de configuración global de respaldo
SCREEN_WIDTH: Final[int] = 800
SCREEN_HEIGHT: Final[int] = 600
FPS: Final[int] = 60
C64_BLACK: Final[tuple[int, int, int]] = (0, 0, 0)


def procesar_eventos() -> bool:
    """Gestiona la cola de eventos de Pygame.

    Utiliza el patrón de retorno temprano (Early Return) para evaluar el evento
    de salida inmediatamente y evitar la anidación de condicionales.

    Returns:
        bool: Retorna True si la aplicación debe continuar, False si se solicita salir.
    """
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return False
            
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            return False

    return True


async def main() -> None:
    """Bucle principal asíncrono de la aplicación.

    La naturaleza asíncrona de esta función es mandatoria para pygbag.
    El uso de 'await asyncio.sleep(0)' cede el control al bucle de eventos
    del navegador web, previniendo que la pestaña se congele en la ejecución WASM.
    """
  pygame.init()
    
    # Patrón de Degradación Elegante para entornos sin hardware de audio (ej. Codespaces)
    try:
        pygame.mixer.init()
    except pygame.error as e:
        import logging
        logging.warning(f"Audio no disponible ({e}). Ejecutando en modo silencioso.")

    pantalla: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("🧪 KidsLab · Oracle Kids")
    
    reloj: pygame.time.Clock = pygame.time.Clock()
    esta_corriendo: bool = True

    while esta_corriendo:
        # 1. Gestión de Entradas (Input)
        esta_corriendo = procesar_eventos()
        if not esta_corriendo:
            break

        # 2. Actualización de Estado (Update)
        # Aquí se gestionará el cambio de pantallas en el futuro
        
        # 3. Renderizado (Render)
        pantalla.fill(C64_BLACK)
        
        # Omitimos lógica pesada de dibujo directamente aquí para mantener
        # alta cohesión y bajo acoplamiento arquitectónico.
        
        pygame.display.flip()
        
        # 4. Control de Framerate y Sincronización Web
        reloj.tick(FPS)
        # Línea crítica para pygbag: cede tiempo de ejecución al navegador
        await asyncio.sleep(0)

    pygame.mixer.quit()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    # Inicialización del entorno asíncrono estándar de Python
    asyncio.run(main())
