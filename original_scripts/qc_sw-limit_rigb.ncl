; Written by Wang, Wenshan 2017-05-23 Tuesday 22:08:24
load "$HOME/scripts/ncl_script/wenshanw.ncl"
load "$HOME/cloud/gcnet/cal_para.ncl"
;*************************************************************
; Purpose: rm impossible values
; Prototype: ../cre/qc_sw-limit.ncl
; - slightly different: make this version to complete rigb process --> easy use (no need to change back and forth)
; Rules:
; - dat < 0 --> 0
; - rm fsds > 95% TOA
; - rm fsds < 5% TOA and fsds <> 0
; - rm 5% fsds < fsus < 95% fsds
; - if fsds = 0, fsus = 0
;*************************************************************
begin
drc_aws = "/data/wenshanw/gcnet/tilt_df/"
drc_crs = "/data/wenshanw/ceres/stn_gkp/"

lst_stn = "stn_tilt_df.txt"
cmd = "cat "+lst_stn+" | grep -v ';'"
stns = systemfunc( cmd+"| awk '{print $1}'")
lats = tofloat(systemfunc(cmd+" | awk '{print $2}'"))
lons = tofloat(systemfunc(cmd+" | awk '{print $3}'"))
nstn = dimsizes(stns)
;print(stns+"  "+lats+"  "+lons)
;exit

yb = 2008
ye = 2013
ny = ye-yb+1
mb = 5
me = 9
nm = me-mb+1
nhr_crs = 8
hr_crs = fspan(1.5,22.5,nhr_crs)
;print("hr = "+hr)
;exit

nhr_aws = 24
hr_aws = fspan(0.5,23.5,nhr_aws)
dat_fsdt = new((/ny,nm,31,nhr_aws/),float)
dat_fsdt!0 = "yr"
dat_fsdt!1 = "mth"
dat_fsdt!2 = "day"
dat_fsdt!3 = "hr"
dat_fsdt&yr = ispan(yb,ye,1)
dat_fsdt&mth = ispan(mb,me,1)
dat_fsdt&day = ispan(1,31,1)
dat_fsdt&hr = hr_aws
fsds_thr = dat_fsdt

var_fsdt = "toa_comp_sw-down_all_3h"

do i = 0, nstn - 1    ; i = stn
  stn = stns(i)
  lat_deg = lats(i)
  lon_deg = lons(i)
  print("stn = "+stn)

  fn_crs = drc_crs+stn+".2008-2016.05-09.3hr.format.nc"
  fin_crs = addfile(fn_crs,"r")
  fsdt_crs = fin_crs->$var_fsdt$

;= cal TOA swd
  do yr = yb, ye
    do mth = mb, me
      do j = 0, 30
        fsdt = fsdt_crs({yr},{mth},j,:)
        hr_id = ind(.not.ismissing(fsdt))
        if (dimsizes(hr_id).lt.2)
          delete(hr_id)
          continue
        end if
        dat_fsdt({yr},{mth},j,:) = ftcurv(hr_crs(hr_id),fsdt(hr_id),hr_aws) 
        delete(hr_id)
      end do        ; j = day
;- if TOA is missing, use thr
      nday_mth = days_in_month(yr,mth)
      days = ispan(1,nday_mth,1)
      ddd0 = day_of_year(yr,mth,1)
      ddd = ispan(ddd0,ddd0+nday_mth-1,1)
      fsds_thr({yr},{mth},{days},:) = tofloat(thr_clr_fsds(yr,ddd,hr_aws,lat_deg,lon_deg))
      delete([/nday_mth,days,ddd,ddd0/])
    end do    ; mth
  end do    ; yr
;- if TOA is missing, use thr
;  print_stats(fsds_thr)
  dat_fsdt = where(ismissing(dat_fsdt),fsds_thr,dat_fsdt)
  dat_fsdt = where(dat_fsdt.lt.0,fsds_thr,dat_fsdt)

;= read data
  fn_aws = drc_aws+stn+".tilt-fixed.05-09.nc"
  fin_aws = addfile(fn_aws,"w")
  fsds = fin_aws->fsds_rigb({yb:ye},{mb:me},:,:)
  fsus = fin_aws->fsus_rigb({yb:ye},{mb:me},:,:)
;  exit

; - dat < 0 --> 0
  fsds = where(fsds.lt.0,0,fsds)
  fsus = where(fsus.lt.0,0,fsus)
; - rm fsds > 95% TOA
  fsds = where(fsds.gt.0.95*dat_fsdt, fsds@_FillValue, fsds)
; - rm fsds < 5% TOA and fsds <> 0
  fsds = where(fsds.lt.0.05*dat_fsdt.and.fsds.ne.0, fsds@_FillValue,fsds)
; - rm 5% fsds < fsus < 95% fsds
  fsus = where(fsus.gt.fsds*0.95.or.fsus.lt.fsds*0.05,fsus@_FillValue,fsus)
; - if fsds = 0, fsus = 0
  fsus = where(fsds.eq.0,0,fsus)

  fsds@qc = "qc_sw-limit_rigb.ncl: dat < 0 --> 0; rm fsds > 95% TOA; rm fsds < 5% TOA and fsds <> 0; rm 5% fsds < fsus < 95% fsds; if fsds = 0, fsus = 0"
  fsus@qc = "qc_sw-limit_rigb.ncl: dat < 0 --> 0; rm fsds > 95% TOA; rm fsds < 5% TOA and fsds <> 0; rm 5% fsds < fsus < 95% fsds; if fsds = 0, fsus = 0"

;  print_stats(fsds)
;  print_stats(fsus)
  
  fin_aws->fsds_rigb = fsds
  fin_aws->fsus_rigb = fsus

end do    ; i = stn

print("done!")
end
