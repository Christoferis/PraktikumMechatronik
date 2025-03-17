#include "control.h"
#include "servo360.h"
#include "protcom.h"
#include "gamepad.h"


void control_run()
{
    // set stuff up
    servo360_connect(LIFT_PIN_SIGNAL, LIFT_PIN_FEEDBACK);
    servo360_connect(BRUSH_PIN_SIGNAL, BRUSH_PIN_FEEDBACK);


    while (1)
    {
        // brush section
        servo360_speed(BRUSH_PIN_SIGNAL, brush_speed * brush);
        
        // lift section -> sends the ack back itself

        if (lift * lift == 1)
        {
            servo360_goto(LIFT_PIN_SIGNAL, lift_step * lift);

            if (lift)
            {
                sendack(LIFT_UP);
                
            } else
            {
                sendack(LIFT_DOWN);
            }

            lift = 0;
        }

    }
    

}