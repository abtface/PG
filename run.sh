#!/bin/bash
docker run -it --rm  \
  -v $(pwd):/usr/src/barcodez \
  barcodez bash
