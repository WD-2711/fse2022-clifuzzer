/* 返回传递给 getopt 库的值的代码，然后可以选择调用实际的 getopt 函数 */
/* 新的 getopt|getopt_long 函数*/
#define _GNU_SOURCE
#include <stdio.h>                                                              
#include <stdlib.h>                                                             
#include <getopt.h>
#include <dlfcn.h>

typedef int (*orig_getopt_type)(int argc, char *const *argv, const char *options);
                                                                                
typedef int (*orig_getopt_long_type)(int argc, char *const *argv, const char *optstring, const struct option *longopts, int *longindex);

/*
argc 参数个数
argv 参数字符串指针
optstring 选项字符串
*/
int getopt (int argc, char *const *argv, const char *optstring)                                                                                                                         
{                                                                               
    int ind;                                                                                                                                   
    printf ("optstring: %s\n", (char*)optstring);                               
    // 接下来调用实际的 getopt 函数，如果不需要则注释掉
    // dlsym(RTLD_NEXT,"getopt") 表示从下一个动态链接库实例中查找名为 getopt 的符号
    /*
    orig_getopt_type orig_getopt;                                               
    orig_getopt = (orig_getopt_type)dlsym(RTLD_NEXT,"getopt");                  
    return orig_getopt(argc, argv, optstring);        
    */
    exit(0);                                                                                                                              
}

/*
与 getopt 相比，多了 long_options 与 opt_index
option 结构体定义如下： 
struct option {
    const char *name;
    int has_arg;
    int *flag;
    int val;
};

*/
int getopt_long (int argc, char *const *argv, const char *options, const struct option *long_options, int *opt_index)                                                                              
{                                                                               
    int ind;                                                                    
    const struct option *p;                                                                                                                               
    printf ("optstring: %s\n", (char*)options);                                                                           
    for (p = long_options; p->name != 0; p++){                                           
        printf("name:%s has_argument:%i\n", p->name, p->has_arg);               
    }
    /*
    orig_getopt_long_type orig_getopt_long;                                     
    orig_getopt_long = (orig_getopt_long_type)dlsym(RTLD_NEXT,"getopt_long");   
    return orig_getopt_long(argc, argv, options, long_options, opt_index);     
    */                                                                       
    exit(0);                                                                                                                          
}

int getopt_long_only (int argc, char *const *argv, const char *options, const struct option *long_options, int *opt_index)                                                              
{                                                                               
    return getopt_long(argc, argv, options, long_options, opt_index);           
}
