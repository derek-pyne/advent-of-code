import logging
import sys
from typing import List

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class IntCodeComputer:

    def __init__(self, memory, loglevel=logging.DEBUG) -> None:
        self.logger = logger
        self.logger.setLevel(loglevel)
        self.memory = memory+1000*[0]
        self.relative_base = 0

    def run(self, input=0):
        pointer = 0
        output = ''
        while True:
            self.logger.debug(f'Pointer: {pointer}')
            instruction = self.memory[pointer]
            opcode = instruction % 100
            parameter_modes = instruction // 100

            if opcode == 1:
                # Sum
                self.logger.info(f'Sum with parameter_modes: {parameter_modes}')
                num1, num2, target = self._get_parameters(pointer + 1, 3, parameter_modes, write_params=[2])
                num_sum = num1 + num2
                self.logger.debug(f'Writing {num_sum} to {target}')
                self.memory[target] = num_sum
                pointer += 4
            elif opcode == 2:
                # Multiply
                self.logger.info(f'Multiply with parameter_modes: {parameter_modes}')
                num1, num2, target = self._get_parameters(pointer + 1, 3, parameter_modes, write_params=[2])
                num_multiply = num1 * num2
                self.logger.debug(f'Writing {num_multiply} to {target}')
                self.memory[target] = num_multiply
                pointer += 4
            elif opcode == 3:
                # Read input
                self.logger.info(f'Input with parameter_modes: {parameter_modes}')
                if parameter_modes == 2:
                    self.memory[self.memory[pointer + 1]+self.relative_base] = input
                else:
                    self.memory[self.memory[pointer + 1]] = input
                self.logger.info(f'Input of: {input} from position {self.memory[pointer + 1]}')
                pointer += 2
            elif opcode == 4:
                # Write output
                self.logger.info(f'Output with parameter_modes: {parameter_modes}')
                output, = self._get_parameters(pointer + 1, 1, parameter_modes)
                self.logger.info(f'Output of: {output} from {self.memory[pointer + 1]}')
                print(f'Output: {output}')
                pointer += 2
            elif opcode == 5:
                # Jump-if-true
                self.logger.info(f'Jump-if-true with parameter_modes: {parameter_modes}')
                condition, target = self._get_parameters(pointer + 1, 2, parameter_modes)
                if condition != 0:
                    pointer = target
                    self.logger.debug(f'Condition true, jumping pointer to {target}')
                else:
                    self.logger.debug(f'Condition false, doing nothing')
                    pointer += 3
            elif opcode == 6:
                # Jump-if-false
                self.logger.info(f'Jump-if-false with parameter_modes: {parameter_modes}')
                condition, target = self._get_parameters(pointer + 1, 2, parameter_modes)
                if condition == 0:
                    pointer = target
                    self.logger.debug(f'Condition false, jumping pointer to {target}')
                else:
                    self.logger.debug(f'Condition true, doing nothing')
                    pointer += 3
            elif opcode == 7:
                # Less than
                self.logger.info(f'Less than with parameter_modes: {parameter_modes}')
                param1, param2, target = self._get_parameters(pointer + 1, 3, parameter_modes, write_params=[2])
                value = int(param1 < param2)
                self.logger.debug(f'Writing {value} to {target}')
                self.memory[target] = value
                pointer += 4
            elif opcode == 8:
                # Equals
                self.logger.info(f'Equals with parameter_modes: {parameter_modes}')
                param1, param2, target = self._get_parameters(pointer + 1, 3, parameter_modes, write_params=[2])
                value = int(param1 == param2)
                self.logger.debug(f'Writing {value} to {target}')
                self.memory[target] = value
                pointer += 4
            elif opcode == 9:
                # Adjust relative base
                self.logger.info(f'Adjust relative base with parameter_modes: {parameter_modes}')
                param1, = self._get_parameters(pointer + 1, 1, parameter_modes)
                self.logger.debug(f'Increasing relative base by {param1}')
                self.relative_base += int(param1)
                pointer += 2
            elif opcode == 99:
                # Exit
                break
            else:
                raise ValueError(f'Unknown opcode: {opcode}')
        return output

    def _get_digit(self, number, n):
        return number // 10 ** n % 10

    def _get_parameters(self, params_start, n, parameter_modes, write_params=None) -> List[int]:
        write_params = write_params if write_params is not None else []
        params = []
        for i in range(n):
            mem_value = self.memory[params_start + i]
            param_mode = self._get_digit(parameter_modes, i)
            # Position Mode
            if param_mode == 0:
                if i not in write_params:
                    value = self.memory[mem_value]
                else:
                    value = mem_value
            # Immediate Mode
            elif param_mode == 1:
                value = mem_value
            # Relative Mode
            elif param_mode == 2:
                if i not in write_params:
                    value = self.memory[mem_value + self.relative_base]
                else:
                    value = mem_value + self.relative_base
            else:
                raise ValueError(f'Invalid parameter mode: {param_mode}')
            params.append(value)
        self.logger.debug(f'Params: {params} with parameter modes: {parameter_modes}')
        return params
