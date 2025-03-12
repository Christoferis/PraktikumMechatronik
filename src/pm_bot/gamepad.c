#include "gamepad.h"
#include "strutil.h"
#include "abdrive360.h"
#include "prottrans.h"
#include "protcom.h"


const char* buttons[] = {"00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "d0", "d1", "d2", "d3", "d4", "d5", "d6", "d7", "14"};
const buttonfunction mapping[] = {{.designation = "09", .function = &testfunction}}; 

// search and execute
// send back e514 
void execute (char* designation)
{
    int i = 0;

    for (i = 0; i < len_mapping; i++)
    {
        if (strcmpm(mapping[i].designation, designation))
        {
            mapping[i].function();
            sendack(designation);
            return;
        }
    }

    sendack(designation);
    senderror(14);
}

// define button functions, if any


// joysticks
void joystick_left (char* coords) {

}

void joystick_right (char* coords)
{


}


// testfunction
void testfunction ()
{
    //turns light 28 on or off
    toggle(28);
}