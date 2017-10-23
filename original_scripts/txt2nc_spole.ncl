; Written by Wang, Wenshan 2016-05-19 Thursday 15:35:08
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$HOME/scripts/ncl_script/wenshanw.ncl"
;*************************************************************
; Purpose: txt2nc for aws from IMAU
; Note:
;   - AWS14: 2 hr in advance from 200901 to 20110105; 2 hr lag from 20110106 to 20110115
;       it's actually 2 hr 12 mnt; use time var to keep record
;************************************************************
begin
drc = "/data/wenshanw/aws/spole/"
fn = "AWS14_SWdata_Wenshan.txt"

ncol = 5
opt = 0

varn = (/"fsds","fsus"/)
varu = (/"W/m^2","W/m^2"/)
nvar = dimsizes(varn)

yb = 2009
ye = 2010
ny = ye-yb+1
mb = 1
me = 12
nm = me-mb+1
nhr = 24

dout = new((/ny,nm,31,nhr,nvar/),float)
dout!0 = "yr"
dout!1 = "mth"
dout!2 = "day"
dout!3 = "hr"
dout!4 = "var"
dout&yr = ispan(yb,ye,1)
dout&mth = ispan(mb,me,1) 
dout&day = ispan(1,31,1)
;dout&hr = fspan(0.5,23.5,nhr)+0.5
dout&hr = fspan(0,23,nhr)

var_id = ispan(3,nvar-1+3,1)

dd = readAsciiTable(drc+fn, ncol, "float", opt)
;print(num(isnan_ieee(dd)))
;print(dd(:10,0)+" "+dd(:10,1)+" "+dd(:10,2)+" "+dd(:10,3)+" "+dd(:10,4))
;exit

;- deal with nan
if (any(isnan_ieee(dd))) then
  replace_ieeenan(dd, dd@_FillValue, 0)
end if
;print(num(isnan_ieee(dd)))
;exit

dim_dd = dimsizes(dd)
nrow = dim_dd(0)
;print("nrow = "+nrow)
;stn = toint(dd(0,0))
stn = "aws14"
;print("stn id = "+stn)
;exit

do j = 0, nrow - 1      ; loop: rows
  yr = toint(dd(j,0))
  ddd = toint(dd(j,1))

;  if (isleapyear(yr)) then
;    if (ddd.gt.366) then
;      print("Too many ddds: "+yr+"; "+ddd)
;      continue
;    end if
;  else
;    if (ddd.gt.365) then
;      print("Too many ddds: "+yr+"; "+ddd)
;      continue
;    end if
;  end if 
;  print(j+" "+yr+"  "+ddd)
;  if (j.lt.24)
;    continue
;  end if
;  exit

  if (yr .ge. yb .and. yr .le. ye) then       ; pick the yrs I want
    hr = tofloat(dd(j,2))/100
    if (isleapyear(yr)) then
      if (ddd.eq.367) then
        yr = yr+1
        ddd = 1
        hr = 0
      end if
    else
      if (ddd.eq.366) then
        yr = yr+1
        ddd = 1
        hr = 0
      end if
    end if
    md = monthday(yr,ddd)
    mth = toint(md/100)
;      print(stn+" "+yr+"  "+day+" "+hr+"  "+mth)
;      if (any(mth .eq. mon) ) then       ; pick up the mth
    dm = md - mth*100
    if (hr.gt.24) then
      print("hr too large: "+hr)
      continue
    end if

;= time logger problem
    if (toint(yr+sprinti("%02i",mth)+sprinti("%02i",dm)).le.20110105) then
;      hr = hr+2
;      hr = hr+3.5
      hr = hr+2.5
;    else if (toint(yr+sprinti("%02i",mth)+sprinti("%02i",dm)).le.20110115) then
;      hr = hr-2
;    end if
    end if

;= time stamp
    hr = hr - 0.5  
    if (hr.lt.0) then
      dm = dm - 1
      hr = hr+24
      if (dm.lt.1) then
        mth = mth - 1
        if (mth.lt.1) then
          yr = yr -1
          mth = mth+12
          if (yr.lt.yb) then
            continue
          end if
        end if
        dm = dm+days_in_month(yr,mth)     ; must be at this place after the alternate of mth and yr
      end if
    end if
    if (hr.ge.24) then
      hr = hr-24
      dm = dm+1
      if (dm.gt.days_in_month(yr,mth)) then
        dm = dm-days_in_month(yr,mth)
        mth = mth+1
        if (mth.gt.12) then
          mth = mth-12
          yr = yr+1
          if (yr.gt.ye) then
            continue
          end if
        end if
      end if
    end if

;    print("hr = "+hr)
    dout({yr},{mth},{dm},{hr},:) = (/dd(j,var_id)/)
  end if      ; if done: pick years
end do      ; loop done: rows
print("Row loop done")

if (all(ismissing(dout))) then
  print(stns(i)+" has no data we want!")
;    delete([/dd, fsds, fsus, fnns,ttc1,ttc2,tcs1,tcs2,rh1,rh2,ps, albedo, zenith/])
;    delete([/dd, fsds, fsus, fnns,ttc1,ttc2,tcs1,tcs2,rh1,rh2,u1,u2,ud1,ud2,ps,wind2m,wind10m,wind_height1,wind_height2, albedo, zenith/])
  delete([/dim_dd, nrow, yr, ddd, md, mth, dm, hr,dd/])
  dout = dout@_FillValue
end if

; output nc for each station
;============================================================
dout = where(dout.eq.999, dout@_FillValue, dout)
dout = where(dout.eq.-9999, dout@_FillValue, dout)

;- AWS 14 time var
;time = new((/ny,nm,31,nhr/),float)
;copy_VarCoords(dout(:,:,:,:,0),time)
;time = conform_dims(dimsizes(time),fspan(0.5,23.5,nhr),(/3/))
;time({2009:2010},:,:,:) = conform_dims(dimsizes(time({2009:2010},:,:,:)),fspan(0.5,23.5,nhr)+12./60.,(/3/))
;time({2011},{1},{:5},:) = conform_dims(dimsizes(time({2011},{1},{:5},:)),fspan(0.5,23.5,nhr)+12./60.,(/1/))
;time({2011},{1},{6:15},:) = conform_dims(dimsizes(time({2011},{1},{6:15},:)),fspan(0.5,23.5,nhr)-12./60.,(/1/))
;time@note = "2 hr 12 mnt in advance from 200901 to 20110105; 2 hr 12 mnt lag from 20110106 to 20110115"
dout&hr = dout&hr+2/60.

;fo = "ktrns_"+stns(i)+"_"+yb+"-"+ye+"_v20150930.nc"
;fo = drc+stn+"_sw_2009-2015.nc"
;fo = drc+stn+"_sw_2011-2015_new-time-logger.nc"
fo = drc+stn+"_sw_2009-2010_3h32m.nc"
system("/bin/rm -f "+fo)
fout = addfile(fo,"c")

do k = 0, nvar - 1       ; k = var
  dt = dout(:,:,:,:,k)
  dt@units = varu(k)
;- AWS14
  dt@WARNING = "Time var is correct for both files"
;------------------------------------------------------------
  fout->$varn(k)$ = dt
  delete(dt)
end do

;fout->time = time

;delete([/dim_dd, nrow, yr, ddd, md, mth, dm, hr,dd,time/])
delete([/dim_dd, nrow, yr, ddd, md, mth, dm, hr,dd/])
dout = dout@_FillValue

print("done!")
end
