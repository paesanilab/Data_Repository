program freq_relax_probe

  implicit none

  integer, parameter :: Ndim = 3

  integer, parameter :: Ngroup = 3

  !.......................................................

  character(20) :: atom

  integer :: Nmof, Nwat, Natom, Ntime, Nstep, Nskip, Ntmp, Nprint, Nlimit, Ncount, Nline
  integer, allocatable :: Nav(:)

  real(8) :: ssx, ssy, ssz, xss, yss, zss, det, tstep
  real(8) :: cell(9), rcell(9)
  real(8), allocatable :: time(:)
  real(8), allocatable :: dx(:)
  real(8), allocatable :: pos(:,:,:)

  !.......................................................

  !! Relaxation time
  real(8) :: cth_OH1, cth_OH2
  real(8) :: Pleg1, Pleg2, Pleg3
  real(8), allocatable :: relax_time1_OH(:), relax_time2_OH(:), relax_time3_OH(:)
  real(8), allocatable :: relax_time1_OH1(:), relax_time2_OH1(:), relax_time3_OH1(:)
  real(8), allocatable :: relax_time1_OH2(:), relax_time2_OH2(:), relax_time3_OH2(:)
  real(8), allocatable :: R_OH1(:,:,:), R_OH2(:,:,:)

  !.......................................................

  integer :: imof, idim, iatom, iwat, itime, itmp, iatm, igroup,iwat_in, iwat_fin
  integer :: itime1, itime2
  integer :: itmp1, itmp2

  real(8) :: err1, err2
  real(8) :: tmp, tmp1, tmp2

  !.......................................................

  namelist/input/Ntime,Nmof,Nwat,Natom,Nskip,Nprint,Nlimit,Nstep,tstep,iwat_in,iwat_fin

  !.......................................................

  open(unit=1,file='input_orientation')
  open(unit=11,file='POSITION_CMD')
  open(unit=1000,file='legendre1_tot.res')
  open(unit=1001,file='legendre1_OH1.res')
  open(unit=1002,file='legendre1_OH2.res')
  open(unit=2000,file='legendre2_tot.res')
  open(unit=2001,file='legendre2_OH1.res')
  open(unit=2002,file='legendre2_OH2.res')
  open(unit=3000,file='legendre3_tot.res')
  open(unit=3001,file='legendre3_OH1.res')
  open(unit=3002,file='legendre3_OH2.res')


  !.......................................................

  read(1,nml=input)

  Ntime = Ntime - 1
  Nprint = Nprint - 1

  !.......................................................

  allocate( dx(Ndim) )
  allocate( time(0:Ntime) )
  allocate( Nav(0:Ntime) )
  allocate( pos(Ndim,Natom,Nwat) )
  allocate( R_OH1(Ndim,Nwat,0:Ntime) )
  allocate( R_OH2(Ndim,Nwat,0:Ntime) )
  allocate( relax_time1_OH(0:Ntime) )
  allocate( relax_time2_OH(0:Ntime) )
  allocate( relax_time3_OH(0:Ntime) )
  allocate( relax_time1_OH1(0:Ntime) )
  allocate( relax_time2_OH1(0:Ntime) )
  allocate( relax_time3_OH1(0:Ntime) )
  allocate( relax_time1_OH2(0:Ntime) )
  allocate( relax_time2_OH2(0:Ntime) )
  allocate( relax_time3_OH2(0:Ntime) )

  !.......................................................

  !! Initialize correlation functions.
  relax_time1_OH1(:) = 0.d0
  relax_time2_OH1(:) = 0.d0
  relax_time3_OH1(:) = 0.d0

  !.......................................................

  !! Read trajectories.
   do itime = 0, Ntime
      time(itime) = tstep*dble(itime*Nstep)
      read(11,*)
      read(11,*) cell(1:3)
      read(11,*) cell(4:6)
      read(11,*) cell(7:9)
      call invert(cell,rcell,det)
      do imof = 1, Nmof
         read(11,*) atom, tmp, tmp, tmp
      end do
      do iwat  = 1, Nwat
         read(11,*) atom, pos(:,1,iwat)
         do iatom = 2, Natom
            read(11,*) atom, pos(:,iatom,iwat)
            dx(:) = pos(:,iatom,iwat) - pos(:,1,iwat)
            ssx = rcell(1)*dx(1) + rcell(4)*dx(2) + rcell(7)*dx(3)
            ssy = rcell(2)*dx(1) + rcell(5)*dx(2) + rcell(8)*dx(3)
            ssz = rcell(3)*dx(1) + rcell(6)*dx(2) + rcell(9)*dx(3)
            xss = ssx - nint(ssx)
            yss = ssy - nint(ssy)
            zss = ssz - nint(ssz)
            pos(1,iatom,iwat) = pos(1,1,iwat) + (cell(1)*xss + cell(4)*yss + cell(7)*zss)
            pos(2,iatom,iwat) = pos(2,1,iwat) + (cell(2)*xss + cell(5)*yss + cell(8)*zss)
            pos(3,iatom,iwat) = pos(3,1,iwat) + (cell(3)*xss + cell(6)*yss + cell(9)*zss)
        enddo
     enddo

     do iwat  = 1, Nwat
        do idim  = 1, Ndim
           R_OH1(idim,iwat,itime) = pos(idim,2,iwat) - pos(idim,1,iwat)
           R_OH2(idim,iwat,itime) = pos(idim,3,iwat) - pos(idim,1,iwat)
        enddo
     enddo
  enddo

  !.......................................................

  do itime1 = 0, Ntime, Nskip
     do itime2 = itime1, Ntime, Nskip
        itime = itime2 - itime1
        if (itime>Nlimit) cycle
        Nav(itime) = Nav(itime)+1
        Ncount = 0
        do iwat = iwat_in, iwat_fin
           Ncount = Ncount+1
           tmp1 = sqrt(sum(R_OH1(:,iwat,itime1)**2))
           tmp2 = sqrt(sum(R_OH1(:,iwat,itime2)**2))
           cth_OH1 = sum(R_OH1(:,iwat,itime2)*R_OH1(:,iwat,itime1))
           cth_OH1 = cth_OH1/tmp1/tmp2
           Pleg1 = cth_OH1
           Pleg2 = 0.5d0*(3.d0*cth_OH1**2-1.d0)
           Pleg3 = 0.5d0*(5.d0*cth_OH1**3-3.d0*cth_OH1)
           relax_time1_OH1(itime) = relax_time1_OH1(itime) + Pleg1
           relax_time2_OH1(itime) = relax_time2_OH1(itime) + Pleg2
           relax_time3_OH1(itime) = relax_time3_OH1(itime) + Pleg3

           tmp1 = sqrt(sum(R_OH2(:,iwat,itime1)**2))
           tmp2 = sqrt(sum(R_OH2(:,iwat,itime2)**2))
           cth_OH2 = sum(R_OH2(:,iwat,itime2)*R_OH2(:,iwat,itime1))
           cth_OH2 = cth_OH2/tmp1/tmp2
           Pleg1 = cth_OH2
           Pleg2 = 0.5d0*(3.d0*cth_OH2**2-1.d0)
           Pleg3 = 0.5d0*(5.d0*cth_OH2**3-3.d0*cth_OH2)
           relax_time1_OH2(itime) = relax_time1_OH2(itime)+Pleg1
           relax_time2_OH2(itime) = relax_time2_OH2(itime)+Pleg2
           relax_time3_OH2(itime) = relax_time3_OH2(itime)+Pleg3
        enddo

     enddo
  enddo

  do itime = 0, Nprint, Nskip

     relax_time1_OH1(itime) = relax_time1_OH1(itime)/dble(Nav(itime))/dble(Ncount)
     relax_time2_OH1(itime) = relax_time2_OH1(itime)/dble(Nav(itime))/dble(Ncount)
     relax_time3_OH1(itime) = relax_time3_OH1(itime)/dble(Nav(itime))/dble(Ncount)

     relax_time1_OH2(itime) = relax_time1_OH2(itime)/dble(Nav(itime))/dble(Ncount)
     relax_time2_OH2(itime) = relax_time2_OH2(itime)/dble(Nav(itime))/dble(Ncount)
     relax_time3_OH2(itime) = relax_time3_OH2(itime)/dble(Nav(itime))/dble(Ncount)

     relax_time1_OH(itime) = relax_time1_OH1(itime)+relax_time1_OH2(itime)
     relax_time2_OH(itime) = relax_time2_OH1(itime)+relax_time2_OH2(itime)
     relax_time3_OH(itime) = relax_time3_OH1(itime)+relax_time3_OH2(itime)

     relax_time1_OH(itime) = 0.5d0*relax_time1_OH(itime)
     relax_time2_OH(itime) = 0.5d0*relax_time2_OH(itime)
     relax_time3_OH(itime) = 0.5d0*relax_time3_OH(itime)

     write(1000,*) time(itime), relax_time1_OH(itime)
     write(2000,*) time(itime), relax_time2_OH(itime)
     write(3000,*) time(itime), relax_time3_OH(itime)

     write(1001,*) time(itime), relax_time1_OH1(itime)
     write(2001,*) time(itime), relax_time2_OH1(itime)
     write(3001,*) time(itime), relax_time3_OH1(itime)

     write(1002,*) time(itime), relax_time1_OH2(itime)
     write(2002,*) time(itime), relax_time2_OH2(itime)
     write(3002,*) time(itime), relax_time3_OH2(itime)

  enddo

end program

!=======================================================================
subroutine invert(a,b,d)

   implicit none

   real(8) a(9),b(9),d,r

   !! calculate adjoint matrix
   b(1)=a(5)*a(9)-a(6)*a(8)
   b(2)=a(3)*a(8)-a(2)*a(9)
   b(3)=a(2)*a(6)-a(3)*a(5)
   b(4)=a(6)*a(7)-a(4)*a(9)
   b(5)=a(1)*a(9)-a(3)*a(7)
   b(6)=a(3)*a(4)-a(1)*a(6)
   b(7)=a(4)*a(8)-a(5)*a(7)
   b(8)=a(2)*a(7)-a(1)*a(8)
   b(9)=a(1)*a(5)-a(2)*a(4)

   !! calculate determinant
   d=a(1)*b(1)+a(4)*b(2)+a(7)*b(3)
   r=0.d0
   if(abs(d).gt.0.d0)r=1.d0/d

   !! complete inverse matrix
   b(1)=r*b(1)
   b(2)=r*b(2)
   b(3)=r*b(3)
   b(4)=r*b(4)
   b(5)=r*b(5)
   b(6)=r*b(6)
   b(7)=r*b(7)
   b(8)=r*b(8)
   b(9)=r*b(9)

end

!=======================================================================

