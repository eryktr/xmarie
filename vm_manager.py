from typing import Dict, List, Optional

from xmarievm import api
from xmarievm.api import get_line_array
from xmarievm.breakpoints import BreakpointHit
from xmarievm.runtime import snapshot_maker
from xmarievm.runtime.snapshot_maker import Snapshot
from xmarievm.runtime.vm import MarieVm


class VmManager:
    vms: Dict[str, MarieVm]

    def __init__(self):
        self.vms = {}

    def has_client(self, token: str):
        return token in self.vms

    def register_client(self, token, max_num_calls=1_000_000):
        vm = MarieVm.get_default()
        vm.max_num_of_executed_instrs = max_num_calls
        self.vms[token] = vm

    def debugstep(self, token):
        return self.vms[token].debugstep()

    def hit_breakpoint(self, token):
        return self.vms[token].hit_breakpoint()

    def run(self, token, code: str, input_: str):
        self.register_client(token)
        program = api.parse_code(code)
        line_array = get_line_array(code)
        vm = self.vms[token]
        vm.execute(program, line_array)
        return snapshot_maker.make_snapshot(vm)

    def debug(self, token: str, code: str, input_: str, breakpoints: List[int]) -> BreakpointHit:
        # TODO Implement input handling
        self.register_client(token)
        program = api.parse_code(code)
        parsed_breakpoints = api.parse_breakpoints(code, breakpoints)
        vm = self.vms[token]
        line_array = get_line_array(code)
        vm.setup_debug(program, parsed_breakpoints, line_array)
        return vm.hit_breakpoint()

    def continue_debug(self, token: str) -> Optional[BreakpointHit]:
        vm = self.vms[token]
        vm.step()
        return vm.hit_breakpoint()
