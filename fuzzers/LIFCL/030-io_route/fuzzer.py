from fuzzconfig import FuzzConfig
from interconnect import fuzz_interconnect
import re

configs = [
    {
        "cfg": FuzzConfig(job="IOROUTE5", device="LIFCL-40", sv="../shared/route_40.v", tiles=["CIB_R56C8:SYSIO_B5_0", "CIB_R56C9:SYSIO_B5_1"]),
        "rc": (56, 8),
    },
    {
        "cfg": FuzzConfig(job="IOROUTE4", device="LIFCL-40", sv="../shared/route_40.v", tiles=["CIB_R56C16:SYSIO_B4_0", "CIB_R56C17:SYSIO_B4_1"]),
        "rc": (56, 16),
    },
    {
        "cfg": FuzzConfig(job="IOROUTE3", device="LIFCL-40", sv="../shared/route_40.v", tiles=["CIB_R56C56:SYSIO_B3_0", "CIB_R56C57:SYSIO_B3_1"]),
        "rc": (56, 56),
    },
    {
        "cfg": FuzzConfig(job="IOROUTE2", device="LIFCL-40", sv="../shared/route_40.v", tiles=["CIB_R44C87:SYSIO_B2_0"]),
        "rc": (44, 87),
    },
    {
        "cfg": FuzzConfig(job="IOROUTE1", device="LIFCL-40", sv="../shared/route_40.v", tiles=["CIB_R8C87:SYSIO_B1_0"]),
        "rc": (8, 87),
    },
    {
        "cfg": FuzzConfig(job="IOROUTE0", device="LIFCL-40", sv="../shared/route_40.v", tiles=["CIB_R0C84:SYSIO_B0_0"]),
        "rc": (0, 84),
    },
    {
        "cfg": FuzzConfig(job="IOROUTE7", device="LIFCL-40", sv="../shared/route_40.v", tiles=["CIB_R3C0:SYSIO_B7_0"]),
        "rc": (3, 0),
    },
    {
        "cfg": FuzzConfig(job="IOROUTE6", device="LIFCL-40", sv="../shared/route_40.v", tiles=["CIB_R49C0:SYSIO_B6_0"]),
        "rc": (49, 0),
    },
]

ignore_tiles = set([
    "CIB_R55C8:CIB",
    "CIB_R55C9:CIB",
    "CIB_R55C16:CIB",
    "CIB_R55C17:CIB",
    "CIB_R55C56:CIB",
    "CIB_R55C57:CIB",
    "CIB_R44C86:CIB_LR",
    "CIB_R45C86:CIB_LR",
    "CIB_R8C86:CIB_LR",
    "CIB_R9C86:CIB_LR",
    "CIB_R1C84:CIB_T",
    "CIB_R1C85:CIB_T",
    "CIB_R3C1:CIB_LR",
    "CIB_R4C1:CIB_LR",
    "CIB_R49C1:CIB_LR",
    "CIB_R50C1:CIB_LR",
])

def main():
    for config in configs:
        cfg = config["cfg"]
        cfg.setup()
        r, c = config["rc"]
        nodes = ["R{}C{}_*".format(r, c)]
        def nodename_filter(x, nodes):
            return ("R{}C{}_".format(r, c) in x) and ("_GEARING_PIC_TOP_" in x or "SEIO18_CORE" in x or "DIFFIO18_CORE" in x or "I217" in x or "I218" in x or "SEIO33_CORE" in x or "SIOLOGIC_CORE" in x)
        def pip_filter(pip, nodes):
            from_wire, to_wire = pip
            return not ("ADC_CORE" in to_wire or "ECLKBANK_CORE" in to_wire or "MID_CORE" in to_wire
                or "REFMUX_CORE" in to_wire or "CONFIG_JTAG_CORE" in to_wire or "CONFIG_JTAG_CORE" in from_wire
                or "REFCLOCK_MUX_CORE" in to_wire)
        fuzz_interconnect(config=cfg, nodenames=nodes, nodename_predicate=nodename_filter, pip_predicate=pip_filter, regex=True, bidir=True, ignore_tiles=ignore_tiles)

if __name__ == "__main__":
    main()
