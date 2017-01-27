# icm
The ICM model for representation of quantum circuits.

How to use this script
======================

* Install the development version of the ICM code from qutip

```
pip install git+https://github.com/sahmed95/qutip.git@icm
```

```
pip install docopt
```

* Describe your circuit in the file test.txt. Indexing of bits starts from 0.

* Run the file `main.py` (with the optional keyword `latex` to get the circuit images)
NOTE : You should use Python3

```python3 main.py```
```python3 main.py latex```

* The outputs are in the folder "outputs". `geometry.json` can be dragged and dropped to visualise the TQC using the TQC viewer by opening `tqc_viewer/index.html`. `circuit.json` describes the ICM circuit.
