/**
 * This is the main pm_bot program file.
 */

#include "simpletools.h"
#include "prottrans.h"
#include "servo360.h"
#include "abdrive360.h"
#include "gamepad.h"
#include "control.h"

int main(void)
{
  pause(50);
  control_init();

  pause(50);

  // run sink
  sink();

  return 0;
}