; Written by Wang Wenshan 2015-04-10 Friday 14:36:52
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "~/scripts/ncl_script/math.ncl"
load "cal_para.ncl"
;*************************************************************
; Purpose: remove dents and interp
; Method:
;   - Try 1: compare the differencials of fsds and fsus
; Steps:
;   - 0.05*TOA < fsds < TOA from CERES
;   - 0.1*fsds < fsus < fsds*0.99
;   - dent free
;************************************************************
begin
;- para
thd = 0.1       ; dent-free threshold = 0.1

lst_stn = "~/cloud/gcnet/stn_spole.txt"
stns = systemfunc("cat "+lst_stn+" | awk '{print $1}'")
nstn = dimsizes(stns)
;yb = 2009
;ye = 2010
yb = 2011
ye = 2015
ny = ye - yb + 1
;mb = 9
;me = 9
;nm = me - mb + 1
mths = (/1,2,3,4,9,10,11,12/)
nm = dimsizes(mths)
;print("stn = "+stns)
;exit

;drc_gc = "/data/wenshanw/gcnet/tilt_df/"
drc_gc = "/data/wenshanw/aws/spole/"

drc_crs = "/data/wenshanw/ceres/stn_gkp/"
var_crs = "toa_comp_sw-down_all_3h"
;hr = fspan(0.5,23.5,24)
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
hr_crs = fspan(1.5,22.5,8)
;hr_crs = fspan(1.5,22.5,8)+12./60.
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

toa = new((/ny,nm,31,24/),float)
toa!0 = "yr"
toa!1 = "mth"
toa!2 = "day"
toa!3 = "hr"
toa&yr = ispan(yb,ye,1)
;toa&mth = ispan(mb,me,1)
toa&mth = mths
toa&day = ispan(1,31,1)
fsds_thr = toa

;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
do i = 0, nstn - 1        ; i = stn
;do i = 1, 1        ; i = stn
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  stn = stns(i)
  lat_deg = tofloat(systemfunc("cat "+lst_stn+" | grep "+stn+" | awk '{print $2}'"))
  lon_deg = tofloat(systemfunc("cat "+lst_stn+" | grep "+stn+" | awk '{print $3}'"))
;  print("stn = "+stn+" lat = "+lat_deg+" lon = "+lon_deg)
;  exit

;- dent-free
;-- read gcnet
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
;  fn_gc = drc_gc+stn+"_tilt-fixed.nc"
;  fn_gc = drc_gc+stn+"_tilt-fixed_Sept.nc"
  fn_gc = drc_gc+stn+"_tilt-fixed_hr05.nc"
;  fn_gc = drc_gc+stn+"_tilt-fixed_hr07.nc"
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
;  fin_gc = addfile(fn_gc,"r")
  fin_gc = addfile(fn_gc,"w")
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  fsds = tofloat(fin_gc->fsds_fixed({yb:ye},{mths},:,:))
  fsus = fin_gc->fsus_gc({yb:ye},{mths},:,:)
  hr = fin_gc->hr
  toa&hr = hr
  fsds_thr&hr = hr
  copy_VarCoords(fsus,fsds)
;  print("hr = "+hr)
;  exit

;-- cal albedo
  fsds_alb = where(fsds.le.0.or.fsus.lt.0,fsds@_FillValue,fsds)
  alb = fsus/fsds_alb
  dff = abs(dffrt(dffrt(alb,hr,0.01,1),hr,0.01,1))      ; !!! abs is important!!!

;  print("# start = "+num(.not.ismissing(fsds)))
;  print("start = "+fsds(0,0,{11},:)+" "+dff(0,0,10,:))
  fsds = where(.not.ismissing(dff).and.dff.gt.thd, fsds@_FillValue, fsds)
;  print("# albedo = "+num(.not.ismissing(fsds)))
;  print("albedo = "+fsds(0,0,{11},:))
;  exit

  delete([/fsds_alb,alb,dff/])

;- TOA
;- fsds, fsus
  fsds = where(fsds.lt.0,0,fsds)
;  print("# fsds < 0 = "+num(.not.ismissing(fsds)))
;  print("fsds<0 = "+fsds(0,0,{11},:))
  fsds = where(fsus.eq.0,0,fsds)
;  print("# fsus = 0 = "+num(.not.ismissing(fsds)))
;  print("fsus=0 = "+fsds(0,0,{11},:))
  
;-- read CERES
;     8 hr ---> 24 hr
;  fn_crs = drc_crs+stn+".smr.2007-2013.3hr.format.nc"
  fn_crs = systemfunc("ls "+drc_crs+stn+".*.nc")
  fin_crs = addfile(fn_crs,"r")
  toa_3hr = fin_crs->$var_crs$({yb:ye},{mths},:,:)
  toa = toa@_FillValue
  do yr = yb, ye        ; yr
    do j = 0, nm - 1       ; mth
      mth = mths(j)
      do day = 1, 31        ; day
        hr_id  = ind(.not.ismissing(toa_3hr({yr},{mth},{day},:)))
        if (num(.not.ismissing(hr_id)).lt.2) then
          delete(hr_id)
          continue
        end if
        toa({yr},{mth},{day},:) = ftcurv(hr_crs(hr_id),toa_3hr({yr},{mth},{day},hr_id),hr)
    
        delete(hr_id)
      end do        ; day
;- if TOA is missing, use thr
      nday_mth = days_in_month(yr,mth)
      days = ispan(1,nday_mth,1)
      ddd0 = day_of_year(yr,mth,1)
      ddd = ispan(ddd0,ddd0+nday_mth-1,1)
      fsds_thr({yr},{mth},{days},:) = tofloat(thr_clr_fsds(yr,ddd,hr,lat_deg,lon_deg))
      delete([/nday_mth,days,ddd,ddd0/])
    end do        ; mth
  end do        ; yr
;- if TOA is missing, use thr
  toa = where(ismissing(toa),fsds_thr,toa)
;- fsds vs TOA
  fsds = where(fsds.gt.toa.or.fsds.lt.toa*0.05,fsds@_FillValue,fsds)      ; remove impossible fsds
;  print("# toa = "+num(.not.ismissing(fsds)))
;  print("toa = "+fsds(0,0,{11},:))
;  exit
  fsus = where(fsds.gt.toa.or.fsds.lt.toa*0.05,fsus@_FillValue,fsus)      ; remove fsus as well; cannot tell whether it's right

;- fsus vs fsds
  fsus = where(fsus.gt.fsds*0.99.or.fsus.lt.fsds*0.1,fsus@_FillValue,fsus)    ; remove impossible fsus

;- give back 0 W/m^2
  fsds = where(fsds_thr.eq.0,0,fsds)
  fsus = where(fsds.eq.0,0,fsus)
  
;- output
  fsds@long_name = "fsds after dent_free"
  fsus@long_name = "fsus after dent_free"
;  printVarSummary(fsds)
;  fo = drc_gc+stn+"_dent-test.nc"
;  system("/bin/rm -f "+fo)
;  fout = addfile(fo,"c")
;  fin_gc->fsds_dent({yb:ye},{mb:me},:,:) = fsds
;  fin_gc->fsus_dent({yb:ye},{mb:me},:,:) = fsus
;  print_stats(fsds)
;  print_stats(fsus)
;  exit
  fin_gc->fsds_dent = fsds
  fin_gc->fsus_dent = fsus
end do        ; i = stn

print("done!")
end
