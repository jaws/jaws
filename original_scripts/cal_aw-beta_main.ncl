; Written by Wang Wenshan 2015-02-26 Thursday 11:18:17
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "cal_parts.ncl"
;*************************************************************
; Series: cal_aw-beta_main
; Role: main function
; Purpose: cal (aw,beta) given clr days in that month
; Usage:
;   - change lst_in and lst_out
;************************************************************
begin
;- constants
;============================================================
pi = 3.1415926535898d
;lon_ref = 0       ; GMT ref longitude
;noon_min = 12*60.        ; local solar noon in minutes
;df = 0.2        ; clr-sky diffuse ratio

;- para
;============================================================
;- input list
;lst_in = "clr-days.txt"
lst_in = "clr-days_test.txt"

;- output list
;lst_out = "tilt_netcdf/lst-pair_aw-beta_all-stn.txt"
;lst_out = "tilt_netcdf/lst-pair_aw-beta_all-stn_no-early-morning.txt"
;lst_out = "tilt_netcdf/lst-pair_aw-beta_all-stn_no-high-sza.txt"
lst_out = "tilt_netcdf/lst-pair_aw-beta_all-stn_working.txt"
;lst_out = "tilt_netcdf/lst-pair_aw-beta_all-stn_no-late-morning.txt"
;lst_out = "tilt_netcdf/lst-pair_aw-beta_all-stn_noon.txt"
system("/bin/rm -f "+lst_out)
system("echo stn yyyymm aw/radians beta/radians >> "+lst_out)

;- input
;============================================================
str = asciiread(lst_in,-1,"string")
nln = dimsizes(str)
lst_stn = "~/cloud/gcnet/stn_spole.txt"

;!!! temp !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
do i = 0, nln-1       ; i = line
;do i = 31, nln-1       ; i = line
;do i = 0, 0       ; i = line
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

;- get rid of comments
  ln = str_split(str_get_field(str(i),1,"%")," ")       ; opt: 1: ignores any delimiter inside single quotes
;  print(ln)
  stn = ln(0)
  lat_deg = tofloat(systemfunc("cat "+lst_stn+" | grep "+stn+" | awk '{print $2}'"))
  lon_deg = tofloat(systemfunc("cat "+lst_stn+" | grep "+stn+" | awk '{print $3}'"))
  lat = lat_deg/180.*pi
;  print(stn+" "+lat_deg+" "+lon_deg)
  
  yrs = toint(ln(1:))/10000
  mths = toint(str_get_cols(ln(1:),4,5))
  days = toint(str_get_cols(ln(1:),6,7))
  ddd = day_of_year(yrs,mths,days)
  print(stn+" "+yrs(0)+"  "+mths(0))

;- temp
;  fo = "aw-beta_temp.nc"
;  fo = "temp_tilt.nc"

;- part 1: get all the possible aw-beta pairs (phase shift condition)
;============================================================
  pair_pbl = pbl_prs(stn,lat_deg,lon_deg,yrs,mths,days,ddd)        ; output all the possible aw-beta pairs
  if (all(pair_pbl(0,:).eq.-999)) then
;    print("All zero part 1")     ; reason will be addressed in cal_parts
    system("echo "+stn+" "+yrs(0)+sprinti("%02i",mths(0))+" missing >> "+lst_out)
    delete([/yrs,mths,days,ddd/])
    delete([/ln,pair_pbl/])
    continue
  end if
;============================================================
;!!! check part 1 function !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
;  delete([/pair_pbl,ln/])
;  delete([/yrs,mths,days,ddd/])
;  continue
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
;  print(pair_pbl(:,0)+" "+pair_pbl(:,1))
;  printVarSummary(pair_pbl)        ; (/npair,2/)
;  system("/bin/rm -f "+fo)
;  fout = addfile(fo,"c")
;  fout->pair_pbl = pair_pbl
;  exit

;- part 2: check corrected fsds with CRM fsds
;------------------------------------------------------------
;- read part 1 results in for test
;  fo = "temp_tilt.nc"
;  fin = addfile(fo,"r")
;  pair_pbl = fin->pair_pbl
;============================================================
  pair_top = crm_match(stn,lat_deg,lon_deg,yrs,mths,days,ddd,pair_pbl)        ; output the top pairs close to CRM simu
  dim_pair_top = dimsizes(pair_top)
;  print(pair_top)
  if (all(pair_top(0,:).eq.-999)) then        ; no pair
;    print("All zero part 2")     ; reason will be addressed in cal_parts
    system("echo "+stn+" "+yrs(0)+sprinti("%02i",mths(0))+" missing >> "+lst_out)
    delete([/yrs,mths,days,ddd/])
    delete([/ln,pair_pbl,pair_top/])
    delete(dim_pair_top)
    continue
  end if
  if (dim_pair_top(0).eq.1) then       ; only one pair
    print("Only one aw-beta pair; Output directly")
    system("echo "+stn+" "+yrs(0)+sprinti("%02i",mths(0))+" "+pair_top(0,0)+" "+pair_top(0,1)+" >> "+lst_out)
    delete([/yrs,mths,days,ddd/])
    delete([/ln,pair_pbl,pair_top/])
    delete(dim_pair_top)
    continue
  end if
;============================================================

;  printVarSummary(pair_top)
;  system("/bin/rm -f "+fo)
;  fout = addfile(fo,"c")
;  fout->pair_top = pair_top
;  if (all(pair_top).eq.0.) then
;    print("Fail at pair_top")
;    system("echo "+stn+" "+yrs(0)+sprinti("%02i",mths(0))+" missing >> "+lst_out)
;    continue
;  end if

;- part 3: pick the one with the least spikes
;  fo = "temp_tilt.nc"
;  fin = addfile(fo,"r")
;  pair_top = fin->pair_top

;============================================================
  no_spike(stn,lat_deg,lon_deg,yrs,mths,days,ddd,pair_top,lst_out)        ; output the final pair to lst_out
;============================================================
;  print(pair(0)/pi*180.+" "+pair(1)/pi*180.)

  delete([/ln,pair_pbl,pair_top/])
;  delete([/ln,pair_top/])
  delete([/yrs,mths,days,ddd/])
  delete(dim_pair_top)
end do         ; i = line

print("done!")
end
