#ifndef GAMEPAD
#define GAMEPAD

// amount of mappable buttons
#define BUTTONS_OVERALL 20

// maximum amount of buttons that can be pressed at once
#define BUTTONS_PRESSED 13

// Amount of joysticks the controller has
#define JOYSTICKS 2
#define len_mapping 7

// actual mapping of controller
#define BRUSH_SPEED_P 5
#define BRUSH_SPEED_M 4
#define BRUSH 1

#define LIFT_UP 12
#define LIFT_DOWN 16

// TODO: make struct array with extra space instead
typedef struct _buttonfunc
{
    int designation;
    void (*function)();
} buttonfunction;


// declare functions using *designated initializer*: {.designation = "00", .function = &button00}
// insert before 0 
//amount of buttons mapped (len of mapping)
extern const buttonfunction mapping[];


//button
void execute(int designation);

// joystick functions
void joystick_right(int coords[]);

void joystick_left(int coords[]);

// test functions
// mapped to start (09)
void testfunction();





#endif