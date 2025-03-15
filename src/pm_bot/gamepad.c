#include "gamepad.h"
#include "strutil.h"
#include "abdrive360.h"
#include "prottrans.h"
#include "protcom.h"


const buttonfunction mapping[] = {{.designation = 9, .function = &testfunction}}; 

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

    senderror(14);
}

// joysticks
void joystick_left (char* coords)
{
}

void joystick_right (char* coords)
{
}

// define button functions, if any
// testfunction
void testfunction ()
{
    //turns light 28 on or off
    toggle(27);
}