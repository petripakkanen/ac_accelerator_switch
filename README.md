# accsw - accelerometer switch

Switching capability with accelerometer.
Currently samplerate is simply fast-as-you-can.

Supports tcp streaming to Octave (or matlab).
Configuration is in config.py

aclSignalGroup holds output functions
- sendToOctave()
- initPlotAccVsTime(self, x, y)
- initPlotFFT(y, absolute=True)


**Example outputs:**

![48_samples_5101389134ns@1603021814223731631](https://github.com/petripakkanen/ac_accelerator_switch/assets/52924721/822dd138-c92d-4431-ae05-1ba54503d683)
![@1603050023876691542](https://github.com/petripakkanen/ac_accelerator_switch/assets/52924721/d86ec3bc-98e7-43a5-bf76-9d1b73957398)
![@1603050023876691542_fft](https://github.com/petripakkanen/ac_accelerator_switch/assets/52924721/8587f927-4d79-41e0-b7d2-493f31973672)
