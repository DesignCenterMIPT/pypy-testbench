#include "fun.h"
//#include "try-catch.h"
#include <stdio.h>

void hello(void) {
    printf("Hello, world\n");
}

void printInt(int v) {
    printf("Int=%d\n", v);
}

int returnInt(int v) {
    return v;
}

int sumInt(int lv, int rv) {
    return lv + rv;
}

exception_t* exception_net() {
	exception_t* exp = malloc(sizeof(exception_t));
	exception_init(exp);
	return exp;
}

void exception_init(exception_t* exp) {
	printf("Befour init: %p, %ld\n", exp -> array, exp -> size);
	exp -> array = malloc(1024*sizeof(jmp_buf));
	exp -> size = 0;
	printf("After init: %p, %ld\n", exp -> array, exp -> size);
}

void exception_new_point(exception_t* exp) {
	printf("exception_new_point\n");
    exp -> size++;
	//printf("exception_new_point_end\n");
}

jmp_buf* exception_top(exception_t* exp) {
	printf("exception_top\n");
	return &(exp -> array[exp -> size - 1]);
}

void exception_delete(exception_t* exp) {
	printf("exception_delete\n");
	exp -> size--;
}

void exception_free(exception_t* exp) {
	free(exp -> array);
}

inline void throw(exception_t* exp) {
	//printf("throw\n");
	//printf("exp.array=%p \n", exp -> array);
	longjmp(*exception_top(exp), 1);
	//printf("Why I\'m stile here, just a suffer ;-( \n");
}

#define try_catch_def(exp) setjmp(*exception_top(exp))

int try_catch(exception_t* exp) {
	//printf("try_catch\n");
	//printf("exp.array=%p \n", exp -> array);
	
	int val = setjmp(*exception_top(exp));
	/*
	if (val) {
		for(int i = 0; i < 10; i++) {
			printf("%d ", i);
		}
		printf("\n")
	}*/
	return val;
} 

void try_catch_end(exception_t* exp) {
	printf("try_catch_end\n");
	exception_delete(exp);	
}

int main() {
	exception_t exp;
	exception_init(&exp);
	//exception_new_point(&exp);
	//if(setjmp(*exception_top(&exp))) {
	exception_new_point(&exp);
	if(try_catch_def(&exp)) {
		printf("2.catch section");
	} else {
		printf("1.throw\n");
		throw(&exp);
		printf("error\n");
	}
	try_catch_end(&exp);
	exception_free(&exp);
}