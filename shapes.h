#ifndef shapes_h
#define shapes_h
#endif

#include "Arduino.h"
#include <Wire.h>
#include <Adafruit_GFX.h>
#include "Adafruit_LEDBackpack.h"
#include <WiFiNINA.h>
#include "arduino_secrets.h"
#include "base.h"

// Shapes inherits from class Base
class Shapes : public Base
{
public:
  Shapes();
  Shapes(Adafruit_8x8matrix &_matrix, int _fullCyclePeriod);
  // Call this function once in setup(), accept pointer of pMatrix

  void circle(int currentMillis, bool fill);
  // 1: fill, 0: no fill

  void square_center(int currentMillis, bool fill);

  void square_vertical(int currentMillis, bool fill);

  void square_horizontal(int currentMillis, bool fill);

  void frequencyBlink(int currentMillis);
};


// // Call this function once in setup(), accept pointer of pMatrix
// void shapesInit(Adafruit_8x8matrix *pMatrix, int _fullBreathPeriod);

// void circle(int currentMillis, bool fill);
// // 1: fill, 0: no fill

// void square_center(int currentMillis, bool fill);

// void square_vertical(int currentMillis);

// void square_horizontal(int currentMillis);

// void frequencyBlink(int currentMillis);