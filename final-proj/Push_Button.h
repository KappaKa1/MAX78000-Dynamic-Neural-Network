/*
 * Push_Button.h
 *
 *  Created on: 22 Aug 2024
 *      Author: teohk
 */

#ifndef PUSH_BUTTON_H_
#define PUSH_BUTTON_H_

#include <stdio.h>
#include <string.h>
#include "mxc_device.h"
#include "nvic_table.h"
#include "mxc.h"
#include "board.h"
#include "gpio.h"


// Configure P2.6 to Input to modify Percentage
#define MXC_GPIO_PB_PORT_IN              MXC_GPIO2
#define MXC_GPIO_PB_PIN_IN               MXC_GPIO_PIN_6

// Configure P2.7 to Input to start Inference
#define MXC_GPIO_PB_PORT_IN_2            MXC_GPIO2
#define MXC_GPIO_PB_PIN_IN_2             MXC_GPIO_PIN_7

// Variables used for reading pins
static mxc_gpio_cfg_t gpio_perc;
static mxc_gpio_cfg_t gpio_start;

void initiate_PB(void); // Initiates the Push Buttons
int button_pushed(void); // Wait for any user interaction of the push buttons

#endif /* PUSH_BUTTON_H_ */
