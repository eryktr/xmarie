from typing import Dict, List, Optional

from xmarievm import api
from xmarievm.breakpoints import BreakpointHit
from xmarievm.runtime.snapshot_maker import Snapshot
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

    def debug(self, token: str, code: str, input_: str, breakpoints: List[int]) -> BreakpointHit:
        self.register_client(token)
        program = api.parse_code(code)
        parsed_breakpoints = api.parse_breakpoints(breakpoints, code)
        vm = self.vms[token]
        vm.setup_debug(program, parsed_breakpoints)
        return vm.hit_breakpoint()

    def continue_debug(self, token: str) -> Optional[BreakpointHit]:
        vm = self.vms[token]
        return vm.hit_breakpoint()
