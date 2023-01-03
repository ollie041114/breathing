#include "Arduino.h"
#include <Wire.h>
#include <Adafruit_GFX.h>
#include "Adafruit_LEDBackpack.h"
#include "base.h"
#include "shapes.h"

Shapes::Shapes() {
  // DON'T FORGET TO PROVIDE THIS SHIT!!!!!!!!!!!!!!!!
}


Shapes::Shapes(Adafruit_8x8matrix &_matrix, int _fullCyclePeriod)
  : Base(_matrix, _fullCyclePeriod) {
  // pointMatrix = &_matrix;
  // fullCyclePeriod = _fullCyclePeriod;
}


void Shapes::circle(int currentMillis, bool fill) {
  float size = peak(currentMillis) / 1.5;
  // so the max size is 4
  pointMatrix->clear();
  if (size >= 0.5) {
    // skip the function execution
    if (fill) {
      pointMatrix->fillCircle(4, 4, size, 1);
    } else {
      pointMatrix->drawCircle(4, 4, size, 1);
    }
  } else {
    pointMatrix->clear();
  }
}


void Shapes::square_center(int currentMillis, bool fill) {
  float size = peak(currentMillis);
  // so the max size is 4
  pointMatrix->clear();
  if (size >= 0.5) {
    // skip the function execution
    if (fill) {
      pointMatrix->fillRect(4 - size, 4 - size, 2 * size, 2 * size, 1);
    } else {
      pointMatrix->drawRect(4 - size, 4 - size, 2 * size, 2 * size, 1);
    }
  } else {
    pointMatrix->clear();
  }
}


void Shapes::square_vertical(int currentMillis, bool fill) {
  int size = peak(currentMillis);
  pointMatrix->clear();
  // draw a square ofexpanding vertically from the bottom
  if (fill) {
    pointMatrix->fillRect(0, 8 - size, 8, size, 1);
  } else {
    pointMatrix->drawRect(0, 8 - size, 8, size, 1);
  }
}


void Shapes::square_horizontal(int currentMillis, bool fill) {
  int size = peak(currentMillis);
  pointMatrix->clear();
  // draw a square of expanding horizontally from the right
  if (fill) {
    pointMatrix->fillRect(8 - size, 0, size, 8, 1);
  } else {
    pointMatrix->drawRect(8 - size, 0, size, 8, 1);
  }
}