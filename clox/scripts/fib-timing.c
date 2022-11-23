#include <stdio.h>
#include <time.h>

int fib(int n) {
	if (n < 2) return n;
	return fib(n - 1) + fib(n - 2);
}

int main(int argc, char** argv) {
	clock_t start = clock(), diff;
	fib(40);
	diff = clock() - start;
	int msec = diff * 1000 / CLOCKS_PER_SEC;
	printf("time taken %d s %d ms\n", msec/1000, msec%1000);
}
