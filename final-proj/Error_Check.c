/*
 * Error_Check.c
 *
 *  Created on: 21 Aug 2024
 *      Author: teohk
 */
#include "mxc.h"
#include <string.h>
#include <stdio.h>

void print_matrix(uint32_t image[]) {
    printf("\n\t{\\\n");

    for (int row = 0; row < 28; row++){
        // Print the first 4 bytes of the current row
        printf("0x%x",image[row * 7]);

        // Print the rest of the 4-byte segments in the row
        for (int col = 1; col < 7; col++) {
            printf(",0x%x",image[row * 7 + col]);
        }

        printf(", \ \n");
    }

    printf("\t}\n");
}

void print_buffer(uint32_t * addr)
{
	printf("\n\t{\\\n");

	for (int row = 0; row < 28; row++){
	    // Print the first 4 bytes of the current row
	    printf("0x%x",*((volatile uint32_t *) addr));
	    *addr++;
	    // Print the rest of the 4-byte segments in the row
	    for (int col = 1; col < 7; col++) {
	        printf(",0x%x",*((volatile uint32_t *) addr));
	        *addr++;
	    }

	    printf(", \ \n");
	}

	    printf("\t}\n");
}
