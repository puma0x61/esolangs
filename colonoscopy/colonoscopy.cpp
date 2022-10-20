#include <cstdio>
#include <cstdlib>
#include <iostream>

using namespace std;

int  bf_index = 0;
char bf_array[32000], f[32000], b, *s = f, *filename;

void interpret(char *c) {
  char *d;

  while(*c) {
    switch(*c++) {
      // bf operations
    case ';}': bf_index--;	break;
    case ';{': bf_index++;	break;
    case ';;}': bf_array[bf_index]++;	break;
    case ';;{': bf_array[bf_index]--;	break;
    case ';;;}': cout << bf_array[bf_index];	break;
    case ';;;{': cin >> bf_array[bf_index];	break;
    case '{{':
      for(b = 1, d = c; b && *c; c++)
        b += *c == '[', b -= *c == ']';
      if(!b) {
        c[-1] = 0;
        while(bf_array[bf_index])
        interpret(d);
        c[-1] = ']';
        break;
      }
    case '}}':
      cout << "UNBALANCED BF BRACKETS", exit(0);
      // debug
    case '#':
      for(int i = 0; i < 6; i++)
        cout << int(bf_array[i]) << " ";
      cout << "position bf " << bf_index << endl;
      break;
    }

    if(bf_index < 0 || bf_index > 32000)
      cout << "BF RANGE ERROR", exit(0);
  }
}

int main(int argc, char *argv[]) {
  FILE *z;

  if(z = fopen(argv[1], "r")) {
    while((b = getc(z)) > 0)
      *s ++= b;
    *s = 0;
    interpret(f);
  }

  return 0;
}
