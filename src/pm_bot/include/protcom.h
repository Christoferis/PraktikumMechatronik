#ifndef PROTCOM
#define PROTCOM

#define COMMAND_CTRL_SWITCH_MODE 's'
#define COMMAND_CTRL_FOLLOW_PATH 'z'
#define COMMAND_CTRL_ULTRA_SWEEP 'u'
#define COMMAND_CTRL_TEST        't'

#define COMMAND_BOT_RADAR 'r'
#define COMMAND_BOT_REACHED 'x'

// main function to process
void receive(char st[]);
void sendintarray(char command, int* array, int len);
void sendvoid(char command);

// to be declared in other c files
/*
  to define a function listed here, just include the header file in a c source file and define the functions
  those functions are called in protcom.c, not defined
  char* is the standard input and represent miscelleanious parameters left for the user to decode using functions in
*/
void switchmode(char st[]);
void followpath(char st[]);
void deepsweep(char st[]);

//exception: this test function declared in protcom.c returns a number and turns on light 27 as a test
void testlight(char st[]);

#endif
