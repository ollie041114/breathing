#ifndef Velocity_h
#define Velocity_h
#endif

#include "Arduino.h"
#include <Wire.h>
#include <Adafruit_GFX.h>
#include "Adafruit_LEDBackpack.h"
#include <WiFiNINA.h>
#include "base.h"


class Velocity : public Base
{
public:
    Velocity();
    Velocity(Adafruit_8x8matrix &_matrix, int _fullCyclePeriod);
    void veloHoriz(int currentMillis);
    void veloCircle(int currentMillis);
    void veloFreq(int currentMillis);


private:
    int prevMillis;
    int blinkPeriod;
    int prevSize;
};