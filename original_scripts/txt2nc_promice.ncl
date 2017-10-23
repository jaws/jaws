; Written by Wang Wenshan 2014-11-11 Tuesday 13:57:23
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
;*************************************************************
; Purpose: txt2nc for promice data
; Prototype: txt2nc_promice.ncl
; Note:
;   - no qc?
;
; Structure: see google drive: cloud/promice_stn_info/var
;************************************************************
begin
; read in txt
;------------------------------------------------------------
drc = "/data/wenshanw/promice/"
;drc_in = drc+"dat/wind/"
drc_in = drc+"dat/2016/"
drc_out = drc+"netcdf/"
;drc_in = drc+"check/"
;drc_out = drc+"check/"
;fns = systemfunc("ls "+drc_in+"*.dat*112[23]")
;fns = systemfunc("ls "+drc_in+"s*")
fns = systemfunc("ls "+drc_in+"*.txt")
;fns = systemfunc("ls "+drc_in+"*v02.txt")
nfn = dimsizes(fns)
stns = systemfunc("ls "+drc_in+"*.txt | cut -d '/' -f 7 | cut -d '_' -f 1-2 ")
;stns_p = systemfunc("ls "+drc_in+"*v02.txt | cut -d '/' -f 6 | cut -d '_' -f 1 ")
;stns_s = systemfunc("ls "+drc_in+"*v02.txt | cut -d '/' -f 6 | cut -d '_' -f 2 ")
;print(""+fns)
;print(""+nfn)
;print(""+stns)
;;stns_s(6) = ""
;;print(stns_p+"  "+stns_s)
;exit

ncol = 44       ; the actual col number of the dat file
opt = 1        ; lines to skip at the beginning of the file
;varn = (/"ta","rh","u","ud","ps","fsds","fsus","flds","flus"/)
;varu = (/"degC","%","m/s","deg","hPa","W/m^2","W/m^2","",""/)
varn = (/"ps","ta","rh","u","ud","fsds","fsds_noshift","fsus","fsus_noshift","alb","flds","flus","cf","ts","tilt_east","tilt_north"/)
var_id = (/6,7,10,11,12,13,14,15,16,17,18,19,20,21,34,35/)
varu = (/"hPa","degC","%","m/s","deg","W/m^2","W/m^2","W/m^2","W/m^2","","W/m^2","W/m^2","","degC","deg","deg"/)
nvar = dimsizes(varn)       ; no qc 
;print(""+nvar)
;print(varn+"  "+varu+"  "+var_id)
;exit

; stn id vs name
;------------------------------------------------------------
; naming: no dash; use abbr.
;stns = systemfunc("cat $HOME/cloud/doc/stn/stn24_id-name.txt | awk '{print $2}'")
;stns = systemfunc("cat stn17_id-name.txt | awk '{print $2}'")
;stns = (/"s10","s05","s06","s09"/)
;stn_id_str = systemfunc("cat stn17_id-name.txt | awk '{print $1}'")
;stn_id = toint(stn_id_str)
;;print(stn_id)
;stns!0 = "id"
;stns&id = stn_id
;;print(stns({11}))
;;exit

; new data
;------------------------------------------------------------
yb = 2008
ye = 2016
ny = ye-yb+1
;mth = (/7,8,9/)     ; July
dout = new((/ny,12,31,24,nvar/),float)
dout!0 = "yr"
dout!1 = "mth"
dout!2 = "day"
dout!3 = "hr"
dout!4 = "var"
dout&yr = ispan(yb, ye, 1)
dout&mth = ispan(1,12,1) 
dout&day = ispan(1, 31, 1)
;dout&hr = ispan(0, 23, 1)
dout&hr = fspan(0.5, 23.5, 24)
;dout&var = (/"fsds","fsus","fnns","ttc1","ttc2","tcs1","tcs2","rh1","rh2","ps","albedo","zenith"/)
;var_id = (/3,4,5,6,7,8,9,10,11,12,21,22/)       ; col of var - 1
;dout&var = (/"fsds","fsus","fnns","ttc1","ttc2","tcs1","tcs2","rh1","rh2","u1","u2","ud1","ud2","ps","wind2m","wind10m","wind_height1","wind_height2","albedo","zenith"/)
;var_id = ispan(3,22,1)       ; col of var - 1
dout&var = varn
;var_id = ispan(3,nvar-1+3,1)
;printVarSummary(var_id)
;exit

;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
do i = 0, nfn - 1     ; loop: files (ie, stations)
;do i = 21, 21     ; loop: files (ie, stations)
;do i = 21, nfn - 1     ; loop: files (ie, stations)
;do i = 0, 0     ; loop: files
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  print("i = "+i+" fn = "+fns(i)+" stn = "+stns(i))
  dd = readAsciiTable(fns(i), ncol, "float", opt)
;  print(num(isnan_ieee(dd)))
;  printVarSummary(dd)
;  print(dd(:10,0)+" "+dd(:10,1)+" "+dd(:10,2)+" "+dd(:10,3)+" "+dd(:10,4)+" "+dd(:10,5)+" "+dd(:10,6)+" "+dd(:10,7))
;  exit

;- deal with nan
  if (any(isnan_ieee(dd))) then
    replace_ieeenan(dd, dd@_FillValue, 0)
  end if
  print("#NAN = "+num(isnan_ieee(dd)))
;  exit

  dim_dd = dimsizes(dd)
  nrow = dim_dd(0)
;  print("nrow = "+nrow)
;  stn = toint(dd(0,0))
;  print("stn id = "+stn)
;  exit

  do j = 0, nrow - 1      ; loop: rows
;  do j = 65780, 66880      ; loop: rows
;  do j = 100994, 101994
;  do j = 0, 1000
;    print(""+stn)
    yr = toint(dd(j,0))
    ddd = toint(dd(j,4))

    if (isleapyear(yr)) then
      if (ddd.gt.366) then
        print("Too many ddds: "+yr+"; "+ddd)
        continue
      end if
    else
      if (ddd.gt.365) then
        print("Too many ddds: "+yr+"; "+ddd)
        continue
      end if
    end if 

    if (yr .ge. yb .and. yr .le. ye) then       ; pick the yrs I want
      md = monthday(yr,ddd)
      mth = toint(md/100)
;      print(stn+" "+yr+"  "+day+" "+hr+"  "+mth)
;      if (any(mth .eq. mth) ) then       ; pick up the mth
        dm = md - mth*100
;        hr = toint(dd(j,2))/100
        hr = tofloat(dd(j,3))+0.5					; PROMICE time stamp
        if (hr.ge.24) then
          print("hr too large: "+hr)
          continue
        end if
;        print("stn "+stns(i)+" year = "+yr+" mth = "+mth+" day = "+dm+" hr = "+hr+" "+varn+" = "+dd(j,var_id))
;        exit
        dout({yr},{mth},{dm},{hr},:) = (/dd(j,var_id)/)
;      end if        ; pick up the mth
    end if      ; if done: pick years
  end do      ; loop done: rows
;  print("Row loop done")

  if (all(ismissing(dout))) then
    print(stns(i)+" has no data we want!")
;    delete([/dd, fsds, fsus, fnns,ttc1,ttc2,tcs1,tcs2,rh1,rh2,ps, albedo, zenith/])
;    delete([/dd, fsds, fsus, fnns,ttc1,ttc2,tcs1,tcs2,rh1,rh2,u1,u2,ud1,ud2,ps,wind2m,wind10m,wind_height1,wind_height2, albedo, zenith/])
    delete([/dim_dd, nrow, yr, ddd, md, mth, dm, hr,dd/])
    dout = dout@_FillValue
    continue
  end if

; output nc for each station
;============================================================
  dout = where(dout.eq.999, dout@_FillValue, dout)
  dout = where(dout.eq.-999, dout@_FillValue, dout)

;  fo = "ktrns_"+stns(i)+"_"+yb+"-"+ye+".nc"
;  fo = stns_p(i)+"-"+stns_s(i)+"_"+yb+"-"+ye+".nc"
  fo = stns(i)+"_"+yb+"-"+ye+".nc"
  system("/bin/rm -f "+drc_out+fo)
  fout = addfile(drc_out+fo,"c")

  do k = 0, nvar - 1       ; k = var
    dt = dout(:,:,:,:,k)
    dt@units = varu(k)
    fout->$varn(k)$ = dt
    delete(dt)
  end do

  print("File "+stns(i)+" is done!")
;  delete([/dd, fsds, fsus, fnns,ttc1,ttc2,tcs1,tcs2,rh1,rh2,u1,u2,ud1,ud2,ps,wind2m,wind10m,wind_height1,wind_height2, albedo, zenith/])
  delete([/dim_dd, nrow, yr, ddd, md, mth, dm, hr,dd/])
  dout = dout@_FillValue
end do        ; loop done: files

print("done!")
end
