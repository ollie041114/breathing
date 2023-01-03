#include "Arduino.h"
#include <Wire.h>
#include <Adafruit_GFX.h>
#include "Adafruit_LEDBackpack.h"
#include "base.h"
#include "freq.h"

FreqBright::FreqBright()
{
}

FreqBright::FreqBright(Adafruit_8x8matrix &_matrix, int _fullCyclePeriod) : Base(_matrix, _fullCyclePeriod)
{
  prevMillis = 0;
  blinkStarted = true;
  frequency = 1;
}


void FreqBright::blinkAtFrequency(int frequency, int currentMillis)
{
  int blinkPeriod = 1000/frequency;
  if ((currentMillis % blinkPeriod) > (blinkPeriod / 2)) {
    // in the second half of the blink, just null the matrix
    pointMatrix->clear();
  }
  else {
    // just do nothing 
  }
}

void FreqBright::frequencyBlink(int currentMillis)
{
  if (currentMillis < prevMillis) {
    prevMillis = currentMillis;
  }
  if (currentMillis - prevMillis > 250) {
    // only update the frequency every 200 ms 
    prevMillis = currentMillis;
    float scale = peak(currentMillis);
      // 0 to 8 
    frequency = map(scale, 0, 8, 2, 10);
  }
  
  blinkAtFrequency(frequency, currentMillis);
}

void FreqBright::brightness(int currentMillis)
{
  int scale = 2 * peak(currentMillis);
  // make it a multiple of 1/16

  // int brightness = 3 * (1000 / frequency);
  pointMatrix->setBrightness(scale);
  // analogWrite(9, brightness);
}