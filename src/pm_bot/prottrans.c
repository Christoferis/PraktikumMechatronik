#include "prottrans.h"
#include "fdserial.h"
#include "protcom.h"
#include "strutil.h"
#include "propeller.h"
#include "abdrive360.h"

// defines
#define lenmsg 128
#define pingtime 500

// file wide variables
fdserial *con = 0;
int countdown = pingtime;
int pingprogress = 0;
int newping = 0;

void readString(char st[]);

// prototypes
void send(char header, char st[]);

// this function will be run in a cog
void sink()
{
  int happened = -1;
  
  char msg[lenmsg];

  if (con == 0)
  {
    con = fdserial_open(8, 7, 0, 115200);
  }

  while (1)
  {

    // ping section
    if (fdserial_rxCount(con) < 1)
    {
      newping++;
      
      if (newping == pingtime)
      {
        send('m', "\r");
        newping = 0;
      }

      //reset servos if no message (joysticks should always be sent): only if servos are there
      //drive_speed(0, 0);

      pause(10);
      continue;
    } else { //bot should only ping when timeouting
      newping = 0;
    }
    
    readString(msg);
    
    switch (msg[0])
    {
    case 'm':
      send('p', "\r");

      if (pingprogress == 1)
      {
        pingprogress = 0;
      }
      break;

    case 'p':
      pingprogress = 0;
      break;

    case 'r':
      receive(msg + 1);
      break;

    // echo back to host since logging is done on host, but host wouldnt send e in first place
    case 'e':
      break;

    default:
      send('e', "404\r");
      break;
    }    
  }
}

// send a msg through the protocol (internal function)
void send(char header, char st[])
{
  int lockid = locknew();
  int i;
  char c = 0;

  while (!lockset(lockid));


  fdserial_txChar(con, header);

  for (i = 0; i < lenmsg && c != '\r'; i++)
  {
    c = st[i];
    fdserial_txChar(con, c);
  }

  lockclr(lockid);
  lockret(lockid);
}

void sendrequest(char st[])
{
  send('r', st);
}

// only use a two digit number, as a 5 is going to be prefixed anyway
void senderror(int number)
{
  // more just as a buffer (just in case)
  char err[16];

  int digit = inttostr(number + 500, err);
  err[digit] = '\r';

  send('e', err);
}

void sendlog(char st[])
{
  send('l', st);
}

// won't wait if no message received (like java implementation)
void readString(char st[])
{
  char c = 0;
  int i = 0;

  for (i = 0; i < lenmsg && (c != '\r' && c != '\n'); ++i)
  {
    c = fdserial_rxChar(con);    
    st[i] = c;
  }

  ++i;

  // fill the rest with zeroes to reset array
  for (; i < lenmsg; i++)
  {
    st[i] = 0;
  }
}
