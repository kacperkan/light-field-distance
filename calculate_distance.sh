#!/bin/bash

file1=$1
file2=$2

cp volume/* Executable/
cd Executable

echo "Aligning shape: ${file1} ..."
./3DAlignment ${file1}

echo "Aligning shape: ${file2} ..."
./3DAlignment ${file2}

echo "Calculating distance..."
./Distance ${file1} ${file2}
