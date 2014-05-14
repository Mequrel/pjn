#!/bin/bash

MEDIAN=`cat $1-median.txt`

gnuplot << EOF

k = 10
zipf(rank) = k / rank
fit zipf(x) '$1.txt' using 1:2:(1) via k

P = 10
d = 1
B = 1

mandelbrot(rank) = exp( P - B * log(rank + d) )
fit mandelbrot(x) '$1.txt' using 1:2:(1) via P,d,B

median = $MEDIAN

set arrow from median,graph(0,0) to median,graph(1,1) nohead lw 3 lc rgb 'orange'

set xlabel "Rank"
set ylabel "Occurences"
set term pngcairo enhanced size 1280,1024
set output "$1-zipf.png"
set title "Potop"
set grid

plot zipf(x), mandelbrot(x), '$1.txt'

set output "$1-zipf-loglog.png"
set logscale xy

plot zipf(x), mandelbrot(x), '$1.txt'


set nologscale xy
set output "$1-zipf-middle.png"
set xrange [0:2000]
set yrange [0:2000]

plot zipf(x), mandelbrot(x), '$1.txt'


EOF
