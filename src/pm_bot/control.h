#ifndef CONTROL
#define CONTROL

#define LIFT_PIN_FEEDBACK 2
#define LIFT_PIN_SIGNAL 2

#define BRUSH_PIN_FEEDBACK 2
#define BRUSH_PIN_SIGNAL 2

#define LIFT_STEP 1


void control_init();

// bot functions
void brush_speedinc();
void brush_speeddec();
void brush_toggle();

void lift_ascend();
void lift_descend();

#endif