//Code taken from https://www.gnu.org/software/libc/manual/html_node/Example-of-Getopt.html
//and modified.

#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/stat.h>


//NOTE: Ideally I should have a testcase to test when an option 
//expects a specific value, maybe from a set. COREUTILS implements 
//this in a more complex way. 
//This seems too much work for UT. Will just ignore for now.

int
main (int argc, char **argv)
{
  int aflag = 0;
  char *bvalue = NULL;
  char *cvalue = NULL;
  int index;
  int c;

  opterr = 0;
  struct stat sb;
  while ((c = getopt (argc, argv, "ab:c::")) != -1)
    switch (c)
      {
      case 'a':
        aflag = 1;
        break;
      case 'b':
        bvalue = optarg;
        break;
      case 'c':
        cvalue = optarg;
        break;
      case '?':
        if (optopt == 'c')
          fprintf (stderr, "Option -%c requires an argument.\n", optopt);
        else if (isprint (optopt))
          fprintf (stderr, "Unknown option `-%c'.\n", optopt);
        else
          fprintf (stderr,
                   "Unknown option character `\\x%x'.\n",
                   optopt);
        return 1;
      default:
        if (isprint (optopt))
          fprintf (stderr, "Unknown option `-%c'. Aborting\n", optopt);
        else
          fprintf (stderr, "Unknown option. Aborting\n");
        abort ();
      }

  printf ("aflag = %d, bvalue = %s, cvalue = %s\n",
          aflag, bvalue, cvalue);

  for (index = optind; index < argc; index++){
    printf ("Non-option argument %s\n", argv[index]);
    if (lstat(argv[index], &sb) == -1) {
               perror("lstat");
               exit(EXIT_FAILURE);
    }
    
  }
    
  return 0;
}