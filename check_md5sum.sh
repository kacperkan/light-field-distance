#!/bin/bash

cd Executable 
./3DAlignment 3dcafe_a-10
echo `ls -lha 3dcafe_a-10_q8_v1.8.art`
echo `md5sum 3dcafe_a-10_q8_v1.8.art`
./3DAlignment cup1
./3DAlignment CUP2
./Distance cup1 3dcafe_a-10
./Distance cup1 CUP2
