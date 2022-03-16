# run this once before you run the fuzzer

CC=gcc
CFLAGS=-shared -fPIC

all: mygetopt.so myopen.so mystat.so mystrcmp.so

mygetopt.so:
	$(CC) $(CFLAGS) mygetopt.c -o $@ -ldl
myopen.so:
	$(CC) $(CFLAGS) myopen.c -o $@ -ldl
mystat.so:
	$(CC) $(CFLAGS) mystat.c -o $@ -ldl
mystrcmp.so:
	$(CC) $(CFLAGS) mystrcmp.c -o $@ -ldl

clean:
	-rm -rf *.so
