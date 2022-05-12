#include<stdio.h>

#include"hello.h"

void hello() {
	printf("Hello, world\n");
}

void printMyInt(struct MyInt* v) {
	printf("pointer = %p\n", v);
	printf("MyInt{Int=%d}\n", v -> Int);
}

int return42() {
	return 42;
}
