#include "gamepad.h"
#include "prottrans.h"
#include "protcom.h"
#include "abdrive360.h"
#include "control.h"

#define COORDS_OFFSET 128

const buttonfunction mapping[] = {
    {.designation = 9, .function = &testfunction},
    {.designation = 0, .function = &brush_toggle},
    {.designation = 14, .function = &brush_speedinc},
    {.designation = 18, .function = &brush_speeddec},
    {.designation = 12, .function = &lift_ascend},
    {.designation = 16, .function = &lift_descend},
    {.designation = 3, .function = &brush_reverse}
}; 

// search and execute
// send back e514
void execute(int designation)
{  
    int i = 0;
    for (i = 0; i < len_mapping; i++)
    { 
        if (mapping[i].designation == designation)
        {
            mapping[i].function();
            return;
        }
    }

    sendack(designation);
    senderror(14);
}

// joysticks: only left one is used (for now)
void joystick_left (int coords[])
{
  //movement
  drive_speed((coords[1] - 128) - (coords[0] - 128), (coords[1] - 128) + (coords[0] - 128));
}

void joystick_right (int coords[])
{
}

// define button functions, if any
// testfunction
void testfunction ()
{ 
    //turns light 28 on or off
    toggle(27);
    sendack(9);
}
