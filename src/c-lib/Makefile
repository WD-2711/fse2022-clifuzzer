# 再运行 fuzzer 之前，运行 make
# -ldl 表示在链接过程中需要使用 libdl 库，此库提供了函数（dlopen|dlsym等），用于在运行时加载共享库
# -shared -fPIC 表示生成动态链接库，且位置无关
# 定义了指令 clean，此时回删除所有 so 文件

all: mygetopt.so myopen.so mystat.so mystrcmp.so

mygetopt.so:
	gcc -shared -fPIC mygetopt.c -o $@ -ldl
myopen.so:
	gcc -shared -fPIC myopen.c -o $@ -ldl
mystat.so:
	gcc -shared -fPIC mystat.c -o $@ -ldl
mystrcmp.so:
	gcc -shared -fPIC mystrcmp.c -o $@ -ldl

clean:
	-rm -rf *.so
