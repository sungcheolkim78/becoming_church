#!/bin/bash

filename=yaml_40days/day$1.yaml

if [ -e $filename ]; then
  echo "... $filename exists!"
else
  cat > $filename << EOF
day: '$1'
title: ''
song: ''
prayer: ''
summary: ''
verses:
- ''
EOF
  echo "... create $filename"
fi
