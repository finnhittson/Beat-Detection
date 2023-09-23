# Beat Detection Algorithm

This algorithm is used to detect the beat of an input signal using signal processing techniques.

## Description

The system to detect the beat of an input signal is broken down into three parts.
1. Generate onset signal strength (OSS): This step transforms the audio signal into a signal that indicates where human ears percieve onsets. The signal is the output of the OSS step.
2. Beat period detection (BPD): The signal generated from OSS is parsed into smaller segments which are then analyzed for the tempo. The output is a single digit which is an estimate of the tempo from the original audio input. 
3. Accumulator and overall estimate: Tempo estimates are accumulated and an overall estimate is determined from these samples. A heuristic is used to evaluate whether the tempo is correct and whether the it should be halved or doubled since this estimation method can produce tempo estimates that are either double or half of the true tempo.
The system outputs a singal number which stand for the number of beats per minute (i.e. 168 BPM). The optimal phase can be extracted from the BPD step. 

## Getting Started

### Installing

Clone repository into local directory.
```
git clone https://github.com/finnhittson/beat.git
```

### Executing program

In the `src` directory, execute with the following command parameters.
```
python detectbeat.py --path=ballroom.wav --framesize=1024 --hop=128
```
1. `--path` is the path to the input sound file.
2. `--framesize` is the length of the sound data points to consider in a single frame.
3. `--hop` is the number of sound data points to overlap the frames by.

## Acknowledgments

This project was used for a music visualizer in a Spotify web-app, PurdyMusic. Other contributions to this app are from Aaron Orenstein, Walter Graham, Vinayak Sharma, Josh Nagler, and Rupika Pendyala. It was inspired and guided with the help of the authors Graham Percival and George Tzanetakis of the paper Streamlined Tempo Estimation Based on Autocorrelation and Cross-correlation With Pulses.  
  
1. G. Percival and G. Tzanetakis, "Streamlined Tempo Estimation Based on Autocorrelation and Cross-correlation With Pulses," in IEEE/ACM Transactions on Audio, Speech, and Language Processing, vol. 22, no. 12, pp. 1765-1776, Dec. 2014, doi: 10.1109/TASLP.2014.2348916.
