; Written by Wang, Wenshan 2016-01-27 Wednesday 11:51:41
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$HOME/scripts/ncl_script/res.ncl"
load "$HOME/scripts/ncl_script/plot.ncl"
;*************************************************************
; Purpose: generate clr days list from high_dfs-std.txt
;	Steps:
;		- read high_dfs-std.txt: each line
;		- find in clr-days.txt and output each day per line
;************************************************************
begin
lst_qk = "high_dfs-std.txt"
lst_clr = "clr-days.txt"

;lst_out = "clr-days_test.txt"
lst_out = "clr-days_qk.txt"

str = asciiread(lst_qk,-1,"string")
nln = dimsizes(str)

do i = 0, nln - 1				; i = qk line
;	print("str = "+str)
  lns = str_split(str(i)," ")
	stn = lns(0)
	yr = lns(1)
	mth = lns(2)
	mm = sprinti("%02i",toint(mth))
	print(stn+" "+yr+mm)

	ln_clr = systemfunc("grep '"+stn+" "+yr+mm+"' "+lst_clr)
	print("ln_clr = "+ln_clr)
	lns_clr = str_split(ln_clr," ")
	nln_clr = dimsizes(lns_clr)-1

	do j = 0, nln_clr-1				; j = clr line
  	system("echo "+stn+" "+lns_clr(j+1)+" >> "+lst_out)
	end do				; j = clr line

	delete([/lns,stn,yr,mth,mm,ln_clr,lns_clr,nln_clr/])
end do

print("done!")
end
