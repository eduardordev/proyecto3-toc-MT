import yaml

class TuringMachine:
    def __init__(self, config):
        self.states = config['q_states']['q_list']
        self.initial_state = config['q_states']['initial']
        self.final_states = [config['q_states']['final']]
        self.current_state = self.initial_state
        self.transitions = config['delta']
        self.tape_alphabet = config['tape_alphabet']
        self.tape = []
        self.head_position = 0

    def load_tape(self, input_string):
        self.tape = list(input_string) + ['_']  # Añade espacio en blanco al final
        self.head_position = 0

    def step(self):
        if self.head_position < 0 or self.head_position >= len(self.tape):
            self.tape.append('_')  # Expande la cinta si el cabezal se sale de los límites

        current_symbol = self.tape[self.head_position]
        transition_found = False

        for transition in self.transitions:
            if (self.current_state == transition['params']['initial_state'] and
                current_symbol == transition['params']['tape_input']):
                transition_found = True
                self.current_state = transition['params']['output']['final_state']
                self.tape[self.head_position] = (transition['params']['output']['tape_output']
                                                 if transition['params']['output']['tape_output']
                                                 else current_symbol)
                direction = transition['params']['output']['tape_displacement']
                self.head_position += 1 if direction == 'R' else -1 if direction == 'L' else 0
                break

        if not transition_found:
            return False  # No se encontró transición válida, detiene la simulación
        return True

    def run(self):
        print(f"Inicio de la simulación con la cinta: {''.join(self.tape)}")
        while self.step():
            print(f"Estado actual: {self.current_state} | Cinta: {''.join(self.tape)} | Cabezal en: {self.head_position}")
            if self.current_state in self.final_states:
                print("Cadena aceptada")
                return True
        print("Cadena rechazada")
        return False

class AlteringTuringMachine(TuringMachine):
    def step(self):
        """Realiza una acción de alteración en la cinta, como invertir la cadena."""
        if self.head_position < 0 or self.head_position >= len(self.tape):
            self.tape.append('_')  # Expande la cinta si el cabezal se sale de los límites

        current_symbol = self.tape[self.head_position]
        transition_found = False

        # Si se encuentra un símbolo 'a' o 'b', lo cambiamos por 'x' para alterarlo
        if current_symbol == 'a' or current_symbol == 'b':
            transition_found = True
            self.tape[self.head_position] = 'x'  # Reemplazamos 'a' o 'b' por 'x'

            # Mueve el cabezal de izquierda a derecha
            self.head_position += 1 if self.head_position < len(self.tape) - 1 else 0

        if not transition_found:
            return False  # No se encontró transición válida, detiene la simulación
        return True

    def run(self):
        print(f"Inicio de la simulación con la cinta: {''.join(self.tape)}")
        while self.step():
            print(f"Estado actual: Alterando | Cinta: {''.join(self.tape)} | Cabezal en: {self.head_position}")
        print(f"Cinta alterada: {''.join(self.tape)}")
        return True

# Carga de configuraciones desde YAML
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Máquina de Turing reconocedora (para cadenas de la forma a^n b^n)
print("\n--- Simulación de la Máquina Reconocedora ---")
recognizer = TuringMachine(config)

# Probar cadenas de entrada para la máquina reconocedora
for input_string in config['simulation_strings']:
    print(f"\nSimulando la cadena: {input_string}")
    recognizer.load_tape(input_string)
    recognizer.run()

# Máquina de Turing alteradora (invierte la cadena)
print("\n--- Simulación de la Máquina Alteradora ---")
alterer = AlteringTuringMachine(config)

# Probar cadenas de entrada para la máquina alteradora
example_strings = ['aabb', 'bbbaaa', 'ab', 'abab']
for input_string in example_strings:
    print(f"\nSimulando la cadena a alterar: {input_string}")
    alterer.load_tape(input_string)
    alterer.run()
