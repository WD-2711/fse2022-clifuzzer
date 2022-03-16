/*
 *Code to return values passed to getopt library
 *and then optionally call the actual getopt function
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <dlfcn.h>
#include <unistd.h>
#include <sys/stat.h>
#include <string.h>

typedef int (*orig_stat) (const char *path, struct stat *buf);
typedef int (*orig_lstat) (const char *path, struct stat *buf);

typedef int (*orig__xstat) (int __ver,
             const char *__filename,
             struct stat *__stat_buf);

typedef int (*orig__lxstat) (int __ver,
              const char *__filename,
              struct stat *__stat_buf);

int stat(const char *path, struct stat *buf)
{
    char * pch;
    pch = strstr(path, "/AppleInternal");
    if (pch != NULL){
        orig_stat orig_st;
        orig_st = (orig_stat) dlsym (RTLD_NEXT, "stat");
        return orig_st(path, buf);
    }
    printf("stat: %s\n", (char *)path);
    exit(0);
}

int lstat(const char *path, struct stat *buf)
{
    char * pch;
    pch = strstr(path, "/AppleInternal");
    if (pch != NULL){
        orig_stat orig_lst;
        orig_lst = (orig_stat) dlsym (RTLD_NEXT, "lstat");
        return orig_lst(path, buf);
    }
    printf("lstat: %s\n", (char *)path);
    exit(0);
}

int __xstat (int __ver,
             const char *__filename,
             struct stat *__stat_buf)
{
    printf("__xstat: %s\n", (char *)__filename);
    exit(0);
}

int __lxstat (int __ver,
              const char *__filename,
              struct stat *__stat_buf)
{
    printf("__lxstat: %s\n", (char *)__filename);
    exit(0);
}
