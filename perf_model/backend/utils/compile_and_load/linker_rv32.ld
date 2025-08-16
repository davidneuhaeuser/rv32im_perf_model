RAMSIZE = 4K;
IMEMO = 0x00100000;
MEMORY
{
    RAM (XR): ORIGIN = 0x0000, LENGTH = RAMSIZE
    IMEM (W!X): ORIGIN = IMEMO, LENGTH = 64K
}

SECTIONS
{
    .text.start : {
        *(.text.start)
        *(SORT_NONE(.init))
        *(.text.start.fini)
    } > IMEM
    .text : {
        *(.text)

    } > IMEM
    .fini           :
    {
        KEEP (*(SORT_NONE(.fini)))
    } > IMEM

    PROVIDE (__etext = .);
    PROVIDE (_etext = .);
    PROVIDE (etext = .);
    .data : {
        *(.data)
        *(.sdata)
        *(.rodata*)
    } > RAM


    _edata = .; PROVIDE (edata = .);
    .bss : {
        *(.bss COMMON)
        *(.sbss)
        *(COMMON)
    } > RAM
    . = ALIGN(64 / 8);
    _end = .; PROVIDE (end = .); PROVIDE (bssend = .);
    /*. = DATA_SEGMENT_END (.);*/
}
