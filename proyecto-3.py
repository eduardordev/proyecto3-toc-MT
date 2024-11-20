import yaml

class TuringMachine:
    def __init__(self, config):
        self.q_states = config['q_states']['q_list']
        self.initial_state = config['q_states']['initial']
        self.final_states = config['q_states']['final'] if isinstance(config['q_states']['final'], list) else [config['q_states']['final']]
        self.alphabet = config['alphabet']
        self.tape_alphabet = config['tape_alphabet']
        self.blank_symbol = ''
        self.delta = self.build_transition_function(config['delta'])
        self.simulation_strings = config['simulation_strings']

    def build_transition_function(self, delta_list):
        transition_function = {}
        for transition in delta_list:
            params = transition['params']
            output = transition['output']

            initial_state = params['initial_state']
            mem_cache_value = params.get('mem_cache_value')
            if mem_cache_value is None:
                mem_cache_value = self.blank_symbol
            tape_input = params.get('tape_input')
            if tape_input is None:
                tape_input = self.blank_symbol

            key = (initial_state, mem_cache_value, tape_input)

            final_state = output['final_state']
            output_mem_cache_value = output.get('mem_cache_value')
            if output_mem_cache_value is None:
                output_mem_cache_value = self.blank_symbol
            tape_output = output.get('tape_output')
            if tape_output is None:
                tape_output = self.blank_symbol
            tape_displacement = output['tape_displacement']

            value = (final_state, output_mem_cache_value, tape_output, tape_displacement)
            transition_function[key] = value
        return transition_function

    def simulate(self):
        for input_string in self.simulation_strings:
            print(f"\nSimulating input: {input_string}")
            result = self.run_machine(input_string)
            print(f"Result: {'Accepted ' if result else 'Rejected '}{input_string}\n{'-'*50}")

    def run_machine(self, input_string):
        tape = list(input_string)
        head_position = 0
        current_state = self.initial_state
        mem_cache = self.blank_symbol
        step = 0

        tape.extend([self.blank_symbol] * 100)

        while True:
            tape_symbol = tape[head_position]

            key = (current_state, mem_cache, tape_symbol)

            self.print_instantaneous_description(tape, head_position, current_state, mem_cache, step)

            if current_state in self.final_states:
                return True

            if key not in self.delta:
                return False

            (new_state, new_mem_cache, new_tape_symbol, movement) = self.delta[key]

            tape[head_position] = new_tape_symbol

            mem_cache = new_mem_cache

            if movement == 'R':
                head_position += 1
            elif movement == 'L':
                head_position -= 1
            elif movement == 'S':
                pass

            current_state = new_state
            step += 1

    def print_instantaneous_description(self, tape, head_position, current_state, mem_cache, step):
        tape_str = ''.join([symbol if symbol != self.blank_symbol else '' for symbol in tape[:50]])
        head_str = ' ' * head_position + '^'
        print(f"Step {step}:")
        print(f"State: {current_state}, Mem Cache: {mem_cache if mem_cache != self.blank_symbol else ''}")
        print(f"Tape: {tape_str}")
        print(f"       {head_str}\n")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        sys.exit(1)

    config_file = sys.argv[1]

    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)

    tm = TuringMachine(config)
    tm.simulate()
