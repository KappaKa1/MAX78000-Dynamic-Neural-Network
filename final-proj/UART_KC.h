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

#define UART_BAUD           	115200     // Configure this based on the UART settings
#define TX_SIZE					      20 + 2     // Transmit Buffer's size
#define RX_SIZE					      1*28*28    // Receive Buffer's size
#define UART_SETTING			    UART2_IRQn // Configure this based on the UART being used
#define UART_NO					      MXC_UART2  // Configure this based on the UART being used


void init_UART(void); // Initiates UART
void UART_setup(uint8_t* buffer, uint8_t* output); // Sets-up UART for Communication
void UART_start(void); // Starts Communication

#endif /* UART_KC_H_ */
