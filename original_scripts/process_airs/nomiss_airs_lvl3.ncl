; Written by Wang, Wenshan 2017-02-06 Monday 10:48:05
load "$HOME/scripts/ncl_script/wenshanw.ncl"
;*************************************************************
; Purpose: use info only from AIRS
; Prototype: track_nomiss_sup_pres.ncl and track_nomiss_sup_pres-stn.ncl
; Note: 
; - one AIRS file one day
; - one day two outputs: A(scending) and D(escending)
; - reverse plev
;*************************************************************
begin
xpt="airx3std"
drc_in="/data/wenshanw/airs/stn_lvl3/"
drc_out="/data/wenshanw/airs/nomiss_lvl3/" 

yr=2016

lst_stn = "stn_run.txt"
stns = systemfunc("cat "+lst_stn+" | awk '{print $1}'")
nstn = dimsizes(stns)
;print("stns = "+stns)
;exit

mb = 5
me = 9
mmb = sprinti("%02i",mb)
mme = sprinti("%02i",me)
nm = me - mb + 1

;- var
nplev = 24
nplev_h2o = 12
pin = new((/nplev+1/),float)       ; pressure lev + surface
tin = new((/nplev+1/),float)       ; pressure lev + surface
qin = new((/nplev+1/),float)       ; pressure lev + surface

sfxs = (/"_A","_D"/)
nsfx = dimsizes(sfxs)

q_top = 1e-7       ; constrain q at TOA

do i = 0, nstn - 1        ; i = stn
  stn = stns(i)

  cmd = "bash -c 'ls "+drc_in+stn+"."+xpt+"."+yr+".{"+mmb+".."+mme+"}.??.nc | cut -d '.' -f 3-5'"
  dates = systemfunc(cmd)
  nfn = dimsizes(dates)
;  print("fns = "+dates)
;  exit

  fin = addfile(drc_in+stn+"."+xpt+"."+dates(0)+".nc","r")
  vp = "StdPressureLev:ascending_TqJoint"
  plev = fin->$vp$(::-1)
  fill_value(plev)
;  print(plev)
;  exit

  do j = 0, nfn - 1       ; j = file
    date = dates(j)

    fn_airs = drc_in+stn+"."+xpt+"."+date+".nc"
    fin = addfile(fn_airs,"r")

    do k = 0, nsfx-1      ; k = A or D
      sfx = sfxs(k)

;= time: daily

;= pressure
;   - use AIRS sfc pressure
;   - fill all missing
;============================================================
      pin(:(nplev-1)) = (/plev/)

      v_ps_airs = "SurfPres_Forecast_TqJ"+sfx
      ps_airs = fin->$v_ps_airs$
;      print(ps_airs+"")
      if (.not.ismissing(ps_airs))
        pin(nplev) = (/ps_airs/)
      else
        print("no ps: "+stn+" "+date+" "+sfx)
        continue
      end if

;= temperature
;============================================================
      v_t_airs = "Temperature_TqJ"+sfx
      tin(:(nplev-1)) = (/fin->$v_t_airs$(::-1)/)
      v_ta_airs = "SurfAirTemp_TqJ"+sfx
      ta_airs = fin->$v_ta_airs$
      if (.not.ismissing(ta_airs))
        tin(nplev) = (/ta_airs/)
      end if
;- check ts first, since no ts --> no simu
      v_ts_airs = "SurfSkinTemp_TqJ"+sfx
      ts_airs = fin->$v_ts_airs$
      if (ismissing(ts_airs))
        print("no ts: "+stn+" "+date+" "+sfx)
        continue
      end if

;= water vapor mixing ratio
;============================================================
      v_q_airs = "H2O_MMR_TqJ"+sfx
      qin(0) = (/q_top/)
      qin((nplev - nplev_h2o):(nplev-1)) = (/fin->$v_q_airs$(::-1)/1000./)        ; unit: kg/kg
      v_qs_airs = "H2O_MMR_Surf_TqJ"+sfx
      qs_airs = fin->$v_qs_airs$
      if (.not.ismissing(qs_airs))
        qin(nplev) = (/qs_airs/1000./)
      end if

;- all pressure >= ps
      tin(:(nplev-1)) = where(pin(:(nplev-1)).gt.(pin(nplev)-5), tin@_FillValue,tin(:(nplev-1)))        ; fill plev larger than sfc; -5 safety measure)
      qin(:(nplev-1)) = where(pin(:(nplev-1)).gt.(pin(nplev)-5), qin@_FillValue,qin(:(nplev-1)))        ; fill plev larger than sfc; -5 safety measure)
      pin(:(nplev-1)) = where(pin(:(nplev-1)).gt.(pin(nplev)-5), pin@_FillValue,pin(:(nplev-1)))        ; fill plev larger than sfc; -5 safety measure)

;- fill missing
;      print(pin+" "+tin+" "+qin)
      pin = linmsg(pin, -1)       ; beginning and end set to the nearest non-missing value
      pout = (/pin(:(nplev-1))/)

      tin = int2p(pin,tin,pin,-2)
      tout = (/tin(:(nplev-1))/)
      qin = int2p(pin,qin,pin,-2)     ; log interpolation; might extrapolate
      qout = (/qin(:(nplev-1))/)

;      print(pin+" "+tin+" "+qin)
;      print(ps_airs+" "+ta_airs+" "+ts_airs+" "+qs_airs)
;      exit

;= Ozone
      fin_o3 = addfile("o3_lev73_sub-Arctic.nc","r")
      o3in = fin_o3->o3
      o3out = int2p_Wrap(o3in&plev,o3in,pout,-2)

;= output
      pout!0 = "PLEV"
      pout@units = "hPa"
      pout@long_name = "Pressure profile: diff every grid point from AIRS (StdPressureLev:ascending_TqJoint)"
      pout@interp = "NCL linmsg: AIRS use surface pressure as constrain"
      tout!0 = "PLEV"
      tout@units = "K"
      tout@long_name = "Temperature profile from AIRS (Temperature_TqJ"+sfx+")"
      tout@interpolation = "Surface constrained by AIRS sfc or extrapolation; no profile shift"
      tout@interpolation_method = "NCL int2p; log"
      qout!0 = "PLEV"
      qout@units = "kg/kg"
      qout@long_name = "Water vapor mixing ratio profile from AIRS (H2O_MMR_TqJ"+sfx+")"
      qout@interpolation = "Surface constrained by AIRS sfc or extrapolation; no profile shift"
      qout@interpolation_method = "NCL int2p; log"
      o3out@units = "kg/kg"
      o3out@long_name = "Ozone volume mixing ratio from lev73 sub-Arctic"
      o3out@interpolation = "Extrapolated to the surface"
      o3out@interpolation_method = "NCL int2p_Wrap; log"
;    printVarSummary(pout)
;    printVarSummary(tout)
;    printVarSummary(qout)
;    printVarSummary(o3out)
 
;      solzen = fin->solzen
;      solzen@long_name = "Solar Zenith Angle"
;      solazi = fin->solazi
;      solazi@long_name = "Solar Azimuth Angle"
;      cf = fin->CldFrcTot
;      cf@long_name = "Total Cloud Frction"
;      cf_qc = fin->CldFrcTot_QC
;      cf_qc@long_name = "Quality Flag for Total Cloud Frction"
;      land_frc = fin->landFrac
;      land_frc@long_name = "Land Fraction"
  
      sfc_air_tmp = (/tin(nplev)/)
      sfc_air_tmp!0 = "scaler"
      sfc_air_tmp@long_name = "Near-surface air temperature: tin(nplev) --> AIRS (SurfAirTemp_TqJ) or extrap"
      sfc_air_tmp@units = "K"

      skin_tmp = (/ts_airs/)
      skin_tmp!0 = "scaler"
      skin_tmp@long_name = "Ground/surface (skin) temparature: AIRS (SurfSkinTemp_TqJ)"
      skin_tmp@units = "K"

      sfc_prs = (/ps_airs/) 
      sfc_prs!0 = "scaler"
      sfc_prs@long_name = "Surface pressure from AIRS (SurfPres_Forecast_TqJ)"
      sfc_prs@units = "hPa"

      sfc_q = (/qin(nplev)/)
      sfc_q@long_name = "Surface water vapor mixing ratio: AIRS (H2O_MMR_Surf_TqJ) or extrap"
      sfc_q@units = "kg/kg"
  
      fo = drc_out+stn+"."+xpt+"."+date+sfx+".nc"
;      print("fo = "+fo)
;      exit
      system("/bin/rm -f "+fo)
      fout = addfile(fo,"c")
      fout->plev = pout
      fout->t = tout
      fout->q = qout
      fout->o3 = o3out
  
;      fout->solzen = solzen
;      fout->solazi = solazi
;      fout->cf = cf
;      fout->cf_qc = cf_qc
;      fout->time = time
  
      fout->sfc_tmp = skin_tmp
      fout->sfc_air_tmp = sfc_air_tmp
      fout->sfc_q = sfc_q
      fout->sfc_prs = sfc_prs
;      fout->land_frc = land_frc

      pin = pin@_FillValue
      tin = tin@_FillValue
      qin = qin@_FillValue
    end do        ; k = A or D
  end do        ; j = file

  delete(dates)
end do        ; i = stn

print("done!")
end
