#include <stdio.h>
#include "SYS_init.h"
#include "NUC100Series.h"

void setupInterrupt(){
  // Interrupt for Timer 0
	NVIC->ISER[0] |= (1 << 8);
	NVIC->IP[2] &= ~(0x3 << 6);

  // GPB15 Interrupt
  NVIC->ISER[0] |= (1 << 3);
	NVIC->IP[0] &= ~(0x3 << 30);
}