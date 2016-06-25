# -*- coding: utf-8 -*-

import enum
from enum import Enum
class Architecture(Enum):
	X86_16_INTEL = 0
	X86_32_INTEL = 1
	X86_64_INTEL = 2
	X86_16_ATT = 3
	X86_32_ATT  = 4
	X86_64_ATT = 5
	ARM_LE = 6
	ARM_BE = 7
	ARM_THUMB_LE = 8
	ARM_THUMB_BE = 9
	ARM_AARCH64 = 10
	MIPS = 11
	MIPS_BE = 12
	MIPS64 = 13
	MIPS64_BE = 14
	PPC = 15
	PPC64 = 16
	SPARC = 17
	SPARC_BE = 18
	SPARC64 = 19
	SPARC64_BE = 20

X86_GPR = ["AX", "BX", "CX", "DX", "SI", "DI", "IP", "BP", "SP"]
X86_PGR = ["CS", "DS", "ES", "FS", "GS", "SS"]
X86_FLAG = ["EFLAGS", ]
X86_16_REGS = X86_GPR
X86_32_REGS = ["E"+x for x in X86_GPR] + X86_FLAG
X86_64_REGS = ["R"+x for x in X86_GPR] + ["R%d"%i for i in range(8,16)] + X86_FLAG

# http://www.keil.com/support/man/docs/armasm/armasm_dom1359731128950.htm
ARM_GPR = ["R%d"%i for i in range(11)] + ["R12",]
ARM_FLAG = ["CPSR", ]
ARM_REGS = ARM_GPR + ["FP", "SP", "LR", "PC",] + ARM_FLAG

AARCH64_GPR = ["X%d"%i for i in range(31)]
AARCH64_FLAG = ["NZCV", ] # http://infocenter.arm.com/help/index.jsp?topic=/com.arm.doc.dui0801a/BABIBIGB.html
AARCH64_REGS = AARCH64_GPR + ["PC",] + AARCH64_FLAG

# https://msdn.microsoft.com/en-us/library/ms253512(v=vs.90).aspx
MIPS_GPR = ["ZERO", "AT", "V0", "V1" ] + ["A%d"%i for i in range(4)] + ["T%d"%i for i in range(10)] + ["S%d"%i for i in range(9)]  + ["S%d"%i for i in range(9)] + ["K0", "K1"]
MIPS_REGS = MIPS_GPR + ["GP", "SP", "RA", "PC"]

PPC_GPR = ["R%d"%i for i in range(32)]
PPC_REGS = PPC_GPR + ["PC", ]

SPARC_GPR = ["G%d"%i for i in range(8)] + ["L%d"%i for i in range(8)] + ["I%d"%i for i in range(8)] + ["O%d"%i for i in range(8)]
SPARC_FLAG = ["ICC", ] # incomplete https://www.kernel.org/pub/linux/kernel/people/marcelo/linux-2.4/include/asm-sparc/psr.h
SPARC_REGS = SPARC_GPR + ["PC", ] + SPARC_FLAG

modes = {"x86":[ (Architecture.X86_16_INTEL, "16bit, Intel syntax", X86_16_REGS, "IP", "SP"),
                 (Architecture.X86_32_INTEL, "32bit, Intel syntax", X86_32_REGS, "EIP", "ESP"),
                 (Architecture.X86_64_INTEL, "64bit, Intel syntax", X86_64_REGS, "RIP", "RSP"),
                 (Architecture.X86_16_ATT, "16bit, AT&T syntax", X86_16_REGS, "IP", "SP"),
                 (Architecture.X86_32_ATT, "32bit, AT&T syntax", X86_32_REGS, "EIP", "ESP"),
                 (Architecture.X86_64_ATT, "64bit, AT&T syntax", X86_64_REGS, "RIP", "RSP"), ],

         "arm":[ (Architecture.ARM_LE, "ARM - little endian", ARM_REGS, "PC", "SP"),
                 (Architecture.ARM_BE, "ARM - big endian", ARM_REGS, "PC", "SP"),
                 (Architecture.ARM_THUMB_LE, "ARM Thumb mode - little endian", ARM_REGS, "PC", "SP"),
                 (Architecture.ARM_THUMB_BE, "ARM Thumb mobe - big endian", ARM_REGS, "PC", "SP"),
                 (Architecture.ARM_AARCH64, "ARMv8 AARCH64", AARCH64_REGS, "PC", "SP"), ],

         "mips":[ (Architecture.MIPS, "MIPS - little endian", MIPS_REGS, "PC", "SP"),
                  (Architecture.MIPS_BE, "MIPS - big endian", MIPS_REGS, "PC", "SP"),
                  (Architecture.MIPS64, "MIPS64 - little endian", MIPS_REGS, "PC", "SP"),
                  (Architecture.MIPS64_BE, "MIPS64 - big endian", MIPS_REGS, "PC", "SP"), ],

#         "ppc": [ (Architecture.PPC, "PowerPC - big endian", PPC_REGS, "PC", "SP"),
#                  (Architecture.PPC64, "PowerPC64 - big endian", PPC_REGS, "PC", "SP"),],

         "sparc":[ (Architecture.SPARC, "SPARC - little endian", SPARC_REGS, "PC", "SP"),
                   (Architecture.SPARC_BE, "SPARC - big endian", SPARC_REGS, "PC", "SP"),
                   (Architecture.SPARC64, "SPARC64 - little endian", SPARC_REGS, "PC", "SP"),
                   (Architecture.SPARC64_BE, "SPARC64 - big endian", SPARC_REGS, "PC", "SP"),],
}


class Mode:

    def __init__(self, *args, **kwargs):
        # the default mode is x86-32
        self.set_new_mode(Architecture.X86_32_INTEL)
        return

    def get_current_mode(self):
        return self.__selected

    def set_new_mode(self, i):
        for arch in modes.keys():
            for mode in modes[arch]:
                if mode[0]==i:
                    self.__selected = mode
                    return

        raise Exception("Invalid arch/mode")

    def get_id(self):
        return self.__selected[0]

    def get_title(self):
        return self.__selected[1]

    def get_registers(self):
        return self.__selected[2]

    def get_pc(self):
        return self.__selected[3]

    def get_sp(self):
        return self.__selected[4]

    def __eq__(self, x):
        return x==self.get_id()

    def get_memory_alignment(self):
        if self.get_id() in (Architecture.X86_16_INTEL,
                               Architecture.ARM_THUMB_LE,
                               Architecture.ARM_THUMB_BE):
            return 16

        if self.get_id() in (Architecture.X86_64_INTEL,
                               Architecture.X86_64_ATT,
                               Architecture.ARM_AARCH64):
            return 64

        return 32
