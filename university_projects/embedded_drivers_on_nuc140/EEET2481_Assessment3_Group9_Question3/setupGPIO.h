#include <stdio.h>
#include "SYS_init.h"
#include "NUC100Series.h"


void setupGPIO(){
	// --START GPIO INITIALIZATION--
	PC->PMD &= ~(0xFF << 8);
	PC->PMD |= (0b01010101 << 8);
	
	// Enable GPC10 as output	for frequency verification
	PC->PMD &= ~(0xFF << 20);
	PC->PMD |= (0b01 << 20);
	
	// Enable LED5 - LED8 as output
	PC->PMD &= ~(0xFF << 24);
	PC->PMD |= (0b01010101 << 24);
	
	// Enable button as input
	PB->PMD &= ~(0x3 << 30);
	PB->IMD &= (~(1 << 15)); // set up interrupt mode control - 1 = Level trigger interrupt; 0 = Edge trigger interrupt
	PB->IEN |= (1 << 15); 
	
	// Enable four 7-segment LEDs
	PE->PMD &= ~(0xFFFF << 0);
	PE->PMD |= 0b0101010101010101<<0; 
}

//function to set GPIO mode for key matrix 
void KeyPadEnable(void){
	GPIO_SetMode(PA, BIT0, GPIO_MODE_QUASI);
	GPIO_SetMode(PA, BIT1, GPIO_MODE_QUASI);
	GPIO_SetMode(PA, BIT2, GPIO_MODE_QUASI);
	GPIO_SetMode(PA, BIT3, GPIO_MODE_QUASI);
	GPIO_SetMode(PA, BIT4, GPIO_MODE_QUASI);
	GPIO_SetMode(PA, BIT5, GPIO_MODE_QUASI);
}

//function to scan the key pressed
uint8_t KeyPadScanning(void){
	PA0=1; PA1=1; PA2=0; PA3=1; PA4=1; PA5=1;
	if (PA3==0) return 1;
	if (PA4==0) return 4;
	if (PA5==0) return 7;
	PA0=1; PA1=0; PA2=1; PA3=1; PA4=1; PA5=1;
	if (PA3==0) return 2;
	if (PA4==0) return 5;
	if (PA5==0) return 8;
	PA0=0; PA1=1; PA2=1; PA3=1; PA4=1; PA5=1;
	if (PA3==0) return 3;
	if (PA4==0) return 6;
	if (PA5==0) return 9;
	return 0;
}