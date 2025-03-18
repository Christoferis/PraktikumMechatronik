/**
 * This is the main pm_bot program file.
 */

#include "simpletools.h"
#include "prottrans.h"
#include "servo360.h"
#include "abdrive360.h"
#include "gamepad.h"

int main(void)
{
  // race conditions
  pause(50);

  // starting servo cog
  cog_run(&sink, 512);
  
  pause(50);

  
  return 0;
}