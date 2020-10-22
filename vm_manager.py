from typing import Dict

from xmarievm import api
from xmarievm.runtime.vm import MarieVm


class VmManager:
    vms: Dict[str, MarieVm]

    def has_client(self, token: str):
        return token in self.vms

    def register_client(self, token, max_num_calls=1_000_000):
        vm = MarieVm.get_default()
        vm.max_num_of_executed_instrs = max_num_calls
        self.vms[token] = vm

    def step(self, token):
        return self.vms[token].step()

    def hit_breakpoint(self, token):
        return self.vms[token].hit_breakpoint()

    def run(self, code: str, input_: str):
        api.run(code, debug=False, input_=input_)

    def debug(self, token: str, code: str, input_: str):
        self.register_client(token)
        program = api.parse(code)
        self.vms[token].setup_debug()