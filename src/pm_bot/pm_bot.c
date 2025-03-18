/**
 * This is the main pm_bot program file.
 */

#include "prottrans.h"
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