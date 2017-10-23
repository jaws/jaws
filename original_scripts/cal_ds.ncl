; Written by Wang Wenshan 2015-03-19 Thursday 16:42:56
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
;*************************************************************
; Purpose: cal ds use eq from /cite{Reda2004}
; Assumption: declination doesn't change in a day
; Note: 
;   - cal in double (high precision)
; Usage:
;   - input hr must be in GMT
;************************************************************
pi = 3.1415926535898d

;- cal ds 
;- opt: input hr is 0: standard time; 1: solar time
;-  if opt = 1, lon_deg will not be used
;- NOTES: both standard and solar time must be in GMT not local
undef ("cal_ds")
function cal_ds(yr:numeric, ddd:numeric, hr:numeric)
local ds,yr_cfm,ddd_cfm,hr_cfm,nddd,nhr,md,mth,day,jd,T,dT,d_tau,lamda,u,eps_0,eps,X,coe,Y,X_cfm,d_psi,d_eps,jde,jc,jce,jme,fn,fin,L0i,L1i,L2i,L3i,L4i,L5i,L0,L1,L2,L3,L4,L5,L_deg,L,B0i,B1i,B0,B1,B_deg,B,R0i,R1i,R2i,R3i,R4i,R0,R1,R2,R3,R4,Theta,beta,Yr,M,D,A,Br,dim_coe,coe_cfm,dim_B0,B0i_cfm,jme_cfm,dim_B1,B1i_cfm,dim_R0,R0i_cfm,dim_R1,R1i_cfm,dim_R2,R2i_cfm,dim_R3,R3i_cfm,dim_R4,R4i_cfm,jce_cfm,Y_cfm,dim_Y
begin
;;- temp inputs
;------------------------------------------------------------
;;yr = 2005
;yr = 2003
;mth = 10 
;day = 17
;ddd = day_of_year(yr,mth,day)
;print("ddd = "+ddd)
;exit
;ddd = 290
;------------------------------------------------------------

;- yr must be scalar
if (dimsizes(yr).ne.1) then
  print("yr must be a scalar")
  return -999
end if

;- YMD
nddd = dimsizes(ddd)
nhr = dimsizes(hr)
yr@calendar = "gregorian" 
yr_cfm = conform_dims((/nddd,nhr/),yr,-1)
ddd_cfm = conform_dims((/nddd,nhr/),ddd,(/0/))
md = monthday(yr_cfm,ddd_cfm)
;print("md = "+md)
mth = md/100
day = md-md/100*100
;print(yr+"  "+mth+" "+day)
; local ,md,mth,day

;- JD
;- input time: standard or solar time
;- no need to convert: since eq asks for UT
hr_cfm = todouble(conform_dims((/nddd,nhr/),hr,(/1/)))
;if (opt.eq.0) then        ; standard time: convert to solar time
;  ET = cal_ET(ddd_cfm)        ; ET(/nddd, nhr/)
;  hr_cfm = hr_cfm*60.+ET(i)+4.*(lon_deg-lon_ref)   ; solar time in min
;end if
; local ,ET
;hr_fake = conform_dims((/nddd,nhr/),-1,-1)
;jd1 = greg2jul(yr_cfm,mth,day,hr_fake)       ; NCL function: jd1
;- reda method
Yr = where(mth.le.2, yr_cfm-1,yr_cfm)
M = where(mth.le.2, mth+12,mth)
D = day+hr_cfm/24.
A = toint(yr_cfm/100)
Br = 2-A+toint(A/4)
jd = toint(365.25*(Yr+4716))+toint(30.6001*(M+1))+D+Br-1524.5       ; jd2
;print(jd1+" "+jd2)
;print(jd1+" "+jd)
;- jd1 = jd2 so use jd1 way
;- need to go back to use jd2's way (Reda's way), since my hr is not integer
;------------------------------------------------------------
;- temp
;jd = 2452930.312847d
;print("jd = "+jd)
;printVarSummary(jd)
;------------------------------------------------------------
; local ,jd
; local ,Yr,M,D,A,Br

;- delta T
T = (yr_cfm-1820)/100.
dT = todouble(-20+32*T^2)       ; Morrison & Stephenson eq
;- temp
;dT = 67d
;print("dT = "+dT)
; local ,T,dT

;- JDE, JC, JCE and JME
jde = jd + dT/86400.
;print("jde = "+jde)
jc = (jd-2451545)/36525.
;print("jc = "+jc)
jce = (jde-2451545)/36525.
;print("jce = "+jce)
jme = jce/10.       ; (/nddd,nhr/)
;print("jme = "+jme)
; local ,jde,jc,jce,jme

;- L
;- read in para
fn = "$HOME/cloud/gcnet/ds_para.nc"
fin = addfile(fn,"r")
L0i = fin->L0
dim_L0 = dimsizes(L0i)
L0i_cfm = conform_dims((/dim_L0(0),dim_L0(1),nddd,nhr/),L0i,(/0,1/))
jme_cfm = conform_dims((/dim_L0(0),nddd,nhr/),jme,(/1,2/))
;L0 = sum(L0i(:,0)*cos((L0i(:,1)+L0i(:,2)*jme)/180.*pi))
L0 = dim_sum_n((L0i_cfm(:,0,:,:)*cos(L0i_cfm(:,1,:,:)+L0i_cfm(:,2,:,:)*jme_cfm)),0)
delete(jme_cfm)
L1i = fin->L1
dim_L1 = dimsizes(L1i)
L1i_cfm = conform_dims((/dim_L1(0),dim_L1(1),nddd,nhr/),L1i,(/0,1/))
jme_cfm = conform_dims((/dim_L1(0),nddd,nhr/),jme,(/1,2/))
L1 = dim_sum_n((L1i_cfm(:,0,:,:)*cos(L1i_cfm(:,1,:,:)+L1i_cfm(:,2,:,:)*jme_cfm)),0)
delete(jme_cfm)
L2i = fin->L2
dim_L2 = dimsizes(L2i)
L2i_cfm = conform_dims((/dim_L2(0),dim_L2(1),nddd,nhr/),L2i,(/0,1/))
jme_cfm = conform_dims((/dim_L2(0),nddd,nhr/),jme,(/1,2/))
L2 = dim_sum_n((L2i_cfm(:,0,:,:)*cos(L2i_cfm(:,1,:,:)+L2i_cfm(:,2,:,:)*jme_cfm)),0)
delete(jme_cfm)
L3i = fin->L3
dim_L3 = dimsizes(L3i)
L3i_cfm = conform_dims((/dim_L3(0),dim_L3(1),nddd,nhr/),L3i,(/0,1/))
jme_cfm = conform_dims((/dim_L3(0),nddd,nhr/),jme,(/1,2/))
L3 = dim_sum_n((L3i_cfm(:,0,:,:)*cos(L3i_cfm(:,1,:,:)+L3i_cfm(:,2,:,:)*jme_cfm)),0)
delete(jme_cfm)
L4i = fin->L4
dim_L4 = dimsizes(L4i)
L4i_cfm = conform_dims((/dim_L4(0),dim_L4(1),nddd,nhr/),L4i,(/0,1/))
jme_cfm = conform_dims((/dim_L4(0),nddd,nhr/),jme,(/1,2/))
L4 = dim_sum_n((L4i_cfm(:,0,:,:)*cos(L4i_cfm(:,1,:,:)+L4i_cfm(:,2,:,:)*jme_cfm)),0)
delete(jme_cfm)
L5i = fin->L5
dim_L5 = dimsizes(L5i)
L5i_cfm = conform_dims((/dim_L5(0),dim_L5(1),nddd,nhr/),L5i,(/0,1/))
jme_cfm = conform_dims((/dim_L5(0),nddd,nhr/),jme,(/1,2/))
L5 = dim_sum_n((L5i_cfm(:,0,:,:)*cos(L5i_cfm(:,1,:,:)+L5i_cfm(:,2,:,:)*jme_cfm)),0)
delete(jme_cfm)
;print("L0 = "+L0)
;print("L1 = "+L1)
;print("L2 = "+L2)
;print("L3 = "+L3)
;print("L4 = "+L4)
;print("L5 = "+L5)
L_deg = ((L0+L1*jme+L2*jme^2+L3*jme^3+L4*jme^4+L5*jme^5)/(10^8))/pi*180.        ; in degree
L = L_deg - toint(L_deg/360.)*360.        ; in degree
;print("L = "+L)
;printVarSummary(L)
; local ,fn,fin,L0i,L1i,L2i,L3i,L4i,L5i,L0,L1,L2,L3,L4,L5,L_deg,L
; local ,dim_L0,L0i_cfm,jme_cfm,dim_L1,L1i_cfm,dim_L2,L2i_cfm,dim_L3,L3i_cfm,dim_L4,L4i_cfm,dim_L5,L5i_cfm

;- B
B0i = fin->B0
dim_B0 = dimsizes(B0i)
B0i_cfm = conform_dims((/dim_B0(0),dim_B0(1),nddd,nhr/),B0i,(/0,1/))
jme_cfm = conform_dims((/dim_B0(0),nddd,nhr/),jme,(/1,2/))
B0 = dim_sum_n((B0i_cfm(:,0,:,:)*cos(B0i_cfm(:,1,:,:)+B0i_cfm(:,2,:,:)*jme_cfm)),0)
delete(jme_cfm)
B1i = fin->B1
dim_B1 = dimsizes(B1i)
B1i_cfm = conform_dims((/dim_B1(0),dim_B1(1),nddd,nhr/),B1i,(/0,1/))
jme_cfm = conform_dims((/dim_B1(0),nddd,nhr/),jme,(/1,2/))
B1 = dim_sum_n((B1i_cfm(:,0,:,:)*cos(B1i_cfm(:,1,:,:)+B1i_cfm(:,2,:,:)*jme_cfm)),0)
delete(jme_cfm)
;print("B0 = "+B0)
;print("B1 = "+B1)
B_deg = ((B0+B1*jme)/(10^8))/pi*180.        ; in degree
B = B_deg - toint(B_deg/360.)*360.        ; in degree
;print("B = "+B)
;printVarSummary(B)
; local ,B0i,B1i,B0,B1,B_deg,B
; local ,dim_B0,B0i_cfm,jme_cfm,dim_B1,B1i_cfm

;- R
R0i = fin->R0
dim_R0 = dimsizes(R0i)
R0i_cfm = conform_dims((/dim_R0(0),dim_R0(1),nddd,nhr/),R0i,(/0,1/))
jme_cfm = conform_dims((/dim_R0(0),nddd,nhr/),jme,(/1,2/))
;R0 = sum(R0i(:,0)*cos((R0i(:,1)+R0i(:,2)*jme)/180.*pi))
R0 = dim_sum_n((R0i_cfm(:,0,:,:)*cos(R0i_cfm(:,1,:,:)+R0i_cfm(:,2,:,:)*jme_cfm)),0)
delete(jme_cfm)
R1i = fin->R1
dim_R1 = dimsizes(R1i)
R1i_cfm = conform_dims((/dim_R1(0),dim_R1(1),nddd,nhr/),R1i,(/0,1/))
jme_cfm = conform_dims((/dim_R1(0),nddd,nhr/),jme,(/1,2/))
R1 = dim_sum_n((R1i_cfm(:,0,:,:)*cos(R1i_cfm(:,1,:,:)+R1i_cfm(:,2,:,:)*jme_cfm)),0)
delete(jme_cfm)
R2i = fin->R2
dim_R2 = dimsizes(R2i)
R2i_cfm = conform_dims((/dim_R2(0),dim_R2(1),nddd,nhr/),R2i,(/0,1/))
jme_cfm = conform_dims((/dim_R2(0),nddd,nhr/),jme,(/1,2/))
R2 = dim_sum_n((R2i_cfm(:,0,:,:)*cos(R2i_cfm(:,1,:,:)+R2i_cfm(:,2,:,:)*jme_cfm)),0)
delete(jme_cfm)
R3i = fin->R3
dim_R3 = dimsizes(R3i)
R3i_cfm = conform_dims((/dim_R3(0),dim_R3(1),nddd,nhr/),R3i,(/0,1/))
jme_cfm = conform_dims((/dim_R3(0),nddd,nhr/),jme,(/1,2/))
R3 = dim_sum_n((R3i_cfm(:,0,:,:)*cos(R3i_cfm(:,1,:,:)+R3i_cfm(:,2,:,:)*jme_cfm)),0)
delete(jme_cfm)
R4i = fin->R4
dim_R4 = dimsizes(R4i)
R4i_cfm = conform_dims((/dim_R4(0),dim_R4(1),nddd,nhr/),R4i,(/0,1/))
jme_cfm = conform_dims((/dim_R4(0),nddd,nhr/),jme,(/1,2/))
R4 = dim_sum_n((R4i_cfm(:,0,:,:)*cos(R4i_cfm(:,1,:,:)+R4i_cfm(:,2,:,:)*jme_cfm)),0)
delete(jme_cfm)
;print("R0 = "+R0)
;print("R1 = "+R1)
;print("R2 = "+R2)
;print("R3 = "+R3)
;print("R4 = "+R4)
R = ((R0+R1*jme+R2*jme^2+R3*jme^3+R4*jme^4)/(10^8))        ; in AU
;print("R = "+R)
;printVarSummary(R)
; local ,R0i,R1i,R2i,R3i,R4i,R0,R1,R2,R3,R4
; local ,dim_R0,R0i_cfm,jme_cfm,dim_R1,R1i_cfm,dim_R2,R2i_cfm,dim_R3,R3i_cfm,dim_R4,R4i_cfm

;- Theta (in degree): geocentric lon
Theta = L+180
Theta = Theta-toint(Theta/360)*360.       ; no larger than 360.
;- beta (in degree): geocentric lat
beta = -B
;print("Theta = "+Theta)
;print("beta = "+beta)
; local ,Theta,beta

;- d_psi and d_eps (in deg): nutation in lon and obliquity
X = new((/5,nddd,nhr/), double)      ; in degree
X(0,:,:) = jce^3/189474.0-0.0019142*jce^2+445267.11148*jce+297.85036
X(1,:,:) = -jce^3/300000.0-0.0001603*jce^2+35999.05034*jce+357.52772
X(2,:,:) = jce^3/56250.0+0.0086972*jce^2+477198.867398*jce+134.96298
X(3,:,:) = jce^3/327270.0-0.0036825*jce^2+483202.017538*jce+93.27191
X(4,:,:) = jce^3/450000.0+0.0020708*jce^2-1934.136261*jce+ 125.04452
coe = fin->coe
dim_coe = dimsizes(coe)
coe_cfm = conform_dims((/dim_coe(0),dim_coe(1),nddd,nhr/),coe,(/0,1/))
jce_cfm = conform_dims((/dim_coe(0),nddd,nhr/),jce,(/1,2/))
Y = fin->Y
dim_Y = dimsizes(Y)
X_cfm = conform_dims((/dim_Y(0),5,nddd,nhr/),X,(/1,2,3/))
Y_cfm = conform_dims((/dim_Y(0),5,nddd,nhr/),Y,(/0,1/))
d_psi = dim_sum_n((coe_cfm(:,0,:,:)+coe_cfm(:,1,:,:)*jce_cfm)*sin(dim_sum_n(X_cfm*Y_cfm,1)/180.*pi),0)/36000000.
d_eps = dim_sum_n((coe_cfm(:,2,:,:)+coe_cfm(:,3,:,:)*jce_cfm)*cos(dim_sum_n(X_cfm*Y_cfm,1)/180.*pi),0)/36000000.
delete(jce_cfm)
;print("d_psi = "+d_psi)
;print("d_eps = "+d_eps)
; local ,X,coe,Y,X_cfm,d_psi,d_eps
; local ,dim_coe,coe_cfm
; local ,jce_cfm,Y_cfm,dim_Y
;printVarSummary(d_psi)

;- eps (in deg): true obliquity of the ecliptic
u = jme/10.
eps_0 = 84381.448 + u*(-4680.93 + u*(-1.55 + u*(1999.25 + u*(-51.38 + u*(-249.67 + u*(  -39.05 + u*( 7.12 + u*(  27.87 + u*(  5.79 + u*2.45)))))))))
eps = eps_0/3600.+d_eps
;eps = 0.40908977151899578/pi*180.
;print("eps = "+eps/180.*pi)
;printVarSummary(eps)
; local ,u,eps_0,eps

;- d_tau (in deg): aberration correction
d_tau = -20.4898/(3600.*R)
;print("d_tau = "+d_tau)
;- lamda (in deg): apparent sun lon
lamda = Theta + d_psi+ d_tau
;lamda = 3.0365356746351990/pi*180.
;print("lamda = "+lamda/180.*pi)
; local ,d_tau,lamda

;- ds (in radians): geocentric sun declination
ds = asin(sin(beta/180.*pi)*cos(eps/180.*pi)+cos(beta/180.*pi)*sin(eps/180.*pi)*sin(lamda/180.*pi))
;ds = asin(sin(eps/180.*pi)*sin(lamda/180.*pi))
;print("ds = "+ds/pi*180.)
;printVarSummary(ds)

return ds
end
