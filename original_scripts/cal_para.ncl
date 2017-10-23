; Written by Wang Wenshan 2015-02-26 Thursday 11:43:55
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$HOME/cloud/gcnet/cal_ds.ncl"
;*************************************************************
; Series: cal_aw-beta_main
; Role: para function
; Purpose: a batch of equations to cal aw-beta related parameters
; Functions:
;   cal_ET(ddd); return ET(/ddd/)
;   cal_ds(ddd); return ds(/ddd/)
;   procedure para_twte(yr,ddd,lat_deg,tw,te); change tw(/ddd/),te(/ddd/)
;   function hr_SunRiseSet(yr,ddd,lat_deg) ; reture mnt from noon (/ddd/)
;   procedure solar_position(yr,ddd,hr,lat_deg,lon_deg,alpha,as); change alpha(/ddd,hr/),as(/ddd,hr/)
;   function noon(ddd,lon_deg); return gmt_noon(/ddd/)
;   thr_clr_fsds(yr,ddd,hr,lat_deg,lon_deg); return fsds_thr(/ddd,hr/)
; Notes:
;   ALL INPUT TIME must be GMT/UTC (corresponding to mean solar time)
;************************************************************
;- contants
pi = 3.1415926535898d
noon_min = 12*60.        ; local solar noon in minutes
lon_ref = 0       ; GMT ref longitude

;- cal ET: equation of time
;- note: data type is double
undef ("cal_ET")
function cal_ET(ddd)
local B,ET
begin
B = (360.*(todouble(ddd)-81.)/364.)/180.*pi       ; in radians
ET = 9.87*sin(2*B)-7.53*cos(B)-1.5*sin(B)      ; in min
return ET
end

;- cal ds 
;- use the one in cal_ds.ncl instead
;- return double
;undef ("cal_ds")
;function cal_ds(yr,ddd,hr)        ; yr: not used; to match the input of cal_ds in cal_ds.ncl
;;local ds,nday,nhr,dddhr,hrddd
;local ds,nday,nhr,dddhr,hrddd,theta
;begin
;;------------------------------------------------------------
;;- Method 1: from "Principles of Solar Engineering"
;;ds = 23.45*sin(360.*(284.+ddd)/365./180.*pi)/180.*pi        ; in radians
;;ds = asin(sin(23.45/180.*pi)*sin(360.*(284.+ddd)/365./180.*pi))        ; in radians
;;------------------------------------------------------------
;;- Method 2: from Zender's script /home/zender/c/slr_crd.c
;;  theta=2.*M_PI*calendar_day_of_year/DAYS_PER_YEAR;
;;  delta=.006918-.399912*cos(theta)+.070257*sin(theta)-
;;    .006758*cos(2.*theta)+.000907*sin(2.*theta)-
;;      .002697*cos(3.*theta)+.001480*sin(3.*theta);
;nday = dimsizes(ddd)
;nhr = dimsizes(hr)
;dddhr = todouble(conform_dims((/nday,nhr/),ddd,(/0/)))
;hrddd = todouble(conform_dims((/nday,nhr/),hr,(/1/)))/24.
;dddhr = dddhr+hrddd
;;print(dddhr)
;;printVarSummary(dddhr)
;
;theta = new((/nday,nhr/),double)
;ds = new((/nday,nhr/),double)
;theta = 2.*pi*dddhr/365.
;ds = 0.006918-0.399912*cos(theta)+0.070257*sin(theta)-0.006758*cos(2.*theta)+0.000907*sin(2.*theta)-0.002697*cos(3.*theta)+0.001480*sin(3.*theta)
;;printVarSummary(ds)
;;------------------------------------------------------------
;;print("ds = "+ds)
;return ds
;end

;- cal tw and te (azimuth related)
;- note: output tw and te are in solar time
undef ("para_twte")
procedure para_twte(yr,ddd,lat_deg,tw,te)
local lat,ds,hr
begin
lat = lat_deg/180.*pi 
;ds = cal_ds(yr,ddd)
;ds = cal_ds(ddd)
hr = ispan(0,23,1)
ds = dim_avg(cal_ds(yr,ddd,hr))
;ds = cal_ds(yr,ddd,12+3)
;printVarSummary(ds)
;printVarSummary(te)
te = noon_min-(acos(tan(ds)/tan(lat))/pi*180.)/15.*60      ; te in min 
;tt = noon_min-(acos(tan(ds)/tan(lat))/pi*180.)/15.*60      ; te in min 
;printVarSummary(tt)
tw = noon_min+(acos(tan(ds)/tan(lat))/pi*180.)/15.*60      ; tw in min 
end       ; procedure para_twte

;- cal sun-rise and sunset time as mnt from local solar noon
;-    eg, return 319 min; sunrise time = noon - 319 min; sunset time = noon + 319 min
;- comments: a problematic method for sunrise and sunset
;-    sunrise and sunset are defined as alpha = 0. 
;-    a practical definition should be the times when the upper limb of the sun is on horizon
undef ("hr_SunRiseSet")
function hr_SunRiseSet(yr,ddd,lat_deg) 
local lat,ds,hr,mnt_noon
begin
print(yr+"  "+ddd+" "+lat_deg)
lat = lat_deg/180.*pi 
hr = ispan(0,23,1)
ds = dim_avg(cal_ds(yr,ddd,hr))
print("ds = "+ds)
print(-tan(lat)*tan(ds))
mnt_noon = (acos(-tan(lat)*tan(ds)))/pi*180.*4
print("mnt_noon = "+mnt_noon)
return mnt_noon
end       ; procedure hr_SunRiseSet

;- cal alpha and as given dates and hrs
undef ("solar_position")
;- alpha: solar altitude angle
;- as: solar azimuth angle
;- hr: LST at Greenwich
;- opt: 0: input standard time; 1: input solar time
;procedure solar_position(ddd,hr,lat_deg,lon_deg,alpha,as)
;- Note:
;   20160526: try to make possible multi-dimensional hr but stopped 'cos needs to change cal_ds.ncl as well
procedure solar_position(yr:numeric,ddd:numeric,hr:numeric,lat_deg:numeric,lon_deg:numeric,alpha:double,as:double)
local nday,nhr,dim,ET, ds, te, tw, lat,st,hs,st4as,hr_cfm
begin
nday = dimsizes(ddd)
nhr = dimsizes(hr)
;- dim_alpha == dim_as
if (any(dimsizes(alpha).ne.dimsizes(as))) then
  print("Wrong alpha or as input format!")
  print("dim_alpha must be the same as dim_as!")
  exit
end if
;- check dim 'day'
dim = dimsizes(alpha)
if (dim(0).ne.nday) then
  print("Wrong alpha input format!")
  print("alpha = new((/nday,nhr/),double): nday == #ddd")
  exit
end if
;- check dim 'hr'
if (dim(1).ne.nhr) then
  print("Wrong alpha input format!")
  print("alpha = new((/nday,nhr/),double): nhr == #hr")
  exit
end if

lat = lat_deg/180.*pi

;- convert hr to LOCAL solar time if opt = 0
hr_cfm = conform_dims((/nday,nhr/),hr,(/1/))
;!!! temp !!!
;if (opt.eq.0) then          ; standard time --> local solar time
;ET = conform_dims((/nday,nhr/),cal_ET(ddd),(/0/))
ET = conform_dims(dim,cal_ET(ddd),(/0/))
st = hr_cfm*60.+ET+4.*(lon_deg-lon_ref)   ; solar time in min
;else        ; GMT solar time --> local solar time
;  st = hr_cfm*60.+4.*(lon_deg-lon_ref)
;end if        ; output st in (/ddd,hr/)
;- local ,hr_cfm
;mnt = hr*60.

ds = cal_ds(yr,ddd,hr)
;ds = cal_ds(ddd,hr)
;print("max ds = "+max(ds/pi*180.))
;printVarSummary(ds)
tw = new(nday,double)
te = new(nday,double)
para_twte(yr,ddd,lat_deg,tw,te)
;print("solar position ds = "+ds/pi*180.)

do i = 0, nday - 1        ; i = day
;  print("check which data type:")       ; double !!!
;  printVarSummary(st)
  hs = (st(i,:)-noon_min)/4./180.*pi        ; in radians
;  print("standard time = "+mnt+"  solar time = "+st+" hs = "+hs)
  alpha(i,:) = asin(sin(lat)*sin(ds(i,:)) + cos(lat)*cos(ds(i,:))*cos(hs))       ; in radians
;  coszrs = sin(lat)*sin(ds(i)) - cos(lat)*cos(ds(i))*cos((ddd+hr/24.)*2.0*pi+lon_deg/180.*pi)
;  print("coszrs = "+coszrs)

;- CRM cos(sza) = sin(orb_lat)*sin(orb_declin) - cos(orb_lat)*cos(orb_declin)*cos(orb_jday*2.0*orb_pi + orb_lon)

;- check alpha
;    sza = pi/2.-alpha(i,:)       ; in radians
;    print(sza(::2)/pi*180.)
 
  as(i,:) = asin(cos(ds(i,:))*sin(hs)/cos(alpha(i,:)))       ; in radians
  st4as = where(st(i,:).lt.0,st(i,:)+24*60,st(i,:))        ; deal with negative st; not a problem for hs cal though
  as(i,:) = where(st4as.lt.te(i).or.st4as.ge.tw(i), pi-as(i,:), as(i,:))
  as(i,:) = where(as(i,:).gt.pi,as(i,:)-2*pi,as(i,:))       ; not exactly as the book; need to consider negative as
;  print(as)
end do
;  print(as/pi*180.)
;print("hs = "+hs)
end       ; solar_position

;- cal alpha and as given dates and SOLAR TIME
;- assume input is solar time not mean time
;undef ("solar_position_solar_hr")
;;- alpha: solar altitude angle
;;- as: solar azimuth angle
;;- usage: alpha and as (/nday,nhr/)
;;procedure solar_position_solar_hr(ddd,hr,lat_deg,lon_deg,alpha,as)
;procedure solar_position_solar_hr(yr,ddd,hr,lat_deg,lon_deg,alpha,as)
;local nday, nhr, lat, mnt, ds, ET, tw, te, hs, st
;begin
;nday = dimsizes(ddd)
;nhr = dimsizes(hr)
;
;lat = lat_deg/180.*pi
;mnt = hr*60.
;
;;ds = cal_ds(ddd,hr)
;ds = cal_ds(yr,ddd,hr)
;;ds = 0.04172425
;;print("ds = "+ds)
;ET = cal_ET(ddd)
;tw = new(nday,double)
;te = new(nday,double)
;para_twte(yr,ddd,lat_deg,tw,te)
;;ds = 2.15/180.*pi
;;print("solar position solar hr ds = "+ds/pi*180.)
;
;do i = 0, nday - 1        ; i = day
;;  st = mnt+ET(i)+4.*(lon_ref+lon_deg)   ; solar time in min
;  st = mnt-3*60.        ; 3 hr delay; assuming GMT solar time
;  hs = (st-noon_min)/4./180.*pi        ; in radians
;;  print("solar time = "+mnt+" hs = "+hs)
;  alpha(i,:) = asin(sin(lat)*sin(ds(i,:)) + cos(lat)*cos(ds(i,:))*cos(hs))       ; in radians
;  coszrs = sin(lat)*sin(ds(i,:)) - cos(lat)*cos(ds(i,:))*cos((ddd+hr/24.)*2.0*pi+lon_deg/180.*pi)
;;  print("CRM coszrs = "+coszrs+"  sin_alpha = "+sin(alpha(i,:)))
;
;;------------------------------------------------------------
;;- cal st_ideal
;;  sin_alpha = 0.488191
;;  sin_alpha = 0.473327
;;  cos_hs = (sin_alpha-sin(lat)*sin(ds(i)))/(cos(lat)*cos(ds(i)))
;;  print(sin(lat)+"  "+sin(ds(i))+"  "+cos(lat)+"  "+cos(ds(i)))
;;  print("cos_hs = "+cos_hs)
;;  hs = acos(cos_hs)
;;  st = hs/pi*180.*4.+noon_min
;;  mnt = st-ET(i)-4.*(lon_ref+lon_deg)
;;  print("st = "+st+" mnt = "+mnt+" hs = "+hs)
;;------------------------------------------------------------
;
;;- CRM cos(sza) = sin(orb_lat)*sin(orb_declin) - cos(orb_lat)*cos(orb_declin)*cos(orb_jday*2.0*orb_pi + orb_lon)
;
;;- check alpha
;;    sza = pi/2.-alpha(i,:)       ; in radians
;;    print(sza(::2)/pi*180.)
; 
;  as(i,:) = asin(cos(ds(i,:))*sin(hs)/cos(alpha(i,:)))       ; in radians
;  st4as = where(st.lt.0,st+24*60,st)        ; deal with negative st; not a problem for hs cal though
;  as(i,:) = where(st4as.lt.te(i).or.st4as.ge.tw(i), pi-as(i,:), as(i,:))
;  as(i,:) = where(as(i,:).gt.pi,as(i,:)-2*pi,as(i,:))       ; not exactly as the book; need to consider negative as
;end do
;;  print(as/pi*180.)
;;print("hs = "+hs)
;end       ; solar_position_solar_hr

;- cal solar noon in GMT in precision of 0.5 hr
undef ("noon")
function noon(ddd,lon_deg)
local ET,gmt_noon_mnt,gmt_noon
begin
ET = cal_ET(ddd)

gmt_noon_mnt = noon_min-ET-(lon_deg-lon_ref)*4     ; lon in negative so use lon_ref+lon
gmt_noon = round(gmt_noon_mnt/30,1)/2.        ; real solar noon in GMT at 0.5 hr precision; round(*,1): return float
;print(gmt_noon_mnt)
return gmt_noon
end       ; noon

;;- cal solar noon in GMT in precision of 0.5 hr: output solar time
;undef ("noon_st")
;function noon_st(ddd,lon_deg)
;local ET,gmt_noon_st_mnt,gmt_noon_st
;begin
;ET = cal_ET(ddd)
;
;gmt_noon_st_mnt = noon_min-(lon_deg-lon_ref)*4     ; lon in negative so use lon_ref+lon
;gmt_noon_st = round(gmt_noon_st_mnt/30,1)/2.        ; real solar noon in GMT at 0.5 hr precision; round(*,1): return float
;;print(gmt_noon_mnt)
;return gmt_noon_st
;end       ; noon_st

;- cal theoretical fsds
undef ("thr_clr_fsds")
function thr_clr_fsds(yr,ddd,hr,lat_deg,lon_deg)
local Cn,I0,k,df,I_1d,I,alpha,as,fsds_thr,nday,nhr
begin
Cn = 1        ; clearness; don't know the details but ref set it to 1
;I0 = 1367.7       ; solar constant: W/m^2
I0 = 1353       ; solar constant: W/m^2 from the book
k = 0.2       ; average atmospheric optical depth; rough
df = 0.25      ; diffuse ratio

nday = dimsizes(ddd)
nhr = dimsizes(hr)

alpha = new((/nday,nhr/),double)
as = new((/nday,nhr/),double)
solar_position(yr,ddd,hr,lat_deg,lon_deg,alpha,as)
alpha = where(alpha.le.0,2.22507e-38,alpha)       ; deal with negative alpha

I_1d = I0*(1+0.034*cos((360.*ddd/365.25)/180.*pi))     ; (/nday/)
I = conform_dims(dimsizes(alpha),I_1d,(/0/))
;I = conform_dims(dimsizes(alpha),I0,(/-1/))

fsds_thr = Cn*I*exp(-k/sin(alpha))*(df+sin(alpha))      ; theoretical fsds

return fsds_thr
end

;= main function for testing
begin
;= test solar_position hr structure
;stn = "aws14"
;lst_stn = "~/cloud/gcnet/stn_spole.txt"
;stns = systemfunc("cat "+lst_stn+" | awk '{print $1}'")
;lat_deg = tofloat(systemfunc("cat "+lst_stn+" | grep "+stn+" | awk '{print $2}'"))
;lon_deg = tofloat(systemfunc("cat "+lst_stn+" | grep "+stn+" | awk '{print $3}'"))
;
;drc = "/data/wenshanw/aws/spole/"
;drc_in = drc
;fn = systemfunc("ls "+drc_in+"*"+stn+"*2015_new-time-logger.nc")
;fin= addfile(fn,"r")
;time = fin->time
;;printVarSummary(time)
;
;yb = 2009
;ye = 2015
;ny = ye - yb + 1
;mths = (/1,2,3,4,9,10,11,12/)
;nm = dimsizes(mths)
;
;nhr = 24
;alpha = new((/ny,nm,31,nhr/),double)
;as = new((/ny,nm,31,nhr/),double)
;alpha!0 = "yr"
;alpha!1 = "mth"
;alpha!2 = "day"
;alpha!3 = "hr"
;alpha&yr = ispan(yb,ye,1)
;alpha&mth = mths
;alpha&day = ispan(1,31,1)
;;alpha&hr = hr
;copy_VarCoords(alpha,as)
; 
;do yr = yb,ye
;  do i = 0, nm - 1
;    mth = mths(i)
;
;    nday = days_in_month(yr,mth)
;    ddd = new(nday,integer)
;    ddd1 = day_of_year(yr,mth,1)
;    ddd = ispan(ddd1,ddd1+nday-1,1)
;
;    solar_position(yr,ddd,time({yr},{mth},0,:),lat_deg,lon_deg,alpha({yr},{mth},:(nday-1),:),as({yr},{mth},:(nday-1),:))
;  end do
;end do
;
end
