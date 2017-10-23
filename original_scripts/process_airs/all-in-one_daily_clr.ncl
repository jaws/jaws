; Written by Wang, Wenshan 2017-02-06 Monday 15:19:00
load "$HOME/scripts/ncl_script/wenshanw.ncl"
;*************************************************************
; Purpose: input AIRS lvl3 DAILY data; no time var in file
; Prototype: all-in-one_clr.ncl
; Note:
; - change to loop over stn and parallel yr
;*************************************************************
begin
yr=2016

xpt="airx3std"
drc_airs="/data/wenshanw/airs/nomiss_lvl3/" 
drc_out="/data/wenshanw/aio/airs_lvl3_std/run/"

lst_stn = "stn_run.txt"
stns = systemfunc("cat "+lst_stn+" | awk '{print $1}'")
lats = tofloat(systemfunc("cat "+lst_stn+" | awk '{print $2}'"))
lons = tofloat(systemfunc("cat "+lst_stn+" | awk '{print $3}'")) + 360.
nstn = dimsizes(stns)
;print(stns+"  "+lats+"  "+lons)

std = "/home/wenshanw/cloud/crm/add-cld/std_lev24.nc"

do i = 0, nstn - 1        ; i = stn
  stn = stns(i)
  lat = lats(i)
  lon = lons(i)

  cmd = "ls "+drc_airs+stn+"."+xpt+"."+yr+".*.nc | cut -d '.' -f 3-5"
  dates = systemfunc(cmd+" | cut -d '_' -f 1")
  mths = systemfunc(cmd+" | cut -d '.' -f 2")
  days = systemfunc(cmd+" | cut -d '.' -f 3 | cut -d '_' -f 1")
  sfxs = systemfunc(cmd+" | cut -d '_' -f 2")
  ndate = dimsizes(dates)
;  print("dates = "+dates+"  sfxs = "+sfxs+" "+mths+"  "+days)
;  exit

  do j = 0, ndate - 1       ; j = file
    date = dates(j)
    mth = mths(j)
    day = days(j)
    sfx = sfxs(j)

    fn_airs = drc_airs+stn+"."+xpt+"."+date+"_"+sfx+".nc"
    fin_airs = addfile(fn_airs,"r")
    print("fn_airs = "+fn_airs)

;- time
    ymd = yr+mth+day
    hm = "0030"
    doy = day_of_year(yr,toint(mth),toint(day))
    day_frc = doy+(30./60.)/24.        ; 00:30
;    print(day_frc)

;- AOD
    aod = tofloat(systemfunc("cat /home/wenshanw/cloud/mod/aod_grp.txt | grep '"+stn+"' | awk '{print $2}'"))

;- output files
;------------------------------------------------------------
    fo = drc_out+stn+"."+ymd+"."+hm+"."+sfx+".nc"
;    print("fo = "+fo)
;    exit
    system("/bin/rm -f "+fo+";cp "+std+" "+fo+";chmod 644 "+fo)
    fout = addfile(fo,"w")

;- time
    fout->gmt_yr=(/yr/)
    fout->gmt_doy=(/day_frc/)
;    fout->lcl_yr_day=(/day_frc/)

;- lat/lon
    fout->lat_dgr = lat
    fout->lon_dgr = lon

;- skin tmp
    fout->tpt_skn = (/fin_airs->sfc_tmp/)

;- air tmp
;-- use AIRS
    fout->tpt_sfc = (/fin_airs->sfc_air_tmp/)       ; doesn't affect LW down in CRM

;- sfc pressure
    fout->prs_sfc = (/(fin_airs->sfc_prs)*100./)

;- pressure
    plev = fin_airs->plev
    fout->prs = (/plev/)*100.
    fout->lev = (/plev/)*100.

;- tmp
    fout->tpt = (/fin_airs->t/)

;- water vapor mixing ratio
;- add water vapor proportionally
    q_pfl = fin_airs->q
;    if (stn.eq."KAN_B") then
;      add_water = 0.12			; total water added; kg/kg
;      q_wgt = q_pfl/sum(q_pfl)
;      fout->q_H2O = (/q_pfl+add_water*q_wgt/)
;    else
      fout->q_H2O = (/q_pfl/)
;    end if

;- o3 mass mixing ratio
    fout->q_O3 = (/fin_airs->o3/)

;- AOD
    fout->odxl_obs_aer = (/aod/)
;    fout->odxl_obs_aer = 0.12
;    fout->odxl_obs_aer = 0

;- albedo
;= interp to hms
;	idx = ind(.not.ismissing(alb({yyyy},{mth},{day},:)))
;	if (dimsizes(idx).gt.8) then
;		albedo = ftcurv(hr(idx),alb({yyyy},{mth},{day},idx),hms)
;		if (.not.ismissing(albedo).and.albedo.lt.1.and.albedo.gt.0) then
;; 	   fout->alb_sfc_NIR_dff = (/2*r*albedo/(1+r)/)
;; 	   fout->alb_sfc_NIR_drc = (/2*r*albedo/(1+r)/)
;; 	   fout->alb_sfc_vsb_dff = (/2*albedo/(1+r)/)
;; 	   fout->alb_sfc_vsb_drc = (/2*albedo/(1+r)/)
;	    fout->alb_sfc_NIR_dff = (/albedo/)
;	    fout->alb_sfc_NIR_drc = (/albedo/)
;	    fout->alb_sfc_vsb_dff = (/albedo/)
;	    fout->alb_sfc_vsb_drc = (/albedo/)
;	  end if
;  	delete(albedo)
;	end if
;  albedo = alb({yyyy},{mth},{day},{hms})
;  r = 0.67/0.98       ; ratio of NIR albedo to vsb albedo
;= otherwise: default albedo
;	delete(idx)
;= spole: use default albedo

;- cld

;- clear-up
    delete([/plev,q_pfl/])
  end do        ; j = file

;  exit        ; run ALE alone
  delete([/dates,mths,days,sfxs/])
end do        ; i = stn

print("done!")
end
