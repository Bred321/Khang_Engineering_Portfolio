#include <stdio.h>
#include "SYS_init.h"
#include "NUC100Series.h"

void handleResetButton(int* countU13, int* countU14){
	if(!(PB->PIN & 1 << 15)){
		*countU13 = 0;
		*countU14 = 0;
		TIMER1->TISR |= (1 << 0); // clear the flag
	}
}

void handlePausedButton(){
	while(!(PB->PIN & 1 << 15));
}