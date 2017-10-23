; Written by Wang, Wenshan 2016-01-27 Wednesday 11:49:18
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "~/scripts/ncl_script/wenshanw.ncl"
load "cal_para.ncl"
;*************************************************************
; Purpose: find when to break in a month automatically
;		Steps:
;			- loop over quick-chg month
;			- cal the diff matrix (pairs of aw-beta vs. clr days): 
;				the difference of corrected fsds vs CRM fsds using aw-beta estimated from diff clr days
;			- while loop: put break: first value > 7 W/m^2 in first row; jump to rows (ie days of aw-beta) next to the break until the end
;			- (old) find the middle dates btw two breaks
;			- (old) output clr-days_test.txt directly
;			- (new) output clr-days_test.txt directly no record of breaks
;		Extreme cases:
;			- check only +/- 6 hrs around noon
;			- check only days with more than one CRM point; if none in a whole month, output for human inspection
;			- bad correction on the estimating day (diag+left > 7 W/m^2) --> skip (output for double-check)
; Note: 
;		- The choice of 7 W/m^2 is based of experience inspecting lots of plots
; Change the Rules:
;		- no self-inspection (good/bad estimate on the same day --> already included in cal_parts
;		- (old) group threshold: diff < 5 W/m^2
;		- (new) group threshold: < 3 W/m^2 safe; 3 < x < 5: check the corresponding pair (aw-beta j and day k)
; To-do:
;		- get rid of bad clear days and output break points (eps no noon CRM points days)
;		- although only one point per day but several days can show a difference
;************************************************************
begin
pi = 3.1415926535898
pho = 0.8     ; ground reflectance: 0.8 for snow

thd_bad = 15				; threshold good estimate (whether a good estimate for the same day); choice kind of arbitrary
thd_grp1 = 3					; for groups (whether in the same group)
thd_grp2 = 5					; for groups (whether in the same group)

lst_qk = "high_dfs-std.txt"
lst_clr = "clr-days_qk.txt"
lst_ab = "tilt_netcdf/lst_aw-beta_qk.txt"

lst_out = "clr-days_brk.txt"			; clr-days lst
system("/bin/rm -f "+lst_out)
lst_brk = "lst_brk.txt"			; lst including break dates; second half begins from the brk dates
system("/bin/rm -f "+lst_brk)

str = asciiread(lst_qk,-1,"string")
nln = dimsizes(str)

drc_gc = "/data/wenshanw/gcnet/nc_stamp/"
drc_crm = "/data/wenshanw/crm/myd_long_clr/"

drc_cf = "/data/wenshanw/ceres/stn_gkp/"
vars_cf = (/"cldarea_high_3h","cldarea_mid-high_3h","cldarea_mid-low_3h","cldarea_low_3h"/)
nvar_cf = dimsizes(vars_cf)

opt = (/0, 9/)        ; 0: beginning and end set to _FillValue; 9: #missing > 9 no interpolation

;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
do i = 0, nln - 1				; i = qk line = qk month
;do i = 19, 19				; i = qk line = qk month
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  lns = str_split(str(i)," ")
	stn = lns(0)
	yr = toint(lns(1))
	mth = toint(lns(2))
	mm = sprinti("%02i",mth)
;	print(stn+" "+yr+mm)

	lns_clr = systemfunc("grep '"+stn+" "+yr+mm+"' "+lst_clr)
	nln_clr = dimsizes(lns_clr)				; number of clr days in one month
;	print(lns_clr)
;	exit
;	print("nln_clr = "+nln_clr)

;- get clr dates
	days_clr = toint(str_get_cols(str_get_field(lns_clr,2," "),6,7))
;	print(days_clr)
;	exit

;- read aw-beta of this month
	str_ab = systemfunc("grep '"+stn+" "+yr+mm+"' "+lst_ab)
	aw = todouble(str_get_field(str_ab, 3, " "))
	beta = todouble(str_get_field(str_ab, 4, " "))
	aw!0 = "day"
	aw&day = days_clr
	copy_VarCoords(aw,beta)
	delete(str_ab)
;	print(str_ab)
;	print(aw+" "+beta)

;- read fsds_gc
  fn = systemfunc("ls "+drc_gc+"*"+stn+"*.nc")
;	print("fn = "+fn)
  fin_gc = addfile(fn,"r")
  fsds_gc = fin_gc->fsds({yr},{mth},{days_clr},:)
	hr = fin_gc->hr
	nhr = dimsizes(hr)
;	printVarSummary(fsds_gc)

;- alpha and as
  alpha = new((/nln_clr,nhr/),double)
  as = new((/nln_clr,nhr/),double)
  alpha!0 = "day"
  alpha!1 = "hr"
	alpha&day = days_clr
	alpha&hr = hr
  copy_VarCoords(alpha,as)
	yr_day = conform_dims(nln_clr,yr,(/-1/))
	mth_day = conform_dims(nln_clr,mth,(/-1/))
  ddds = day_of_year(yr_day,mth_day,days_clr)
	delete([/yr_day,mth_day/])
  lat_deg = tofloat(systemfunc("cat ~/cloud/doc/stn/stn44_gkp.txt | grep "+stn+" | awk '{print $2}'"))
  lon_deg = tofloat(systemfunc("cat ~/cloud/doc/stn/stn44_gkp.txt | grep "+stn+" | awk '{print $3}'"))
  solar_position(yr,ddds,hr,lat_deg,lon_deg,alpha,as)
;	print(alpha(0,:)/pi*180.+"	"+as(0,:))

;- df
;  fn_cf = stn+".smr.2007-2013.3hr.format.nc"
;  fin_cf = addfile(drc_cf+fn_cf,"r")
;	cf_8hr = new((/31,8/),float)			; for interpolation in that month
;  cf_8hr = 0
;  do j = 0, nvar_cf - 1       ; j = var_cf
;    dat = fin_cf->$vars_cf(j)$({yr},{mth},:,:)
;    dat = where(ismissing(dat),0,dat)
;    cf_8hr = cf_8hr+dat
;    delete(dat)
;  end do        ; j = var_cf
;  cf_8hr = cf_8hr/100.        ; unit: 100 --> 1
;;- linear interpolation
;  cf = new((/31,48/),float)
;  cf(:,2::6) = (/cf_8hr/)
;	cf_mth = reshape(cf,(/31*48/))
;  cf_mth = linmsg(cf_mth,opt)
;	cf = reshape(cf_mth,(/31,48/))
;  cf = where(ismissing(cf),0,cf)
;	cf!0 = "day"
;	cf!1 = "hr"
;	cf&day = ispan(1,31,1)
;	cf&hr = fspan(0,23.5,48)
;	
;;- df = 0.25
;	cf = (/where(cf.eq.1, 0.9999999, cf)/)
;  df = (0.2+0.8*cf({days_clr},{hr}))/(0.8-0.8*cf({days_clr},{hr}))
	df = 0.25					; should use this since it's still estimating aw-beta

;- correct
;-- Note: nday == nab since one pair of aw-beta is estimated using one clear-day
;--				define diff var to make array easier to understand
	nday = nln_clr				; how many clear days
	nab = nln_clr					; how many pairs of aw-beta
	aw_3d = conform_dims((/nab,nday,nhr/),aw,(/0/))
	beta_3d = conform_dims((/nab,nday,nhr/),beta,(/0/))
	alpha_3d = conform_dims((/nab,nday,nhr/),alpha,(/1,2/))			; together with ddd --> days_clr
	as_3d = conform_dims((/nab,nday,nhr/),as,(/1,2/))

  cos_i_3d = cos(alpha_3d)*cos(as_3d-aw_3d)*sin(beta_3d)+sin(alpha_3d)*cos(beta_3d)
	fsds_gc_3d = conform_dims((/nab,nday,nhr/),fsds_gc,(/1,2/))
;	df_3d = conform_dims((/nab,nday,nhr/),df,(/1,2/))
	df_3d = conform_dims((/nab,nday,nhr/),df,(/-1/))

  fsds_gc_crt = fsds_gc_3d*(sin(alpha_3d)+df_3d)/(cos_i_3d+df_3d*(1+cos(beta_3d))/2.+pho*(sin(alpha_3d)+df_3d)*(1-cos(beta_3d))/2.)
	delete([/aw_3d,beta_3d,alpha_3d,as_3d,cos_i_3d,fsds_gc_3d,aw,beta,alpha,as,fsds_gc,df,df_3d/])
;	printVarSummary(fsds_gc_crt)
;	print2d(fsds_gc_crt)

;- loop over days to cal daily avg --> matrix (have to loop since CRM points are from diff files)
;-- a new nab*nday array to store the results??? I think so
	dfs_day = new((/nab,nday/),double)				; store daily avg difference
;	std_day = new((/nab,nday/),double)				; store daily avg difference
;	mdn_day = new((/nab,nday/),double)				; store daily avg difference
	do j = 0, nday-1				; j = clr days
;		print("============================================================")
;		print("day = "+days_clr(j))
;    fns = systemfunc("ls "+drc_crm+stn+"/"+stn+"."+yr+ddds(j)+".0[89]??.nc "+drc_crm+stn+"/"+stn+"."+yr+ddds(j)+".1???.nc")
    fns = systemfunc("ls "+drc_crm+stn+"/"+stn+"."+yr+ddds(j)+".????.nc")
;		print("fns = "+fns)
		nfn = dimsizes(fns)
		if (nfn.lt.2) then
			print(stn+" "+yr+mm+sprinti("%02i",days_clr(j))+" contains only one CRM point! Skip!")
			delete(fns)
			continue
		end if
    fsds_crm = new(nfn,float)
    loctim = new(nfn,float)
    coszrs = new(nfn,float)
	  do k = 0, nfn - 1       ; k = crm file
      fin_crm = addfile(fns(k),"r")
      fsds_crm(k) = fin_crm->fsds
      loctim(k) = fin_crm->loctim
      coszrs(k) = fin_crm->coszrs
    end do         ; k = crm file
		if (num(coszrs.ge.cos(75./180.*pi)).lt.2) then
			print(stn+" "+yr+mm+sprinti("%02i",days_clr(j))+" contains only one CRM point at NOON! Skip!")
			delete([/fns,fsds_crm,loctim,coszrs/])
			continue
		end if
    fsds_crm = where(coszrs.lt.cos(75./180.*pi),fsds_crm@_FillValue,fsds_crm)    ; SZA no more than 75 deg
;		print("------------------------------------------------------------")
;		print(loctim+"	"+coszrs+"	"+fsds_crm)

		do k = 0, nab - 1				; k = pairs of aw-beta
      hr_id = ind(.not.ismissing(fsds_gc_crt(k,j,:)))
      fsds_loctim = ftcurv(hr(hr_id),fsds_gc_crt(k,j,hr_id),loctim)
;			print("------------------------------------------------------------")
;			print(hr+"	"+fsds_gc_crt(k,j,:)+"")
;			print("------------------------------------------------------------")
;			print(fsds_crm+"	"+fsds_loctim)
;- compare
      dfs_day(k,j) = avg(abs(fsds_loctim-fsds_crm))
;      std_day(k,j) = stddev(abs(fsds_loctim-fsds_crm))
;      mdn_day(k,j) = dim_median(abs(fsds_loctim-fsds_crm))
;			print(dfs_day(k,j)+"")
			delete([/hr_id,fsds_loctim/])
		end do					; k = pairs of aw-beta

;		print2d(dfs_day)
		delete([/fns,nfn,fsds_crm,loctim,coszrs/])
	end do				; j = clr days
;	print("------------------------------------------------------------")
;	print2d(dfs_day)
;	print("------------------------------------------------------------")
;	print2d(std_day)
;	print("------------------------------------------------------------")
;	print2d(mdn_day)
;	delete([/std_day,mdn_day/])

;- put break
	brk = new(nln_clr,integer)					; max num of breaks is the #clr-1; brk after day N (N starts from 0) is N
	j = 0				; aw-beta counter
	k = 0				; clr-day counter
	m = 0				; break counter
	str_out=""			; output string
	do while (j.lt.nab)				; j = aw-beta counter
;		print("j = "+j+" k = "+k)
;		print(dfs_day(j,k))
;- if estimate on the same day is bad; skip
		if (ismissing(dfs_day(j,k)).or.dfs_day(j,k).gt.thd_bad) then
			print(stn+" "+yr+mm+sprinti("%02i",days_clr(k))+" Bad estimates of aw-beta on this clear day!: "+sprintf("%5.2f",dfs_day(j,k))+" W/m^2")
			j = j + 1
			k = k + 1
			continue
		end if
;- if estimate on the same day is good: output this day
		str_out = stn+" "+yr+mm+sprinti("%02i",days_clr(k))
		k = k + 1
		do while (k.lt.nday)				; k = clr-day counter
;			if ((abs(dfs_day(j,k)-dfs_day(j,j))).gt.thd_grp) then
;;				brk(m) = k
;;				m = m + 1
;				system("echo "+str_out+" >> "+lst_out)
;				str_out = ""
;				break
;			end if
			if (.not.ismissing(dfs_day(j,k)).and.(abs(dfs_day(j,k)-dfs_day(j,j))).le.thd_grp1) then
				str_out = str_out+" "+yr+mm+sprinti("%02i",days_clr(k))
				k = k + 1 
			else if (.not.ismissing(dfs_day(j,k)).and.((abs(dfs_day(j,k)-dfs_day(j,j))).le.thd_grp2).and.((abs(dfs_day(k,j)-dfs_day(k,k))).le.thd_grp1)) then 
				str_out = str_out+" "+yr+mm+sprinti("%02i",days_clr(k))
				k = k + 1 
			else
				system("echo "+str_out+" >> "+lst_out)
				str_out = ""
				brk(m) = k - 1
				m = m + 1
				break
			end if
			end if
		end do				; k = clr-day counter
		j = k 
	end do				; j = aw-beta counter
	if (str_out.ne."") then
		system("echo "+str_out+" >> "+lst_out)
		str_out = ""
	end if
;	print(brk+"")

;- output middle dates
	nbrk = num(.not.ismissing(brk))
	if (nbrk.lt.1) then				; if 0 or 1 brk, delete that line in lst_out
		system("sed -i '/"+stn+" "+yr+mm+"/ d' "+lst_out)
		print(stn+" "+yr+mm+" No break")
		print2d(dfs_day)
	else
		str_out = stn+" "+yr+mm
		do j = 0, nbrk - 1				; j = #brk
			str_out = str_out+" "+sprinti("%02i",round((days_clr(brk(j))+days_clr(brk(j)+1))/2.,3))
		end do				; j = #brk
		system("echo "+str_out+" >> "+lst_brk)
	end if

;	exit
	delete([/lns,stn,yr,mth,mm,lns_clr,nln_clr/])
	delete([/fn,fin_gc,hr,nhr,ddds,lat_deg,lon_deg/])
;	delete([/fn_cf,fin_cf/])
;	delete([/cf_8hr,cf,cf_mth/])
	delete(fsds_gc_crt)
	delete([/dfs_day,days_clr/])
	delete([/brk/])
end do				; i = qk line = qk month

print("done!")
end
