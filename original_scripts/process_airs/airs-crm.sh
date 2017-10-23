#!/bin/bash
# Written by Wang Wenshan 2014-07-11 Friday 13:37:34
#============================================================
# Run CRM with AIRS pfl under clr-sky
# Steps:
#   - read in all-in-one files
#   - follow clr file list
#   - run clm, crm, organize output
# NB!!!
#   different stn cannot be ran in the same drc since crm.nc may conflict
# Usage:
#   - change xpt (experiment)
#   - change input time type if switch btw PROMICE and other datasets
#============================================================
#- para
#stn='dye'
stn='ale'
#stn='smt'
#stn='KPC_U'
#stn='alaska'
#stn='KAN_B'
#xpt='myd_long_all'
#xpt='myd_long_clr'
#xpt='arm'
#xpt='airs_long_all'
#xpt='time_test_gmt'
#xpt='spole'
xpt='vld_bsrn_smt'
#xpt='cre_myd1'

#- output drc
#drc_out='/data/wenshanw/crm/airs_may-sept/'
#drc_out='/data/wenshanw/agu/crm_cld-cwp-50/'
#drc_out='/data/wenshanw/crm/airs_mth-aod/'
#drc_out='/data/wenshanw/crm/invisi/'
#drc_out='/data/wenshanw/crm/crf_myd_stn/'
#drc_out='/data/wenshanw/crm/clr_myd_stn/'
#drc_out='/data/wenshanw/crm/airs_clr_std/'
#drc_out='/data/wenshanw/crm/airs_sup_clr/'
#drc_out='/data/wenshanw/crm/myd_long_clr/'
#drc_out=/data/wenshanw/crm/${xpt}/
#drc_out=/data/wenshanw/crm/vld_bsrn_rerun/
#drc_out=/data/wenshanw/crm/vld_bsrn_restn/
#drc_out=/data/wenshanw/crm/vld_bsrn_recut/
drc_out=/data/wenshanw/crm/vld_bsrn_reall/
#drc_out='/data/wenshanw/crm/airs_long_all/'
#drc_out='/data/wenshanw/crm/cld_myd-crs/'
#drc_out='/data/wenshanw/crm/alb_ratio_all/'
#drc_out='/data/wenshanw/crm/lw_ctp/'
#drc_out='/data/wenshanw/crm/low-cld_ctn/'
#drc_out='/data/wenshanw/crm/low-cld_half/'
#drc_out='/data/wenshanw/crm/low-cld_only/'
#drc_out='/data/wenshanw/crm/cwp_xpt/'
#drc_out='/data/wenshanw/crm/sw_no-ctr/'
#drc_out='/data/wenshanw/crm/high-cld/'
drc_clm="${drc_out}clm/"
drc_txt="${drc_out}txt/"
drc_nc="${drc_out}${stn}/"
#- if not exist, mkdir
if [ ! -d ${drc_clm} ]; then
  mkdir -p ${drc_clm} ${drc_txt}
fi
if [ ! -d ${drc_nc} ]; then
  mkdir -p ${drc_nc}
fi

#- file list & output name
#drc_in='/data/wenshanw/agu/aio/'
#drc_in='/data/wenshanw/aio/airs_clr/run/'
#drc_in='/data/wenshanw/aio/airs_mth-aod/run/'
#drc_in='/data/wenshanw/aio/crf_myd_stn/run/'
#drc_in='/data/wenshanw/aio/airs_clr_std/run/'
#drc_in='/data/wenshanw/aio/airs_sup_cld/run/'
#drc_in='/data/wenshanw/aio/cld_myd-crs/run/'
#drc_in='/data/wenshanw/aio/sw_no-ctr/run/'
#drc_in='/data/wenshanw/aio/promice/run/'
#drc_in='/data/wenshanw/aio/myd_long_clr/run/'
#drc_in=/data/wenshanw/aio/${xpt}/run/
#drc_in=/data/wenshanw/aio/${xpt}/rerun/
#drc_in=/data/wenshanw/aio/${xpt}/restn/
#drc_in=/data/wenshanw/aio/${xpt}/recut/
drc_in=/data/wenshanw/aio/${xpt}/reall/
#drc_in=/data/wenshanw/aio/time_test/gmt/
#drc_in='/data/wenshanw/aio/airs_long_all/run/'
#drc_in='/data/wenshanw/aio/lw_ctp/run/'
#drc_in='/data/wenshanw/aio/low-cld_ctn/run/'
#drc_in='/data/wenshanw/aio/low-cld_half/run/'
#drc_in='/data/wenshanw/aio/low-cld_only/run/'
#drc_in='/data/wenshanw/aio/cwp_xpt/run/'
#- Use clear day list
#fns=$( cat clr_${stn}_airs.txt )

#- use clear day list
#for fn in ${fns}; do
#- cp clear day files in all-in-one script
for fn in $(ls ${drc_in}${stn}.*.nc); do
#  sfx=$( echo ${fn} | cut -d '.' -f 1-4 )
#  pfx=$( echo ${fn} | cut -d '/' -f 7 )
  pfx=$( echo ${fn} | cut -d '/' -f 7 )
  sfx=$( echo ${fn} | cut -d '/' -f 7 | cut -d '.' -f 1-3 )
  echo ${fn} ${pfx} ${sfx}
#  exit

#- run clm:
#   -l 20: 20 vertical lyr
#   -g: use GMT (may not be needed)
#   -n: use netcdf as input
#   -i: must be full path (cannot use output way since some default input file not in my input drc)
#   -o: output netcdf file name
#   -t: output txt file name
#------------------------------------------------------------
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#  ~/bin/LINUXAMD64/clm -l 28 -g -n -i ${drc_in}${fn} --drc_out ${drc_clm} -o ${fn} -t ${sfx}.txt 
  ~/bin/LINUXAMD64/clm -l 100 -g -n -i ${drc_in}${pfx} --drc_out ${drc_clm} -o ${pfx} -t ${sfx}.txt 
  #- PROMICE uses solar time (no: 20150428); so no -g
#  ~/bin/LINUXAMD64/clm -l 100 -n -i ${drc_in}${pfx} --drc_out ${drc_clm} -o ${pfx} -t ${sfx}.txt 
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  ~/crm/bin/crm < ${drc_clm}${sfx}.txt > ${drc_txt}${sfx}.txt 
  mv crm.nc ${drc_nc}${sfx}.nc
#  rm ${drc_clm}${sfx}.txt ${drc_clm}${sfx}.nc
  rm ${drc_clm}${sfx}.nc
#  rm ${drc_txt}${sfx}.txt
#exit
done

echo Done!
