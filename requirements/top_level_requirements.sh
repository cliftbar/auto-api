#!/usr/bin/env bash
conda config --append channels conda-forge

conda install flask flask-restful flask-cors webargs apispec
pip install python-magic-win64
