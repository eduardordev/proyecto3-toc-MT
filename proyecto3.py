import yaml  # Importamos la librería yaml para manejar archivos YAML
import sys

class TuringMachine:
    def __init__(self, config):
        # Inicializamos la Máquina de Turing con la configuración proporcionada
        self.q_states = config['q_states']['q_list']  # Lista de estados
        self.initial_state = config['q_states']['initial']  # Estado inicial
        self.final_states = config['q_states']['final'] if isinstance(config['q_states']['final'], list) else [config['q_states']['final']]
        self.alphabet = config['alphabet']  # Alfabeto de entrada
        self.tape_alphabet = config['tape_alphabet']  # Alfabeto de la cinta
        self.blank_symbol = ''  # Símbolo en blanco
        # Construimos la función de transición a partir de la configuración
        self.delta = self.build_transition_function(config['delta'])
        self.simulation_strings = config['simulation_strings']  # Cadenas para simular

    def build_transition_function(self, delta_list):
        # Construye la función de transición a partir de la lista de transiciones
        transition_function = {}
        for transition in delta_list:
            params = transition['params']
            output = transition['output']

            # Extraemos los parámetros necesarios
            initial_state = params['initial_state']  # Estado inicial de la transición
            mem_cache_value = params.get('mem_cache_value')
            if mem_cache_value is None:
                mem_cache_value = self.blank_symbol
            tape_input = params.get('tape_input')
            if tape_input is None:
                tape_input = self.blank_symbol

            # Creamos las llave para la función de transición
            key = (initial_state, mem_cache_value, tape_input)

            # Extraemos los valores de salida de la transición
            final_state = output['final_state'] 
            output_mem_cache_value = output.get('mem_cache_value')
            if output_mem_cache_value is None:
                output_mem_cache_value = self.blank_symbol
            tape_output = output.get('tape_output')
            if tape_output is None:
                tape_output = self.blank_symbol
            tape_displacement = output['tape_displacement']  # Movimiento del cabezal ('R', 'L', 'S')

            # Creamos el valor para la función de transición
            value = (final_state, output_mem_cache_value, tape_output, tape_displacement)
            transition_function[key] = value
        return transition_function

    def simulate(self):
        # Simula la máquina de Turing para cada cadena
        for input_string in self.simulation_strings:
            print(f"\nSimulando entrada: {input_string}")
            result = self.run_machine(input_string)
            print(f"Resultado: {'Aceptada' if result else 'Rechazada'} {input_string}\n{'-'*50}")

    def run_machine(self, input_string):
        # Ejecuta la máquina de Turing para una cadena de entrada específica
        tape = list(input_string)  # Inicializamos la cinta como una lista de símbolos
        head_position = 0  # Posición inicial del cabezal en la cinta
        current_state = self.initial_state  # Estado actual de la máquina
        mem_cache = self.blank_symbol  # Valor inicial de la memoria interna
        step = 0  # Contador de pasos ejecutados
        tape.extend([self.blank_symbol] * 100)

        while True:
            tape_symbol = tape[head_position]  # Leemos el símbolo actual en la cinta

            # Creamos la llave para buscar en la función de transición
            key = (current_state, mem_cache, tape_symbol)

            # Imprimimos la descripción instantánea de la máquina
            self.print_instantaneous_description(tape, head_position, current_state, mem_cache, step)

            if current_state in self.final_states:
                # Si estamos en un estado de aceptación, retornamos True (cadena aceptada)
                return True

            if key not in self.delta:
                # Si no hay transición definida, retornamos False (cadena rechazada)
                return False

            # Obtenemos la transición correspondiente
            (new_state, new_mem_cache, new_tape_symbol, movement) = self.delta[key]

            tape[head_position] = new_tape_symbol  # Escribimos el nuevo símbolo en la cinta
            mem_cache = new_mem_cache  # Actualizamos el valor en memoria

            # Movemos el cabezal según el desplazamiento especificado
            if movement == 'R':
                head_position += 1  # Mover a la derecha
            elif movement == 'L':
                head_position -= 1  # Mover a la izquierda
            elif movement == 'S':
                pass  # No se mueve el cabezal

            current_state = new_state  # Actualizamos el estado actual
            step += 1  # Incrementamos el contador de pasos

    def print_instantaneous_description(self, tape, head_position, current_state, mem_cache, step):
        # Imprime el estado actual de la máquina en cada paso
        tape_str = ''.join([symbol if symbol != self.blank_symbol else '' for symbol in tape[:50]])  # Convertimos la cinta a una cadena
        head_str = ' ' * head_position + '^'  # Indicamos la posición del cabezal
        print(f"Paso {step}:")
        print(f"Estado: {current_state}, Memoria: {mem_cache if mem_cache != self.blank_symbol else ''}")
        print(f"Cinta: {tape_str}")
        print(f"       {head_str}\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)

    config_file = sys.argv[1]

    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)

    tm = TuringMachine(config)  # Creamos una instancia de la Máquina de Turing con la configuración
    tm.simulate()  # Ejecutamos la simulación
