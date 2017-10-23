; Written by Wang, Wenshan 2017-04-18 Tuesday 11:09:13
load "$HOME/scripts/ncl_script/wenshanw.ncl"
;*************************************************************
; Purpose: txt2nc for GC-Net
; - time stamp
; - including qc flags
; Data sample see google drive cloud/gcnet_samples.spreadsheet
;*************************************************************
begin
drc_in = "/data/wenshanw/gcnet/dat/2016/"
drc_out = "/data/wenshanw/gcnet/netcdf/"

lst_stn = "stn17_id-name.txt"
stns = systemfunc("cat "+lst_stn+" | awk '{print $2}'")
stns_id = toint(systemfunc("cat "+lst_stn+" | awk '{print $1}'"))
nstn = dimsizes(stns)
;print(stns_id+" "+stns)

yb = 2008
ye = 2016
ny = ye-yb+1

ncol = 52       ; the actual col number of the dat file
opt = 54        ; lines to skip at the beginning of the file
varn = (/"fsds","fsus","fnns","ttc1","ttc2","tcs1","tcs2","rh1","rh2","u1","u2","ud1","ud2","pres","snow_height1","snow_height2","tsnow1","tsnow2","tsnow3","tsnow4","tsnow5","tsnow6","tsnow7","tsnow8","tsnow9","tsnow10","battery","fsds_max","fsus_max","fnns_max","ttc1_max","ttc2_max","ttc1_min","ttc2_min","u1_max","u2_max","u1_stddev","u2_stddev","ref_tmp","u2m","u10m","wind_sensor_height1","wind_sensor_height2","albedo","sza"/)
varu = (/"W/m^2","W/m^2","W/m^2","degC","degC","degC","degC","%","%","m/s","m/s","deg","deg","hPa","m","m","degC","degC","degC","degC","degC","degC","degC","degC","degC","degC","V","W/m^2","W/m^2","W/m^2","degC","degC","degC","degC","m/s","m/s","m/s","m/s","degC","m/s","m/s","m","m","","deg"/)
nvar = 45

dout = new((/ny,12,31,24,nvar/),float)
dout!0 = "yr"
dout!1 = "mth"
dout!2 = "day"
dout!3 = "hr"
dout!4 = "var"
dout&yr = ispan(yb, ye, 1)
dout&mth = ispan(1,12,1) 
dout&day = ispan(1, 31, 1)
dout&hr = fspan(0.5, 23.5, 24)

var_id = ispan(3,nvar-1+3,1)

;= qc
varn_qc = (/"fsds","fsus","fnns","ttc1","ttc2","tcs1","tcs2","rh1","rh2","u1","u2","ud1","ud2","pres","snow_height1","snow_height2","tsnow1","tsnow2","tsnow3","tsnow4","tsnow5","tsnow6","tsnow7","tsnow8","tsnow9","tsnow10","battery"/)
varn_qc = varn_qc+"_qc"
nvar_qc = 27       ; deal with qc in txt2nc_gcnet_qc.ncl

dout_qc = new((/ny,12,31,24,nvar_qc/),float)
copy_VarCoords_1(dout,dout_qc)
dout_qc!4 = "var"
var_id_qc = (/49,50,51,52/)        ; 1-based
;printVarSummary(dout_qc)
;exit

zero_offset = charactertoshort(stringtocharacter("0"))        ; string "0" = integer "48"

do i = 0, nstn - 1    ; i = stn
  stn_id = stns_id(i)
  stn = stns(i)

  fn = systemfunc("ls "+drc_in+sprinti("%02i",stn_id)+"c.dat_*")
  fo = drc_out+stn+"."+yb+"-"+ye+".nc"
  print(fn+"  "+fo)

  din = readAsciiTable(fn, ncol, "float", opt)
  din_qc_all = asciiread(fn, -1, "string")
  din_qc = din_qc_all(opt:)
  delete(din_qc_all)

;- deal with nan
  if (any(isnan_ieee(din))) then
    replace_ieeenan(din, din@_FillValue, 0)     ; option = 0: currently not used
  end if

  dim_din = dimsizes(din)
  nrow = dim_din(0)

;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  do j = 0, nrow - 1      ; j = rows
;  do j = 0, 50      ; j = rows
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    if (din(j,1).eq.yb.and.din(j,2).eq.1)
      continue    ; skip 20080101 0 --> avg (20071231 23 -> 24)
    end if
    yr = toint(din(j,1))
    ddd = toint(din(j,2))
;    print(yr+"  "+ddd)

    if (isleapyear(yr)) then
      if (ddd.gt.366) then
        print("Too many ddds: "+yr+"; "+din(j,2))
        continue
      end if
    else
      if (ddd.gt.365) then
        print("Too many ddds: "+yr+"; "+din(j,2))
        continue
      end if
    end if 

    if (yr .ge. yb .and. yr .le. ye) then       ; pick the yrs I want
      md = monthday(yr,ddd)
      mth = toint(md/100)
      day = md - mth*100

      hh = round((din(j,2)-ddd)*24, 3)
      if (hh.ge.24) then
        print("hr too large: "+hh+" "+yr+"  "+din(j,2))
        continue
      end if
      hr = hh-0.5
      valid_time(yr,mth,day,hr,0)

;      print(din(j,2)+"  "+mth+" "+day+" "+hr)

      dout({yr},{mth},{day},{hr},:) = (/din(j,var_id)/)

;= qc
      dat_qc = toshort(stringtocharacter(str_get_field(din_qc(j),var_id_qc(0)," "))) - zero_offset(0)
      dout_qc({yr},{mth},{day},{hr},:7) = (/dat_qc(:7)/)
      dat_qc = toshort(stringtocharacter(str_get_field(din_qc(j),var_id_qc(1)," "))) - zero_offset(0)
      dout_qc({yr},{mth},{day},{hr},8:15) = (/dat_qc(:7)/)
      dat_qc = toshort(stringtocharacter(str_get_field(din_qc(j),var_id_qc(2)," "))) - zero_offset(0)
      dout_qc({yr},{mth},{day},{hr},16:23) = (/dat_qc(:7)/)
      delete(dat_qc)
      dat_qc = toshort(stringtocharacter(str_get_field(din_qc(j),var_id_qc(3)," "))) - zero_offset(0)
      dout_qc({yr},{mth},{day},{hr},24:) = (/dat_qc(:2)/)
      delete(dat_qc)

;= print test
;      str_prt = ""
;      do k = 0, nvar_qc-1
;        str_prt = str_prt+dout_qc({yr},{mth},{day},{hr},k)
;      end do
;      print("qc = "+str_prt)

    end if    ; pick the yrs I want
  end do    ; j = rows

;= output
  if (all(ismissing(dout))) then
    print(stn+" has no data we want!")
    delete([/din,din_qc/])
    dout = dout@_FillValue
    dout_qc = dout_qc@_FillValue
    continue
  end if

  dout = where(dout.eq.999, dout@_FillValue, dout)

  system("/bin/rm -f "+fo)
  fout = addfile(fo,"c")

  do k = 0, nvar - 1       ; k = var
    dt = dout(:,:,:,:,k)
    dt@units = varu(k)
    fout->$varn(k)$ = dt
    delete(dt)
  end do

  do k = 0, nvar_qc - 1       ; k = var
    dt = dout_qc(:,:,:,:,k)
    dt@long_name = "QC: "+varn(k)
    dt@description = "1: unmodified; 2: linearly interpolated; 3: device frozen; 5: radiation fill; 6,7: wind problem; 8: tmp estimated from RH; 9: filled"
    fout->$varn_qc(k)$ = dt
    delete(dt)
  end do

  glbatt = True
  glbatt@txt2nc_script = "txt2nc_gcnet.ncl"
  fileattdef(fout,glbatt)

  print("File "+stn+" is done!")

  delete([/din,din_qc/])
  dout = dout@_FillValue
  dout_qc = dout_qc@_FillValue
end do    ; i = stn

print("done!")
end
