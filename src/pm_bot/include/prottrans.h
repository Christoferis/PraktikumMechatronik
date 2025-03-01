#ifndef PROTTRANS
#define PROTTRANS

//should be run in a cog
void sink();

//sends generic string to host
void sendrequest(char st[]);
void senderror(int number);
void sendlog(char st[]);

#endif