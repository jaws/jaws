; Written by Wang, Wenshan 2015-05-04 Monday 13:34:30
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
;*************************************************************
; Purpose: check why some dfs are so large
;************************************************************
begin
lst_hgh = "high_dfs-std.txt"
;lst_hgh = "high_dfs-std_upe.txt"
str_hgh = asciiread(lst_hgh,-1,"string")
nln = dimsizes(str_hgh)

lst_clr = "clr-days.txt"

;drc_gc = "/data/wenshanw/gcnet/tilt_fix/"
drc_gc = "/data/wenshanw/gcnet/tilt_re/"
drc_crm = "/data/wenshanw/crm/myd_long_clr/"

;PLOT_CLR = 1       ; plot only clr day if 1; plot all days if 0
PLOT_CLR = 0

; resourses
;------------------------------------------------------------
lgd = (/"fsds","fsds_fixed"/)
if (PLOT_CLR.eq.1) then
  fname = "pdf_tilt/check-xy_quick-chg_clr"
else
  fname = "pdf_tilt/check-xy_quick-chg_all"
end if
wks = gsn_open_wks("pdf", fname)
gsn_define_colormap(wks,"amwg")

res = True

res@gsnDraw  = False                          ; don't draw
res@gsnFrame = False                          ; don't advance frame
res@gsnMaximize  = True
;res@gsnLeftStringFontColor = 15       ; red
;res@gsnRightStringFontColor = 3       ; blue

;--- canvas size
;res@vpXF = 0.05 
;res@vpYF = 0.9 
res@vpHeightF = 0.3 ; change aspect ratio of plot
res@vpWidthF = 0.8

;--- legend
res@pmLegendDisplayMode    = "Always"            ; turn on legend
res@pmLegendSide           = "Top"               ; Change location of 
res@pmLegendParallelPosF   = .15                  ; move units right
res@pmLegendOrthogonalPosF = -0.45                ; move units down
res@pmLegendWidthF         = 0.15                ; Change width and
res@pmLegendHeightF        = 0.08                ; height of legend.
res@lgPerimOn              = False               ; turn off box around
res@lgLabelFontHeightF     = .015                 ; label font height
res@xyExplicitLegendLabels = lgd          ; create explicit labels

res@tiXAxisString = "GMT Hour"           ; y axis title
res@tiYAxisString = "Radiation"
;res@tiXAxisOn = True
;res@tiYAxisOn = True

;- gc-net
;res@xyMarkLineMode = "MarkLines"
res@xyMarkLineMode = "Lines"
;res@xyMarkLineMode = "Markers"
;res@xyMarkerSizes = (/0.015,0.015,0.015,0.015,0.015,0.015/)
res@xyLineColors = (/3,9,15,17/)        ; 1: black
;res@xyMarkerColors = res@xyLineColors
res@xyLineThicknessF = 2
res@xyDashPatterns = (/1,2,3,4/) 

; add polygon/line
gres = True
gres@gsMarkerIndex = 5        ; cross
gres@gsMarkerSizeF = 0.007
gres@gsMarkerThicknessF = 2.0
gres@gsMarkerColor = 15        ; blue: 3; red: 15
lres = True
lres@gsLineThicknessF = 2.0
lres@gsLineColor = 17
lres@gsLineDashPattern = 4

resp = True
resp@gsnMaximize         = True    ; The default for PS/PDF
resp@gsnPaperOrientation = "portrait" 
;res@wkOrientation = "portrait" 
;resp@wkOrientation = "portrait" 

do i = 0, nln - 1       ; i = high line
;- high stn-mth
  ln_hgh = str_split(str_hgh(i)," ")
;  print("ln_hgh = "+ln_hgh)
  stn = ln_hgh(0)
  yr_hgh = toint(ln_hgh(1))
  mth_hgh = toint(ln_hgh(2))
;  dfs = tofloat(ln_hgh(5))
;- clr days
  if (PLOT_CLR.eq.1) then        ; plot only clr days
    str_clr = systemfunc("cat "+lst_clr+" | grep '"+stn+" "+yr_hgh+sprinti("%02i",mth_hgh)+"'")
    ln_clr = str_split(str_clr," ")
    yrs = toint(ln_clr(1:))/10000
    mths = toint(str_get_cols(ln_clr(1:),4,5))
    days = toint(str_get_cols(ln_clr(1:),6,7))
    ddd = day_of_year(yrs,mths,days)
    nday = dimsizes(days)
    delete([/str_clr,ln_clr,yrs,mths/])
  else        ; plot all days
    nday = days_in_month(yr_hgh,mth_hgh)
    days = ispan(1,nday,1)
    ddd0 = day_of_year(yr_hgh,mth_hgh,1)
    ddd = ispan(ddd0,ddd0+nday-1,1)
;    print("days = "+days+"  "+ddd)
;    exit
  end if
;  print(stn+" "+yrs+" "+mths+"  "+days+"  "+ddd)
;  print("nday = "+nday)
;- GC-Net
  fn_gc = stn+"_tilt-fixed.nc"
  fin_gc = addfile(drc_gc+fn_gc,"r")
  fsds = fin_gc->fsds_gc({yr_hgh},{mth_hgh},{days},:)
  fsds_fix = fin_gc->fsds_fixed({yr_hgh},{mth_hgh},{days},:)
	hr = fin_gc->hr

  dr = new((/2,nday,24/),float)
  dr(0,:,:) = (/fsds/)
  dr(1,:,:) = tofloat(fsds_fix)

  plot = new(nday,graphic)
  dum = new(nday,graphic)

;- CRM
  do j = 0, nday - 1        ; j = day
    fns_crm = systemfunc("ls "+drc_crm+stn+"/"+stn+"."+yr_hgh+ddd(j)+".????.nc")
    if (all(ismissing(fns_crm))) then
      print("no CRM on "+yr_hgh+ddd(j))
      delete(fns_crm)
      continue
    end if
    nfn = dimsizes(fns_crm)
    dat = new(nfn,float)
    loctim = new(nfn,float)
    do k = 0, nfn - 1       ; k = file
      fin_crm = addfile(fns_crm(k),"r")
      dat(k) = fin_crm->fsds
      loctim(k) = fin_crm->loctim
    end do        ; k = file

    res@gsnRightString = yr_hgh+sprinti("%02i",mth_hgh)+sprinti("%02i",days(j))
;    res@gsnLeftString = sprintf("%5.2f",dfs)
    plot(j) = gsn_csm_xy(wks,hr,dr(:,j,:),res)
    dum(j) = gsn_add_polymarker(wks,plot(j),loctim,dat,gres)
  
    delete([/fns_crm,dat,loctim/])
  end do        ; j = day

  resp@txString = stn+" "+yr_hgh+sprinti("%02i",mth_hgh)
  gsn_panel(wks,plot,(/nday/4+1,4/),resp)

  delete([/ln_hgh,stn,yr_hgh,mth_hgh/])
  delete([/days,ddd,nday/])
  delete([/fn_gc,fin_gc,fsds,fsds_fix/])
  delete([/plot,dum,dr/])
end do        ; i = high line

print("done!")
end
