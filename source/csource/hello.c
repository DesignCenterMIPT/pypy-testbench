#include<stdio.h>

#include"hello.h"

void hello() {
	printf("Hello, world\n");
}

void printMyInt(struct MyInt v) {
	printf("MyInt{Int=%d}", v.Int);
}
