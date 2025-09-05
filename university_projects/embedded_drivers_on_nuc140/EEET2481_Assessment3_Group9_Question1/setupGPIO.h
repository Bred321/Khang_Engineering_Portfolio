#include <stdio.h>
#include "SYS_init.h"
#include "NUC100Series.h"


void setupGPIO(){
	// --START GPIO INITIALIZATION--
	PC->PMD &= ~(0xFF << 8);
	PC->PMD |= (0b01010101 << 8);
	
	PC->PMD &= ~(0x3 << 28);
	PC->PMD |= (0x1 << 28);
	
	PB->PMD &= ~(0x3 << 30);
	PB->PMD |= (0x0 << 30);
	
	PE->PMD &= ~(0xFFFF << 0);
	PE->PMD |= 0b0101010101010101<<0; 
}