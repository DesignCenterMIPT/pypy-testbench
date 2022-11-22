#ifndef C_FUN_DEF
#define C_FUN_DEF

#include<stdio.h>
#include<setjmp.h>
#include<stdlib.h>

typedef struct {
	jmp_buf* array;
	size_t size;
} exception_t;

void hello(void);

void printInt(int);

int returnInt(int);

int sumInt(int, int);

exception_t* exception_new();

void exception_init(exception_t* exp);

void exception_new_point(exception_t* exp);

void exception_delete(exception_t* exp);

jmp_buf* exception_top(exception_t* exp);

void exception_free(exception_t* exp);

int try_catch(exception_t* exp);

void try_catch_end(exception_t* exp);

void throw(exception_t* exp);

#endif