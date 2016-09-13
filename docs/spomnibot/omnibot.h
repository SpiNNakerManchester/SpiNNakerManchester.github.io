/*
 * omnibot.h
 * handles sensorimotor data from omnibot
 *  Created on: 10.10.2012
 *      Author: denk
 */

#ifndef OMNIBOT_H_
#define OMNIBOT_H_

#include <stm32f4xx.h>
#include "spin_link.h"
#include "leds.h"

#define TOPKEY 0xFFFFFFFF
#define NUM_SENSORS_VALUE_CODING 6+3+3+3+3+4

#define DEL_LOWER_16 0xFFFF0000
#define DEL_UPPER_16 0x0000FFFF


//Defines for Motor Commands
#define X_DECAY 0.9f
#define Y_DECAY 0.9f
#define T_DECAY 0.9f

// ------------------------------------------------------------ //
// 						MGMT DEFINITIONS						//
// ------------------------------------------------------------ //

//BIT FOR MANAGEMENT: bit 10 i.e. 0x400
#define 	MGMT_BIT 									0x400			//If set within a received MC key, it indicates a MGMT packet


//Actuators:
#define		MOTION_FORWARD								0x01			//Motion commands in "x,y,r" space, -70...+70
#define		MOTION_BACK									0x02
#define		MOTION_RIGHT								0x03
#define		MOTION_LEFT									0x04
#define		MOTION_CLOCKWISE							0x05
#define		MOTION_C_CLKWISE                            0x06
#define		MOTION_STOP									0x07



//Not implemented yet, but soon to come...

#define		WHEEL_0_VEL_CLKWISE							0x10			//Motion commands in wheel space, -70...+70
#define		WHEEL_0_VEL_C_CLKWISE						0x11
#define		WHEEL_0_VEL_STOP							0x12
#define		WHEEL_1_VEL_CLKWISE							0x13
#define		WHEEL_1_VEL_C_CLKWISE						0x14
#define		WHEEL_1_VEL_STOP							0x15
#define		WHEEL_2_VEL_CLKWISE							0x16
#define		WHEEL_2_VEL_C_CLKWISE						0x17
#define		WHEEL_2_VEL_STOP							0x18
#define		WHEEL_VEL_ALL_STOP							0x19			// Stop all wheel immediately


#define		RESET_ROB									0x1A			// Entirely resets the Robot (i.e. all velocities to zero)
#define		BEEP										0x1B			// Emit single beep
#define		BEEP_BEEP									0x1C			// Emit double beep


#define		ENABLE_VELOCITY_CONTROL						0x20			// Enable DIRECT velocity control, Default is ENABLE
#define		DISABLE_VELOCITY_CONTROL					0x21

#define		WHEEL_0_ANGULAR_POSITION					0x30			//in deg, no rate coding
#define		WHEEL_1_ANGULAR_POSITION					0x31
#define		WHEEL_2_ANGULAR_POSITION					0x32

#define		WHEEL_0_PWM_SIGNAL							0x33			//PWM in ys, -640...+640, no rate coding
#define		WHEEL_1_PWM_SIGNAL							0x34
#define		WHEEL_2_PWM_SIGNAL							0x35



//---------------------------------------------------------------------
//---------------------------------------------------------------------

//SENSORS:

#define		RATE_CODING_ACTUATORS_ENABLE				0x40			//Payload == 1 enables rate coding for actuators, payload==0 disables rate coding
#define		RATE_CODING_SENSORS_ENABLE					0x41			//Payload == 1 enables rate coding for sensors, payload==0 disables rate coding
#define 	OMNIBOT_XY									0x42			//Payload indicates the X and Y address of the Omnibot Sensors in the upper 16bit (X(8bit) Y(8bit) DATA(16bit)). The lower 16bit will be ignored
#define 	EDVS1_XY									0x43 			//Payload indicates the X and Y address of the first EDVS sensor in the upper 16bit (X(8bit) Y(8bit) DATA(16bit)). The lower 16bit will be ignored
#define 	EDVS2_XY									0x44			//Payload indicates the X and Y address of the second EDVS sensor in the upper 16bit (X(8bit) Y(8bit) DATA(16bit)). The lower 16bit will be ignored
#define 	EDVS1_ENABLE								0x45			//Payload == 1 --> Enable Retina || Payload == 0 --> Disable Retina
#define 	EDVS2_ENABLE								0x46			//Payload == 1 --> Enable Retina || Payload == 0 --> Disable Retina


#define		BUMP0										0x50			//If Rate Coding Enable >> "frequentspikes", else: Payload == 1 --> BUMP pressed, payload==0 --> BUMP released
#define		BUMP1										0x51
#define		BUMP2										0x52
#define		BUMP3										0x53
#define		BUMP4										0x54
#define		BUMP5										0x55

#define		WHEEL_0_VEL_POSITIVE						0x60			//Upper 16bit are IGNORED! (Set using OMNIBOT_XY)
#define		WHEEL_0_VEL_NEGATIVE						0x61
#define		WHEEL_1_VEL_POSITIVE						0x62			//If Rate-Coding: frequency corresponds to absolute value, else: payload (positive or negative) contains absolute value
#define		WHEEL_1_VEL_NEGATIVE						0x63			//Negative neurons not used when rate coding is disabled
#define		WHEEL_2_VEL_POSITIVE						0x64
#define		WHEEL_2_VEL_NEGATIVE						0x65

#define		GYRO_x_POSITIVE								0x70			//If Rate-Coding: frequency corresponds to absolute value, else: payload (positive or negative) contains absolute value
#define		GYRO_x_NEGATIVE								0x71			//Negative neurons not used when rate coding is disabled
#define		GYRO_y_POSITIVE								0x72
#define		GYRO_y_NEGATIVE								0x73			//Upper 16bit are IGNORED! (Set using OMNIBOT_XY)
#define		GYRO_z_POSITIVE								0x74
#define		GYRO_z_NEGATIVE								0x75

#define		ACCEL_x_POSITIVE							0x80			//If Rate-Coding: frequency corresponds to absolute value, else: payload (positive or negative) contains absolute value
#define		ACCEL_x_NEGATIVE							0x81			//Negative neurons not used when rate coding is disabled
#define		ACCEL_y_POSITIVE							0x82
#define		ACCEL_y_NEGATIVE							0x83			//Upper 16bit are IGNORED! (Set using OMNIBOT_XY)
#define		ACCEL_z_POSITIVE							0x84
#define		ACCEL_z_NEGATIVE							0x85

#define		EULER_x_POSITIVE							0x90			//If Rate-Coding: frequency corresponds to absolute value, else: payload (positive or negative) contains absolute value
#define		EULER_x_NEGATIVE							0x91			//Negative neurons not used when rate coding is disabled
#define		EULER_y_POSITIVE							0x92
#define		EULER_y_NEGATIVE							0x93			//Upper 16bit are IGNORED! (Set using OMNIBOT_XY)
#define		EULER_z_POSITIVE							0x94
#define		EULER_z_NEGATIVE							0x95

#define		COMPASS_0_POSITIVE							0x100			//If Rate-Coding: frequency corresponds to absolute value, else: payload (positive or negative) contains absolute value
#define		COMPASS_0_NEGATIVE							0x101			//Negative neurons not used when rate coding is disabled
#define		COMPASS_1_POSITIVE							0x102
#define		COMPASS_1_NEGATIVE							0x103			//Upper 16bit are IGNORED! (Set using OMNIBOT_XY)
#define		COMPASS_2_POSITIVE							0x104
#define		COMPASS_2_NEGATIVE							0x105
#define		COMPASS_3_POSITIVE							0x106
#define		COMPASS_3_NEGATIVE							0x107

// ------------------------------------------------------------ //
// 					END MGMT DEFINITIONS						//
// ------------------------------------------------------------ //

#define MOTOR_COMMAND_CYCLE 100
#define MOTOR_INIT_COMMAND_CYCLE 10000
#define TIMEOUT_MS 5000


typedef struct {
	//gyro:
	int32_t g_0;
	int32_t g_1;
	int32_t g_2;

	//Accelerometer:
	int32_t a_0;
	int32_t a_1;
	int32_t a_2;

	//Euler:
	int32_t e_0;
	int32_t e_1;
	int32_t e_2;

	//Compass:
	int32_t c_0;
	int32_t c_1;
	int32_t c_2;
	int32_t c_3;

	//Bump:
	uint8_t bump;

	//Wheel Velocities:
	int32_t w_0;
	int32_t w_1;
	int32_t w_2;


} omnisensors_t;

//Functions
uint8_t omnibot_sensor_data_handler(char* buffer, uint32_t buff_length);
uint8_t omnibot_init();
int32_t decay_speeds();
int32_t send_motor_command_rate_coding();
int32_t send_motor_command_value_coding();
int32_t omnibot_command_cycle();
void value_coding(spin_link_pkg_t *);
int32_t manage_neurons(uint32_t key, uint32_t payload);

//Global Variables
extern int32_t timeout_var;
extern uint32_t MGMT_ARRAY[0x200];
extern int32_t x_accumulator;
extern int32_t x_payload_speed;
extern int32_t y_accumulator;
extern int32_t y_payload_speed;
extern int32_t t_accumulator;
extern int32_t t_payload_speed;
extern uint32_t omniAvailFlag;
extern omnisensors_t robotSensorData;

#endif /* OMNIBOT_H_ */
