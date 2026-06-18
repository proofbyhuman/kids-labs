"""Motor lógico para el minijuego HakerBox (Math Quest).

Gestiona la generación procedural de ecuaciones matemáticas, validación de
respuestas y progresión de niveles (cofres). Diseñado con baja dependencia
gráfica para facilitar su testeo unitario y portabilidad.
"""

import random
from typing import Final, Tuple, Optional

# Constantes de configuración global de dificultad
OPERADORES_NIVEL_1: Final[Tuple[str, ...]] = ("+", "-")
OPERADORES_NIVEL_2: Final[Tuple[str, ...]] = ("+", "-", "*")
MAX_COFRES_POR_NIVEL: Final[int] = 3


class HakerBoxEngine:
    """Núcleo lógico de HakerBox.
    
    Mantiene el estado de la partida (nivel, cofres) y genera
    los desafíos de forma dinámica según la progresión del jugador.
    """

    def __init__(self, nivel_inicial: int = 1) -> None:
        """Inicializa el estado del motor. 
        Evitamos argumentos mutables por defecto usando int estáticos."""
        self.nivel_actual: int = nivel_inicial
        self.cofres_abiertos: int = 0
        self.pregunta_actual: str = ""
        self.respuesta_correcta: int = 0
        
        # Generar la primera ecuación al instanciar
        self.generar_nueva_ecuacion()

    def generar_nueva_ecuacion(self) -> None:
        """Genera un problema matemático acorde al nivel actual.
        
        El por qué: Ajustamos los rangos numéricos y operadores basándonos en el
        nivel para mantener una curva de dificultad progresiva que no frustre al jugador.
        """
        operadores = OPERADORES_NIVEL_2 if self.nivel_actual >= 3 else OPERADORES_NIVEL_1
        operador = random.choice(operadores)
        
        # Escalar dificultad multiplicando el nivel actual
        rango_max = 5 + (self.nivel_actual * 5)
        
        num1: int = random.randint(1, rango_max)
        num2: int = random.randint(1, rango_max)

        # Prevenir resultados negativos en restas para niños pequeños
        if operador == "-" and num1 < num2:
            num1, num2 = num2, num1

        self.pregunta_actual = f"{num1} {operador} {num2} = ?"
        
        # Calcular respuesta correcta explícitamente sin usar la función eval()
        if operador == "+":
            self.respuesta_correcta = num1 + num2
        elif operador == "-":
            self.respuesta_correcta = num1 - num2
        elif operador == "*":
            # Limitar la dificultad de las multiplicaciones a las tablas del 2 al 9
            num1 = random.randint(2, 9)
            num2 = random.randint(2, 9)
            self.pregunta_actual = f"{num1} * {num2} = ?"
            self.respuesta_correcta = num1 * num2

    def validar_respuesta(self, respuesta_usuario: Optional[str]) -> bool:
        """Valida la entrada del usuario y avanza el estado del juego.
        
        Aplica Early Return para rechazar entradas inválidas inmediatamente
        y evitar anidación profunda en la lógica de resolución.
        """
        # 1. Early Return: Entrada nula, vacía o solo espacios
        if not respuesta_usuario or not respuesta_usuario.strip():
            return False
            
        # 2. Early Return: Entrada con caracteres no numéricos (letras, símbolos)
        if not respuesta_usuario.isdigit():
            return False
            
        valor_entero: int = int(respuesta_usuario)
        
        # 3. Early Return: Respuesta matemática incorrecta
        if valor_entero != self.respuesta_correcta:
            return False
            
        # Camino feliz (Happy Path): La respuesta es correcta
        self._avanzar_progreso()
        return True

    def _avanzar_progreso(self) -> None:
        """Maneja la lógica interna de progresión tras un acierto."""
        self.cofres_abiertos += 1
        
        # Subir de nivel si se completan los cofres requeridos
        if self.cofres_abiertos >= MAX_COFRES_POR_NIVEL:
            self.nivel_actual += 1
            self.cofres_abiertos = 0
            
        # Preparar el siguiente desafío
        self.generar_nueva_ecuacion()
        