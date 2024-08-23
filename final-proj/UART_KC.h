/*
 * UART_KC.h
 *
 *  Created on: 21 Aug 2024
 *      Author: teohk
 */

#ifndef UART_KC_H_
#define UART_KC_H_

#include <stdio.h>
#include "uart.h"
#include "nvic_table.h"
#include "mxc.h"

#define UART_BAUD           	115200
#define TX_SIZE					20
#define RX_SIZE					1*28*28
#define UART_SETTING			UART2_IRQn
#define UART_NO					MXC_UART2


void init_UART(void); // Initiates UART
void UART_setup(uint8_t* buffer, uint8_t* output); // Sets-up UART for Communication
void UART_start(void); // Starts Communication

#endif /* UART_KC_H_ */
