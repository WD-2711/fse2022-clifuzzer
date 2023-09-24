
/* 重写 strcmp 函数 */
#define _GNU_SOURCE
#include <stdio.h>
#include <string.h>
#include <dlfcn.h>
#include <stdlib.h>

typedef int (*orig_strcmp_type)(const char *p1, const char *p2);

typedef int (*orig_strncmp_type)(const char *s1, const char *s2, size_t n);

int strcmp (const char *p1, const char *p2)
{
    printf("first parameter:'%s', second parameter:'%s', third parameter:None \n", (char*) p1, (char*) p2);
    orig_strcmp_type orig_strcmp;
    orig_strcmp = (orig_strcmp_type)dlsym(RTLD_NEXT,"strcmp");
    return orig_strcmp(p1, p2);
    exit(0);
}

int strncmp(const char *s1, const char *s2, size_t n)
{

    printf("first parameter:'%s', second parameter:'%s', third parameter:'%i' \n", (char*) s1, (char*) s2, (int) n);
    orig_strncmp_type orig_strncmp;
    orig_strncmp = (orig_strncmp_type)dlsym(RTLD_NEXT,"strncmp");
    return orig_strncmp(s1, s2, n);
    exit(0);

}

