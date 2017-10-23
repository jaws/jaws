; Written by Wang Wenshan 2015-02-26 Thursday 11:59:02
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "cal_para.ncl"
;*************************************************************
; Series: cal_aw-beta_main
; Role: part function
; Purpose: 
;   part 1 (pbl_prs): cal all the possible aw-beta pairs
;   part 2 (crm_match): closest to CRM
;   part 3 (no_spike): pick the one with the least spikes
;************************************************************
;- constants
pi = 3.1415926535898d
;lon_ref = 0       ; GMT ref longitude
;noon_min = 12*60.        ; local solar noon in minutes
;df = 0.2        ; seek aw-beta under clr-sky conditions; diffuse ratio: diffuse/direct
df = 0.25        ; seek aw-beta under clr-sky conditions; diffuse ratio: diffuse/direct
pho = 0.8     ; ground reflectance: 0.8 for snow
noon_min = 12*60.        ; local solar noon in minutes

;- drc
;drc_crm = "/data/wenshanw/crm/myd_long_clr/"
drc_crm = "/data/wenshanw/crm/spole/"
;drc_crm = "/data/wenshanw/crm/arm/"
;drc_gc = "/data/wenshanw/gcnet/netcdf/"
drc_gc = "/data/wenshanw/aws/spole/"

;- part 1 function
;- usage pair_pbl = pbl_prs(stn,lat_deg,lon_deg,yrs,mths,days,ddd)        ; output all the possible aw-beta pairs
undef ("pbl_prs")       ; possible pairs
function pbl_prs(stn:string,lat_deg:float,lon_deg:float,yrs:integer,mths:integer,days:integer,ddd:integer)
local n_aw,n_beta,aw,beta,pair,nday,nhr,hr,alpha,as,fn_gc,fin_gc,fsds_gc,fsds_gc_qc,hr_id,fsds_gc4nhr,fsds_gc_max,gmt_noon,i,pair_true,j,k,cos_i,fsds_gc_crt,shift_max_hr,crt_max_hr,ind_pair,dim_pair,npair,alpha_3d,as_3d, aw_3d, beta_3d, fsds_gc4nhr_3d,nmr,dnm,bln_pair,hr_gc
begin
;- aw and beta
n_aw = 720      ; every half deg
n_beta = 180       ; from 0~30, every half deg
;!!! temp !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
beta = fspan(0.25,45, n_beta)/180.*pi        ; in radians
;beta = fspan(0,89.5, n_beta)/180.*pi        ; in radians
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
pair_true = new((/n_aw,n_beta/),integer)       ; keep all the possible pairs of (aw,beta); 1: possible; 0: impossible
shift_max_hr = new((/n_aw,n_beta/),float)       ; max hr of cos_i
crt_max_hr = new((/n_aw,n_beta/),float)       ; max hr of the corrected fsds_gc

;- cal alpha and as
nday = dimsizes(days)
nhr = 48        ; precision: half an hour; too artificial if higher
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
;hr = fspan(0,23.5,nhr)
hr = fspan(0,23.5,nhr)+2/60.
;hr = fspan(0,23.5,nhr)+12./60.
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
alpha = new((/nday,nhr/),double)
as = new((/nday,nhr/),double)
solar_position(yrs(0),ddd,hr,lat_deg,lon_deg,alpha,as)     ; ddd: days in yr
;print(alpha(0,:)/pi*180+"  "+as(0,:)/pi*180)

;- get fsds 
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
;fn_gc = systemfunc("ls "+drc_gc+"*"+stn+"*.nc")
;fn_gc = systemfunc("ls "+drc_gc+"*"+stn+"*2015_new-time-logger.nc")
fn_gc = systemfunc("ls "+drc_gc+"*"+stn+"*2009-2010*.nc")
;fn_gc = systemfunc("ls "+drc_gc+"*"+stn+"*2011_new-time-logger.nc")
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
fin_gc = addfile(fn_gc,"r")       ; fsds that needs to be corrected
fsds_gc = new((/nday,24/),float)
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
fsds_gc = tofloat(fin_gc->fsds({yrs(0)},{mths(0)},{days},:))
;- use initial guess
;fsds_gc = tofloat(fin_gc->fsds_ini({yrs(0)},{mths(0)},{days},:))
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
hr_gc = fin_gc->hr
;- structure problem with one day
;if (nday.eq.1) then
;  fsds_gc = new((/nday,24/),float)
;  fsds_gc(0,:) = fin_gc->fsds({yrs(0)},{mths(0)},{days},:)
;  fsus_gc = new((/nday,24/),float)
;  fsus_gc(0,:) = fin_gc->fsus({yrs(0)},{mths(0)},{days},:)
;;!!! temp: no qc in promice
;;  fsds_gc_qc = new((/nday,24/),float)
;;  fsds_gc_qc(0,:) = fin_gc->fsds_qc({yrs(0)},{mths(0)},{days},:)
;else
;  fsds_gc = fin_gc->fsds({yrs(0)},{mths(0)},{days},:)
;  fsus_gc = fin_gc->fsus({yrs(0)},{mths(0)},{days},:)
;;  fsds_gc_qc = fin_gc->fsds_qc({yrs(0)},{mths(0)},{days},:)
;end if
;- quality flag
;- if gcnet data, apply quality flag

if (str_get_field(str_get_field(fn_gc,5,"/"),1,"_").eq."gcnet") then
  fsds_gc_qc = new((/nday,24/),float)
  fsds_gc_qc = fin_gc->fsds_qc({yrs(0)},{mths(0)},{days},:)
  fsds_gc = where(fsds_gc_qc.ne.1, fsds_gc@_FillValue, fsds_gc)       ; use only high quality data
end if

;- initialize pair
pair_true = 1        ; initialize as all possible; no missing here

;- use loop because of maxind, which is easy to use but can handle only 1D
do i = 0, nday - 1        ; i = day
;- fsds max hr
;!!! temp !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  hr_id = ind(.not.ismissing(fsds_gc(i,:)))
;  hr_id = (/0,1,2,3,4,5,6,7,8,9,18,19,20,21,22,23/)
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  fsds_gc4nhr = ftcurv(hr_gc(hr_id),fsds_gc(i,hr_id),hr)  ; no need to check hr_id since clr-days are picked manually
  fsds_gc_max = hr(maxind(fsds_gc4nhr))       ; max hr in gc-net: shifted
;  print(fsds_gc(i,:))
;  print(fsds_gc4nhr)

  gmt_noon = noon(ddd(i),lon_deg)       ; return noon in GMT with precision of 0.5 hr
;  gmt_noon = noon_st(ddd(i),lon_deg)
;  print("day = "+ddd(i)+"  true noon = "+gmt_noon+"   shifted noon = "+fsds_gc_max)
;  print("day = "+ddd(i)+"  true noon = "+gmt_noon+"   fsus noon = "+fsus_gc_max+" thr max hr = "+fsds_thr_hr)
;  continue
;  exit
;- redefine aw
;  print(fsds_gc_max+" "+gmt_noon)
;!!! temp !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  if (fsds_gc_max.ge.gmt_noon) then
    aw = fspan(0,179.75, n_aw)/180.*pi
  else
    aw = fspan(-179.75, 0, n_aw)/180.*pi
  end if
;  aw = fspan(-180,179.5, n_aw)/180.*pi       ; in radians: will be redefined after know fsds_gc_max
;  aw = new(n_aw,double)
;  aw(:359) = fspan(-179.75,-90, n_aw/2)/180.*pi       ; in radians: will be redefined after know fsds_gc_max
;  aw(360:) = fspan(90,179.75, n_aw/2)/180.*pi       ; in radians: will be redefined after know fsds_gc_max
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
;  print("aw = "+aw/pi*180.)
;  exit

;- cal cos_i
  alpha_3d = conform_dims((/n_aw,n_beta,nhr/),alpha(i,:),(/2/))
  as_3d = conform_dims((/n_aw,n_beta,nhr/),as(i,:),(/2/))
  aw_3d = conform_dims((/n_aw,n_beta,nhr/),aw,(/0/))
  beta_3d = conform_dims((/n_aw,n_beta,nhr/),beta,(/1/))
  cos_i = cos(alpha_3d)*cos(as_3d-aw_3d)*sin(beta_3d)+sin(alpha_3d)*cos(beta_3d)
;  if (any(cos_i.eq.0)) then
;    ind_zero = ind_resolve(ind(ndtooned(cos_i).eq.0),(/n_aw,n_beta,nhr/))
;    print(alpha_3d(ind_zero(:,0),ind_zero(:,1),ind_zero(:,2))+" "+as_3d(ind_zero(:,0),ind_zero(:,1),ind_zero(:,2))+" "+beta_3d(ind_zero(:,0),ind_zero(:,1),ind_zero(:,2))+" "+aw_3d(ind_zero(:,0),ind_zero(:,1),ind_zero(:,2)))
;    exit
;  end if
;  cos_i = where(cos_i.eq.0,2.22507e-308,cos_i)

;- correct fsds_gc
  fsds_gc4nhr_3d = conform_dims((/n_aw,n_beta,nhr/),fsds_gc4nhr,(/2/))
;  fsds_gc_crt = fsds_gc4nhr_3d*df/((1+cos(beta_3d))/2.) + fsds_gc4nhr_3d*(1-df)/cos_i*sin(alpha_3d)
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
;- no negative cos(sza) when correcting fsds_gc
;  sza_3d = pi/2.-alpha_3d
;  sza_3d = where(sza_3d.gt.pi/2,pi/2,sza_3d)       ; no sza > 90 deg
  alpha_3d = where(alpha_3d.lt.0,0,alpha_3d)
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  nmr = fsds_gc4nhr_3d*(sin(alpha_3d)+df)
  dnm = cos_i+df*(1+cos(beta_3d))/2.+pho*(sin(alpha_3d)+df)*(1-cos(beta_3d))/2.
  if (any(dnm.eq.0)) then       ; make sure there is no zeros in dnm
    ind_zero = ind_resolve(ind(ndtooned(dnm).eq.0),(/n_aw,n_beta,nhr/))
    print("zeros in dnm:")
    print(yrs(0)+"  "+mths(0)+" "+days(i))
    print(ind_zero(:,0)+" "+ind_zero(:,1)+" "+ind_zero(:,2))
    dnm = where(dnm.eq.0,2.22507e-308,dnm)
  end if
  fsds_gc_crt = nmr/dnm
;  print(cos_i(:10,:10,:)+" "+fsds_gc_crt(:10,:10,:))
;  exit
; local ,nmr,dnm,pho -sza_3d

;- cal max hr for each pair of (aw,beta)
  do j = 0, n_aw - 1        ; j = aw
    do k = 0, n_beta - 1        ; k = beta
;- whether the pair is possible
      shift_max_hr(j,k) = hr(maxind(cos_i(j,k,:)))
      crt_max_hr(j,k) = hr(maxind(fsds_gc_crt(j,k,:)))
    end do        ; k = beta
  end do        ; j = aw

;- turn off impossible pairs
;!!! temp !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
;  bln_pair = (shift_max_hr.ne.fsds_gc_max).or.(crt_max_hr.ne.gmt_noon)
;  if (num(bln_pair).eq. n_aw*n_beta) then
;    delete(bln_pair)
;    bln_pair = ((shift_max_hr.lt.fsds_gc_max-0.5).or.(shift_max_hr.gt.fsds_gc_max+0.5)).or.(crt_max_hr.ne.gmt_noon)
;    if (num(bln_pair).eq. n_aw*n_beta) then
;      delete(bln_pair)
      bln_pair = ((shift_max_hr.lt.fsds_gc_max-0.5).or.(shift_max_hr.gt.fsds_gc_max+0.5)).or.((crt_max_hr.lt.gmt_noon-0.5).or.(crt_max_hr.gt.gmt_noon+0.5))
;- it's reasonable for multi-day too: now possible shift_max_hr should be the max of the multiple days 
;    end if
;  end if
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  pair_true = where(bln_pair,0,pair_true)
;  print(shift_max_hr+"  "+fsds_gc_max+" "+crt_max_hr+"  "+gmt_noon)
;  print(fsds_gc_max)
;  print(num(pair_true.eq.1))

  delete([/hr_id,bln_pair/])
end do        ; i = day

if (num(pair_true.eq.1).eq.0) then        ; if no such a pair
  print("Fail: no possible pairs")
  print("Check GC-Net data")
  print("Function: pbl_prs")
;!!!! changed pair_top to pair: could there be any problems?
  pair = new((/1,2/),double)
  pair = -999.
  return pair
end if

ind_pair = ind_resolve(ind(ndtooned(pair_true.eq.1)),dimsizes(pair_true))
dim_pair = dimsizes(ind_pair)
npair = dim_pair(0)
pair = new((/npair,2/),double)
pair(:,0) = aw(ind_pair(:,0))
pair(:,1) = beta(ind_pair(:,1))

;============================================================
;- temp: output part 1 results
;print("# possible pairs = "+npair)
;fo = "temp_tilt.nc"
;system("/bin/rm -f "+fo)
;fout = addfile(fo,"c")
;fout->pair_pbl = pair     ; test the first line: nsu 200307 for now
;============================================================

;- check results
;- no exactly the same pairs?
;- do I need some new strategies?
;- Mar. 1, 2015: leave it so
;  do i = 0, npair - 1       ; i = pair
;    awt = pair(i,0)
;    betat = pair(i,1)
;    do j = 0, nday - 1        ; j = day
;      cos_it = cos(alpha(j,:))*cos(as(j,:)-awt)*sin(betat)+sin(alpha(j,:))*cos(betat)
;      max_hr_cos_it = hr(maxind(cos_it))
;      fsds_gc_crtt = fsds_gc4nhr*df/((1+cos(betat))/2.) + fsds_gc4nhr*(1-df)/cos_it*sin(alpha(j,:))
;      max_hr_fsds_gc_crtt = hr(maxind(fsds_gc_crtt))
;      print("aw = "+awt/pi*180.+"  beta = "+betat/pi*180.+" day = "+ddd(j)+"  truenoon = "+gmt_noon+"  crtnoon = "+max_hr_fsds_gc_crtt+"   shfnoon = "+fsds_gc_max+"  pdtnoon = "+max_hr_cos_it)
;
;    end do        ; j = day
;  end do        ; i = pair
 
return pair
end

;- part 2 function
;- usage: pair_top = crm_match(stn,lat_deg,lon_deg,yrs,mths,days,ddd,pair_pbl)
undef ("crm_match")       ; possible pairs
function crm_match(stn:string,lat_deg:float,lon_deg:float,yrs:integer,mths:integer,days:integer,ddd:integer,pair_pbl[*][2]:double)
;local nday,dfs_min,fn_gc,fin_gc,fsds_gc,fsds_gc_qc,alpha,as,hr_id,fsds_gc_loctim,fns_crm,hh,nfn_id,nfn,loctim,fsds_crm,coszrs,i,j,fin,npair,dim_pair,aw,beta,cos_i, dfs,dfs_ttl,dfs_count,rank,ntop,win_rank,win_max,win_id,nwin,pair_top
local nday,dfs_min,fn_gc,fin_gc,fsds_gc,fsds_gc_qc,alpha,as,hr_id,fsds_gc_loctim,fns_crm,hh,nfn_id,nfn,loctim,fsds_crm,coszrs,i,j,fin,npair,dim_pair,aw,beta,cos_i, dfs,dfs_ttl,dfs_count,ntop,pair_top,top_id, dfs_range, hr_gc
; local ,nwin,win_id,win_max,win_rank,rank
; local: top_id,ntop,dfs_min
begin
;print("Part 2: crm_match")
nday = dimsizes(days)

;- read in fsds_gc
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
;fn_gc = systemfunc("ls "+drc_gc+"*"+stn+"*.nc")
;fn_gc = systemfunc("ls "+drc_gc+"*"+stn+"*2015_new-time-logger.nc")
fn_gc = systemfunc("ls "+drc_gc+"*"+stn+"*2009-2010*.nc")
;fn_gc = systemfunc("ls "+drc_gc+"*"+stn+"*2011_new-time-logger.nc")
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
fin_gc = addfile(fn_gc,"r")
fsds_gc = new((/nday,24/),float)
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
fsds_gc = tofloat(fin_gc->fsds({yrs(0)},{mths(0)},{days},:))
;- initial guess
;fsds_gc = tofloat(fin_gc->fsds_ini({yrs(0)},{mths(0)},{days},:))
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
hr_gc = fin_gc->hr
;- quality flag
;- if gcnet data, apply quality flag
if (str_get_field(str_get_field(fn_gc,5,"/"),1,"_").eq."gcnet") then
  fsds_gc_qc = new((/nday,24/),float)
  fsds_gc_qc = fin_gc->fsds_qc({yrs(0)},{mths(0)},{days},:)
  fsds_gc = where(fsds_gc_qc.ne.1, fsds_gc@_FillValue, fsds_gc)       ; use only high quality data
end if

dim_pair = dimsizes(pair_pbl)
npair = dim_pair(0)
aw = pair_pbl(:,0)
beta = pair_pbl(:,1)

dfs_ttl = new(npair,float)
dfs_ttl = 0.
;rank = new(npair,integer)
dfs_count = 0       ; used to cal avg

;- cal sunrise and sunset time
;- purpose: involve only daytime time points
;- fail: eq from Yogi's book is not fit
;mnt_noon = hr_SunRiseSet(yrs(0),ddd,lat_deg)
;te = (noon_min - mnt_noon)/60.        ; sunrise
;tw = (noon_min + mnt_noon)/60.        ; sunset
;print(mnt_noon+"  "+te+"  "+tw)

;- loop over days
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
do i = 0, nday - 1        ; i = day
;do i = 2, nday - 1        ; i = day
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
;- read in CRM
  fns_crm = systemfunc("ls "+drc_crm+stn+"/"+stn+"."+yrs(0)+sprinti("%02i",mths(0))+sprinti("%02i",days(i))+".????.nc")
  if (all(ismissing(fns_crm))) then
    print("no CRM data on "+yrs(0)+sprinti("%02i",mths(0))+sprinti("%02i",days(i)))
    delete(fns_crm)
    continue
  end if
  hh = toint(systemfunc("ls "+drc_crm+stn+"/"+stn+"."+yrs(0)+sprinti("%02i",mths(0))+sprinti("%02i",days(i))+".????.nc | cut -d '.' -f 3 | cut -c 1-2 "))
;- change to filter using SZA
;  nfn_id = ind(hh.ge.te(i).and.hh.le.tw(i))        ; only take the time points after sunrise and before sunset
  nfn_id = ind(hh.ge.0.and.hh.le.23)        ; only take the time points after sunrise and before sunset
  nfn = dimsizes(nfn_id)
;  print(yrs(0)+"  "+mths(0)+" "+days(i))

  loctim = new(nfn,float)
  fsds_crm = new(nfn,float)
  coszrs = new(nfn,double)
  do j = 0, nfn - 1       ; j = nfn
;    print("fn = "+fns_crm(nfn_id(j)))
    fin = addfile(fns_crm(nfn_id(j)),"r")
    loctim(j) = fin->loctim
    fsds_crm(j) = fin->fsds
    coszrs(j) = fin->coszrs
  end do        ; w = nfn
;- use only daytime: sza > 75 deg
;!!! option !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
;  fsds_crm = where(coszrs.lt.cos(75./180.*pi),fsds_crm@_FillValue,fsds_crm)
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
;  print(loctim+"  "+acos(coszrs)/pi*180.+"  "+fsds_crm)

;- cal alpha and as
  alpha = new((/1,nfn/),double)
  as = new((/1,nfn/),double)
;  print(ddd(i)+"  "+loctim+"  "+lat_deg+" "+lon_deg)
  solar_position(yrs(0),ddd(i),loctim,lat_deg,lon_deg,alpha,as)
;  print("alpha = "+alpha/pi*180+"  as = "+as/pi*180)
;  print(loctim+"  "+fsds_crm+"  "+coszrs)
;  exit

;- loop over nCRM in a day to assess
  hr_id = ind(.not.ismissing(fsds_gc(i,:)))
  fsds_gc_loctim = ftcurv(hr_gc(hr_id),fsds_gc(i,hr_id),loctim)

;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  do j = 0, nfn - 1       ; j = crm files
;  do j = 2, nfn - 1       ; j = crm files
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    if (ismissing(fsds_crm(j))) then
      continue
    end if
    cos_i = cos(alpha(0,j))*cos(as(0,j)-aw)*sin(beta)+sin(alpha(0,j))*cos(beta)
;    dfs = abs(fsds_crm(j) - (fsds_gc_loctim(j)*df/((1+cos(beta))/2.) + fsds_gc_loctim(j)*(1-df)/cos_i*coszrs(j)))
;- use corrected eq
;    dfs = abs(fsds_crm(j) - (fsds_gc_loctim(j)*(coszrs(j)+df)/(cos_i+df*(1+cos(beta))/2.)))
;- keep the same wrong coszrs for now: corrected (Apr. 6, 2015)
;- use modified correction eq (Apr. 6, 2015)
    dfs = abs(fsds_crm(j) - (fsds_gc_loctim(j)*(sin(alpha(0,j))+df)/(cos_i+df*(1+cos(beta))/2.+pho*(sin(alpha(0,j))+df)*(1-cos(beta))/2.)))
;    printMinMax(dfs,True)
;    printVarSummary(dfs)
;    print(dfs(:10))
;    print(coszrs(j)+" "+df+"  "+fsds_gc_loctim(j)+" "+fsds_crm(j)+" "+alpha(0,j)/pi*180.+"  "+as(0,j)/pi*180.)
;    print(days(i)+" aw = "+aw/pi*180.+" beta = "+beta/pi*180.+" cos_i = "+cos_i+" crm = "+fsds_crm(j)+" crt = "+((fsds_gc_loctim(j)*(sin(alpha(0,j))+df)/(cos_i+df*(1+cos(beta))/2.+pho*(sin(alpha(0,j))+df)*(1-cos(beta))/2.))))
    dfs_ttl = dfs_ttl+tofloat(dfs)

    delete([/cos_i,dfs/])
  end do        ; j = crm files
  dfs_count = dfs_count + num(.not.ismissing(fsds_crm))

  delete([/fns_crm,hh,nfn_id,loctim,fsds_crm,coszrs,alpha,as,hr_id,fsds_gc_loctim/])
end do        ; j = day

if (dfs_count.eq.0) then     ; if no CRM 
  print("Fail: dfs_count = 0; possible all crm data missing due to high sza")
  print("Function: crm_match")
  pair_top = new((/1,2/),double)        ; output (aw,beta) pairs
  pair_top = -999
  return pair_top
end if

dfs_ttl = dfs_ttl/dfs_count       ; total difference for this pair
;print("dfs_ttl = "+dfs_ttl)
;------------------------------------------------------------
;- top pair strategy 2:
;   - (top n - top 1) < 10 W/m^2
;dfs_min = 50        ; take all the pairs with avg < 30 W/m^2 over a month
dfs_min = min(dfs_ttl)        ; now is the min of all
print("dfs_min = "+dfs_min)
dfs_range = 5       ; 5 W/m^2
top_id = ind(dfs_ttl.le.(dfs_min+dfs_range))      ; take the pairs with dfs a little (now: dfs_range W/m^2) larger than the min(dfs)
ntop = dimsizes(top_id)

pair_top = new((/ntop,2/),double)        ; output (aw,beta) pairs
;- if dfs_min is too large
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
if (dfs_min.gt.50) then     ; if the dfs too large
;if (dfs_min.gt.1000) then     ; if the dfs too large
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  print("Fail: dfs_ttl too large")
  print("Function: crm_match")
  pair_top = -999
  return pair_top
end if
;print("ntop = "+ntop)
;print(aw(top_id)/pi*180.+"  "+beta(top_id)/pi*180+" "+dfs_ttl(top_id))
;exit
; local: top_id,ntop,dfs_min

;- output pairs not sorted
pair_top(:,0) = aw(top_id)
pair_top(:,1) = beta(top_id)
; local: pair_top
print("# top pairs = "+ntop)

;------------------------------------------------------------
;- top pair strategy 1:
;   - less than dfs_min or top 10%
;rank(dim_pqsort(dfs_ttl,1)) = ispan(1,npair,1)        ; rank for this pair
;ntop = npair/10      ; top 10
;win_rank = dim_pqsort(rank,1)
;;print(ntop+"  "+aw(win_rank(:(ntop-1)))/pi*180.+" "+beta(win_rank(:(ntop-1)))/pi*180.+" "+dfs_ttl(win_rank(:(ntop-1)))+" "+rank(win_rank(:(ntop-1))))
;;print(ntop+"  "+aw(win_rank(ntop-1))/pi*180.+" "+beta(win_rank(ntop-1))/pi*180.+" "+dfs_ttl(win_rank(ntop-1))+" "+rank(win_rank(ntop-1)))
;;- if all top n < dfs_min, get all top n; if not get only the ones < dfs_min (sorted too)
;;print(dfs_ttl(win_rank(ntop-1))+"  "+dfs_min)
;if (dfs_ttl(win_rank(ntop-1)).gt.dfs_min) then
;; win_max(0) = 1 problem
;  if (dfs_ttl(win_rank(0)).gt.dfs_min) then
;    print("Fail: dfs_ttl too large")
;    print("Function: crm_match")
;;    print("yr = "+yrs(0)+" mth = "+mths(0))
;    pair_top = new((/1,1/),float)
;    pair_top = 0.
;    return pair_top 
;  end if
;  win_max = ind(dfs_ttl(win_rank).gt.dfs_min)
;  win_id = win_rank(:(win_max(0)-1))
;  delete(win_max)
;else
;  win_id = win_rank(:(ntop-1))
;end if
;nwin = dimsizes(win_id)
;;print(aw(win_id)/pi*180.+"  "+beta(win_id)/pi*180.+"  "+dfs_ttl(win_id)+" "+rank(win_id))
;
;;- fail
;if (nwin.lt.1) then
;  print("Fail: dfs_ttl too large")
;  print("Function: crm_match")
;  pair_top = new((/1,1/),float)
;  pair_top = 0.
;  return pair_top 
;end if
;; local ,nwin,win_id,win_max,win_rank,rank
;------------------------------------------------------------

return pair_top
end

;- part 3 function
;- usage  no_spike(stn,lat_deg,lon_deg,yrs,mths,days,ddd,pair_top,lst_out)
undef ("no_spike")       ; possible pairs
procedure no_spike(stn:string,lat_deg:float,lon_deg:float,yrs:integer,mths:integer,days:integer,ddd:integer,pair_top[*][2]:numeric,lst_out[1]:string)
local nday,cos_i,fsds_gc_3d,fsds_thr_3d,dfs,dfs_pair,alpha_3d,as_3d,aw_3d,beta_3d,alpha,as,nhr,hr,fsds_thr,fn_gc,fin_gc,fsds_gc,fsds_gc_qc,dim_pair,npair,aw,beta,rank,win_id,hr_gc
begin
nday = dimsizes(days)

;- read in fsds_gc
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
;fn_gc = systemfunc("ls "+drc_gc+"*"+stn+"*.nc")
;fn_gc = systemfunc("ls "+drc_gc+"*"+stn+"*2015_new-time-logger.nc")
fn_gc = systemfunc("ls "+drc_gc+"*"+stn+"*2009-2010*.nc")
;fn_gc = systemfunc("ls "+drc_gc+"*"+stn+"*2011_new-time-logger.nc")
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
fin_gc = addfile(fn_gc,"r")
fsds_gc = new((/nday,24/),float)
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
fsds_gc = tofloat(fin_gc->fsds({yrs(0)},{mths(0)},{days},:))
;- inital guess
;fsds_gc = tofloat(fin_gc->fsds_ini({yrs(0)},{mths(0)},{days},:))
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
hr_gc = fin_gc->hr
;- quality flag
;- if gcnet data, apply quality flag
if (str_get_field(str_get_field(fn_gc,5,"/"),1,"_").eq."gcnet") then
  fsds_gc_qc = new((/nday,24/),float)
  fsds_gc_qc = fin_gc->fsds_qc({yrs(0)},{mths(0)},{days},:)
  fsds_gc = where(fsds_gc_qc.ne.1, fsds_gc@_FillValue, fsds_gc)       ; use only high quality data
end if

dim_pair = dimsizes(pair_top)
npair = dim_pair(0)
aw = pair_top(:,0)
beta = pair_top(:,1)

;- theoretical fsds
nhr = 24
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
;hr = ispan(0,23,1)
hr = ispan(0,23,1)+2/60.
;hr = ispan(0,23,1)+12./60.
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
fsds_thr = thr_clr_fsds(yrs(0),ddd,hr,lat_deg,lon_deg)       ; fsds_thr(nday,nhr)
;print(fsds_thr)

;============================================================
;- temp: output part 2 results
;fo = "temp_tilt.nc"
;;system("/bin/rm -f "+fo)
;;fout = addfile(fo,"c")
;fout = addfile(fo,"w")
;fout->pair_top = pair_top     ; test the first line: nsu 200307 for now
;fout->fsds_thr = fsds_thr
;============================================================

alpha = new((/nday,nhr/),double)
as = new((/nday,nhr/),double)
solar_position(yrs(0),ddd,hr,lat_deg,lon_deg,alpha,as)

alpha_3d = conform_dims((/npair,nday,nhr/),alpha,(/1,2/))
as_3d = conform_dims((/npair,nday,nhr/),as,(/1,2/))
aw_3d = conform_dims((/npair,nday,nhr/),aw,(/0/))
beta_3d = conform_dims((/npair,nday,nhr/),beta,(/0/))
cos_i = cos(alpha_3d)*cos(as_3d-aw_3d)*sin(beta_3d)+sin(alpha_3d)*cos(beta_3d)

fsds_gc_3d = conform_dims((/npair,nday,nhr/),fsds_gc,(/1,2/))
fsds_thr_3d = conform_dims((/npair,nday,nhr/),fsds_thr,(/1,2/))
;alpha_3d = where(alpha_3d.lt.0,0.0000001,alpha_3d)       ; deal with negative alpha
;dfs = abs(fsds_gc_3d*df/((1+cos(beta_3d))/2.) + fsds_gc_3d*(1-df)/cos_i*sin(alpha_3d) - fsds_thr_3d)
;- use corrected eq
dfs = abs((fsds_gc_3d*(sin(alpha_3d)+df)/(cos_i+df*(1+cos(beta_3d))/2.+pho*(sin(alpha_3d)+df)*(1-cos(beta_3d))/2.))-fsds_thr_3d)
;printMinMax(dfs,True)

n_large_dfs = dim_num(dfs.gt.fsds_thr_3d*0.1)       ; spike: 10% fsds at that time
;n_large_dfs = dim_num(dfs.gt.50)       ; spike: 50 W/m^2 in dfs

;print(n_large_dfs(:,0)+"  "+n_large_dfs(:,1)+"  "+n_large_dfs(:,2)+"  "+n_large_dfs(:,3)+"  "+n_large_dfs(:,4)+"  "+n_large_dfs(:,5)+"  "+n_large_dfs(:,6))
;print(dfs+" "+fsds_thr_3d*0.1)

n_large_dfs_day = dim_num(n_large_dfs.eq.0)       ; how many days with 0 spikes
;print("large dfs day = "+n_large_dfs_day)
if (all(n_large_dfs_day.lt.nday)) then        ; all have spikes; use the least spike one
  dfs_pair = dim_avg(dim_avg(dfs))        ; avg diff from fsds_thr
  ;print(dfs_pair)
  ;- local: n_large_dfs,n_lare_dfs_day
  
  ;- pick the one
  rank = new(npair,integer)
  rank(dim_pqsort(dfs_pair,1)) = ispan(1,npair,1)
  ;print(aw_win/pi*180+" "+beta_win/pi*180+" "+dfs_final+" "+rank)
  ;win_id = ind(rank.lt.31)        ; output top 30 to check
  win_id = dim_pqsort(rank,1)        ; output top 30 to check; sorted
  ;print(aw(win_id(:29))/pi*180.+"  "+beta(win_id(:29))/pi*180.+"  "+dfs_pair(win_id(:29))+" "+rank(win_id(:29)))
else        ; some no spikes; use the one closet to CRM
  print("no spikes at all!")
  win_id = ind(n_large_dfs_day.eq.nday)
  print(n_large_dfs_day)
;- local ,no_spike_id
end if

system("echo "+stn+" "+yrs(0)+sprinti("%02i",mths(0))+" "+aw(win_id(0))+" "+beta(win_id(0))+" >> "+lst_out)
end
