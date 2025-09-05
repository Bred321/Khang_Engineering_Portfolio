#include <stdio.h>
#include "SYS_init.h"
#include "NUC100Series.h"

#define TIMER1_COUNT 6000000-1


void enableTimer0(){
	// Select HCLK clock source
	CLK->CLKSEL1 &= ~(0x7 << 12);
	//CLK->CLKSEL1 |= (0x1 << 12);
	
	// Enable timer 0
	CLK->APBCLK |= (1 << 3);
	
	// Set up timer 0
	TIMER1->TCSR &= ~(0xFF << 0);
	TIMER1->TCSR |= (1 << 26);
	//TIMER0->TCSR |= (0xB << 0); // Prescaler
	
	// Timer 0 operation mode
	TIMER1->TCSR &= ~(0x3 << 27);
	TIMER1->TCSR |= (0x1 << 27);
	TIMER1->TCSR &= ~(1 << 24); 
	
	// Update value to TDR continuously
	TIMER1->TCSR |= (1 << 16);
	
	// Interrupt enable bit
	TIMER1->TCSR |= (1 << 29);
	
	// Set up compare value
	TIMER1->TCMPR = TIMER1_COUNT;
	
	TIMER1->TCSR |= (1 << 30);
}