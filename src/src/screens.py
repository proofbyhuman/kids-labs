"""Gestor de pantallas visuales para KidsLab.

Contiene la interfaz de usuario (UI) para HakerBox, conectando el motor lógico
con el renderizado de Pygame utilizando una estética de terminal retro.
"""

from typing import Final
import pygame

from src.haker_box import HakerBoxEngine

# Constantes de paleta de colores retro C64
C64_GREEN: Final[tuple[int, int, int]] = (53, 209, 53)
C64_BLACK: Final[tuple[int, int, int]] = (0, 0, 0)
WHITE: Final[tuple[int, int, int]] = (255, 255, 255)


class HakerBoxScreen:
    """Pantalla interactiva para el minijuego de matemáticas.
    
    Se encarga exclusivamente de capturar el input del teclado (teclas numéricas)
    y de dibujar el estado actual dictado por el HakerBoxEngine.
    """

    def __init__(self, screen: pygame.Surface) -> None:
        """Inicializa la pantalla inyectando la superficie principal de Pygame."""
        self.screen: pygame.Surface = screen
        self.engine: HakerBoxEngine = HakerBoxEngine()
        
        # Tipografías por defecto (idealmente luego se reemplazarán por fuentes retro de assets/)
        self.font_grande: pygame.font.Font = pygame.font.Font(None, 72)
        self.font_chica: pygame.font.Font = pygame.font.Font(None, 36)
        
        self.input_usuario: str = ""
        self.mensaje_estado: str = "INGRESA TU RESPUESTA Y PRESIONA ENTER"

    def procesar_evento(self, evento: pygame.event.Event) -> None:
        """Procesa las pulsaciones de teclado del jugador.
        
        Se utiliza Early Return extensivamente para descartar eventos irrelevantes
        y mantener el flujo de lectura lineal.
        """
        # 1. Early Return: Solo nos interesan las teclas presionadas
        if evento.type != pygame.KEYDOWN:
            return

        # 2. Early Return: Tecla de borrado (Backspace)
        if evento.key == pygame.K_BACKSPACE:
            self.input_usuario = self.input_usuario[:-1]
            return

        # 3. Early Return: Confirmar respuesta (Enter)
        if evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            self._validar_input()
            return

        # 4. Acumular entrada solo si es un número válido y no supera 3 dígitos
        if evento.unicode.isdigit() and len(self.input_usuario) < 3:
            self.input_usuario += evento.unicode

    def _validar_input(self) -> None:
        """Comunica la entrada del usuario al motor lógico y actualiza la UI."""
        # Early return si el usuario presiona Enter sin escribir nada
        if not self.input_usuario:
            return

        es_correcto: bool = self.engine.validar_respuesta(self.input_usuario)
        
        if es_correcto:
            self.mensaje_estado = "¡ACCESO CONCEDIDO! GENERANDO NUEVO COFRE..."
        else:
            self.mensaje_estado = "ERROR: RESPUESTA INCORRECTA. INTENTA DE NUEVO."
            
        # Limpiar la entrada del usuario para el siguiente intento
        self.input_usuario = ""

    def renderizar(self) -> None:
        """Dibuja todos los elementos en la pantalla."""
        self.screen.fill(C64_BLACK)
        
        # 1. Renderizar Cabecera / HUD
        texto_hud: str = f"NIVEL: {self.engine.nivel_actual}  |  COFRES: {self.engine.cofres_abiertos}/3"
        superficie_hud: pygame.Surface = self.font_chica.render(texto_hud, True, C64_GREEN)
        self.screen.blit(superficie_hud, (20, 20))
        
        # 2. Renderizar Pregunta Matemática
        superficie_pregunta: pygame.Surface = self.font_grande.render(self.engine.pregunta_actual, True, WHITE)
        self.screen.blit(superficie_pregunta, (int(self.screen.get_width() / 2 - superficie_pregunta.get_width() / 2), 200))
        
        # 3. Renderizar Input del Usuario (con cursor parpadeante simulado)
        texto_input: str = f"> {self.input_usuario}_"
        superficie_input: pygame.Surface = self.font_grande.render(texto_input, True, C64_GREEN)
        self.screen.blit(superficie_input, (int(self.screen.get_width() / 2 - superficie_input.get_width() / 2), 300))
        
        # 4. Renderizar Mensaje de Estado
        superficie_estado: pygame.Surface = self.font_chica.render(self.mensaje_estado, True, C64_GREEN)
        self.screen.blit(superficie_estado, (int(self.screen.get_width() / 2 - superficie_estado.get_width() / 2), 500))
        