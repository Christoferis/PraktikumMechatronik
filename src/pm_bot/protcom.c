#include "protcom.h"
#include "prottrans.h"
#include "simpletools.h"
#include "protutil.h"

void receive(char msg[])
{
    //one byte command header
  char* datablock = msg + 1;
  
  switch (msg[0])
  {
    case COMMAND_CTRL_SWITCH_MODE:
        switchmode(datablock);
        break;

    case COMMAND_CTRL_FOLLOW_PATH:
        followpath(datablock);
        break;

    case COMMAND_CTRL_ULTRA_SWEEP:
        deepsweep(datablock);
        break;

    case COMMAND_CTRL_TEST:
        testlight(datablock);
        break;

    default:
        senderror(4);
        break;
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
