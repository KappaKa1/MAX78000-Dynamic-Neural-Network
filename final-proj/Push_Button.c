/*
 * Push_Button.c
 *
 *  Created on: 22 Aug 2024
 *      Author: teohk
 */
// visit website below for more details
// https://github.com/ahn-github/MAX78000_SDK/blob/master/Examples/MAX78000/GPIO/main.c


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
static int perc = 100;

void initiate_PB(void)
{
	// High when not pressed, Low when pressed
	gpio_perc.port = MXC_GPIO_PB_PORT_IN;
	gpio_perc.mask = MXC_GPIO_PB_PIN_IN;
	gpio_perc.pad = MXC_GPIO_PAD_PULL_UP;
	gpio_perc.func = MXC_GPIO_FUNC_IN;
	MXC_GPIO_Config(&gpio_perc);

	gpio_start.port = MXC_GPIO_PB_PORT_IN_2;
	gpio_start.mask = MXC_GPIO_PB_PIN_IN_2;
	gpio_start.pad = MXC_GPIO_PAD_PULL_UP;
	gpio_start.func = MXC_GPIO_FUNC_IN;
	MXC_GPIO_Config(&gpio_start);

	return;
}


int button_pushed(void)
{
	// High when not pressed, Low when pressed
	printf("The current percentage is %d%\n", perc);
	while(1)
	{
		if (!(MXC_GPIO_InGet(gpio_perc.port, gpio_perc.mask)))
		{
			if (perc == 100) perc = 25;
			else perc = perc + 25;
			while(!(MXC_GPIO_InGet(gpio_perc.port, gpio_perc.mask)));
			MXC_Delay(1000);
			printf("The current percentage selected is %d%\n", perc);
	    }
		if (!(MXC_GPIO_InGet(gpio_start.port, gpio_start.mask)))
		{
			return perc;
		}
		MXC_Delay(5000);
	}
	return -1;
}


