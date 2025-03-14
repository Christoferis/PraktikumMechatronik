#include "protutil.h"
#include "strutil.h"

//utility file to handle datatypes for the protocol


int decodeintarray(char *data, int *array, int len)
{
  int i = 0;

  while (i < len)
  {
    array[i++] = strtoint(data);

    // go to next
    data = strchrm(data, ',');
    if (!data) {
        break;
    }

    // increment to next starting number (while loop stops at ,)
    data++;
  }

  return i;
}

void encodeintarray(int *array, int len, char *out)
{
  int i;
  out += inttostr(array[0], out);

  for (i = 1; i < len; i++)
  {
    // inttostr returns written bytes aka pointer to last digit -> write comma -> increment + 2 to skip comma and to get to new area

    *out = ',';
    out += 1;
    out += inttostr(array[i], out);
  }

  *out = '\r';
}
