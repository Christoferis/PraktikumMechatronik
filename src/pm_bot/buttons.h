#ifndef BUTTONS
#define BUTTONS

// amount of mappable buttons
#define BUTTONS_OVERALL 20

// maximum amount of buttons that can be pressed at once
#define BUTTONS_PRESSED 13

// TODO: make struct array with extra space instead
typedef struct _buttonfunc
{
    char* designation;
    void* function;
} buttonfunction;


//button
const char* buttons[] = {"00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "d0", "d1", "d2", "d3", "d4", "d5", "d6", "d7", "14"};

// declare functions using *designated initializer*: {.designation = "00", .function = &button00} 

#endif