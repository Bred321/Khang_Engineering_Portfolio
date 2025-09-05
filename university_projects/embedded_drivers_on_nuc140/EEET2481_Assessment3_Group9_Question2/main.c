#include <stdio.h>
#include "SYS_init.h"
#include "NUC100Series.h"
#include "enableClockSource.h"
#include "setupGPIO.h"
#include "enableTimer0.h"
#include "displayDigit.h"
#include "setupInterrupts.h"

#define BOUNCING_DLY 100000

// Pre-defined functions
void countingLogic();
void stateLEDs();
void changeState();
void scanKeyPress();
void recordTime();

// Display value for each segment
int countU11 = 0;
int countU12 = 0;
int countU13 = 0;
int countU14 = 0;

// An array for each segment to store the time laps
int U12_values[5] = {0, 0, 0, 0, 0};
int U13_values[5] = {0, 0, 0, 0, 0}; 
int U14_values[5] = {0, 0, 0, 0, 0};
int lap_num = 0;
int disp_lap_num = 1;
int disp_lap_pos = 0;

// Value to track pressed key
uint8_t pressed_key = 0;

// Enum type to store the program states
enum program_states {IDLE, CNT, PAUSE, CHECK}; // define three program modes: Idle, Counting, and Stop
enum program_states state;

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
		scanKeyPress(); // Scan which key is pressed
		changeState(); // Change the state when a key is pressed
	}
}

void countingLogic(){
	if (countU14 == 10){
		countU14 = 0;
		++countU13;
	}  
	if (countU13 == 10){
		countU13 = 0;
		++countU12;
	} 
	if (countU12 == 6){
		// Increase 1 min at 59 sec
		countU12 = 0;
		++countU11;
	}
	if (countU11 == 10){
		countU11 = 0;
	}
	++countU14;
}

void TMR0_IRQHandler(){
	// Timer 0 Interrupt
	PC->DOUT ^= (1 << 10);
	countingLogic();
	TIMER0->TISR |= (1 << 0);
}

void EINT1_IRQHandler(){
	// External Button GPB15 Interrupt
	++disp_lap_num;
	++disp_lap_pos;
	if(disp_lap_num == 6){disp_lap_num = 1;}
	if(disp_lap_pos == 5){disp_lap_pos = 0;}
	PB->ISRC |= (1 << 15);
}

void stateLEDs(){
	// LEDs display for each mode
	switch(state){
		case IDLE:
			// Turn on LED5, turn off LED6 and LED7
			PC->DOUT &= ~(1 << 12);
			PC->DOUT |= (1 << 13);
			PC->DOUT |= (1 << 14);
			PC->DOUT |= (1 << 15);
			countU11 = countU12 = countU13 = countU14 = 0;
			break;
		case CNT:
			// Turn on LED6, turn off LED5 and LED7
			PC->DOUT |= (1 << 12);
			PC->DOUT &= ~(1 << 13);
			PC->DOUT |= (1 << 14);
			PC->DOUT |= (1 << 15);
			break;
		case PAUSE:
			// Turn on LED7, turn off LED5 and LED6
			PC->DOUT |= (1 << 12);
			PC->DOUT |= (1 << 13);
			PC->DOUT &= ~(1 << 14);
			PC->DOUT |= (1 << 15);
			break;
		case CHECK:
			// Turn on LED7 and LED8, turn off LED5 and LED6
			PC->DOUT |= (1 << 12);
			PC->DOUT |= (1 << 13);
			PC->DOUT &= ~(1 << 14);
			PC->DOUT &= ~(1 << 15);
			break;
		default:
			PC->DOUT &= ~(1 << 12);
			PC->DOUT |= (1 << 13);
			PC->DOUT |= (1 << 14);
			PC->DOUT |= (1 << 15);
			countU11 = countU12 = countU13 = countU14 = 0;
			break;
	}
}

void changeState(){
	// State transition logic
	// Pressing K1 Key logic
	if(pressed_key == 1){
		switch(state){
			case IDLE:
				state = CNT;
				// Start counting when transitioning to Count Mode
				TIMER0->TCSR |= (1 << 30);
				break;
			case CNT:
				state = PAUSE;	
				// Halt the counting at the Pause mode
				TIMER0->TCSR &= ~(1 << 30);
				break;
			case PAUSE:
				state = CNT;
				// Continue counting when transitioning from Pause to Count Mode
				TIMER0->TCSR |= (1 << 30);
				break;
			default:
				//state = IDLE;
				break;		
		}
	}
	// Pressing K9 Key logic
	if(pressed_key == 9){
		switch(state){
			case PAUSE:
				// Move to IDLE MODE if pressing K9 in PAUSE mode
				state = IDLE;
				break;
			case CNT:
				// Record timestamp if pressing K9 in COUNT mode
				recordTime();
				break;
			default:
				//state = IDLE;
				break;
		}
	}
	// Pressing K5 Key logic
	if(pressed_key == 5){
		switch(state){
			case PAUSE:
				// Move to  CHECK mode if pressing K5 in PAUSE mode
				state = CHECK;
				break;
			case CHECK:
				// Move back to PAUSE mode if pressing K5 in CHECK mode
				state = PAUSE;
				showFourNumbers(countU11, countU12, countU13, countU14);
				break;
			default:
				//state = IDLE;
				break;
		}
	}
	// Reset key press to 0
	pressed_key = 0;
	// Bouncing Delay logic
	CLK_SysTickDelay(BOUNCING_DLY);
}


void scanKeyPress(){
	// Check which key is pressed in the key matrix
	while (pressed_key==0) {
	pressed_key = KeyPadScanning(); // scan for key press activity
	// Display four numbers for each segment
	if (state != CHECK){
		// Display in COUNT and PAUSE modes
		showFourNumbers(countU11, countU12, countU13, countU14);
	} else {
		// Display in CHECK mode
		showFourNumbersCheckMode(disp_lap_num, U12_values[disp_lap_pos], U13_values[disp_lap_pos], U14_values[disp_lap_pos]);
	}
	stateLEDs();
	}
}

void recordTime(){
	// Record the timestamp logic
	U12_values[lap_num] = countU12;
	U13_values[lap_num] = countU13;
	U14_values[lap_num] = countU14;
	++lap_num; // increase the lap number when GPB15 is pressed
	if(lap_num == 5){
		lap_num = 0;
	}
}
