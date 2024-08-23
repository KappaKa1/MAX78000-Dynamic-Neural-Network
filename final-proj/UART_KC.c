/*
 * UART_KC.c
 *
 *  Created on: 21 Aug 2024
 *      Author: teohk
 */
#include <stdio.h>
#include "uart.h"
#include "nvic_table.h"
#include "mxc.h"

#define UART_BAUD           	115200
#define TX_SIZE					20 + 2
#define RX_SIZE					1*28*28
#define UART_SETTING			UART1_IRQn
#define UART_NO					MXC_UART1

static int error = 0;
static mxc_uart_req_t read_req;

/***** Functions for UART*****/
void UART_Handler(void)
{
    MXC_UART_AsyncHandler(UART_NO);
}

void init_UART(void)
{
	// Initiates the UART for Communication
	error = 0;
    	NVIC_ClearPendingIRQ(UART_SETTING);
    	NVIC_DisableIRQ(UART_SETTING);
    	NVIC_SetVector(UART_SETTING, UART_Handler);
    	NVIC_EnableIRQ(UART_SETTING);

	error = MXC_UART_Init(UART_NO, UART_BAUD, MXC_UART_APB_CLK);
    	if (error < E_NO_ERROR) {
        	printf("-->Error initializing UART: %d\n", error);
        	printf("-->Example Failed\n");

        	while (1) {}
    	}
    	else {
        	printf("-->UART Initialized\n\n");
    	}
}

void UART_setup(uint8_t* buffer, uint8_t* output)
{
	// Sets up the Buffer's that will be used for Communication
	read_req.uart = UART_NO;
	read_req.rxData = buffer;
	read_req.txData = output;
	read_req.rxLen = RX_SIZE;
	read_req.txLen = TX_SIZE;
	read_req.callback = NULL;
	return;
}

void UART_start(void)
{
	// Starts the Communication protocol between 2 devices
	MXC_UART_ClearRXFIFO(UART_NO);
	error = MXC_UART_Transaction(&read_req);
}
/*****************************/
