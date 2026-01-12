from typing import List, Tuple, Dict
import json


def calculate_panels(panel_width: int, panel_height: int, 
                    roof_width: int, roof_height: int) -> int:
    
    # Implementa acá tu solución
    
    # Primero se revisa si el panel cabe dentro del techo
    if (panel_height > roof_height or panel_width > roof_width):
        return 0
    
    # El siguiente paso es ver el numero maximo de paneles que caben a
    # lo ancho o a lo alto para cada una de las opciones, vertical u horizontal
    
    # Para esto me baso en el ejemplo y uso la division entera en las 4 diferentes opciones
    # x//a, x//b, y//a, y//b (Notar que x//a <=> y//b and x//b <=> y/a)
    # Y luego entregar recursivamente para cada una de ellas la otra posicion, 
    # luego ver cual es la que da el numero mayor
    
    num_max_init = 0
    
    # Caso x//a
    max_x_a = roof_width // panel_width
    
    # Caso y//a
    max_y_a = roof_height // panel_width
    
    if (max_x_a >= max_y_a):
        num_max_init = max_x_a
        
        # Espacios sobrantes
        new_width = roof_width # Ya que el espacio sobrante en este caso si o si es a lo alto
        new_height = roof_height - panel_height
        
        # Se prueba con el panel en la otra posicion
        extra_horizontal_panels = calculate_panels(panel_height, panel_width, new_width, new_height)
        
        return num_max_init + extra_horizontal_panels
    
    else:
        num_max_init = max_y_a
        
        # Espacios sobrantes
        new_width = roof_width - panel_width
        new_height = roof_height # Ya que el espacio sobrante en este caso si o si es a lo largo
        
        extra_vertical_panels = calculate_panels(panel_height, panel_width, new_width, new_height)
        
        return num_max_init + extra_vertical_panels
    
    return 0




def calculate_panels_triangular_rectangular(panel_width: int, panel_height: int, 
                    roof_width: int, roof_height: int) -> int:
    
    # Explicacion de las variables en el readme
    
    rec_insc_width = roof_width // 2
    rec_insc_height = roof_height // 2
    
    # Se revisa si el panel cabe dentro del maximo rectangulo inscrito
    if (panel_height > roof_height or panel_width > roof_width):
        return 0
    
    # Obtener la mayor cantidad de paneles en el mayor rectangulo inscrito
    max_rec_insc = calculate_panels(panel_width, panel_height, rec_insc_width, rec_insc_height)
    
    # A diferencia de la funcion con triangulo isoceles, en este caso el resultado de extraer el rectangulo inscrito, 
    # da como resultado 2 triangulos rectangulos restantes equivalentes en medidas, por tanto se duplica la recursion 
    
    triangle_recursive = 2 * calculate_panels_triangular_rectangular(panel_width, panel_height, rec_insc_width / 2, rec_insc_height)
    
    return max_rec_insc + triangle_recursive




def calculate_panels_triangular_isoceles(panel_width: int, panel_height: int, 
                    roof_width: int, roof_height: int) -> int:

    # Para resolver este problema se me ocurrio hacer recursion con el problema anterior
    # Para eso necesito encontrar el mayor rectangulo inscrito en el triangulo, y luego
    # hacer lo mismo para los triangulos resultantes de extraer el primer rectangulo
    
    # Explicacion de las variables en el readme
    
    rec_insc_width = roof_width // 2
    rec_insc_height = roof_height // 2
    
    # Se revisa si el panel cabe dentro del maximo rectangulo inscrito
    if (panel_height > roof_height or panel_width > roof_width):
        return 0
    
    # Obtener la mayor cantidad de paneles en el mayor rectangulo inscrito
    max_rec_insc = calculate_panels(panel_width, panel_height, rec_insc_width, rec_insc_height)
    
    # Luego se revisa recursivamente a los 3 triangulos resultantes de extraer el maximo rectangulo incrito
    # Ojo que dos de estos triangulos son triangulos rectangulos y otro triangulo isoceles
    # Por tanto se revisa hacia un lado y luego se duplica el resultado
    # Esto para evitar tener que hacer un caso particular para el triangulo isoceles,
    # y de esta forma tratar a todos como triangulos rectangulos
    
    triangles_rectangles = 2 * calculate_panels_triangular_rectangular(panel_width, panel_height, rec_insc_width / 2, rec_insc_height)
    
    # La base es el ancho del rectangulo inscrito 
    triangle_isoceles = calculate_panels_triangular_isoceles(panel_width, panel_height, rec_insc_width, rec_insc_height)
    
    return max_rec_insc + triangles_rectangles + triangle_isoceles




# Dado a que se puede parametrizar el area overlapeada, se le dara un ancho y largo 
def calculate_panels_double_rectangle(panel_width: int, panel_height: int, 
                    roof_width: int, roof_height: int,
                    overlap_width: int, overlap_height: int) -> int:
    
    # En este caso conviene dividir la geometria en 3 rectangulos y cada uno de ellos tratarlos de manera individual
    
    # Nuevamente explicacion en el readme de como es cada rectangulo y sus dimensiones
    
    rectangle_1_3 = 2 * calculate_panels(panel_width, panel_height, roof_width - overlap_width, roof_height)
    rectangle_2 = calculate_panels(panel_width, panel_height, overlap_width, 2 * roof_height - overlap_height)
    
    return rectangle_1_3 + rectangle_2



def run_tests() -> None:
    with open('test_cases.json', 'r') as f:
        data = json.load(f)
        test_cases: List[Dict[str, int]] = [
            {
                "panel_w": test["panelW"],
                "panel_h": test["panelH"],
                "roof_w": test["roofW"],
                "roof_h": test["roofH"],
                "expected": test["expected"]
            }
            for test in data["testCases"]
        ]
    
    print("Corriendo tests:")
    print("-------------------")
    
    for i, test in enumerate(test_cases, 1):
        result = calculate_panels(
            test["panel_w"], test["panel_h"], 
            test["roof_w"], test["roof_h"]
        )
        passed = result == test["expected"]
        
        print(f"Test {i}:")
        print(f"  Panels: {test['panel_w']}x{test['panel_h']}, "
                f"Roof: {test['roof_w']}x{test['roof_h']}")
        print(f"  Expected: {test['expected']}, Got: {result}")
        print(f"  Status: {'✅ PASSED' if passed else '❌ FAILED'}\n")


def main() -> None:
    print("🐕 Wuuf wuuf wuuf 🐕")
    print("================================\n")
    
    run_tests()


if __name__ == "__main__":
    main()
