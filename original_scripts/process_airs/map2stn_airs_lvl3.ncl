; Written by Wang, Wenshan 2017-01-27 Friday 15:56:42
load "$HOME/scripts/ncl_script/wenshanw.ncl"
;*************************************************************
; Purpose: map2stn for AIRS level 3 data: 
;   for both sfc and profiles; 
;   use the same grid point even though it's missing
; grid point: the closet ONE grid
;*************************************************************
begin
;xpt="airx3spd"       ; check vars
xpt="airx3std"
drc_in="/data/wenshanw/airs/hdf_"+xpt+"/"
drc_out="/data/wenshanw/airs/stn_lvl3/"

yr=2016

fns = systemfunc("ls "+drc_in+xpt+"."+yr+".*.nc")
dates = systemfunc("ls "+drc_in+xpt+"."+yr+".*.nc | cut -d '.' -f 2-4 ")
nfn = dimsizes(fns)
;print(fns+" "+dates)
;exit

fn = fns(0)
fin = addfile(fn,"r")
;time = fin->time
;nhr = dimsizes(time)
;plev = fin->plev
;plev = fin->lev
;nplev = dimsizes(plev)
var_lat = "YDim:ascending"
var_lon = "XDim:ascending"
lat = fin->$var_lat$(:30)       ; N hemi
lon = fin->$var_lon$
nlat = dimsizes(lat)
nlon = dimsizes(lon)
;print(lat)
;print(lon)
;exit

;= var: use all the variables with TqJ(oint)
vars_ori = getfilevarnames(fin)
vars = str_get_field(str_match(vars_ori,"TqJ"),1,"/")
nvar = dimsizes(vars)
;print(vars_ori)
;print(vars)
lnd = fin->LandSeaMask
delete([/vars_ori,fin/])

;= cal distance
;- stn lat&lon
lst_stn = "stn_run.txt"
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
stns = systemfunc("cat "+lst_stn+" | awk '{print $1}'")
;stns = "barrow"
;!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
latstn = tofloat(systemfunc("cat "+lst_stn+" | awk '{print $2}'"))
lonstn = tofloat(systemfunc("cat "+lst_stn+" | awk '{print $3}'"))
;print(stns+"  "+latstn+"  "+lonstn)
nstn = dimsizes(stns)
latstn3d = conform_dims((/nstn,nlat,nlon/),latstn,(/0/))
lonstn3d = conform_dims((/nstn,nlat,nlon/),lonstn,(/0/))
latstn3d@units = "degrees_north"
lonstn3d@units = "degrees_east"

;- lat/lon idx
lat3d = conform_dims((/nstn,nlat,nlon/),lat,(/1/))
lon3d = conform_dims((/nstn,nlat,nlon/),lon,(/2/))
dst = gc_latlon(lat3d,lon3d,latstn3d,lonstn3d,2,-4)       ; 2: no interpolate points; -4: in km
dst_reshp = reshape(dst, (/nstn,nlat*nlon/))
dst_min = dim_min(dst_reshp)        ; checked: all less than 25 km
dst_min_3d = conform_dims((/nstn,nlat,nlon/),dst_min,(/0/))
dst_min_ind = ind_resolve(ind(ndtooned(dst).eq.ndtooned(dst_min_3d)),(/nstn,nlat,nlon/))
dst_min_ind_reshp = reshape(dst_min_ind, (/nstn, 3/))
lat_id = dst_min_ind_reshp(:,1)
lon_id = dst_min_ind_reshp(:,2)
;= test dst: less than 70 km away
lst_dis = "distance_map2stn_airs_lvl3_allstn.txt"
do m = 0, nstn - 1
  print(stns(m)+" "+latstn(m)+" "+lonstn(m)+" "+lat(lat_id(m))+" "+lon(lon_id(m))+" "+dst_min(m)+"  "+lat_id(m)+" "+lon_id(m))
  system("echo "+stns(m)+" "+latstn(m)+" "+lonstn(m)+" "+lat(lat_id(m))+" "+lon(lon_id(m))+" "+dst_min(m)+" >> "+lst_dis)
end do
;= distance diff
print(avg(dst_min)+"	"+min(dst_min)+"	"+max(dst_min))
system("echo "+avg(dst_min)+"	"+min(dst_min)+"	"+max(dst_min)+" >> "+lst_dis)
;exit
delete([/dst,dst_reshp,dst_min,dst_min_3d,dst_min_ind,dst_min_ind_reshp/])

do i = 0, nfn - 1       ; i = files
  fn = fns(i)
  date = dates(i)
  print("date = "+date)

  fin = addfile(fn,"r")

  do j = 0, nstn - 1        ; j = stn
    stn = stns(j)
    fo = drc_out+stn+"."+xpt+"."+date+".nc"
;    print("fo = "+fo)
;    exit
    system("/bin/rm -f "+fo)
    fout = addfile(fo,"c")

    do k = 0, nvar - 1      ; k = var
      var = vars(k)
      if (var.eq."XDim:ascending_TqJoint".or.var.eq."YDim:ascending_TqJoint".or.var.eq."XDim:descending_TqJoint".or.var.eq."YDim:descending_TqJoint")
        continue
      end if
      dat = fin->$var$
      ndim = dimsizes(dimsizes(dat))      ; so far, only 1,2,3
;      print(var+" "+ndim)
      if (ndim.eq.1)
        fout->$var$ = dat
      else if (ndim.eq.2)
        dout = dat(lat_id(j),lon_id(j))
        dout!0 = "scaler"
        fout->$var$ = dout
        delete(dout)
      else if (ndim.eq.3)
        fout->$var$ = dat(:,lat_id(j),lon_id(j))
      end if
      end if
      end if
  
      delete([/dat/])
    end do        ; k = var
    delete([/fo,fout/])
  end do        ; j = stn

  delete([/fn,fin/])
end do        ; i = files

print("done!")
end
