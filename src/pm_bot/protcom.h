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


// send functions
void sendack(int button);


#endif
