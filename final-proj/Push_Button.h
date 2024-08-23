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


//Means P2.6, to select percentage
#define MXC_GPIO_PB_PORT_IN              MXC_GPIO2
#define MXC_GPIO_PB_PIN_IN               MXC_GPIO_PIN_6

//Means P2.7, to start inference
#define MXC_GPIO_PB_PORT_IN_2            MXC_GPIO2
#define MXC_GPIO_PB_PIN_IN_2             MXC_GPIO_PIN_7

static mxc_gpio_cfg_t gpio_perc;
static mxc_gpio_cfg_t gpio_start;

void initiate_PB(void);
int button_pushed(void);

#endif /* PUSH_BUTTON_H_ */
