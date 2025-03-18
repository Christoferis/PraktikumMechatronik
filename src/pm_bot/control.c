#include "control.h"
#include "servo360.h"
#include "protcom.h"
#include "protutil.h"
#include "gamepad.h"

// extern variable declarations
volatile int lift = 0;
int brush = 0;
int brush_speed = 10;
int lift_step = 1;

// prototypes for good measure
// void control_run(void);
// void control_loop(void);

// void lift_move(int);

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
}

void control_init()
{
    // set stuff up
    servo360_connect(LIFT_PIN_SIGNAL, LIFT_PIN_FEEDBACK);
    servo360_connect(BRUSH_PIN_SIGNAL, BRUSH_PIN_FEEDBACK);



    // while (1)
    // {
    //     // brush section
    //     servo360_speed(BRUSH_PIN_SIGNAL, brush_speed * brush);
        
    //     // lift section -> sends the ack back itself

    //     if (lift * lift == 1)
    //     {
    //         servo360_goto(LIFT_PIN_SIGNAL, lift_step * lift);

    //         if (lift)
    //         {
    //             sendack(LIFT_UP);
                
    //         } else
    //         {
    //             sendack(LIFT_DOWN);
    //         }

    //         lift = 0;
    //     }

    // }

}


