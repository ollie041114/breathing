#ifndef FreqBright_h
#define FreqBright_h
#endif

#include "Arduino.h"
#include <Wire.h>
#include <Adafruit_GFX.h>
#include "Adafruit_LEDBackpack.h"
#include <WiFiNINA.h>
#include "base.h"


class FreqBright : public Base
{
public:
    FreqBright();
    FreqBright(Adafruit_8x8matrix &_matrix, int _fullCyclePeriod);
    void frequencyBlink(int currentMillis);
    void velocityMov(int currentMillis);
    void brightness(int currentMillis);

private:
    void blink(int currentMillis, int period);
    int prevMillis;
    bool blinkStarted;
    int frequency;
    void blinkAtFrequency(int frequency, int currentMillis);
};