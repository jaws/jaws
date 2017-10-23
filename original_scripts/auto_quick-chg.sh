#!/bin/bash
# Written by Wang Wenshan 2015-08-29 Saturday 16:16:48
#============================================================
# Notes:
#		added at re-processing:
#		auto_quick-chg.sh: an automatic script to help pick up quick change breaking point
#		now the procedure is:
#			1) quick-chg.ncl: output high_dfs-std.txt
#			2) auto_quick-chg.sh: output plot for human to decide the quick change breaking point
#		note: not fully automatic to output the breaking point because that needs to change fix_tilt.ncl as well
# Steps:
#		- read high_dfs-std.txt to output clr-days_test.txt with one/two clr day one line
#		- ncl cal_aw-beta_main.ncl (no more than 120 lines in clr-days_test.txt)
#		- ncl fix_tilt-test.ncl
#		- ncl plot-xy_cmp_tilt_test.ncl
#============================================================
lst_in='high_dfs-std.txt'

lst_clr_mom='clr-days.txt'
lst_clr='clr-days_test.txt'
#- remember to clear the contents of ${lst_clr}

while read ln; do
	echo ${ln}
	stn=$( echo ${ln} | cut -d ' ' -f 1 )
	yr=$( echo ${ln} | cut -d ' ' -f 2 )
	mth=$( echo ${ln} | cut -d ' ' -f 3 )
	mm=$( printf "%02d" ${mth} )
#	echo ${stn} ${yr} ${mth} ${mm}
	echo ${stn} ${yr}${mm}

	ln_clr_days=$( cat ${lst_clr_mom} | grep "${stn} ${yr}${mm}" | cut -d ' ' -f 2-)
#	echo ${ln_clr_days}
#- write stn and clr days; if more than two CRM points --> next line
	for dt in ${ln_clr_days}; do
		echo ${stn} ${dt} >> ${lst_clr}
	done

done <${lst_in}
