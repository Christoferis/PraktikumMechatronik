#ifndef PROTUTIL
#define PROTUTIL

#define FLOAT_ENCODE 1000


// decodes data into integer array
//output is the length of bytes written to the array
int decodeintarray(char* data, int* array, int len);

// encodes int array into data
void encodeintarray(int* array, int len, char* out);



#endif
