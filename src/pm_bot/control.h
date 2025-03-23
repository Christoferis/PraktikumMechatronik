#ifndef CONTROL
#define CONTROL

#define LIFT_PIN_FEEDBACK 2
#define LIFT_PIN_SIGNAL 16

#define BRUSH_PIN_FEEDBACK 3
#define BRUSH_PIN_SIGNAL 17

#define LIFT_STEP 10
#define BRUSH_STEP 10

void control_init();

// bot functions
void brush_speedinc();
void brush_speeddec();
void brush_toggle();
void brush_reverse();

void lift_ascend();
void lift_descend();

#endif