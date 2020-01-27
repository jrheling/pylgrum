#!/bin/sh

pyreverse --ignore errors.py -o png -p PyLGRum -m y pylgrum/
mv classes_PyLGRum.png docs/
rm -f packages_PyLGRum.png