#include "Arduino.h"
#include "base.h"
#include <Wire.h>
#include <Adafruit_GFX.h>
#include "Adafruit_LEDBackpack.h"
#include <math.h>

Base::Base()
{
    // DON'T FORGET TO PROVIDE THIS SHIT!!!!!!!!!!!!!!!!
}

Base::Base(Adafruit_8x8matrix &_matrix,
           int _fullCyclePeriod)
{
    pointMatrix = &_matrix;
    fullCyclePeriod = _fullCyclePeriod;
}

bool Base::step(int currentMillis, int period)
{
    // step function, which returns 0 and 1 depending on period
    if ((currentMillis % period) < (period / 2))
    {
        return false;
    }
    else
    {
        return true;
    }
}

float Base::peak(int currentMillis)
{
    int magn = 8;
    float peak = magn * (cos(2 * PI * currentMillis / (fullCyclePeriod))) + magn;
    return peak/2;
        // from 0 to 8
}

float Base::speed_peak(float currentMillis)
{
    float peak = 8 * (sin(PI * currentMillis / (fullCyclePeriod)));
        // from -8 to 8
    return peak;
}