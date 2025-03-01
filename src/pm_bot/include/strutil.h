#ifndef STRUTIL
#define STRUTIL


// returns the amount of times a stringcan be split by a delimiter
int strntok (char* string, char delimiter);

//finds first occurence of a char in a string
char* strchrm(char* string, char c);

//converts a string into an integer (negative support), output is found number
int strtoint(char* string);

//converts integer to string representation, output is len of *out
int inttostr(int num, char* out);

// proves if a char is within ascii range 48 - 57 (numeric values)
int isnumeric(char c);

//flushes an array to \r 
void flushstr(char* string, int len);

#endif
