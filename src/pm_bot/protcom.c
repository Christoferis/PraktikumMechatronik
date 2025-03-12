#include "protcom.h"
#include "prottrans.h"
#include "simpletools.h"
#include "protutil.h"
#include "gamepad.h"

void receive(char msg[])
{
    // check for parts: b is not always present but j is.
    char* joystick = strchrm(msg, 'j');

    // button part (pointer diff if button part present)
    if (joystick != msg)
    {
        // all writes btw are on "global" msg array
        *(joystick - 1) = '\r';
        processbuttons(msg);
    }

    //joystick part
    // 0: x, 1: y
    int right[2];
    int left[2];

    

}


void processbuttons(char buttons[])
{
    // max possible pressed buttons at one time: 13; 3 for designation
    char pressed[BUTTONS_PRESSED][3];
    int splits = strtokm(buttons, ';', pressed);

    int i;
    for (i = 0; i < splits; i++)
    {
        execute(*(pressed[i]) + 1);
    }
}


void sendintarray(char command, int* array, int len)
{
    char out[MAX_MSG];
    out[0] = command;

    encodeintarray(array, len, out + 1);
    sendrequest(out);
}

void sendvoid(char command)
{
    char c[2];
    c[0] = command;
    c[1] = '\r';

    sendrequest(c);
}

// declared here as testfunction
void testlight(char st[])
{
    int data[16];
    int len = decodeintarray(st, data, 16);
    sendintarray(COMMAND_CTRL_TEST, data, len);
}

void deepsweep(char st[]) {
    int num_points;
    if (decodeintarray(st, &num_points, 1) == 1) {
        mode_1_deep_sweep(num_points);
    }
}

void followpath(char st[]) {
    int parameters[2];
    if (decodeintarray(st, parameters, 2) == 2) {
        mode_1_set_destination(parameters[0], parameters[1]);
    }
}

void switchmode(char st[]) {
    int mode;
    if (decodeintarray(st, &mode, 1) == 1) {
        switch (mode) {
        case 1:
            switch_mode_to_manual();
            break;
        case 2:
            switch_mode_to_maze();
            break;
        default:
            switch_mode_to_manual();
            senderror(42);
            break;
        }
    }
}
