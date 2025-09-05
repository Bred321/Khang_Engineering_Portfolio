#include <stdio.h>
#include "SYS_init.h"
#include "NUC100Series.h"


#define HXT_STATUS 1 << 0
#define LXT_STATUS 1 << 1


void enableClockSource(){

	// --START SYSTEM INITIALIZATION--
	// Expected Output: Enable HXT and LXT clock sources
	// Enable HXT
	CLK->PWRCON |= (1 << 0);
	while(!(CLK->CLKSTATUS & HXT_STATUS));
	
	CLK->PWRCON |= (1 << 1);
	while(!(CLK->CLKSTATUS & LXT_STATUS));
	
	// Select HXT as clock source
	CLK->CLKSEL0 &= ~(0x7 << 0);
	
	// Set power mode
	CLK->PWRCON &= ~(1 << 7);
	
	// Set up CLKDIV
	CLK->CLKDIV &= ~(0xF << 0);
	
	// --END SYSTEM INITIALIZATION--
}