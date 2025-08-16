/*stdlib Utils:*/

// Double inclusion guard
#ifndef UTILS_C
#include "types.h"
#define UTILS_C

// ctype.h stuff, as per https://en.cppreference.com/w/c/string/byte
int isdigit(char c){
    return c >= '0' && c <= '9';
}
int islower(char c){
    return c >= 'a' && c <= 'z';
}
int isupper(char c){
    return c >= 'A' && c <= 'Z';
}
int isalpha(char c){
    return islower(c) || isupper(c);
}
int isalnum(char c){
    return isalpha(c) || isdigit(c);
}

// Built in math functions the compiler is using
// Defined in https://gcc.gnu.org/onlinedocs/gccint/Integer-library-routines.html
unsigned int __mulsi3(unsigned int a, unsigned int b){
    int result = 0;
    while(b){
        if(b & 1){
            result += a;
        }
        a <<= 1;
        b >>= 1;
    }
    return result;
}

unsigned int __udivsi3 (unsigned int a, unsigned int b){
    unsigned int result = 0;
    while(a >= b){
        a -= b;
        result++;
    }
    return result;
}

unsigned int __umodsi3 (unsigned int a, unsigned int b){
    while(a >= b){
        a -= b;
    }
    return a;
}

// Str stuff
unsigned int strlen(const char *s){
    int i = 0;
    while(s[i] != '\0'){
        i++;
    }
    return i;
}

unsigned int strnlen(const char *s, size_t maxlen){
    int i = 0;
    while((s[i] != '\0') && (i < maxlen)){
        i++;
    }
    return i;
}

/* Public domain. Implementation from libgcc*/
void * memcpy (void *dest, const void *src, size_t len)
{
  char *d = dest;
  const char *s = src;
  while (len--)
    *d++ = *s++;
  return dest;
}

void * memset (void *dest, register int val, register size_t len)
{
  register unsigned char *ptr = (unsigned char*)dest;
  while (len-- > 0)
    *ptr++ = val;
  return dest;
}

void * memmove (void *dest, const void *src, size_t len)
{
  char *d = dest;
  const char *s = src;
  if (d < s)
    while (len--)
      *d++ = *s++;
  else
    {
      char *lasts = s + (len-1);
      char *lastd = d + (len-1);
      while (len--)
        *lastd-- = *lasts--;
    }
  return dest;
}

int memcmp (const void *str1, const void *str2, size_t count)
{
  const unsigned char *s1 = str1;
  const unsigned char *s2 = str2;

  while (count-- > 0)
    {
      if (*s1++ != *s2++)
	  return s1[-1] < s2[-1] ? -1 : 1;
    }
  return 0;
}

/*C function to initialize Stack n shit*/

//basic init function, initializes SP and .bss, calls main and then cleans up with call to _fini
__attribute__((naked, section(".text.start")))
void _start(){
    // four NOPS at the start to allow loading of function inputs into a0 and a1 here instead by the loader
    __asm__("nop\n"
            "nop\n"
            "nop\n"
            "nop\n");
  //.bss initialisation not needed
  //load etext to t3
  //   __asm__("lui	t3, %hi(edata)\n"
	// "lw	t3, %lo(edata)(t3)");
  //   //load _end to t4
  //   __asm__("lui	t4, %hi(bssend)\n"
	// "lw	t4, %lo(bssend)(t4)");
  //   // Initialize .bss
  //   __asm__(
  //       "bge t3, t4, 16\n"
  //       "sw zero, 0(t3)\n"
  //       "addi t3, t3, 4\n"
  //       "jal zero, -12"
  //   );
    //initialize SP
    __asm__("lui	sp, %hi(RAMSIZE)\n"
	"addi	sp, sp, %lo(RAMSIZE)");
    //call main
    __asm__("call main");
    //call cleanup
    __asm__("call _fini");
}

// Basic fini function, just calls ebreak and then loops infinitly
__attribute__((naked, section(".text.start.fini")))
void _fini(){
    //Break
    __asm__("ebreak");
    //endless loop
    __asm__("jal zero, 0");
}

/* stdio */
int putchar (const char s){
  __asm__("lui t5, %0"
            :
            : "i" (PUTSA_LUI)
            :"t5");
  __asm__("add t6, zero, %0"
            :
            : "r" (s)
            :"t6");
  __asm__("sb t6, 4(t5)");
  return 1;

}
int puts(const char *s){
  while (*s)
  {
    putchar(*s);
    s++;
  }
  putchar('\n');
  return 0;
  // slightly more efficient assembly version
  // __asm__("lui t5, %0"
  //         :
  //         : "i" (PUTSA_LUI)
  //         :"t5");
  // while(*s){
  //   __asm__("ecall");
  //   //Print charactrers till terminator
  //   __asm__("add t6, zero, %0"
  //         :
  //         : "r" (*s)
  //         :"t6");
  //   __asm__("sb t6, 4(t5)");
  //   //pc(*s);
  //   s++;
  // }
  // // Print "\n"
  // //pc('\n');
  // __asm__("addi t6, zero, 10\n"
  //         "sb t6, 4(t5)"
  //         :
  //         :
  //         :"t6");
}
// Currently only really here to show alternative implementation of writing to stdout
int fputs(const char *s, FILE *stream){
    if (stream != stdout)
    {
        // Only stdout works for this currently
        return -1;
    }
    int* addr = (int *) stream;
    while(*s){
        *addr = *s;
        s++;
    }
    return 0;
    // no \n line break
}

/// @brief Prints a string to stdout, without appending /n
/// @param s, string to print
/// @return EOF if error, 0 otherwise
int fputs_stdio(const char *s){
    return fputs(s, stdout);
}

// strings.c
#endif
