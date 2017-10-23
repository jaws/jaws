; Written by Wang, Wenshan 2015-05-01 Friday 14:58:20
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
;*************************************************************
; Purpose: large change of (aw,beta) within a month; detect --> manual
; Notes:
;   - similar structure of fix_tilt.ncl: cal dfs instead of correcting
; Warnings:
;   - diff tilt times
;************************************************************
begin
;- constant
pho = 0.8     ; ground reflectance: 0.8 for snow
pi = 3.1415926535898d

drc = "/data/wenshanw/gcnet/"
;drc_in = drc+"tilt_fix/"
;drc_in = drc+"tilt_re/"
drc_in = drc+"tilt_df/"
drc_crm = "/data/wenshanw/crm/myd_long_clr/"

;xpt = "_exact-noon"
;xpt = "_fuzzy-noon"
xpt = ""
lst_aw = "tilt_netcdf/lst_aw-beta_df.txt"
;lst_aw = "tilt_netcdf/lst_aw-beta_stn13.txt"
;lst_aw = "tilt_netcdf/lst_stn44.txt"
;lst_aw = "tilt_netcdf/lst_temp.txt"
;lst_aw = "tilt_netcdf/lst_aw-beta_stamp.txt"
;lst_aw = "tilt_netcdf/lst_aw-beta_stamp_s050609_NUKL.txt"
lst_clr = "clr-days.txt"

yb = 2008
ye = 2013
ny = ye - yb + 1
mb = 5
me = 8
nm = me - mb + 1

;stns = systemfunc("cat ~/cloud/airs/stn13.txt | awk '{print $1}'")
;stns = systemfunc("cat ~/cloud/doc/stn/stn44_gkp.txt | awk '{print $1}'")
;stns = (/"UPE_U","UPE_L"/)
stns = systemfunc("cat stn_fix.txt | awk '{print $1}'")
;stns = (/"s10","KPC_L"/)
;stns = (/"s05","s06","s09","NUK_L"/)
;stns = "UPE_L"
;stns = "humb"
nstn = dimsizes(stns)

;!!! temp !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
do i = 0, nstn - 1        ; i = stn
;do i = 25, nstn - 1        ; i = stn
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  stn = stns(i)
;  print("stn = "+stn)
  fn = drc_in+stn+"_tilt-fixed.nc"
  fin = addfile(fn,"r")
  fsds_fixed = fin->fsds_fixed({yb:ye},{mb:me},:,:)
	hr = fin->hr

;- find the dates with both clr-days and (aw,beta)
  str_clr = systemfunc("cat "+lst_clr+" | grep '"+stn+"'")
  nln_clr = dimsizes(str_clr)
;  print(str_clr)
  if (all(ismissing(str_clr))) then
    print("no clr days at stn = "+stn)
    delete(str_clr)
    continue
  end if

  do j = 0, nln_clr-1       ; j = mth with clr-days
;- loop to see whether (aw,beta) exists
;-- get yr and mth
    ln_clr = str_split(str_clr(j)," ")
;    print("str_clr = "+str_clr(j))
    yrs = toint(ln_clr(1:))/10000
    mths = toint(str_get_cols(ln_clr(1:),4,5))
;    print(stn+" "+yrs(0)+"  "+mths(0))
;-- get (aw,beta) for this mth
    str_aw = systemfunc("cat "+lst_aw+" | grep '"+stn+"' | grep '"+yrs(0)+sprinti("%02i",mths(0))+"'")
    print("str_aw = "+str_aw)
;		delete([/ln_clr,yrs,mths/])
;		continue
    if (ismissing(str_aw).or.str_aw.eq.(stn+" "+yrs(0)+sprinti("%02i",mths(0))+" missing")) then
      print("No (aw,beta) on yr = "+yrs(0)+" mth = "+mths(0))
      delete([/ln_clr,yrs,mths/])
;			exit
      continue
    end if
;- if (aw,beta) exists, cal dfs std in a mth
    days = toint(str_get_cols(ln_clr(1:),6,7))
    ddd = day_of_year(yrs,mths,days)
    nday = dimsizes(days)
    dfs_day = new(nday,float)

    do k = 0, nday - 1        ; k = day
      fns = systemfunc("ls "+drc_crm+stn+"/"+stn+"."+yrs(0)+ddd(k)+".????.nc")
      if (all(ismissing(fns))) then
        print("No crm on "+yrs(0)+ddd(k))
        delete(fns)
        continue
      end if
      nfn = dimsizes(fns)
      dat = new(nfn,float)
      loctim = new(nfn,float)
      coszrs = new(nfn,float)
      do m = 0, nfn - 1       ; m = crm file
        fin_crm = addfile(fns(m),"r")
        dat(m) = fin_crm->fsds
        loctim(m) = fin_crm->loctim
        coszrs(m) = fin_crm->coszrs
      end do         ; m = crm file
      dat = where(coszrs.lt.cos(75./180.*pi),dat@_FillValue,dat)    ; SZA no more than 75 deg

;- interp fsds_fixed to loctim
      hr_id = ind(.not.ismissing(fsds_fixed({yrs(0)},{mths(0)},{days(k)},:)))
      fsds_loctim = ftcurv(hr(hr_id),fsds_fixed({yrs(0)},{mths(0)},{days(k)},hr_id),loctim)
;- compare
      dfs_day(k) = tofloat(avg(abs(fsds_loctim-dat)))
;      print(yrs(0)+"  "+mths(0)+" "+days(k)+" dfs_day = "+dfs_day(k))
;			print(fsds_loctim+"	"+dat)
;			exit

      delete([/fns,dat,loctim,coszrs,fsds_loctim/])
      delete([/hr_id/])
    end do        ; k = day
;- output dfs std
    dfs_std = stddev(dfs_day)
    if (dfs_std.gt.5) then
;      print(stn+" "+yrs(0)+"  "+mths(0)+" dfs_stn = "+dfs_std)
      system("echo "+stn+" "+yrs(0)+"  "+mths(0)+" dfs_stn = "+dfs_std+" >> high_dfs-std.txt")
    end if

    delete([/ln_clr,yrs,mths,str_aw,days,ddd/])
    delete([/dfs_day/])
  end do        ; j = mth with clr-days

  delete([/str_clr,dfs_std/])
end do        ; i = stn

print("done!")
end
