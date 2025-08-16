from perf_model.backend.isa.constants import REGDICTA, REGDICTB


def map_reg_name(reg_name) -> int:
    if isinstance(reg_name, str):
        if reg_name in REGDICTA:
            return map_reg_name(REGDICTA[reg_name])
        elif reg_name in REGDICTB:
            return REGDICTB[reg_name]
        else:
            try:
                num = int(reg_name)
                if num in range(32):
                    return num
            except:
                print("invalid register name")

    elif isinstance(reg_name, int):
        return reg_name


def map_imm_arg(reg_name) -> int:
    if isinstance(reg_name, int):
        return reg_name
    try:
        return int(reg_name)
    except:
        print("invalid immediate value")
        return "invalid immediate value"
