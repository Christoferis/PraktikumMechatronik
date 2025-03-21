#ifndef STRUTIL
#define STRUTIL

#define MAX_LEN 256

// returns the amount of times a stringcan be split by a delimiter
int strntok (char* string, char delimiter);

// splits a string into substrings by delimiter
int strtokm(char* string, char delimiter, char **destination);

// finds first occurence of a char in a string
char* strchrm(char* string, char c);

// compares two strings
int strcmpm(char* str1, char* str2);

// converts a string into an integer (negative support), output is found number
int strtoint(char* string);

// converts integer to string representation, output is len of *out
int inttostr(int num, char* out);

// proves if a char is within ascii range 48 - 57 (numeric values)
int isnumeric(char c);

// flushes an array to \r 
void flushstr(char* string, int len);

#endif
