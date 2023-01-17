1. What this script does
- This script calculates distances between list of location with gps coordinates.
- It uses its data only but could be easily adjusted to calculate custom data.
2. Requirements
- Hardware: 1 CPU, 1 Gb of RAM, 5 Gb HDD.
- It was tested on MacOS 13.0.
3. How to use
- setup python virtual environment with Python 3.7 (I used anaconda)
- activate you virtual environment
- install requirements
```python 
pip install -r requirements.txt
```
- execute script
```python 
# this is a simple run without any parameters
# it will use default data from ./data/places.csv file
python src/calculate_great_circle_distance.py
```
```python 
# this is a run with parameter "n"
# it will generate data with the amount of n specified in the arguement
# n - is an iteger value
python src/calculate_great_circle_distance.py -n 10
```


