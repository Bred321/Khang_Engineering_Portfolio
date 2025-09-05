#include <stdio.h>
#include "SYS_init.h"
#include "NUC100Series.h"
#include "enableClockSource.h"
#include "setupGPIO.h"
#include "enableTimer0.h"
#include "displayDigit.h"
#include "setupInterrupts.h"

#define BOUNCING_DLY 100000
int num = 0;


int main(void)
{
	// -- SYSTEM INITIALIZATION --
	SYS_UnlockReg();
	
	// System configuration
	enableClockSource();
	// Enable Timer 0
	enableTimer0();
	// Set up GPIO
	setupGPIO();
	// Enable Key Matrix
	KeyPadEnable();
	// Set up Interrupt
	setupInterrupt();
	
	SYS_LockReg();
	
	// -- MAIN OPERATION --
	while(1){
	}
}



void TMR1_IRQHandler(){
	// Timer 0 Interrupt
	PC->DOUT ^= (1 << 15);
	ToggleU14();
	ShowOneNumber(num);
	TIMER1->TISR |= (1 << 0);
}

void EINT1_IRQHandler(){
	// External Button GPB15 Interrupt
	++num;
	if(num > 9){num = 0;}
	PB->ISRC |= (1 << 15);
}

