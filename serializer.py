from dataclasses import asdict

from xmarievm.breakpoints import Breakpoint
from xmarievm.runtime.snapshot_maker import Snapshot


def serialize_snashot(snapshot: Snapshot):
    snapshot_dict = asdict(snapshot)
    snapshot_dict['output_stream'] = snapshot.output_stream.buf
    return snapshot_dict


def serialize_breakpoint(breakpoint: Breakpoint):
    return asdict(breakpoint)
