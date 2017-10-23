; Written by Wang, Wenshan 2015-05-05 Tuesday 16:21:47
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "cal_para.ncl"
;*************************************************************
; Purpose: fix the quick change in a mth; breaking points more than 1
; Prototype: fix_qk-chg.ncl
; Step:
;   - fix each line from aw-beta lst: eg, lst_aw-beta_stamp_qk-chg.txt
;			 and breaking point lst: eg, lst_quick-chg_triple.txt
; Warning:
;   - depends HIGHLY on input lst format:
;				stn yyyymm day1 day2 ...
; Note:
;		- diff lst order from the prototype: now read spt first and search aw-beta
;************************************************************
begin
;- constant
pho = 0.8     ; ground reflectance: 0.8 for snow
pi = 3.1415926535898d

;- aw-beta lst
;lst = "tilt_netcdf/lst_stn44_qk-chg.txt"
;lst = "tilt_netcdf/lst-pair_aw-beta_all-stn_no-high-sza.txt"
;lst = "tilt_netcdf/lst_aw-beta_stamp.txt"
lst = "tilt_netcdf/lst_aw-beta_df_brk.txt"
;lst = "tilt_netcdf/lst_aw-beta_stamp_triple.txt"
;lst = "tilt_netcdf/lst-pair_aw-beta_all-stn_working.txt"
;lst ="test.txt"
;lst = "tilt_netcdf/lst_stn44_qk-chg.txt"
;str = asciiread(lst,-1,"string")

;- spt
;lst_spt = "lst_quick-chg_triple.txt"
;lst_spt = "lst_triple_temp.txt"
lst_spt = "lst_brk.txt"
str_spt = asciiread(lst_spt, -1, "string")
nfix = dimsizes(str_spt)
;print(str_spt)
;print(nfix)
;exit

;- gcnet
;drc_gc = "/data/wenshanw/gcnet/tilt_fix/"
;drc_gc = "/data/wenshanw/gcnet/tilt_re/"
drc_gc = "/data/wenshanw/gcnet/tilt_df/"

;hr = ispan(0,23,1)
;nhr = dimsizes(hr)
nhr = 24

;- cf
drc_cf = "/data/wenshanw/ceres/stn_gkp/"
vars_cf = (/"cldarea_high_3h","cldarea_mid-high_3h","cldarea_mid-low_3h","cldarea_low_3h"/)
nvar_cf = dimsizes(vars_cf)
opt = (/0, 9/)        ; for lingsm; 0: beginning and end set to _FillValue; 9: #missing > 9 no interpolation

;!!! temp !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
do i = 0, nfix - 1        ; i = yyyymm
;do i = 0, 0        ; i = yyyymm
;do i = 0, 2        ; i = fix
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
;- spt 
	ln_spt = str_split(str_spt(i)," ")
	nspt = dimsizes(ln_spt)-2				; # split points
;	print(ln_spt)
	stn = ln_spt(0)
	yyyymm = ln_spt(1)
  yr = toint(yyyymm)/100
  mth = toint(yyyymm)-toint(yyyymm)/100*100
	spt = toint(ln_spt(2:))				; days of split points
;	print("spt = "+spt)
;- make it work for no break month to replace fix_patch.ncl
	if (spt(0).eq.1) then
		nspt = 0
	end if
	print(stn+"	"+yr+"	"+mth+"	"+spt)
;	exit

;- info
  lat_deg = tofloat(systemfunc("cat ~/cloud/doc/stn/stn44_gkp.txt | grep "+stn+" | awk '{print $2}'"))
  lon_deg = tofloat(systemfunc("cat ~/cloud/doc/stn/stn44_gkp.txt | grep "+stn+" | awk '{print $3}'"))

;- aw-beta
	str_aw = systemfunc("cat "+lst+" | grep '"+stn+" "+yyyymm+"'")
;	print(str_aw)
	if (dimsizes(str_aw).ne.(nspt+1)) then
		print("# aw-beta doesn't match # spt points!")
		print("Skip "+stn+" "+yyyymm)
		delete([/ln_spt,spt/])
		delete([/str_aw/])
		continue
	end if
	aw = todouble(systemfunc("cat "+lst+" | grep '"+stn+" "+yyyymm+"' | cut -d ' ' -f 3"))
	beta = todouble(systemfunc("cat "+lst+" | grep '"+stn+" "+yyyymm+"' | cut -d ' ' -f 4"))
	print(aw+"	"+beta)
;	exit

;- gcnet
  fn_gc = drc_gc+stn+"_tilt-fixed.nc"
;!!! temp !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  fin_gc = addfile(fn_gc,"w")
;  fin_gc = addfile(fn_gc,"r")
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	hr = fin_gc->hr
  fsds_gc = fin_gc->fsds_gc({yr},{mth},:,:)
  fsds_gc_crt = fsds_gc
  fsds_gc_crt = fsds_gc_crt@_FillValue
  fsds_gc_crt@long_name = "fixed fsds"

;- cf
  nday_mth = days_in_month(yr,mth)
  fn_cf = stn+".smr.2007-2013.3hr.format.nc"
  fin_cf = addfile(drc_cf+fn_cf,"r")
  ;- sum all levels of cld together
  cf_8hr = new((/nday_mth,8/),float)
  cf_8hr = 0
  do k = 0, nvar_cf - 1       ; k = var_cf
    dat = fin_cf->$vars_cf(k)$({yr},{mth},:(nday_mth-1),:)
    dat = where(ismissing(dat),0,dat)
		if (nday_mth.eq.1) then
      cf_8hr(0,:) = cf_8hr(0,:)+dat
		else
      cf_8hr = cf_8hr+dat
		end if
    delete(dat)
  end do        ; k = var_cf
  ;print(num(ismissing(cf_8hr))+"  "+num(cf_8hr.eq.0))
  ;printMinMax(cf_8hr,True)
  cf_8hr = cf_8hr/100.        ; unit: 100 --> 1
  ;- linear interpolate to 24 hr
  ;- better way???
  cf = new((/nday_mth,48/),float)
  cf(:,2::6) = (/cf_8hr/)
  cf_mth = reshape(cf,(/nday_mth*48/))
  ;print(num(ismissing(cf_mth)))
  cf_mth = linmsg(cf_mth,opt)
  ;print(num(ismissing(cf_mth)))
  cf = reshape(cf_mth,(/nday_mth,48/))
  cf = where(ismissing(cf),0,cf)
	cf!0 = "day"
	cf!1 = "hr"
	cf&day = ispan(1,nday_mth,1)
	cf&hr = fspan(0,23.5,48)

;- process parts of month separately
	db = 1
	do j = 0, nspt				; j = parts in a month; #parts = nspt+1
		if (ismissing(beta(j))) then
      print("Warning: missing aw-beta on "+yyyymm+" half = "+j)
      continue
    end if

;- determine: days, db, de
		if (j.eq.nspt) then
			de = nday_mth
		else
			de = spt(j)-1
		end if
		days = ispan(db,de,1)
		nday = dimsizes(days)
		ddd0 = day_of_year(yr,mth,db)
		ddd = ispan(ddd0,ddd0+nday-1,1)
;		print(db+"	"+de)
;		print(days+"	"+ddd)
;		print(nday+"")

;- alpha, as
    alpha = new((/nday,nhr/),double)
    as = new((/nday,nhr/),double)
    solar_position(yr,ddd,hr,lat_deg,lon_deg,alpha,as)
;    print(alpha(0,:)/pi*180+"  "+as(0,:)/pi*180)
;- cos_i
    cos_i = cos(alpha)*cos(as-aw(j))*sin(beta(j))+sin(alpha)*cos(beta(j))
;- df
;    df = 0.2+0.8*cf({days},{hr})
;- new df after peer-review
		cf = (/where(cf.eq.1, 0.9999999, cf)/)
	  df = (0.2+0.8*cf({days},{hr}))/(0.8-0.8*cf({days},{hr}))

;- correct and output
    fsds_gc_half = fsds_gc({days},:)
		if (nday.eq.1) then
	    fsds_gc_crt({days},:) = tofloat(fsds_gc_half*(sin(alpha(0,:))+df)/(cos_i(0,:)+df*(1+cos(beta(j)))/2.+pho*(sin(alpha(0,:))+df)*(1-cos(beta(j)))/2.))
		else
	    fsds_gc_crt({days},:) = tofloat(fsds_gc_half*(sin(alpha)+df)/(cos_i+df*(1+cos(beta(j)))/2.+pho*(sin(alpha)+df)*(1-cos(beta(j)))/2.))
		end if

;- new db
		if (j.ne.nspt) then
			db = spt(j)
		end if

		delete([/days,ddd/])
		delete([/alpha,as,cos_i,df,fsds_gc_half/])
	end do				; j = parts in a month; #parts = nspt+1

	fin_gc->fsds_fixed({yr},{mth},:,:) = fsds_gc_crt
	delete([/ln_spt,spt/])
	delete([/str_aw,aw,beta/])
	delete([/cf,cf_8hr,cf_mth/])
end do				; i = yyyymm

print("done!")
end
