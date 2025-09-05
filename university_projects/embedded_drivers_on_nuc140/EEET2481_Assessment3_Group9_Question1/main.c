#include <stdio.h>
#include "NUC100Series.h"

void System_Config(void);
void UART0_Config(void);
void UART0_Interrupts(void);
void UART02_IRQHandler(void);

#define STR_SIZE 256


volatile char messages[STR_SIZE]; // string to store sent words
volatile int rx_idx = 0; // index for receiving messages
volatile int tx_idx = 0; // index for sending messages

int main(void) {
    System_Config();
    UART0_Config();
		UART0_Interrupts();
	
    while (1) {
        // Main loop remains idle, functionality is handled by interrupts
    }
}

void System_Config(void) {
    SYS_UnlockReg(); // Unlock protected registers

    // Enable clock sources
    CLK->PWRCON |= (0x01 << 0);
    while (!(CLK->CLKSTATUS & (1 << 0)));

    // PLL configuration starts
    CLK->PLLCON &= ~(1 << 19); // 0: PLL input is HXT
    CLK->PLLCON &= ~(1 << 16); // PLL in normal mode
    CLK->PLLCON &= (~(0x01FF << 0));
    CLK->PLLCON |= 48;
    CLK->PLLCON &= ~(1 << 18); // 0: enable PLLOUT
    while (!(CLK->CLKSTATUS & (1 << 2)));
    // PLL configuration ends

    // CPU clock source selection
    CLK->CLKSEL0 &= (~(0x07 << 0));
    CLK->CLKSEL0 |= (0x02 << 0);    
    // Clock frequency division
    CLK->CLKDIV &= (~0x0F << 0);

    // UART0 Clock selection and configuration
    CLK->CLKSEL1 |= (0b11 << 24); // UART0 clock source is 22.1184 MHz
    CLK->CLKDIV &= ~(0xF << 8);   // Clock divider is 1
    CLK->APBCLK |= (1 << 16);     // Enable UART0 clock

    SYS_LockReg(); // Lock protected registers    
}

void UART0_Config(void) {
    // UART0 pin configuration. PB.1 pin is for UART0 TX, PB.0 for UART0 RX
    PB->PMD &= ~(0b11 << 2);
    PB->PMD |= (0b01 << 2); // PB.1 is output pin
    PB->PMD &= ~(0b11 << 0); // PB.0 is input pin
    SYS->GPB_MFP |= (1 << 1); // GPB_MFP[1] = 1 -> PB.1 is UART0 TX pin
    SYS->GPB_MFP |= (1 << 0); // GPB_MFP[0] = 1 -> PB.0 is UART0 RX pin

    // UART0 operation configuration
    UART0->LCR |= (0b11 << 0); // 8 data bits
    UART0->LCR &= ~(1 << 2);   // One stop bit
    UART0->LCR &= ~(1 << 3);   // No parity bit
    UART0->FCR |= (1 << 1);    // Clear RX FIFO
    UART0->FCR |= (1 << 2);    // Clear TX FIFO
    UART0->FCR &= ~(0xF << 16); // FIFO Trigger Level is 1 byte

    // Baud rate config: BRD/A = 1, DIV_X_EN=0
    // --> Mode 0, Baud rate = UART_CLK/[16*(A+2)] = 22.1184 MHz/[16*(10+2)] = 115200 bps
    UART0->BAUD &= ~(0b11 << 28); // Mode 0	
    UART0->BAUD &= ~(0xFFFF << 0);
    UART0->BAUD |= 10;
}


void UART0_Interrupts(){
	   // Enable UART0 interrupt in NVIC
    NVIC->ISER[0] |= 1 << 12;
    NVIC->IP[3] &= ~(0b11 << 6);

    // Enable UART0 interrupts
    UART0->IER |= (1 << 0); // Enable RX interrupt
    UART0->IER |= (1 << 1); // Enable TX interrupt
}
void UART02_IRQHandler(void) {
    if (UART0->ISR & (1 << 0)) { // RDA interrupt flag
        volatile char received_data = UART0->DATA; // Read received data to clear interrupt

        // Add received data to TX buffer
        if (rx_idx < STR_SIZE) { // Check if buffer is not full
            messages[rx_idx++] = received_data;

            // Enable TX interrupt to start sending data
            UART0->IER |= (1 << 1);
        }

        UART0->ISR = (1 << 0); // Clear the RDA interrupt flag
    }

    if (UART0->ISR & (1 << 1)) { // THRE interrupt flag
        if (messages[tx_idx] != '\0') { // Check if there is data to send
            UART0->DATA = messages[tx_idx++];
        } else {
            // Disable TX interrupt if buffer is empty
            UART0->IER &= ~(1 << 1);

            // Reset indices if no data left
            rx_idx = 0;
            tx_idx = 0;
        }

        UART0->ISR = (1 << 1); // Clear the THRE interrupt flag
    }
}
