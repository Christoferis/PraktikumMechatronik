#include "control.h"
#include "servo360.h"
#include "protcom.h"
#include "protutil.h"
#include "gamepad.h"


// boolean: brush on / off
int brush = 0;
int brush_speed = 50;

//angle of lift as variable
int lift_pos = 0;

// int indicates in which way speed is changed: -1: decreased, 1: increased
void brush_changespeed(int direction)
{
    brush_speed += direction;
    brush_speed = clamp(brush_speed, -720, 720);

    if (brush)
    {
        servo360_speed(BRUSH_PIN_SIGNAL, brush_speed);
    }
}

void brush_toggle()
{
    if (brush)
    {
      brush = 0;
    } else {
      brush = 1;
    }
  
    servo360_speed(BRUSH_PIN_SIGNAL, brush_speed * brush);

    sendack(0);
}

// wrapper functions for controller
void brush_speedinc()
{
    brush_changespeed(BRUSH_STEP);
}

void brush_speeddec()
{
    brush_changespeed(-BRUSH_STEP);
}

void brush_reverse()
{
  brush_changespeed(-brush_speed);
}

// lift portion
void lift_move(int direction)
{
    servo360_angle(LIFT_PIN_SIGNAL, max(servo360_getAngle(LIFT_PIN_SIGNAL) + direction, 0));
}

void lift_ascend()
{
    lift_move(LIFT_STEP);
}

void lift_descend()
{
    lift_move(-LIFT_STEP);
}

void control_init()
{
    // set stuff up
    servo360_connect(LIFT_PIN_SIGNAL, LIFT_PIN_FEEDBACK);
    servo360_connect(BRUSH_PIN_SIGNAL, BRUSH_PIN_FEEDBACK);
}


