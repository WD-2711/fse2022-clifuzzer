# run this once before you run the fuzzer

CC=gcc

all: testopt testlongopt

testopt: testopt.c
	$(CC) -g --coverage -o testopt testopt.c
	
testlongopt: testlongopt.c
	$(CC) -g --coverage -o testlongopt testlongopt.c

clean-cov:
	- rm -f *.gcda *.gcov

clean:
	- rm -f testopt testlongopt *.gcno *.gcda *.gcov