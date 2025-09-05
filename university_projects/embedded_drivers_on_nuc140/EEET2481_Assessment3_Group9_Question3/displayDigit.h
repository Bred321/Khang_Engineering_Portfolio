#include <stdio.h>
#include "SYS_init.h"
#include "NUC100Series.h"

// Define an array to display each number in COUNT and PAUSE modes
int segment7[10] = {
      0b10000010, // 0
      0b11101110, // 1
      0b00000111, // 2
      0b01000110, // 3
      0b01101010, // 4
      0b01010010, // 5
      0b00010010, // 6
      0b11100110, // 7
      0b00000010, // 8
      0b01000010, // 9
};

// Define an array to display each number in CHECK mode
int segment7_U13[10] = {
	// Same as segment7[10] but turn on the dot
      0b10000000, // 0
      0b11101100, // 1
      0b00000101, // 2
      0b01000100, // 3
      0b01101000, // 4
      0b01010000, // 5
      0b00010000, // 6
      0b11100100, // 7
      0b00000000, // 8
      0b01000000, // 9
};

void turnOnU14(){
	PC->DOUT |= (1 << 4); // U14
	PC->DOUT &= ~(1 << 5); // U13
	PC->DOUT &= ~(1 << 6); // U12
	PC->DOUT &= ~(1 << 7); 	// U11
}

void ToggleU14(){
	PC->DOUT ^= (1 << 4); // U14
	PC->DOUT &= ~(1 << 5); // U13
	PC->DOUT &= ~(1 << 6); // U12
	PC->DOUT &= ~(1 << 7); 	// U11
}

void turnOnU13(){
	PC->DOUT &= ~(1 << 4); // U14
	PC->DOUT |= (1 << 5); // U13
	PC->DOUT &= ~(1 << 6); // U12
	PC->DOUT &= ~(1 << 7); 	// U11
}

void turnOnU12(){
	PC->DOUT &= ~(1 << 4); // U14
	PC->DOUT &= ~(1 << 5); // U13
	PC->DOUT |= (1 << 6); // U12
	PC->DOUT &= ~(1 << 7); 	// U11
}

void turnOnU11(){
	PC->DOUT &= ~(1 << 4); // U14
	PC->DOUT &= ~(1 << 5); // U13
	PC->DOUT &= ~(1 << 6); // U12
	PC->DOUT |= (1 << 7); 	// U11
}


void turnOffDigit(){
	// Turn off all the LED segments
	PE->DOUT |= (1 << 0); // segment c
	PE->DOUT |= (1 << 1); // segment dot
	PE->DOUT |= (1 << 2); // segment f
	PE->DOUT |= (1 << 3); // segment a
	PE->DOUT |= (1 << 4); // segment b
	PE->DOUT |= (1 << 5); // segment d
	PE->DOUT |= (1 << 6); // segment e
	PE->DOUT |= (1 << 7); // segment g
}


void showFourNumbers(int countU11, int countU12,int countU13, int countU14){
	// Show numbers in COUNT and PAUSE modes
	const int delayTime = 1000;
	
	turnOnU11();
	PE->DOUT = segment7[countU11];
	CLK_SysTickDelay(delayTime); // delay to brighten the LED
	turnOffDigit();
	
	turnOnU12();
	PE->DOUT = segment7[countU12];
	CLK_SysTickDelay(delayTime); // delay to brighten the LED
	turnOffDigit();
	
	turnOnU13();
	PE->DOUT = segment7_U13[countU13];
	CLK_SysTickDelay(delayTime); // delay to brighten the LED
	turnOffDigit();
	
	turnOnU14();
	PE->DOUT = segment7[countU14];
	CLK_SysTickDelay(delayTime); // delay to brighten the LED
	turnOffDigit();
}



void showFourNumbersCheckMode(int countU11, int countU12,int countU13, int countU14){
	// Show numbers in CHECK mode
	const int delayTime = 1000; 
	
	turnOnU11();
	PE->DOUT = segment7[countU11];
	CLK_SysTickDelay(delayTime); // delay to brighten the LED
	turnOffDigit();
	
	turnOnU12();
	PE->DOUT = segment7[countU12];
	CLK_SysTickDelay(delayTime); // delay to brighten the LED
	turnOffDigit();
	
	turnOnU13();
	PE->DOUT = segment7[countU13];
	CLK_SysTickDelay(delayTime); // delay to brighten the LED
	turnOffDigit();
	
	turnOnU14();
	PE->DOUT = segment7[countU14];
	CLK_SysTickDelay(delayTime);
	turnOffDigit();
}

void ShowOneNumber(int num){
	PE->DOUT = segment7[num];
}

void ToggleOneNumber(int num){
	PE->DOUT ^= segment7[num];
}





