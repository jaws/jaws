; Written by Wang Wenshan 2015-03-03 Tuesday 10:51:36
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "cal_para.ncl"
;*************************************************************
; Purpose: correct using lst of aw-beta pairs
; Steps:
;   - read in tilt_netcdf/lst-pair_aw-beta_all-stn.txt 
;   - loop to create mth aw-beta pair
;   - output netcdf with the same structure as the input
; Usage: change lst and stn; probably yb, ye, mb and me
; Modification:
;   - 20150429: fix fsus (fsds*0.1 < fsus < fsds*0.99)
;   - 20150429: no fix on fsus: leave it to dent-free
;   - 20160526: fix cf coordinates
;************************************************************
begin
;- constant
pho = 0.8     ; ground reflectance: 0.8 for snow

;drc = "/data/wenshanw/gcnet/"
;;drc_in = drc+"netcdf/"
;drc_in = drc+"nc_stamp/"
;;drc_out = drc+"tilt_fix/"
;;drc_out = drc+"tilt_re/"
;drc_out = drc+"tilt_df/"
drc = "/data/wenshanw/aws/spole/"
drc_in = drc
drc_out = drc

;- diffuse ratio df sensitivity test
;c = "0.2"
;drc_out = "temp/"

;xpt = "_exact-noon"
;xpt = "_fuzzy-noon"
xpt = ""
;lst = "tilt_netcdf/lst-pair_aw-beta_all-stn.txt"
;lst = "tilt_netcdf/lst-pair_aw-beta_all-stn_no-early-morning.txt"
;lst = "tilt_netcdf/lst-pair_aw-beta_all-stn_no-high-sza"+xpt+".txt"
;lst = "tilt_netcdf/lst_aw-beta_stn13.txt"
;lst = "tilt_netcdf/lst_stn44.txt"
;lst = "tilt_netcdf/lst_temp.txt"
;lst = "tilt_netcdf/lst_aw-beta_stamp.txt"
;lst = "tilt_netcdf/lst_aw-beta_stamp_s050609_NUKL.txt"
;lst = "tilt_netcdf/lst-pair_aw-beta_all-stn_working_"+c+".txt"
;lst = "tilt_netcdf/lst_aw-beta_df.txt"
;lst = "spole/lst_aw-beta_v2_new-time-logger.txt"
lst = systemfunc("ls spole/lst_aw-beta_v7*.txt")
;lst = "tilt_netcdf/lst-pair_aw-beta_all-stn_no-morning.txt"
;lst = "tilt_netcdf/lst-pair_aw-beta_all-stn_noon.txt"

yb = 2009
ye = 2010
ny = ye - yb + 1
mths = (/1,2,3,4,9,10,11,12/)
nm = dimsizes(mths)

;- stn and GC-Net
;============================================================
lst_stn = "~/cloud/gcnet/stn_spole.txt"
;stn = "sdome"
;stn = "nsu"
;stns = systemfunc("cat stn_promice_pck.txt")
;stns = systemfunc("cat ~/cloud/airs/stn13.txt | awk '{print $1}'")
;stns = systemfunc("cat stn_fix.txt | awk '{print $1}'")
;stns = systemfunc("cat ~/cloud/doc/stn/stn44_gkp.txt | awk '{print $1}'")
;stns = systemfunc("cat stn_temp.txt | awk '{print $1}'")
;stns = (/"UPE_U","UPE_L"/)
stns = systemfunc("cat "+lst_stn+" | awk '{print $1}'")
;stns = systemfunc("cat stn_fix-post.txt | awk '{print $1}'")
;stns = "KPC_L"
;stns = "KPC_U"
;stns = (/"sdome"/)
nstn = dimsizes(stns)
;print("stn = "+stns)
;exit

;- cf liner interpolation options
opt = (/0, 9/)        ; 0: beginning and end set to _FillValue; 9: #missing > 9 no interpolation

do j = 0, nstn - 1        ; j = stn
;do j = 0, 0       ; j = stn
  stn = stns(j)

  lat_deg = tofloat(systemfunc("cat "+lst_stn+" | grep "+stn+" | awk '{print $2}'"))
  lon_deg = tofloat(systemfunc("cat "+lst_stn+" | grep "+stn+" | awk '{print $3}'"))
  print("stn = "+stn+" lat = "+lat_deg+" lon = "+lon_deg)
;  exit

;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
;  fn = systemfunc("ls "+drc_in+"*"+stn+"*new-time-logger.nc")
;  fn = systemfunc("ls "+drc_in+"*"+stn+"*2015_new-time-logger.nc")
  fn = systemfunc("ls "+drc_in+"*"+stn+"*2009-2010*.nc")
;  fn = systemfunc("ls "+drc_in+"*"+stn+"*2011_new-time-logger.nc")
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  fin_gc = addfile(fn,"r")
;  fsds_gc = fin_gc->fsds({yb:ye},{mb:me},:,:)
;  fsus_gc = fin_gc->fsus({yb:ye},{mb:me},:,:)
  fsds_gc = fin_gc->fsds({yb:ye},{mths},:,:)
  fsus_gc = fin_gc->fsus({yb:ye},{mths},:,:)
  hr = fin_gc->hr
  print(hr)
;  print(fn)
;  exit
;- quality flag
  if (str_get_field(str_get_field(fn,5,"/"),1,"_").eq."gcnet") then
    fsds_gc_qc = fin_gc->fsds_qc({yb:ye},{mb:me},:,:)
    fsds_gc = where(fsds_gc_qc.ne.1, fsds_gc@_FillValue, fsds_gc)       ; use only high quality data
    fsus_gc_qc = fin_gc->fsus_qc({yb:ye},{mb:me},:,:)
    fsus_gc = where(fsus_gc_qc.ne.1, fsus_gc@_FillValue, fsus_gc)       ; use only high quality data
    delete([/fsds_gc_qc,fsus_gc_qc/])
  end if
  
  ;- para: aw,beta,alpha,as
  ;============================================================
  aw = new((/ny,nm/),float)
  aw!0 = "yr"
  aw!1 = "mth"
  aw&yr = ispan(yb,ye,1)
;  aw&mth = ispan(mb,me,1)
  aw&mth = mths
  beta = new((/ny,nm/),float)
  copy_VarCoords(aw,beta)
  
  nhr = dimsizes(hr)
;  hr = tofloat(ispan(0,23,1))
  alpha = new((/ny,nm,31,nhr/),double)
  as = new((/ny,nm,31,nhr/),double)
  alpha!0 = "yr"
  alpha!1 = "mth"
  alpha!2 = "day"
  alpha!3 = "hr"
  alpha&yr = ispan(yb,ye,1)
;  alpha&mth = ispan(mb,me,1)
  alpha&mth = mths
  alpha&day = ispan(1,31,1)
  alpha&hr = hr
  copy_VarCoords(alpha,as)
  
  fsds_thr = new((/ny,nm,31,nhr/),float)
  copy_VarCoords(alpha,fsds_thr)
  
  do yr = yb, ye        ; yr
;    do mth = mb, me       ; mth
    do i = 0, nm - 1       ; mth
      mth = mths(i)
  ;do yr = 2004, 2005        ; yr
  ;  do mth = 9, 9       ; mth
;- always output thr no matter fix
      nday = days_in_month(yr,mth)
      ddd = new(nday,integer)
      ddd1 = day_of_year(yr,mth,1)
      ddd = ispan(ddd1,ddd1+nday-1,1)
      fsds_thr({yr},{mth},:(nday-1),:) = tofloat(thr_clr_fsds(yr,ddd,hr,lat_deg,lon_deg))       ; theoretical clr-day fsds
      str = systemfunc("cat "+lst+" | grep '"+stn+"' | grep '"+yr+sprinti("%02i",mth)+"'")
      if (ismissing(str).or.str.eq.(stn+" "+yr+sprinti("%02i",mth)+" missing")) then
        print("Fail on yr = "+yr+" mth = "+mth)
        print("str is missing: no file? no this station?")
        delete([/ddd,ddd1/])
        continue
      else
  ;      print("str = "+str)
        aw({yr},{mth}) = tofloat(str_get_field(str,3," "))
        beta({yr},{mth}) = tofloat(str_get_field(str,4," "))
        solar_position(yr,ddd,hr,lat_deg,lon_deg,alpha({yr},{mth},:(nday-1),:),as({yr},{mth},:(nday-1),:))
  ;      print(alpha({yr},{mth},:,:)/pi*180.+" "+as({yr},{mth},:,:)/pi*180.+"  "+aw({yr},{mth})/pi*180.+" "+beta({yr},{mth})/pi*180.)
  ;      print(fsds_thr({yr},{mth},:,:))
        delete([/ddd,ddd1/])
      end if
      delete(str)
    end do        ; mth
  end do        ; yr
  ;print(aw+"  "+beta)
  ;exit
  
  aw_4d = conform_dims(dimsizes(alpha),aw,(/0,1/))
  beta_4d = conform_dims(dimsizes(alpha),beta,(/0,1/))
  cos_i = cos(alpha)*cos(as-aw_4d)*sin(beta_4d)+sin(alpha)*cos(beta_4d)
  ;- no negative alpha
  ;alpha = where(alpha.lt.0,0.,alpha)
  
  ;- df
  ;============================================================
  drc_cf = "/data/wenshanw/ceres/stn_gkp/"
;  fn_cf = stn+".smr.2007-2013.3hr.format.nc"
  fn_cf = systemfunc("ls "+drc_cf+stn+".*.nc")
  fin_cf = addfile(fn_cf,"r")
  cf_8hr = fin_cf->cf({yb:ye},{mths},:,:)
;  printVarSummary(cf_8hr)
;  exit
  cf_8hr = (/cf_8hr/100./)        ; unit: 100 --> 1
  
;- linear interpolate to 24 hr
;- better way???
;------------------------------------------------------------
;  cf = new((/ny,nm,31,nhr/),float)
;  cf(:,:,:,::3) = (/cf_8hr/)
;	print(cf_8hr)
;	print(cf)
;	exit
;  cf_mth = reshape(cf,(/ny,nm,31*24/))
;  ;print(num(ismissing(cf_mth)))
;  opt = (/0, 9/)        ; 0: beginning and end set to _FillValue; 9: #missing > 9 no interpolation
;  cf_mth = linmsg(cf_mth,opt)
;  ;print(num(ismissing(cf_mth)))
;  cf = reshape(cf_mth,(/ny,nm,31,24/))
;  cf = where(ismissing(cf),0,cf)
;------------------------------------------------------------
;- another linear interpolation
  cf = new((/ny,nm,31,48/),float)
  cf(:,:,:,2::6) = (/cf_8hr/)
  cf_mth = reshape(cf,(/ny,nm,31*48/))
  cf_mth = linmsg(cf_mth,opt)
  cf = reshape(cf_mth,(/ny,nm,31,48/))
  cf = where(ismissing(cf),0,cf)
  cf!3 = "hr"
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  cf&hr = fspan(0,23.5,48)
;  cf&hr = fspan(0,23.5,48)+12./60.
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  cf_out = cf(:,:,:,{hr})
;  copy_VarCoords_1(fsds_gc,cf_out)
;  print(cf_out(0,0,0,:))
;  printMinMax(cf_out,True)
;  printVarSummary(cf_out)
	
;- 0.25
  cf_out = (/where(cf_out.eq.1, 0.9999999, cf_out)/)
  df = (0.2+0.8*cf_out)/(0.8-0.8*cf_out)
;  printMinMax(df,True)
;- 0.2
;  df = 0.2+0.8*cf(:,:,:,{hr})
;	cf = (/where(cf.eq.1, 0.9999999, cf)/)
;  df = (0.2+cf(:,:,:,{hr}))/(1-cf(:,:,:,{hr}))
;	printMinMax(df,True)
;- 0.1
;	cf = where(cf.eq.1, 0.9999, cf)
;  df = (0.1+cf(:,:,:,{hr}))/(1-cf(:,:,:,{hr}))
;	printMinMax(df,True)

;	exit
  ;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  ;- test df effect!!!
  ;df = 0.2
  ;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  
  ;- correction
  ;============================================================
  ;fsds_gc_crt = fsds_gc*df/((1+cos(beta_4d))/2.) + fsds_gc*(1-df)/cos_i*sin(alpha)
  ;- use the right eq
  fsds_gc_crt = fsds_gc*(sin(alpha)+df)/(cos_i+df*(1+cos(beta_4d))/2.+pho*(sin(alpha)+df)*(1-cos(beta_4d))/2.)

  copy_VarCoords(fsds_thr,fsds_gc_crt)
  fsds_gc_crt@long_name = "tilt-corrected fsds"
  printVarSummary(fsds_gc_crt)
  printMinMax(fsds_gc_crt,True)
  fsds_thr@long_name = "theoretical fsds under clr-sky conditions"
  printMinMax(fsds_thr,True)

  ;- output to check
  ;============================================================
  ;delete([/yr,mth,hr/])
  ;yr = 2005
  ;mth = 9
  ;day = 17
  ;hr = 15
  ;copy_VarCoords(alpha,cos_i)
  ;tt_ddd = day_of_year(yr,mth,day)
  ;tt_alpha = new((/1,1/),float)
  ;tt_as = new((/1,1/),float)
  ;tt_hr = 14.9927
  ;solar_position(tt_ddd,tt_hr,lat_deg,lon_deg,tt_alpha,tt_as)
  ;print(tt_ddd+"  "+hr+"  "+lat_deg+" "+lon_deg+" "+tt_alpha/pi*180.+"  "+tt_as/pi*180.)
  ;print(alpha({yr},{mth},{day},{hr})/pi*180.+" "+as({yr},{mth},{day},{hr})/pi*180.+"  "+cos_i({yr},{mth},{day},{hr})+"  "+aw({yr},{mth})/pi*180.+" "+beta({yr},{mth})/pi*180.+" "+sin(alpha({yr},{mth},{day},{hr})))
  ;print(fsds_thr({yr},{mth},{day},{hr})+"  "+fsds_gc_crt({yr},{mth},{day},{hr}))
  ;print("fsds_gc = "+fsds_gc({yr},{mth},{day},{hr}))
  ;;tt_fsds_gc_crt = fsds_gc({yr},{mth},{day},{hr})*(0.488495+0.2)/(cos_i({yr},{mth},{day},{hr})+0.2*(1+cos(beta({yr},{mth})))/2.)
  ;tt_fsds_gc_crt = fsds_gc({yr},{mth},{day},{hr})*(sin(tt_alpha)+0.2)/(cos_i({yr},{mth},{day},{hr})+0.2*(1+cos(beta({yr},{mth})))/2.)
  ;print("fsds_gc_crt = "+tt_fsds_gc_crt)
  ;print(fsds_gc({yr},{mth},{day},{hr})+"  "+sin(tt_alpha)+" "+cos_i({yr},{mth},{day},{hr})+"  "+cos(beta({yr},{mth})))
  ;exit
  
  ;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
;  fo = stn+"_tilt-fixed_fsds.nc"
;  fo = stn+"_tilt-fixed.nc"
;  fo = stn+"_tilt-fixed"+xpt+".nc"
;  fo = stn+"_tilt-fixed"+xpt+"_hr05.nc"
  fo = stn+"_tilt-fixed"+xpt+"_2h32m.nc"
;  fo = stn+"_tilt-fixed"+xpt+"_hr07.nc"
;  fo = stn+"_tilt-fixed"+xpt+"_"+c+".nc"
  ;fo = stn+"_tilt-fixed_fsds_clr-days.nc"
  ;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  system("/bin/rm -f "+drc_out+fo)
  fout = addfile(drc_out+fo,"c")
  fout->fsds_fixed = fsds_gc_crt
  fout->fsds_thr = fsds_thr
  ;printVarSummary(fsds_gc)
  fout->fsds_gc = fsds_gc
  fout->fsus_gc = fsus_gc
  cf_out@long_name = "cloud fraction from CERES SYN 1-deg"
  cf_out@units = "1"
  copy_VarCoords(fsds_gc,cf_out)
  fout->cf_out = cf_out

  delete([/aw,beta,alpha,as/])
  delete([/aw_4d, beta_4d/])
  delete([/cf_8hr,cf_mth,cf,cf_out,df/])
  delete([/cos_i, fsds_gc_crt,fsds_thr,fsds_gc,fsus_gc/])
end do        ; j = stn

print("done!")
end
