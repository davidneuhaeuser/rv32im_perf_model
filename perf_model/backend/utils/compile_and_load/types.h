// double inclusion guard
#ifndef TYPES_H
#define TYPES_H

//stdint.h

//unsigned
typedef unsigned char uint8_t;
typedef unsigned short uint16_t;
typedef unsigned int uint32_t;
typedef unsigned int uintmax_t;
typedef unsigned int uintptr_t;
typedef unsigned long long uint64_t; // IS IMPLEMENTED VIRTUALLY; VERY SLOW

#define UINT8_MAX 255
#define UINT16_MAX 65535
#define UINT32_MAX 4294967295
#define UINT64_MAX 18446744073709551615

//signed
typedef char int8_t;
typedef short int16_t;
typedef int int32_t;
typedef int intmax_t;
typedef long long int64_t; // IS IMPLEMENTED VIRTUALLY; VERY SLOW

#define INT8_MIN -128
#define INT16_MIN -32768
#define INT32_MIN -2147483648
#define INT64_MIN = -9223372036854775808

#define INT8_MAX 127
#define INT16_MAX 32767
#define INT32_MAX 2147483647
#define INT64_MAX 9223372036854775807


//typedef.h
typedef unsigned int size_t;
typedef unsigned int ptrdiff_t;

#define NULL (0)
#define true (1)
#define false (0)

//limits.h

#define CHAR_BIT 8
#define CHAR_MIN -128
#define CHAR_MAX 127

#define SCHAR_MIN -128
#define SHRT_MIN -32768
#define INT_MIN -2147483648
#define LONG_MIN -2147483648
#define LLONG_MIN -9223372036854775808

#define SCHAR_MAX 127
#define SHRT_MAX 32767
#define INT_MAX 2147483647
#define LONG_MAX 2147483647
#define LLONG_MAX 9223372036854775807

#define UCHAR_MAX 255
#define USHRT_MAX 65535
#define UINT_MAX 4294967295
#define ULONG_MAX 4294967295
#define ULLONG_MAX 18446744073709551615

// platform specific
#define PUTSA 0x10000004
#define PUTSA_LUI 0x10000
#define PUTSA_ADDI 0x0004

// stdio.h
//TODO: PROPER DEFINITION FOR FILE
typedef void FILE;

FILE* stdout = (FILE*) PUTSA;
#define stdout stdout

#define EOF (-1)

#endif
