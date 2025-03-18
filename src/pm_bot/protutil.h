#ifndef PROTUTIL
#define PROTUTIL

#define FLOAT_ENCODE 1000

// also some very basic math functions
#define max(a, b) ((a < b) ? b : a)
#define min(a, b) ((a < b) ? a : b)
#define clamp(v, imin, imax) (min(imax, max(v, imin)))

// toggles a boolean value
#define toggle(v) (v ? 0 : 1)

// decodes data into integer array
//output is the length of bytes written to the array
int decodeintarray(char* data, int* array, int len);

// encodes int array into data
void encodeintarray(int* array, int len, char* out);



#endif
