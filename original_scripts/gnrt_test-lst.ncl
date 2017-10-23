; Written by Wang, Wenshan 2016-01-30 Saturday 16:56:57
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$HOME/scripts/ncl_script/res.ncl"
load "$HOME/scripts/ncl_script/plot.ncl"
;*************************************************************
; Purpose: generate matched lst_aw-beta and clr-days for fix_tilt_test.ncl to work on
;************************************************************
begin
lst_in = "out_brk"

lst_ab_in = "tilt_netcdf/lst_aw-beta_qk.txt"
lst_ab_out = "lst_aw-beta_test.txt"
system("/bin/rm -f "+lst_ab_out)
system("echo stn yyyymm aw/radians beta/radians >> "+lst_ab_out)
lst_clr_in = "clr-days_qk.txt"				; make sure lst_ab_in and lst_clr_in match!
lst_clr_out = "clr-days_qk_test.txt"
system("/bin/rm -f "+lst_clr_out)

stns = systemfunc("grep 'Bad estimate' "+lst_in+" | cut -d ' ' -f 2")
yrmm = systemfunc("grep 'Bad estimate' "+lst_in+" | cut -d ' ' -f 3 | cut -c 1-6")
strs = stns+" "+yrmm
nstr = dimsizes(strs)
;print("str = "+strs)
;exit

do i = 0, nstr - 1				; i = line
	if (i.ne.0) then				; check whether duplicate
		if (strs(i).eq.strs(i-1)) then
			continue
		end if
	end if

	str_clr = systemfunc("grep '"+strs(i)+"' "+lst_clr_in)
	str_ab = systemfunc("grep '"+strs(i)+"' "+lst_ab_in)
	nclr = dimsizes(str_clr)

	if (nclr.ne.dimsizes(str_ab)) then
		print("Oooops! We have a problem! Check why #aw-beta doesn't match #clr in one month!")
		delete([/str_clr,str_ab/])
		continue
	end if

	do j = 0, nclr - 1			; j = clr
		system("echo "+str_clr(j)+" >> "+lst_clr_out)
		system("echo "+str_ab(j)+" >> "+lst_ab_out)
	end do				; j = clr

	delete([/str_clr,str_ab/])
end do				; i = line

print("done!")
end
