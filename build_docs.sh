#!/bin/sh

pyreverse --ignore errors.py,tests -o png -p PyLGRum -m y pylgrum/
mv classes_PyLGRum.png packages_PyLGRum.png docs/
