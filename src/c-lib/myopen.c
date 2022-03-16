/*
 *Code to return values passed to getopt library
 *and then optionally call the actual getopt function
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <dlfcn.h>
#include <dirent.h>


typedef FILE (*orig_fopen) (const char * filename, const char * mode );

typedef DIR (*orig_opendir) (const char *name);

typedef int (*orig_open_f_type)(const char *pathname, int flags);

int
open(const char *pathname, int flags,...)
{
    printf("open: %s\n", (char *)pathname);
    //The next three lines call the actual open function
    //Comment out if not needed
    //orig_open_f_type orig_open;
    //orig_open = (orig_open_f_type)dlsym(RTLD_NEXT,"open");
    //return orig_open(pathname,flags);

    exit(0);
}

FILE
*fopen(filename, mode)
    const char *filename;
    const char *mode;
{
    printf ("fopen: %s\n", (char*) filename);
    exit(0);
}


DIR
*opendir
(const char *name)
{
    printf("diropen: %s\n", (char*) name);
    exit(0);
}
