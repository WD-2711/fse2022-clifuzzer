%{
/*
 * License - GNU General Public License v3.0
 * Copyright (C) 2007 Free Software Foundation, Inc for the license
 * Adapted from https://github.com/meyerd/flex-bison-example/blob/master/calc.y
 * Changes made - removed floating and mixed expressions. Limited only to
 * addition of int calculations.
 */
#include <stdio.h>
#include <stdlib.h>

extern int yylex();
extern int yyparse();
extern FILE* yyin;

void yyerror(const char* s);
%}

%union {
    int ival;
}

%token<ival> T_INT
%token T_PLUS T_LEFT T_RIGHT
%token T_NEWLINE T_QUIT
%left T_PLUS

%type<ival> expression

%start calculation

%%

calculation:
       | calculation line
;

line: T_NEWLINE
    | expression T_NEWLINE { printf("\tResult: %i\n", $1); }
    | T_QUIT T_NEWLINE { printf("bye!\n"); exit(0); }
;

expression: T_INT               { $$ = $1; }
      | expression T_PLUS expression    { $$ = $1 + $3; }
      | T_LEFT expression T_RIGHT       { $$ = $2; }
;


%%

int main() {
    yyin = stdin;

    do {
        yyparse();
    } while(!feof(yyin));

    return 0;
}

void yyerror(const char* s) {
    fprintf(stderr, "Parse error: %s\n", s);
    exit(1);
}
