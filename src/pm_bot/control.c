#include "control.h"
#include "servo360.h"
#include "protcom.h"
#include "protutil.h"
#include "gamepad.h"

// extern variable declarations
int brush = 0;
int brush_speed = 10;

// int indicates in which way speed is changed: -1: decreased, 1: increased
void brush_changespeed(int direction)
{
    brush_speed += direction;
    brush_speed = clamp(brush_speed, -128, 128);

    if (brush)
    {
        servo360_speed(BRUSH_PIN_SIGNAL, brush_speed);
    }
}

void brush_toggle()
{
    brush = toggle(brush);
    servo360_speed(BRUSH_PIN_SIGNAL, brush_speed * brush);

    sendack(0);
}

// wrapper functions for controller
void brush_speedinc()
{
    brush_changespeed(1);
    sendack(5);
}

void brush_speeddec()
{
    brush_changespeed(-1);
    sendack(4);
}

// lift portion
void lift_move(int direction)
{
    servo360_angle(LIFT_PIN_SIGNAL, max(servo360_getAngle(LIFT_PIN_SIGNAL) + direction, 0));
}

void lift_ascend()
{
    lift_move(1);
    sendack(12);
}

void lift_descend()
{
    lift_move(-1);
    sendack(16);
}

void control_init()
{
    // set stuff up
    servo360_connect(LIFT_PIN_SIGNAL, LIFT_PIN_FEEDBACK);
    servo360_connect(BRUSH_PIN_SIGNAL, BRUSH_PIN_FEEDBACK);
}


