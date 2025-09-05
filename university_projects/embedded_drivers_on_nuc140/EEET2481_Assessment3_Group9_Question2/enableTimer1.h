#include <stdio.h>
#include "SYS_init.h"
#include "NUC100Series.h"

#define TIMER0_COUNT 1200000-1


void enableTimer0(){
	// Select HCLK clock source
	CLK->CLKSEL1 &= ~(0x7 << 8);
	CLK->CLKSEL1 |= (0x1 << 8);
	
	// Enable timer 0
	CLK->APBCLK |= (1 << 2);
	
	// Set up timer 1
	TIMER0->TCSR &= ~(0xFF << 0);
	TIMER0->TCSR |= (1 << 26);
	//TIMER0->TCSR |= (0xB << 0); // Prescaler
	
	// Timer 1 operation mode
	TIMER0->TCSR &= ~(0x3 << 27);
	TIMER0->TCSR |= (0x1 << 27);
	TIMER0->TCSR &= ~(1 << 24); 
	
	// Update value to TDR continuously
	TIMER0->TCSR |= (1 << 16);
	
	// Interrupt enable bit
	TIMER0->TCSR |= (1 << 29);
	
	// Set up compare value
	TIMER0->TCMPR = TIMER0_COUNT;
	
	// Start counting
	TIMER0->TCSR |= (1 << 30);
}