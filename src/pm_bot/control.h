#ifndef CONTROL
#define CONTROL

#define LIFT_PIN_FEEDBACK 2
#define LIFT_PIN_SIGNAL 2

#define BRUSH_PIN_FEEDBACK 2
#define BRUSH_PIN_SIGNAL 2


void control_run();

//control flags

// three way boolean: 0 (normal), -1 (down), 1 (up);
extern volatile int lift = 0;

// three way boolean
extern int brush = 0;

extern int brush_speed = 10;

// how many degrees per tick
extern int lift_step = 1;

//



#endif