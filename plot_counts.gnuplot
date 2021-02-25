#!/usr/bin/env -S gnuplot -p -c
# NOTE: Without 'env -S', 'gnuplot -c' fails to set ARG1

set terminal wxt size 800,600
set key bottom right autotitle columnheader
set datafile separator whitespace
stats ARG1 nooutput
set style data lines

set xlabel  "Date"
set xdata   time
set timefmt '%Y-%m-%dT%H:%M:%S'
set format  x "%Y-%m"
set xtics   rotate by -20

set ylabel  "Downloads"
set decimal locale
set format  y "%'0.0f"
set yrange  [0:]

plot for [i=2:STATS_columns] ARG1 using 1:i linewidth 2
