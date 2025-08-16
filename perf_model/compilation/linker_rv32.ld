RAMSIZE = 4M;
IMEMO = 0x00000000;
DMEMO = 0x00100000;
MEMORY
{
    RAM : ORIGIN = DMEMO, LENGTH = 4M
    IMEM : ORIGIN = IMEMO, LENGTH = 1M
}

SECTIONS
{
    .text.start : {
        *(.text.start)
        *(SORT_NONE(.init))
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

    .stack : {
    . = ALIGN(4);
    . = ALIGN(16);
    stack_start = .;
    . = . + 0x1000;
    stack = .;
  } > RAM

    _edata = .; PROVIDE (edata = .);
    .bss : {
        __bss_start = .;
        *(.bss COMMON)
        *(.sbss)
        *(COMMON)
        __bss_end = .;
    } > RAM
    . = ALIGN(4);
    _end = .; PROVIDE (end = .); PROVIDE (bssend = .);


    /*. = DATA_SEGMENT_END (.);*/
}
