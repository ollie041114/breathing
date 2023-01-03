#include <Wire.h>
#include <Adafruit_GFX.h>
#include "Adafruit_LEDBackpack.h"
#include "shapes.h"
#include "freq.h"
#include "velocity.h"

#ifndef _BV
#define _BV(bit) (1 << (bit))
#endif

Adafruit_8x8matrix matrix = Adafruit_8x8matrix();
// create pointer to matrix
Adafruit_8x8matrix *matrixp = &matrix;
Shapes shapes;
FreqBright freqBright;
Velocity velocity;
uint8_t counter = 0;

int fullCycle = 8000;
bool buttons[13] = { true, false, false, false, false, false, false, false, false, false, false, false, false };

bool frequencyControl = false;
bool brightnessControl = false;

void setup() {
  // array of booleans
  Serial.begin(9600);
  Serial.println("HT16K33 test");
  matrix.begin(0x70);
  shapes = Shapes(matrix, fullCycle);
  freqBright = FreqBright(matrix, fullCycle);
  velocity = Velocity(matrix, fullCycle);
}

// previousMillis
unsigned long previousMillis = 0;
// interval in milliseconds
const long interval = 100;


void change_control(int command) {
  // if one of the first 8 members set to true, make the other ones false
  int orthogonal_members = 9;
  if (command <= orthogonal_members) {
    for (int i = 0; i <= orthogonal_members; i++) {
      if (i == command) {
        buttons[i] = true;
      } else {
        buttons[i] = false;
      }
    }
  } else {
    // else, just toggle
    buttons[command] = !buttons[command];
  }
}


void control_center(int currentMillis) {
  // orthogonal
  if (buttons[0]) {
    velocity.veloHoriz(currentMillis);  // 0
  }

  if (buttons[1]) {
    velocity.veloCircle(currentMillis);  // 0
  }

  if (buttons[2]) {
    velocity.veloFreq(currentMillis); 
  }

  if (buttons[3]) {
    shapes.circle(currentMillis, true);  // 1
  }
  if (buttons[4]) {
    shapes.square_center(currentMillis, true);  // 2
  }
  if (buttons[5]) {
    shapes.square_horizontal(currentMillis, true);  // 3
  }
  if (buttons[6]) {
    shapes.square_vertical(currentMillis, true);  // 4
  }
  if (buttons[7]) {
    shapes.circle(currentMillis, false);  // 5
  }
  if (buttons[8]) {
    shapes.square_center(currentMillis, false);  // 6
  }
  if (buttons[9]) {
    shapes.square_horizontal(currentMillis, false);  // 7
  }
  if (buttons[10]) {
    shapes.square_vertical(currentMillis, false);  // 8
  }

  // frequency control
  if (buttons[11]) {
    freqBright.frequencyBlink(currentMillis);
  }
  // brightness control
  if (buttons[12]) {
    freqBright.brightness(currentMillis);
  }
}


int x = 1;
void loop() {
  if (Serial.available()) {
    x = Serial.readString().toInt();
    Serial.println(x);
    change_control(x);
  }

  unsigned long currentMillis = millis() % fullCycle;

  control_center(currentMillis);

  matrix.writeDisplay();
}