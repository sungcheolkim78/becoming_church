#!/bin/bash

filename=day$1.yaml

if [ -e $filename ]; then
  echo "... $filename exists!"
else
  cat > $filename << EOF
day: '$1'
prayer: ''
song: ''
summary: ''
title: ''
verses:
- ''
- ''
- ''
- ''
- ''
EOF
  echo "... create $filename"
fi
