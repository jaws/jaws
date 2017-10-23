; Written by Wang, Wenshan 2016-05-19 Thursday 14:23:20
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$HOME/scripts/ncl_script/wenshanw.ncl"
load "$HOME/cloud/gcnet/cal_para.ncl"
;*************************************************************
; Purpose: plot fsds and CRM to pick up clear days to do check and tilt correction
; Modification:
; 20160616: plot fsds, fsus on the left and cos(SZA) on the right to better distinguish time logger and tilt
; 20170414: no need to cal alpha and as here; did it in cal_sza.ncl and put the cos(SZA) in file
;************************************************************
begin
;= data
;drc = "/data/wenshanw/bsrn/netcdf/"
;drc = "/data/wenshanw/aws/spole/"
;drc = "/data/wenshanw/aws/3hr_loose/"
drc = "/data/wenshanw/aws/test/"

;lst_stn = "~/cloud/gcnet/stn_spole.txt"
;lst_stn = "~/cloud/gcnet/stn_fix-promice.txt"
;lst_stn = "~/cloud/gcnet/stn_fix-gp.txt"
lst_stn = "~/cloud/cre/stn_2016_promice.txt"
stns = systemfunc("cat "+lst_stn+" | awk '{print $1}'")
lats = tofloat(systemfunc("cat "+lst_stn+" | awk '{print $2}'"))
lons = tofloat(systemfunc("cat "+lst_stn+" | awk '{print $3}'"))
nstn = dimsizes(stns)
;print("stn = "+stns)
;exit

;drc_air = "/data/wenshanw/crm/spole/"

;= plot settings
res = True
res@xyLineColors = (/3,15/)
res = resXY(res,(/"fsds","fsus"/),"hr","radiation (W/m^2)")
resr = True
resr@xyLineColors = (/9/)        ; 1: black
resr@xyDashPatterns = (/2/) 
resr@pmLegendOrthogonalPosF = -0.85                ; move units down
resr = resXY(resr,"cos(SZA)","hr","cos(SZA)")
txres = True
txres = resTX(txres)
resp = True

plots = new(31,graphic)
dums = new(31,graphic)

;hr = fspan(0.5,23.5,24)     ; since I avg the 60 mnt
yb = 2008
ye = 2016       ; for bsrn
ny = ye-yb+1
;mths = (/11,12,1,2,3,4/)
;mths = (/1,2,3,4,9,10,11,12/)
mths = (/5,6,7,8,9/)
nm = dimsizes(mths)

;dr = new((/2,ny,12,31,24/),float)
dr = new((/2,ny,nm,31,24/),float)

alpha = new((/1,24/),double)
as = new((/1,24/),double)

;= plot
do i = 0, nstn - 1        ; i = stn
  stn = stns(i)
  lat = lats(i)
  lon = lons(i)
  print("stn "+stn)

  fn = systemfunc("ls "+drc+stn+"*.nc")
;  fn = systemfunc("ls "+drc+stn+"*2009-2010*.nc")
  fin = addfile(fn,"r")
;  fsds = dim_avg_Wrap(fin->fsds)
  fsds = fin->fsds_limit
  dr(0,:,:,:,:) = fsds({yb:ye},{mths},:,:)
  dr(1,:,:,:,:) = (/fin->fsus_limit({yb:ye},{mths},:,:)/)
;  fsds@_FillValue = default_fillvalue(typeof(fsds))
;  replace_ieeenan(fsds,fsds@_FillValue,0)
;  printVarSummary(fsds)
;  exit
  hr = fin->hr
;  cossza = fin->cossza({yb:ye},{mths},:,:)
;  print("hr = "+hr)
;  exit

;- wks
;  fname = "pdf_spole/clr-pck_"+stn
  fname = "pdf_clr/clr-pck_"+stn
  wks = gsn_open_wks("pdf",fname)
  gsn_define_colormap(wks,"amwg")       ; color map

  do j = 0, ny - 1      ; i = yr
    yr = yb+j
    do k = 0, nm - 1
      mth = mths(k)

      if (all(ismissing(fsds({yr},{mth},:,:))))
        continue
      end if

;- only for bsrn data
;      if (mth.lt.10)
;        yr = yb+j+1
;      else
;        yr = yb+j
;      end if
      yyyymm = yr+sprinti("%02i",mth)

      dx = max(dr(:,{yr},{mth},:,:))-min(dr(:,{yr},{mth},:,:))
      res@trYMinF = min(dr(:,{yr},{mth},:,:))-dx/10.
      res@trYMaxF = max(dr(:,{yr},{mth},:,:))+dx/10.

      do di = 0, 30     ; di = day
;        print(hr+"  "+fsds(j,k,di,:))
;        print("nan = "+num(isnan_ieee(fsds)))

        if (all(ismissing(fsds({yr},{mth},di,:)))) then
          continue
        end if

        ddd = day_of_year(yr,mth,(di+1))
        solar_position(yr,ddd,hr,lat,lon,alpha,as)
        cossza = tofloat(sin(alpha(0,:)))

;        ds = max(cossza)-min(cossza)
;        resr@trYMaxF = max(cossza)+ds/10
;        resr@trYMinF = min(cossza)-ds/10

        yyyymmdd = yyyymm+sprinti("%02i",(di+1))
;        fns = systemfunc("ls "+drc_air+stn+"."+yyyymmdd+".????.nc")
;        if (.not.all(ismissing(fns))) then
;          delete(fns)
;          continue
;        end if

        res@gsnLeftString = yyyymmdd
;        plots(di) = gsn_csm_xy(wks,hr,fsds({yr},{mth},di,:),res)
;        plots(di) = gsn_csm_xy2(wks,hr,dr(:,{yr},{mth},di,:),cossza(i,k,di,:),res,resr)
        plots(di) = gsn_csm_xy2(wks,hr,dr(:,{yr},{mth},di,:),cossza,res,resr)

      end do        ; di = day

      resp@txString = stn+" "+yr+sprinti("%02i",mth)
      plot_panel(wks,plots,(/8,4/),resp)
      plots = plots@_FillValue
    end do        ; k = mth
  end do      ; i = yr

end do        ; i = stn

print("done!")
end
