#include "protcom.h"
#include "prottrans.h"
#include "simpletools.h"
#include "protutil.h"
#include "gamepad.h"

void receive(char msg[])
{
    // check for parts: b is not always present but j is.
    char* joy = strchrm(msg, 'j');

    // button part (pointer diff if button part present)
    if (joy != 0 && joy != msg)
    {
        // all writes btw are on "global" msg array
        *(joy - 1) = '\r';
        processbuttons(msg);
    }

    //processjoystick(joy);
}

// split and sort
void processjoystick(char* joystick)
{
    printf("joystick\r");
  
    // maximum chars: jr1000,1000\r
    char joysticks[JOYSTICKS][12];
    strtokm(joystick, ';', joysticks);
    
    int i;
    for (i = 0; i < JOYSTICKS; i++)
    {
        switch (joysticks[i][1])
        {
            case 'r':
                joystick_right(joysticks[i] + 2);
                break;

            case 'l':
                joystick_left(joysticks[i] + 2);
                break;

            default:
                senderror(4);
                break;
        }
    }
    
}


void processbuttons(char buttons[])
{
    printf("buttons\r");
  
    // max possible pressed buttons at one time: 13; 3 for designation
    char pressed[BUTTONS_PRESSED][4];
    int splits = strtokm(buttons, ';', pressed);

    int i;
    for (i = 0; i < splits; i++)
    {
        execute(pressed[i] + 1);
    }
}

// sends button acknowledge
void sendack(char* button)
{
    char msg[5];
    msg[0] = 'a';
    msg[4] = '\r';

    msg[1] = 'b';
    msg[2] = button[0];
    msg[3] = button[1];

    sendrequest(msg);
}
