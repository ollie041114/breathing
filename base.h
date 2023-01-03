#ifndef Base_h
#define Base_h

#include "Arduino.h"
#include <Wire.h>
#include <Adafruit_GFX.h>
#include "Adafruit_LEDBackpack.h"
#include <math.h>

class Base
{
public:
    Base();
    Base(Adafruit_8x8matrix &_matrix, int _fullCyclePeriod);

protected:
    bool step(int currentMillis, int period);
    float peak(int currentMillis);
    float speed_peak(float currentMillis);
    Adafruit_8x8matrix *pointMatrix;
    int fullCyclePeriod;
};

#endif