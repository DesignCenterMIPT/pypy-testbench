#include<stdio.h>

#include"hello.h"

void hello() {
	printf("Hello, world\n");
}

void printMyInt(struct MyInt* v) {
	printf("MyInt{Int=%d}\n", v -> Int);
}

int return42() {
	return 42;
}
