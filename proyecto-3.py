import yaml

class TuringMachine:
    def __init__(self, tm_data):
        self.states = tm_data['q_states']['q_list']
        self.initial_state = tm_data['q_states']['initial']
        self.final_states = [tm_data['q_states']['final']]
        self.alphabet = tm_data['alphabet']
        self.tape_alphabet = tm_data['tape_alphabet']
        self.blank_symbol = ''
        self.delta_function = self.build_delta_function(tm_data['delta'])
        self.simulation_strings = tm_data['simulation_strings']

    def build_delta_function(self, delta_list):
        delta_function = {}
        for transition in delta_list:
            params = transition['params']
            output = transition['output']
            key = (params['initial_state'], params['tape_input'])
            value = (output['final_state'], output['tape_output'], output['tape_displacement'])
            delta_function[key] = value
        return delta_function

    def simulate(self, input_string):
        tape = list(input_string)
        head_position = 0
        current_state = self.initial_state
        step = 0

        print(f"\nSimulación de la cadena: {input_string}")
        self.print_configuration(step, current_state, tape, head_position)

        while True:
            # Leer el símbolo actual de la cinta
            if head_position < 0:
                # Si el cabezal está en una posición negativa, extender la cinta a la izquierda
                tape.insert(0, self.blank_symbol)
                head_position = 0
            elif head_position >= len(tape):
                # Extender la cinta con el símbolo en blanco si es necesario
                tape.append(self.blank_symbol)

            tape_symbol = tape[head_position]

            # Obtener la transición
            key = (current_state, tape_symbol)
            if key in self.delta_function:
                next_state, tape_output, move_direction = self.delta_function[key]
                # Escribir en la cinta
                tape[head_position] = tape_output

                # Mover el cabezal
                if move_direction == 'R':
                    head_position += 1
                elif move_direction == 'L':
                    head_position -= 1
                elif move_direction == 'S':
                    pass  # No se mueve el cabezal
                else:
                    print(f"Dirección de movimiento inválida: {move_direction}")
                    break

                # Actualizar el estado actual
                current_state = next_state

                # Mostrar la descripción instantánea
                step += 1
                self.print_configuration(step, current_state, tape, head_position)
            else:
                # No hay transición válida, la máquina se detiene
                if current_state in self.final_states:
                    print("Cadena aceptada.\n")
                    return True
                else:
                    print("Cadena rechazada.\n")
                    return False

            # Verificar si se alcanza un estado de aceptación
            if current_state in self.final_states:
                print("Cadena aceptada.\n")
                return True

    def print_configuration(self, step, state, tape, head_position):
        tape_str = ''.join(tape).rstrip(self.blank_symbol)
        # Calcular el indicador del cabezal
        if head_position >= 0:
            head_indicator = ' ' * head_position + '^'
        else:
            head_indicator = '^' + ' ' * (len(tape_str) - 1)
        print(f"Paso {step}: Estado={state}")
        print(f"Cinta: {tape_str}")
        print(f"       {head_indicator}\n")

# Crear la máquina de Turing reconocedora
with open('estructura-mt.yaml', 'r') as file:
    tm_data = yaml.safe_load(file)
tm = TuringMachine(tm_data)
# Simular la MT reconocedora sobre cada cadena de entrada
for input_string in tm.simulation_strings:
    tm.simulate(input_string)

# Crear la máquina de Turing alteradora
with open('alteradora-mt.yaml', 'r') as file:
    tm_data = yaml.safe_load(file)
tm = TuringMachine(tm_data)
# Simular la MT alteradora sobre cada cadena de entrada
for input_string in tm.simulation_strings:
    tm.simulate(input_string)