#include "strutil.h"
#include "math.h"

// own string library to cut down in memory usage (string.h bad)
#define MAX_LOOPS 256

// amount of tokens a string can be split into
int strntok (char* string, char delimiter)
{
  //no trailing comma (n) -> can be split into n + 1 token
  int count = 1;

  // start with one for the chance if a delimiter is directly at the beginning
  int prev = 1;

  int i = 0;  
  char c;
  while ((c = string[i]) != '\r') {

    if (c == delimiter && !prev) {
      prev = 1;
      count++;
    } else if (c != delimiter) {
      prev = 0;
    }

    i++;
  }

  return count;
}

int strtokm(char* string, char delim, char** dest)
{
  int i = 0;
  int splits = 0; 
  int sec = 0; 
  char c = string[i];
  
  // to prevent redundant code 
  while((c = string[i]) != '\r' && (++i) == i) {
    if (c != delim) {
      dest[splits][sec] = string[i];
      sec++;
    } else {
      // add in \r at the end before moving
      dest[splits][sec] = '\r';
      splits++;
      sec = 0; 
    }
  }

  return splits + 1;
}

// finds a certain character in a string and returns a pointer to that spot
char *strchrm(char *string, char c)
{
  int i = 0;
  int found = 0;
  while (string[i] && string[i] != '\r' && i < MAX_LOOPS)
  {
    if (string[i] == c)
    {
      found = 1;
      break;
    }

    i++;
  }

  if (found)
  {
    return string + i;
  }
  else
  {
    return 0;
  }
}

//TODO: match stringarray method

// compares two strings
int strcmpm(char *str1, char *str2)
{
  int i = 0;

  for (int i = 0; (i < MAX_LEN) && str1[i] == str2[i]; i++)
  {
    if (str1[i] == '\r' || str1[i] == '\0')
    {
      return 1;
    }

    return 0;
  }

}

// converts a string into a integer
// stops either when a char is not a number or if end of string
int strtoint(char *string)
{
  int out = 0;
  int i = 0;
  int negative = 0;
  char current = string[0];

  // check for minus sign at the beginning
  if (current == '-')
  {
    current = string[1];
    negative = 1;
  }

  while (isnumeric(current) && i < MAX_LOOPS)
  {
    out = out * 10 + (current - 48);
    i++;

    // one bit offset due to negative number
    current = string[i + negative];
  }

  return negative ? out * -1 : out;
}

int inttostr(int num, char *out)
{
  int negative = 0;

  if (num < 0)
  {
    negative = 1;
    num *= -1;
    out[0] = '-';
  }

  int i;
  int digits = num == 0 ? 1 : (int)(floor(log10((double)num)) + 1) + negative;
  int prev = 0;

  for (i = negative; i < digits; i++)
  {
    // isolates current digit
    int isolated = num / pow(10, digits - 1 - i) - prev;
    out[i] = isolated + 48;
    prev = (prev + isolated) * 10;
  }

  return digits;
}

//function to prove if a char is a representation of a number
// ascii range: 48 - 57
int isnumeric(char c)
{
  return c >= 48 && c <= 57;
}

//make sure to flush appropriately
void flushstr(char* string, int len)
{
  int i;

  for (i = 0; i < len; i++) {
      string[i] = '\r';
  }
}
