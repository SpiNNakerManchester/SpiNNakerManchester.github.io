// -------------------------------------------------------------------------
// $Id$
// -------------------------------------------------------------------------
// COPYRIGHT
// Copyright (c) The University of Manchester, 2012. All rights reserved.
// SpiNNaker Project
// Advanced Processor Technologies Group
// School of Computer Science
// -------------------------------------------------------------------------
// Project            : SpiNNaker link to AER sensor interface
// Module             : top-level module
// Author             : Simon Davidson/Jeff Pepper
// Status             : Review pending
// $HeadURL$
// Last modified on   : $Date$
// Last modified by   : $Author$
// Version            : $Revision$
// -------------------------------------------------------------------------

`timescale 1ns / 1ps

 module spinn_aer_if 
(
    external_clk,
    ext_res_sel,
    ext_7seg,
    ext_strobe,
    data_2of7_to_spinnaker,
    ack_from_spinnaker,
    LED2_OUT,
    volt_test,
    aer_req,
    aer_data,
    aer_ack,
    reset,
    LED3_OUT,
    LED4_OUT
);

input        reset;
output       LED3_OUT;
input        external_clk;
output [6:0] data_2of7_to_spinnaker;
input        ack_from_spinnaker;
output       LED2_OUT;
output       volt_test;
output       LED4_OUT;

input        aer_req;
input [15:0] aer_data;
output       aer_ack;

// 7-segment display signals 
input        ext_res_sel;
output [7:0] ext_7seg;
output [3:0] ext_strobe;


//---------------------------------------------------------------
// constants
//---------------------------------------------------------------
// mode and resolution values
localparam RESOL_BITS  = 4;
localparam RET_128_DEF = 0;
localparam RET_64_DEF  = RET_128_DEF + 1;
localparam RET_32_DEF  = RET_64_DEF  + 1;
localparam RET_16_DEF  = RET_32_DEF  + 1;
localparam COCHLEA_DEF = RET_16_DEF  + 1;
localparam DIRECT_DEF  = COCHLEA_DEF + 1;
localparam RET_128_ALT = DIRECT_DEF  + 1;
localparam RET_64_ALT  = RET_128_ALT + 1;
localparam RET_32_ALT  = RET_64_ALT  + 1;
localparam RET_16_ALT  = RET_32_ALT  + 1;
localparam COCHLEA_ALT = RET_16_ALT  + 1;
localparam DIRECT_ALT  = COCHLEA_ALT + 1;
localparam LAST_VALUE  = DIRECT_ALT;

// alternative chip coordinates
localparam CHIP_ADDR_DEF = 16'h0200;
localparam CHIP_ADDR_ALT = 16'hfefe;


//---------------------------------------------------------------
// internal signals
//---------------------------------------------------------------
// Signals for 'event dump mode'
reg       dump_mode_r;
reg [4:0] wait_counter_r;

wire [15:0]  i_aer_data;
reg          i_aer_ack;
//---------------------------------------------------------------


//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//----------------------------- tasks ---------------------------
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//---------------------------------------------------------------
// BCD to 7-segment converter
// seven segment encoding:
// bcd2sevenSeg[6:0] = abcdefg
//---------------------------------------------------------------
function [6:0] bcd2sevenSeg;
input [3:0] bcd;
begin  
  case (bcd)
     0:    bcd2sevenSeg = 7'b000_0001;
     1:    bcd2sevenSeg = 7'b100_1111;
     2:    bcd2sevenSeg = 7'b001_0010;
     3:    bcd2sevenSeg = 7'b000_0110;
     4:    bcd2sevenSeg = 7'b100_1100;
     5:    bcd2sevenSeg = 7'b010_0100;
     6:    bcd2sevenSeg = 7'b110_0000;
     7:    bcd2sevenSeg = 7'b000_1111;
     8:    bcd2sevenSeg = 7'b000_0000;
     9:    bcd2sevenSeg = 7'b000_1100;
    10:    bcd2sevenSeg = 7'b111_1111;  // space
    11:    bcd2sevenSeg = 7'b111_0010;  // c
    12:    bcd2sevenSeg = 7'b110_0010;  // o
    13:    bcd2sevenSeg = 7'b110_1000;  // h
  default: bcd2sevenSeg = 7'b111_1111;  // all segments off

  endcase
end
endfunction
//---------------------------------------------------------------

//---------------------------------------------------------------
// 2-of-7 NRZ data encoder (SpiNNaker interface)
//---------------------------------------------------------------
 function [6:0] code_2of7_lut ;
  input   [4:0] din;
  input   [6:0] code_2of7;

	casez(din)
		5'b00000 : code_2of7_lut = code_2of7 ^ 7'b0010001; // 0
		5'b00001 : code_2of7_lut = code_2of7 ^ 7'b0010010; // 1
		5'b00010 : code_2of7_lut = code_2of7 ^ 7'b0010100; // 2
		5'b00011 : code_2of7_lut = code_2of7 ^ 7'b0011000; // 3
		5'b00100 : code_2of7_lut = code_2of7 ^ 7'b0100001; // 4
		5'b00101 : code_2of7_lut = code_2of7 ^ 7'b0100010; // 5
		5'b00110 : code_2of7_lut = code_2of7 ^ 7'b0100100; // 6
		5'b00111 : code_2of7_lut = code_2of7 ^ 7'b0101000; // 7
		5'b01000 : code_2of7_lut = code_2of7 ^ 7'b1000001; // 8
		5'b01001 : code_2of7_lut = code_2of7 ^ 7'b1000010; // 9
		5'b01010 : code_2of7_lut = code_2of7 ^ 7'b1000100; // 10
		5'b01011 : code_2of7_lut = code_2of7 ^ 7'b1001000; // 11
		5'b01100 : code_2of7_lut = code_2of7 ^ 7'b0000011; // 12
		5'b01101 : code_2of7_lut = code_2of7 ^ 7'b0000110; // 13
		5'b01110 : code_2of7_lut = code_2of7 ^ 7'b0001100; // 14
		5'b01111 : code_2of7_lut = code_2of7 ^ 7'b0001001; // 15
		5'b1???? : code_2of7_lut = code_2of7 ^ 7'b1100000; // EOP
		default  : code_2of7_lut = 7'bxxxxxxx;
	endcase;
 endfunction;
//---------------------------------------------------------------
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//--------------------------- dump mode -------------------------
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
initial wait_counter_r = 5'b000000;
always @(posedge clk)
 begin
   if (i2_spinnaker_ack != old_spinnaker_ack)
	  wait_counter_r <= 5'b000000; // Ack from spinnaker resets counter
	else
	  wait_counter_r <= wait_counter_r + 1;
	end
 
initial dump_mode_r = 1'b0;
always @(posedge clk)
 begin
   if (i2_spinnaker_ack != old_spinnaker_ack)
	  dump_mode_r <= 1'b0; // Leave dump mode once Spinnaker responds
   else if ((wait_counter_r == 5'b11111)&&(if_state != 0))
	  dump_mode_r <= 1'b1; // Enter dump mode once 31 cycles of no response have passed
 end
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 

//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//------------------------- synchronisers -----------------------
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//---------------------------------------------------------------
// AER sensor request line synchroniser //
//---------------------------------------------------------------
reg     i1_aer_req;
reg     i2_aer_req;
initial i1_aer_req  = 1;
initial i2_aer_req  = 1;

always @(posedge clk)
 begin
  i1_aer_req  <= i_aer_req;
  i2_aer_req  <= i1_aer_req;
 end
//---------------------------------------------------------------

//---------------------------------------------------------------
// Synchronise the acknowledge coming from the SpiNNaker async i/f
//---------------------------------------------------------------
reg i1_spinnaker_ack;
reg i2_spinnaker_ack;
initial i1_spinnaker_ack  = 1'b0;
initial i2_spinnaker_ack  = 1'b0;

always@(posedge clk)
	begin
	 i1_spinnaker_ack <= i_spinnaker_ack;
	 i2_spinnaker_ack <= i1_spinnaker_ack;
	end
//---------------------------------------------------------------
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//---------------------------- mapper ---------------------------
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
reg [RESOL_BITS - 1:0] resolution;
reg             [15:0] chip_addr;


reg   [8:0] if_state;
reg         ack_bit_r;
reg   [6:0] i_spinnaker_data;
reg   [4:0] nibble_and_a_bit;
reg  [39:0] packet;
reg         old_spinnaker_ack;
reg  [14:0] coords;
wire  [6:0] new_x, new_y;
wire        sign_bit;
initial     if_state = 0;
initial     i_spinnaker_data = 0;
initial     i_aer_ack = 1;

//---------------------------------------------------------------
// New on 04/05/2012. Rotate image by 90 degrees clockwise:
//---------------------------------------------------------------
assign new_x = 7'b1111111 - i_aer_data[14:8]; // new_X = 127 - old_Y
assign new_y = 7'b1111111 - i_aer_data[7:1];  // new_Y = 127 - old_X
assign sign_bit = i_aer_data[0];
//---------------------------------------------------------------

//---------------------------------------------------------------
// device and resolution selection 
//---------------------------------------------------------------
always @(*)
  case (resolution)
    RET_128_DEF, // retina 128x128 mode
    RET_128_ALT: coords = {sign_bit, new_y, new_x};

    RET_64_DEF,  // retina 64x64 mode
    RET_64_ALT:  coords = {sign_bit, 2'b00, new_y[6:1], new_x[6:1]};

    RET_32_DEF,  // retina 32x32 mode
    RET_32_ALT:  coords = {sign_bit, 4'b0000, new_y[6:2], new_x[6:2]};

    RET_16_DEF,  // retina 16x16 mode
    RET_16_ALT:  coords = {sign_bit, 6'b000000, new_y[6:3], new_x[6:3]};

    COCHLEA_DEF, // cochlea mode
    COCHLEA_ALT: coords = {3'b000, i_aer_data[1], 3'b000, i_aer_data[7:2],i_aer_data[9:8]};

    DIRECT_DEF,  // straight-through mode
    DIRECT_ALT:  coords = i_aer_data[14:0];

    default:     // make the retina 128x128 mode the default
                 coords = {sign_bit, new_y, new_x};
  endcase
//---------------------------------------------------------------

//---------------------------------------------------------------
// virtual chip address selection
//---------------------------------------------------------------
always @(*)
  case (resolution)
    RET_128_DEF,
    RET_64_DEF,
    RET_32_DEF,
    RET_16_DEF,
    COCHLEA_DEF,
    DIRECT_DEF:  chip_addr = CHIP_ADDR_DEF;
 
    RET_128_ALT,
    RET_64_ALT,
    RET_32_ALT,
    RET_16_ALT,
    COCHLEA_ALT,
    DIRECT_ALT:  chip_addr = CHIP_ADDR_ALT;

    default:     chip_addr = CHIP_ADDR_DEF;
  endcase
//---------------------------------------------------------------
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//------------------------- spiNN driver ------------------------
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
always @(posedge clk)
 begin
 if(debounce_reset == 1)
  begin
   if_state <= 0;
	i_spinnaker_data <= 0;
	i_aer_ack <= 1;
  end
 else
  case(if_state)
   0 :  if(i2_aer_req == 0)
	      begin
			 packet <= {chip_addr, i_aer_data[15], coords, 4'h0, 4'h0}; //create spinnaker packet
			 if_state <= if_state + 1;
			end
	1 :   begin
	       // parity bit is ~(^packet[39:1])
          nibble_and_a_bit <= {1'b0, packet[3:1], ~(^packet[39:1])};         			 
			 if_state <= if_state + 1;
			end
  	2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22
     :   begin
			 i_spinnaker_data <= code_2of7_lut(nibble_and_a_bit, i_spinnaker_data); //transmit 2of7 code to spinnaker
		    packet <= packet >> 4;                                                 //shift the next packet nibble down	 
			 old_spinnaker_ack <= i2_spinnaker_ack;
			 if_state <= if_state + 1;
			end
   3, 5, 7, 9, 11, 13, 15, 17, 19 // set the nibble 
     :   begin
	       nibble_and_a_bit[3:0] <= packet[3:0];
	       if(i2_spinnaker_ack != old_spinnaker_ack) if_state <= if_state +1; //wait for ack from spinnaker
			end
	21 :  begin // set eop
          nibble_and_a_bit[4] <= 1;
	       if(i2_spinnaker_ack != old_spinnaker_ack) if_state <= if_state +1;
	      end
	23 :  if(i2_spinnaker_ack != old_spinnaker_ack) // wait for ack from spinnaker then send ack back to AER sensor
          begin
			  i_aer_ack <= 0;
			  if_state <= if_state +1;
			 end
	24 :  if(i2_aer_req == 1) // wait for AER sensor to "see" the ack then take the ack away
			   begin
				 i_aer_ack <= 1;
 			    if_state <= 0;
	         end
	default: ;
  endcase; 
 end

//---------------------------------------------------------------
// Generate ack bit to AER sensor
//---------------------------------------------------------------
initial ack_bit_r = 1'b1;
always@(posedge clk)
 begin
   if (dump_mode_r) // Ack all requests
	  begin
	    if (!i2_aer_req)
		   ack_bit_r <= 1'b0; // Ack this request
		 else
		   ack_bit_r <= 1'b1; // Stop acknowledging - the request has gone away
	  end
   else
	  begin
	  // When not in dump mode, ack when state machine says, but only if req
	  // is still present (req may have been acked previously by dump_mode state machine,
	  // so don't confuse things by acking again):
	  ack_bit_r <= i_aer_ack | i2_aer_req;
	  end
 end
//---------------------------------------------------------------
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 
  
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//----------------------- leds and buttons ----------------------
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//---------------------------------------------------------------
// Flash LED2 (activity indicator)
//---------------------------------------------------------------
reg  [23:0] STATE;
initial STATE <= 0;

always @(posedge clk)
  if(STATE == 24'hFFFFFF) STATE <= 0;
  else STATE <= STATE +1;
//---------------------------------------------------------------
  
//---------------------------------------------------------------
// Debounce for reset switch
//---------------------------------------------------------------
reg [19:0] debounce_state;
reg        debounce_reset;
reg [2:0]  bounce;
initial debounce_state = 0;
initial debounce_reset = 0;
initial bounce = 0;

always @(posedge clk)
 begin
  bounce[1] <= bounce[0];
  bounce[0] <= ~i_reset;  
  if(bounce[2] != bounce[1]) 
   begin
    bounce[2] <= bounce[1];
    debounce_state <= 0;
   end
  else if(debounce_state == 'hfffff)
   debounce_reset <= bounce[2];
  else
   debounce_state <= debounce_state +1;
 end
//---------------------------------------------------------------

// ---------------------------------------------------------
// Debounce for resolution select switch
// ---------------------------------------------------------
reg [19:0] res_debounce_state;
reg        res_sel_debounced;
reg [2:0]  res_bounce;

initial
begin
  res_debounce_state = 0;
  res_sel_debounced = 1;
  res_bounce = 3'b111;
end

always @(posedge clk)
 begin
  res_bounce[1] <= res_bounce[0];
  res_bounce[0] <= res_sel;  
  if(res_bounce[2] != res_bounce[1]) 
   begin
    res_bounce[2] <= res_bounce[1];
    res_debounce_state <= 0;
   end
  else if(res_debounce_state == 'hfffff)
   res_sel_debounced <= res_bounce[2];
  else
   res_debounce_state <= res_debounce_state + 1;
 end
// ---------------------------------------------------------
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 
  
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//------------------ mode and resolution select -----------------
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// ---------------------------------------------------------
// mode and resolution select
// ---------------------------------------------------------
reg       sel_state;

// ---------------------------------------------------------
// only one resolution change per button press
// ---------------------------------------------------------
initial sel_state  = 0;

always @(posedge clk)
  if(debounce_reset == 1)
    sel_state <= 0;
  else
    if (res_sel_debounced == 1'b0)
      sel_state <= 1;
    else
      sel_state <= 0;
// ---------------------------------------------------------

// ---------------------------------------------------------
// sequence through resolutions
// ---------------------------------------------------------
initial resolution = 3'b000;

always @(posedge clk)
  if(debounce_reset == 1)
    resolution <= 3'b000;
  else
    if ((sel_state == 0) && (res_sel_debounced == 1'b0))
    begin
      if (resolution == LAST_VALUE)
        resolution <= 0;
      else
        resolution <= resolution + 1;
    end
// ---------------------------------------------------------
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//------------------------ display driver -----------------------
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// ---------------------------------------------------------
// display current resolution in 7-segment displays
// ---------------------------------------------------------
always @(posedge clk)
begin
 case (resolution)
   RET_128_DEF,
   RET_128_ALT:
     begin
       digit[0] = 10;
       digit[1] = 1;
       digit[2] = 2;
       digit[3] = 8;
     end

   RET_64_DEF,
   RET_64_ALT:
     begin
       digit[0] = 10;
       digit[1] = 10;
       digit[2] = 6;
       digit[3] = 4;
     end

   RET_32_DEF,
   RET_32_ALT:
     begin
       digit[0] = 10;
       digit[1] = 10;
       digit[2] = 3;
       digit[3] = 2;
     end

   RET_16_DEF,
   RET_16_ALT:
     begin
       digit[0] = 10;
       digit[1] = 10;
       digit[2] = 1;
       digit[3] = 6;
     end

   COCHLEA_DEF,
   COCHLEA_ALT:
     begin
       digit[0] = 11;
       digit[1] = 12;
       digit[2] = 11;
       digit[3] = 13;
     end

   DIRECT_DEF,
   DIRECT_ALT:
     begin
       digit[0] = 0;
       digit[1] = 0;
       digit[2] = 0;
       digit[3] = 0;
     end
 endcase
end
// ---------------------------------------------------------

// ---------------------------------------------------------
// 7-segment display driver
// ---------------------------------------------------------
reg [3:0] digit[0:3];
reg [3:0] point;
reg [1:0] curr_digit;
reg [7:0] o_7seg;
reg [3:0] o_strobe;

//---------------------------------------------------------------
// use decimal point to signal alternate chip_address
//---------------------------------------------------------------
always @(*)
  case (resolution)
    RET_128_DEF,
    RET_64_DEF,
    RET_32_DEF,
    RET_16_DEF,
    COCHLEA_DEF,
    DIRECT_DEF:  point = 4'b1111;
 
    RET_128_ALT,
    RET_64_ALT,
    RET_32_ALT,
    RET_16_ALT,
    COCHLEA_ALT,
    DIRECT_ALT:  point = 4'b1110;

    default:     point = 4'b1111;
  endcase
//---------------------------------------------------------------

//---------------------------------------------------------------
// current digit selection
//---------------------------------------------------------------
initial
begin
  curr_digit = 0;
  digit[0] = 10;
  digit[1] = 10;
  digit[2] = 10;
  digit[3] = 10;
  point    = 4'b1111;
  o_strobe = 4'b0000;
  o_7seg   = 8'b1111_1111;
end

always @(posedge display_clk)
begin
  curr_digit <= curr_digit + 1;
end

always @(posedge display_clk)
begin
  case (curr_digit)
    0: o_strobe <= 4'b0001;
    1: o_strobe <= 4'b0010;
    2: o_strobe <= 4'b0100;
    3: o_strobe <= 4'b1000;
  endcase
end

always @(posedge display_clk)
begin
  o_7seg <= {point[curr_digit], bcd2sevenSeg(digit[curr_digit])};
end
// ---------------------------------------------------------


// ---------------------------------------------------------
// display clock generator (external clock scaled down)
// ---------------------------------------------------------
`define PRESCALE_BITS 14

reg                   display_clk;
reg                   prescale_out;
reg [`PRESCALE_BITS:0] prescale_cnt;

initial
begin
  prescale_cnt = 0;
  prescale_out = 0;
  display_clk = 0;
end

always @(posedge clk)
begin
  prescale_cnt <= prescale_cnt + 1;
end

always @(posedge clk)
begin
  prescale_out <= (prescale_cnt == 0);
end

always @(posedge prescale_out)
begin
  display_clk = ~display_clk;
end
// ---------------------------------------------------------
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//-------------------------- I/O buffers ------------------------
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//---------------------------------------------------------------
// control and status signals
//---------------------------------------------------------------
IBUFG external_clk_i1 (.O (clk), .I (external_clk));
IBUF reset_buf (.O (i_reset), .I (reset));
OBUF ledbuf2  (.I(STATE[23]), .O(LED2_OUT));
OBUF volt_test_buf  (.I(1'b1), .O(volt_test));
OBUF reset_led_buf  (.I(debounce_reset), .O(LED3_OUT));
OBUF dump_mode_buf  (.I(dump_mode_r), .O(LED4_OUT));
//---------------------------------------------------------------

//---------------------------------------------------------------
// Asynchronous 2-of-7 interface between FPGA and Spinnaker chip
//---------------------------------------------------------------
OBUF dataOutToCore0[6:0](.I(i_spinnaker_data), .O(data_2of7_to_spinnaker));
IBUF ackInFromCore0(.I(ack_from_spinnaker), .O(i_spinnaker_ack));
//---------------------------------------------------------------

//---------------------------------------------------------------
// Asynchronous interface between AER sensor and FPGA
//---------------------------------------------------------------
IBUF aer_req_buf       (.I(aer_req),   .O(i_aer_req));
IBUF aer_data_buf[15:0](.I(aer_data),  .O(i_aer_data));
OBUF aer_ack_buf       (.I(ack_bit_r), .O(aer_ack));
//---------------------------------------------------------------

// ---------------------------------------------------------
// Instantiate I/O buffers for resolution select
// ---------------------------------------------------------
IBUF  res_sel_buf (.O (res_sel), .I (ext_res_sel));

OBUF  sevenSeg_buf0 (.I(o_7seg[0]), .O(ext_7seg[0]));
OBUF  sevenSeg_buf1 (.I(o_7seg[1]), .O(ext_7seg[1]));
OBUF  sevenSeg_buf2 (.I(o_7seg[2]), .O(ext_7seg[2]));
OBUF  sevenSeg_buf3 (.I(o_7seg[3]), .O(ext_7seg[3]));
OBUF  sevenSeg_buf4 (.I(o_7seg[4]), .O(ext_7seg[4]));
OBUF  sevenSeg_buf5 (.I(o_7seg[5]), .O(ext_7seg[5]));
OBUF  sevenSeg_buf6 (.I(o_7seg[6]), .O(ext_7seg[6]));
OBUF  sevenSeg_buf7 (.I(o_7seg[7]), .O(ext_7seg[7]));

OBUF  strobe_buf0 (.I(o_strobe[0]), .O(ext_strobe[0]));
OBUF  strobe_buf1 (.I(o_strobe[1]), .O(ext_strobe[1]));
OBUF  strobe_buf2 (.I(o_strobe[2]), .O(ext_strobe[2]));
OBUF  strobe_buf3 (.I(o_strobe[3]), .O(ext_strobe[3]));
// ---------------------------------------------------------
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
endmodule
