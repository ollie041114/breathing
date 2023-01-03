#include "Arduino.h"
#include <Wire.h>
#include <Adafruit_GFX.h>
#include "Adafruit_LEDBackpack.h"
#include "base.h"
#include "velocity.h"

Velocity::Velocity() {
}

Velocity::Velocity(Adafruit_8x8matrix &_matrix, int _fullCyclePeriod)
  : Base(_matrix, _fullCyclePeriod) {
  prevMillis = 0;
  blinkPeriod = 1000;
  prevSize = 0;
}


void Velocity::veloHoriz(int currentMillis) {
  int strength = 5;
  // tracks how "big" should the difference between maximal and minimal speed be
  // 4 = 4 passes across the screen in one period of fullCyclePeriod
  int relativePosition = (strength * peak(currentMillis));
  relativePosition = relativePosition % 8;
  // relativePosition is from 0 to 8. Map these movements from 0 to 7;

  int pos = relativePosition + 4;
  // from 4 to 12

  if (pos > 8) {
    pos = pos - 8;
  }
  pointMatrix->clear();
  pointMatrix->drawLine(pos, 0, pos, 7, HIGH);
}

void Velocity::veloCircle(int currentMillis) {
  int strength = 3;
  // tracks how "big" should the difference between maximal and minimal speed be
  // 4 = 4 passes across the screen in one period of fullCyclePeriod
  int relativePosition = (strength * peak(currentMillis));
  relativePosition = relativePosition % 8;
  //   // relativePosition is from 0 to 8. Map these movements from 0 to 7
  //   int pos = relativePosition + 4;
  //   // from 4 to 12
  //   if (pos > 8) {
  //     pos = pos - 8;
  //   }
  // center is at 4, which you will reach when the relativePosition is 0
  pointMatrix->clear();
  pointMatrix->fillCircle(4, 4, relativePosition / 1.7, 1);
}

void Velocity::veloFreq(int currentMillis) {
  int strength = 4;
  int relativePosition = (strength * peak(currentMillis));


  relativePosition = relativePosition % 8;
  int size = relativePosition / 1.7;
  if (size != prevSize) {
    pointMatrix->clear();
    prevSize = size;
  }

  pointMatrix->fillRect(4, 4, 8, 8, 1);
}