from dataclasses import asdict

from xmarievm.breakpoints import Breakpoint
from xmarievm.const import MEM_BITSIZE
from xmarievm.runtime.snapshot_maker import Snapshot
from xmarievm.util import int_in_2c_to_hex, int_from_2c


def serialize_snashot(snapshot: Snapshot):
    dec_fields = ('AC', 'X', 'Y', 'MAR', 'MBR', 'PC', 'IR')
    snapshot.lineno_to_num_calls = dict(snapshot.lineno_to_num_calls)
    snapshot_dict = asdict(snapshot)
    snapshot_dict['output_stream'] = snapshot.output_stream.buf
    snapshot_dict['stack'] = [serialize_dec_num(n) for n in snapshot_dict['stack']]
    for field in dec_fields:
        snapshot_dict[field] = serialize_dec_num(snapshot_dict[field])
    return snapshot_dict


def serialize_dec_num(dec):
    return {
        'dec': dec,
        'hex': int_in_2c_to_hex(dec, MEM_BITSIZE),
    }


def serialize_hex_num(hx):
    return {
        'dec': int_from_2c(hx, MEM_BITSIZE),
        'hex': hx,

    }


def serialize_breakpoint(breakpoint: Breakpoint):
    return asdict(breakpoint)
