/*
 *Code to return values passed to getopt library
 *and then optionally call the actual getopt function
 */
#define _GNU_SOURCE
#include <stdio.h>                                                              
#include <stdlib.h>                                                             
#include <getopt.h>
#include <dlfcn.h>

typedef int (*orig_getopt_type)(int argc, char *const *argv, const char *options);
                                                                                
typedef int (*orig_getopt_long_type)(int argc, char *const *argv, const char *optstring, const struct option *longopts, int *longindex);

int                                                                             
getopt (argc, argv, optstring)                                                  
     int argc;                                                                  
     char *const *argv;                                                         
     const char *optstring;                                                     
{                                                                               
    int ind;                                                                    
                                                                        
    printf ("optstring: %s\n", (char*)optstring);                               
    
    //The next three lines call the actual getopt function
    //Comment out if not needed
    //orig_getopt_type orig_getopt;                                               
    //orig_getopt = (orig_getopt_type)dlsym(RTLD_NEXT,"getopt");                  
    //return orig_getopt(argc, argv, optstring);                                  
    
    exit(0);                                                                                                                              
}

int                                                                             
getopt_long (argc, argv, options, long_options, opt_index)                      
     int argc;                                                                  
     char *const *argv;                                                         
     const char *options;                                                       
     const struct option *long_options;                                         
     int *opt_index;                                                            
{                                                                               
    int ind;                                                                    
    const struct option *p;                                                                                                                               
    printf ("optstring: %s\n", (char*)options);                                                                           
    for (p = long_options; p->name != 0; p++){                                           
        printf("name:%s has_argument:%i\n", p->name, p->has_arg);               
    }
    //The next three lines call the actual getopt_long function
    //Comment out if not needed
    //orig_getopt_long_type orig_getopt_long;                                     
    //orig_getopt_long = (orig_getopt_long_type)dlsym(RTLD_NEXT,"getopt_long");   
    //return orig_getopt_long(argc, argv, options, long_options, opt_index);      
                                                                                
    exit(0);                                                                                                                          
}

int
getopt_long_only (argc, argv, options, long_options, opt_index)             
     int argc;                                                                  
     char *const *argv;                                                         
     const char *options;                                                       
     const struct option *long_options;                                         
     int *opt_index;                                                            
{                                                                               
    return getopt_long(argc, argv, options, long_options, opt_index);           
}
