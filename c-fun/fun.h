#ifndef C_FUN_DEF
#define C_FUN_DEF

#include<stdio.h>
#include <setjmp.h>
#include <stdlib.h>

void hello(void);

void printInt(int);

int returnInt(int);

int sumInt(int, int);

void exception_init();

void exception_new_point();
void exception_delete();

jmp_buf* exception_top();

void exception_free();

int try_catch();
void try_catch_end();
void throw();

#endif