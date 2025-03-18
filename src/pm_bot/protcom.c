#include "protcom.h"
#include "prottrans.h"
#include "simpletools.h"
#include "protutil.h"
#include "strutil.h"
#include "gamepad.h"

// prototypes
void processjoystick(char*);
void processbuttons(char[]);

void receive(char msg[])
{  
    switch (msg[0])
    {
    case 'b':
        processbuttons(msg + 1);
        break;
    
    case 'j':
        processjoystick(msg + 1);
        break;
    default:
        senderror(4);
        break;
    }
}

// only one joystick at a time
// receives r1000,1000\r here
// error 524 for unknown joystick
void processjoystick(char* joystick)
{  
    int xy[2];
    decodeintarray(joystick + 1, xy , 2);
    
    switch (joystick[0])
    {
        case 'r':
            joystick_right(xy);
            break;

        case 'l':
            joystick_left(xy);
            break;

        default:
            senderror(24);
            break;
    }
}

void processbuttons(char buttons[])
{
    int maximalbuttons[11];
    int pressed = decodeintarray(buttons, maximalbuttons, 11);
    
    int i;
    for (i = 0; i < pressed; ++i)
    {
        execute(maximalbuttons[i]);
    }

}

// sends button acknowledge
void sendack(int button)
{
    char msg[5];
    msg[0] = 'a';
    msg[1] = 'b';

    msg[inttostr(button, msg + 2) + 2] = '\r';

    sendrequest(msg);
}
