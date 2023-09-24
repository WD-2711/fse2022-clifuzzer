/* 返回传递给 getopt 库的值的代码，然后可以选择调用实际的 getopt */
// 定义 _GNU_SOURCE 后可以启用一些扩展函数、数据结构等，如 getopt_long()
// 重写 open|fopen|opendir
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <dlfcn.h>
#include <dirent.h>


typedef FILE (*orig_fopen) (const char * filename, const char * mode );

typedef DIR (*orig_opendir) (const char *name);

typedef int (*orig_open_f_type)(const char *pathname, int flags);

int open(const char *pathname, int flags,...)
{
    printf("open: %s\n", (char *)pathname);
    /*
    orig_open_f_type orig_open;
    orig_open = (orig_open_f_type)dlsym(RTLD_NEXT,"open");
    return orig_open(pathname,flags);    
    */
    exit(0);
}

FILE *fopen(const char *filename, const char *mode)
{
    printf ("fopen: %s\n", (char*) filename);
    exit(0);
}


DIR *opendir(const char *name)
{
    printf("diropen: %s\n", (char*) name);
    exit(0);
}
