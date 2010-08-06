#!/bin/bash
dirname=`dirname $1`
base=`basename $1`
exitname=$dirname/Ui_${base%.*}.py
echo $1 $exitname;
pyuic4 -x "$1" > "$exitname"

echo "$1" > /home/marcos/workspace/EsquipulasPy/uicomp.log
