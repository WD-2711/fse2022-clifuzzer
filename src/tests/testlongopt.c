//code from https://www.gnu.org/software/libc/manual/html_node/Getopt-Long-Option-Example.html
//and modified.

#include <stdio.h>
#include <stdlib.h>
#include <getopt.h>
#include <limits.h>

/* Flag set by ‘--verbose’. */
static int verbose_flag;

enum
{
  NOARG_DUMMY = CHAR_MAX + 1,
  REQARG_DUMMY,
  OPTARG_DUMMY
};

int
main (int argc, char **argv)
{
  int c;

  while (1)
    {
      static struct option long_options[] =
        {
          /* These options set a flag. */
          {"verbose", no_argument,       &verbose_flag, 1},
          {"brief",   no_argument,       &verbose_flag, 0},
          /* These options don’t set a flag.
             We distinguish them by their indices. */
          {"add",          no_argument,       0, 'a'},
          {"noarg_dummy",  no_argument,       NULL, NOARG_DUMMY},
          {"delete",       required_argument, 0, 'd'},
          {"reqarg_dummy", required_argument, NULL, REQARG_DUMMY},
          {"modify",       optional_argument, 0, 'm'},
          {"optarg_dummy", optional_argument, NULL, OPTARG_DUMMY},
          {0, 0, 0, 0}
        };
      /* getopt_long stores the option index here. */
      int option_index = 0;

      c = getopt_long (argc, argv, "abc:d:m::f::",
                       long_options, &option_index);

      /* Detect the end of the options. */
      if (c == -1)
        break;

      switch (c)
        {
        case 0:
          printf ("option %s\n", long_options[option_index].name);
          break;

        case 'a':
          puts ("option -a\n");
          break;

        case 'b':
          puts ("option -b\n");
          break;

        case 'c':
          printf ("option -c with value `%s'\n", optarg);
          break;

        case 'd':
          printf ("option -d with value `%s'\n", optarg);
          break;

        case 'f':
          if (optarg)
            printf ("option -f with value `%s'\n", optarg);
          else
            printf ("option -f with no value \n");
          break;
        
        case 'm':
          if (optarg)
            printf ("option -m with value `%s'\n", optarg);
          else
            printf ("option -m with no value \n");
          break;

        case NOARG_DUMMY:
          puts("option --noarg_dummy");
          break;
        
        case REQARG_DUMMY:
          printf ("option --reqarg_dummy with value `%s'\n", optarg);
          break;

        case OPTARG_DUMMY:
        if (optarg)
            printf ("option --optarg_dummy with value `%s'\n", optarg);
          else
            printf ("option --optarg_dummy with no value \n");
          break;
  
        case '?':
          /* getopt_long already printed an error message. */
          break;

        default:
          abort ();
        }
    }

  /* Instead of reporting ‘--verbose’
     and ‘--brief’ as they are encountered,
     we report the final status resulting from them. */
  if (verbose_flag)
    puts ("verbose flag is set");

  /* Print any remaining command line arguments (not options). */
  if (optind < argc)
    {
      printf ("non-option ARGV-elements: ");
      while (optind < argc)
        printf ("%s ", argv[optind++]);
      putchar ('\n');
    }

  exit (0);
}