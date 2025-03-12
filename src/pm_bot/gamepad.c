#include "gamepad.h"
#include "strutil.h"
#include "abdrive360.h"
#include "prottrans.h"


// search and execute
// send back e514 
void execute(char* designation)
{
    int i = 0;

    for (i = 0; i < len_mapping; i++)
    {
        if (strcmp(mapping[i].designation, designation))
        {
            mapping[i].function();

            return;
        }
    }

    senderror(14);
}

// define button functions, if any


// joysticks
void joystick_left()
{

}

void joystick_right()
{


}