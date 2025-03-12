#ifndef GAMEPAD
#define GAMEPAD

// amount of mappable buttons
#define BUTTONS_OVERALL 20

// maximum amount of buttons that can be pressed at once
#define BUTTONS_PRESSED 13

// Amount of joysticks the controller has
#define JOYSTICKS 2
#define len_mapping 1

// TODO: make struct array with extra space instead
typedef struct _buttonfunc
{
    char* designation;
    void (*function)();
} buttonfunction;


extern const char* buttons[];
extern const buttonfunction mapping[];

//button
void execute(char* designation);

// joystick functions
void joystick_right(char* string);

void joystick_left(char* string);

// test functions
// mapped to start (09)
void testfunction();


// declare functions using *designated initializer*: {.designation = "00", .function = &button00}
// insert before 0 

//amount of buttons mapped (len of mapping)


#endif