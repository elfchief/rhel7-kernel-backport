%global __spec_install_pre %{___build_pre}

# Define the version of the Linux Kernel Archive tarball.
%define RHKver 3.10.0
%define RHKrel 229.14.1

# Build release, and kernel release
%define krelease %{RHKrel}.el7
%define brelease %{RHKrel}.el6

# The following build options are enabled by default.
# Use either --without <option> on your rpmbuild command line
# or force the values to 0, here, to disable them.

# kernel
%define with_std          %{?_without_std:          0} %{?!_without_std:          1}
# kernel-doc
%define with_doc          %{?_without_doc:          0} %{?!_without_doc:          1}
# kernel-headers
%define with_headers      %{?_without_headers:      0} %{?!_without_headers:      1}
# kernel-firmware
%define with_firmware     %{?_without_firmware:     0} %{?!_without_firmware:     1}
# vdso directories installed
%define with_vdso_install %{?_without_vdso_install: 0} %{?!_without_vdso_install: 1}
# use dracut instead of mkinitrd
%define with_dracut       %{?_without_dracut:       0} %{?!_without_dracut:       1}

# Build only the kernel-doc & kernel-firmware packages.
%ifarch noarch
%define with_std 0
%define with_headers 0
%define with_vdso_install 0
%endif

# Build only the 64-bit kernel-headers & kernel packages.
%ifarch x86_64
%define with_doc 1
%define with_firmware 1
%endif

# Define the correct buildarch.
%define buildarch x86_64

# Define the vdso_arches.
%if %{with_vdso_install}
%define vdso_arches x86_64
%endif

#
# Three sets of minimum package version requirements in the form of Conflicts.
#

#
# First the general kernel required versions, as per Documentation/Changes.
#
%define kernel_dot_org_conflicts  ppp < 2.4.3-3, isdn4k-utils < 3.2-32, nfs-utils < 1.0.7-12, e2fsprogs < 1.37-4, util-linux < 2.12, jfsutils < 1.1.7-2, reiserfs-utils < 3.6.19-2, xfsprogs < 2.6.13-4, procps < 3.2.5-6.3, oprofile < 0.9.1-2

#
# Then a series of requirements that are distribution specific, either because
# the older versions have problems with the newer kernel or lack certain things
# that make integration in the distro harder than needed.
#
%define package_conflicts initscripts < 7.23, udev < 145-11, iptables < 1.3.2-1, ipw2200-firmware < 2.4, iwl4965-firmware < 228.57.2, selinux-policy-targeted < 1.25.3-14, squashfs-tools < 4.0, wireless-tools < 29-3

#
# These are firmware packages that have gotten rolled into the 
# kernel-firmware/linux-firmware packages
%define firmware_conflicts bfa-firmware, ql2100-firmware, ql2200-firmware, ql23xx-firmware, ql2400-firmware, ql2500-firmware, rt61pci-firmware, rt73usb-firmware, xorg-x11-drv-ati-firmware

#
# We moved the drm include files into kernel-headers, make sure there's
# a recent enough libdrm-devel on the system that doesn't have those.
#
%define kernel_headers_conflicts libdrm-devel < 2.4.0-0.15

#
# Packages that need to be installed before the kernel because the %post scripts make use of them.
#
%define kernel_prereq fileutils, module-init-tools, initscripts >= 8.11.1-1, grubby >= 7.0.4-1
%if %{with_dracut}
%define initrd_prereq dracut-kernel >= 002-18.git413bcf78
%else
%define initrd_prereq mkinitrd >= 6.0.61-1
%endif

Name: kernel-bp
Summary: The Linux kernel. (The core of any Linux-based operating system.)
Group: System Environment/Kernel
License: GPLv2
URL: http://www.kernel.org/
Version: %{RHKver}
Release: %{brelease}
ExclusiveArch: noarch x86_64
ExclusiveOS: Linux
Provides: kernel = %{version}-%{release}
Provides: kernel-%{_target_cpu} = %{version}-%{release}
Provides: kernel-drm = 4.3.0
Provides: kernel-drm-nouveau = 16
Provides: kernel-modeset = 1
Provides: kernel-uname-r = %{version}-%{release}.%{_target_cpu}
Provides: kernel-bp = %{version}-%{release}
Provides: kernel-bp-%{_target_cpu} = %{version}-%{release}
Provides: kernel-bp-drm = 4.3.0
Provides: kernel-bp-drm-nouveau = 16
Provides: kernel-bp-modeset = 1
Provides: kernel-bp-uname-r = %{version}-%{release}.%{_target_cpu}
Requires(pre): %{kernel_prereq}
Requires(pre): %{initrd_prereq}
Requires(post): /sbin/new-kernel-pkg
Requires(preun): /sbin/new-kernel-pkg
Conflicts: %{kernel_dot_org_conflicts}
Conflicts: %{package_conflicts}
Conflicts: %{kernel_headers_conflicts}
# We can't let RPM do the dependencies automatically because it'll then pick up
# a correct but undesirable perl dependency from the module headers which
# isn't required for the kernel proper to function.
AutoReq: no
AutoProv: yes

# Sources.
Source0: kernel-%{RHKver}-%{RHKrel}.el7.x86_64.rpm
#Source1: kernel-abi-whitelists-%{RHKver}-%{RHKrel}.el7.noarch.rpm
Source2: kernel-devel-%{RHKver}-%{RHKrel}.el7.x86_64.rpm
Source3: kernel-doc-%{RHKver}-%{RHKrel}.el7.noarch.rpm
Source4: kernel-headers-%{RHKver}-%{RHKrel}.el7.x86_64.rpm
Source5: linux-firmware-20140911-0.1.git365e80c.el7.noarch.rpm

# Do not package the source RPMs.
NoSource: 0

%description
This package provides the Linux kernel (vmlinuz), the core of any
Linux-based operating system. The kernel handles the basic functions
of the OS: memory allocation, process allocation, device I/O, etc.

%package devel
Summary: Development package for building kernel modules to match the kernel.
Group: System Environment/Kernel
Provides: kernel-devel-%{_target_cpu} = %{version}-%{release}
Provides: kernel-devel = %{version}-%{release}
Provides: kernel-devel-uname-r = %{version}-%{release}.%{_target_cpu}
Provides: kernel-bp-devel-%{_target_cpu} = %{version}-%{release}
Provides: kernel-bp-devel = %{version}-%{release}
Provides: kernel-bp-devel-uname-r = %{version}-%{release}.%{_target_cpu}
Requires(pre): /usr/bin/find
AutoReqProv: no
%description devel
This package provides the kernel header files and makefiles
sufficient to build modules against the kernel package.

%if %{with_doc}
%package doc
Summary: Various bits of documentation found in the kernel sources.
Group: Documentation
Provides: kernel-doc = %{version}-%{release}
Conflicts: kernel-doc < %{version}-%{release}
BuildArch: noarch
%description doc
This package provides documentation files from the kernel sources.
Various bits of information about the Linux kernel and the device
drivers shipped with it are documented in these files.

You'll want to install this package if you need a reference to the
options that can be passed to the kernel modules at load time.
%endif

%if %{with_headers}
%package headers
Summary: Header files for the Linux kernel for use by glibc
Group: Development/System
Obsoletes: glibc-kernheaders
Provides: glibc-kernheaders = 3.0-46
Provides: kernel-headers = %{version}-%{release}
Conflicts: kernel-headers < %{version}-%{release}
Obsoletes: kernel-headers < %{version}-%{release}
%description headers
This package provides the C header files that specify the interface
between the Linux kernel and userspace libraries & programs. The
header files define structures and constants that are needed when
building most standard programs. They are also required when
rebuilding the glibc package.
%endif

%if %{with_firmware}
%package firmware
Summary: Firmware files used by the Linux kernel
Group: Development/System
License: GPL+ and GPLv2+ and MIT and Redistributable, no modification permitted
Provides: kernel-firmware = %{version}-%{release}
Conflicts: kernel-firmware < %{version}-%{release}
Obsoletes: kernel-firmware < %{version}-%{release}
Conflicts: %{firmware_conflicts}
Obsoletes: %{firmware_conflicts}
BuildArch: noarch
%description firmware
This package provides the firmware files required for some devices to operate.
%endif

# Disable the building of the debug package(s).
%define debug_package %{nil}

%prep

%build

%install
%{__rm} -rf %{buildroot}
%{__mkdir} -p %{buildroot}
cd %{buildroot}

rpm2cpio %{SOURCE0} | cpio -idm
#rpm2cpio %{SOURCE1} | cpio -idm
rpm2cpio %{SOURCE2} | cpio -idm
rpm2cpio %{SOURCE3} | cpio -idm
rpm2cpio %{SOURCE4} | cpio -idm
rpm2cpio %{SOURCE5} | cpio -idm

# Set up template (emtpy) initial ramdisk
%if %{with_dracut}
    # We estimate the size of the initramfs because rpm needs to take this size
    # into consideration when performing disk space calculations.
    dd if=/dev/zero of=boot/initramfs-%{version}-%{krelease}.%{_target_cpu}.img bs=1M count=20
%else
    dd if=/dev/zero of=initrd-%{version}-%{krelease}.%{_target_cpu}.img bs=1M count=5
%endif

# Put firmware in the right place for EL6
%{__mv} usr/lib/firmware lib/firmware
%{__mv} usr/share/doc/linux-firmware-20140911 usr/share/doc/kernel-firmware-%{version}

# And make the docs dir match our package name
%{__mv} usr/share/doc/kernel-doc-%{version} usr/share/doc/%{name}-doc-%{version}

# These symlinks are for humans more than anything technical, but will help
# if someone is trying to access kernel stuff based on the package name
# rather than what 'uname' says.
ln -s %{version}-%{krelease}.%{_target_cpu} usr/src/kernels/%{version}-%{brelease}.%{_target_cpu}
ln -s %{version}-%{krelease}.%{_target_cpu} lib/modules/%{version}-%{brelease}.%{_target_cpu}

ln -s vmlinuz-%{version}-%{krelease}.%{_target_cpu} boot/vmlinuz-%{version}-%{brelease}.%{_target_cpu}
ln -s System.map-%{version}-%{krelease}.%{_target_cpu} boot/System.map-%{version}-%{brelease}.%{_target_cpu}
ln -s symvers-%{version}-%{krelease}.%{_target_cpu}.gz boot/symvers-%{version}-%{brelease}.%{_target_cpu}.gz
ln -s config-%{version}-%{krelease}.%{_target_cpu} boot/config-%{version}-%{brelease}.%{_target_cpu}


%clean
%{__rm} -rf $RPM_BUILD_ROOT

# Scripts section.
%if %{with_std}
%posttrans
NEWKERNARGS=""
(/sbin/grubby --info=`/sbin/grubby --default-kernel`) 2> /dev/null | grep -q crashkernel
if [ $? -ne 0 ]; then
        NEWKERNARGS="--kernel-args=\"crashkernel=auto\""
fi
%if %{with_dracut}
/sbin/new-kernel-pkg --package kernel --mkinitrd --dracut --depmod --update %{version}-%{krelease}.%{_target_cpu} $NEWKERNARGS || exit $?
%else
/sbin/new-kernel-pkg --package kernel --mkinitrd --depmod --update %{version}-%{krelease}.%{_target_cpu} $NEWKERNARGS || exit $?
%endif
/sbin/new-kernel-pkg --package kernel --rpmposttrans %{version}-%{krelease}.%{_target_cpu} || exit $?
if [ -x /sbin/weak-modules ]; then
    /sbin/weak-modules --add-kernel %{version}-%{krelease}.%{_target_cpu} || exit $?
fi

%post
if [ `uname -i` == "i386" ] && [ -f /etc/sysconfig/kernel ]; then
    /bin/sed -r -i -e 's/^DEFAULTKERNEL=kernel-NONPAE$/DEFAULTKERNEL=kernel/' /etc/sysconfig/kernel || exit $?
fi
if grep --silent '^hwcap 0 nosegneg$' /etc/ld.so.conf.d/kernel-*.conf 2> /dev/null; then
    /bin/sed -i '/^hwcap 0 nosegneg$/ s/0/1/' /etc/ld.so.conf.d/kernel-*.conf
fi
/sbin/new-kernel-pkg --package kernel --install %{version}-%{krelease}.%{_target_cpu} || exit $?

%preun
/sbin/new-kernel-pkg --rminitrd --rmmoddep --remove %{version}-%{krelease}.%{_target_cpu} || exit $?
if [ -x /sbin/weak-modules ]; then
    /sbin/weak-modules --remove-kernel %{version}-%{krelease}.%{_target_cpu} || exit $?
fi

%post devel
if [ -f /etc/sysconfig/kernel ]; then
    . /etc/sysconfig/kernel || exit $?
fi
if [ "$HARDLINK" != "no" -a -x /usr/sbin/hardlink ]; then
    pushd /usr/src/kernels/%{version}-%{krelease}.%{_target_cpu} > /dev/null
    /usr/bin/find . -type f | while read f; do
        hardlink -c /usr/src/kernels/*.fc*.*/$f $f
    done
    popd > /dev/null
fi
%endif

# Files section.
%if %{with_std}
%files
%defattr(-,root,root)
/boot/vmlinuz-%{version}-%{krelease}.%{_target_cpu}
/boot/.vmlinuz-%{version}-%{krelease}.%{_target_cpu}.hmac
/boot/System.map-%{version}-%{krelease}.%{_target_cpu}
/boot/symvers-%{version}-%{krelease}.%{_target_cpu}.gz
/boot/config-%{version}-%{krelease}.%{_target_cpu}

# symlinks for files
/boot/vmlinuz-%{version}-%{brelease}.%{_target_cpu}
/boot/System.map-%{version}-%{brelease}.%{_target_cpu}
/boot/symvers-%{version}-%{brelease}.%{_target_cpu}.gz
/boot/config-%{version}-%{brelease}.%{_target_cpu}

%dir /lib/modules/%{version}-%{krelease}.%{_target_cpu}
/lib/modules/%{version}-%{krelease}.%{_target_cpu}/kernel
/lib/modules/%{version}-%{krelease}.%{_target_cpu}/extra
/lib/modules/%{version}-%{krelease}.%{_target_cpu}/build
/lib/modules/%{version}-%{krelease}.%{_target_cpu}/source
/lib/modules/%{version}-%{krelease}.%{_target_cpu}/updates
/lib/modules/%{version}-%{krelease}.%{_target_cpu}/weak-updates
%ifarch %{vdso_arches}
/lib/modules/%{version}-%{krelease}.%{_target_cpu}/vdso
/etc/ld.so.conf.d/kernel-%{version}-%{krelease}.%{_target_cpu}.conf
%endif
/lib/modules/%{version}-%{krelease}.%{_target_cpu}/modules.*

# symlink for modules directory
/lib/modules/%{version}-%{brelease}.%{_target_cpu}

%if %{with_dracut}
%ghost /boot/initramfs-%{version}-%{krelease}.%{_target_cpu}.img
%else
%ghost /boot/initrd-%{version}-%{krelease}.%{_target_cpu}.img
%endif

%files devel
%defattr(-,root,root)
%dir /usr/src/kernels
/usr/src/kernels/%{version}-%{krelease}.%{_target_cpu}
/usr/src/kernels/%{version}-%{brelease}.%{_target_cpu}
%endif

%if %{with_doc}
%files doc
%defattr(-,root,root)
%{_datadir}/doc/%{name}-doc-%{version}/Documentation/*
%dir %{_datadir}/doc/%{name}-doc-%{version}/Documentation
%dir %{_datadir}/doc/%{name}-doc-%{version}
%{_datadir}/doc/kernel-keys/%{version}-%{krelease}/*
%dir %{_datadir}/doc/kernel-keys/%{version}-%{krelease}
%{_datadir}/man/man9/*
%endif

%if %{with_headers}
%files headers
%defattr(-,root,root)
/usr/include/*
%endif

%if %{with_firmware}
%files firmware
%defattr(-,root,root)
/lib/firmware/*
%doc %{_datadir}/doc/kernel-firmware-%{version}/*
%endif

%changelog
* Thu Oct 01 2015 Alan Bartlett <ajb@elrepo.org> - 3.10.90-1
- Updated with the 3.10.90 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.90]

* Mon Sep 21 2015 Alan Bartlett <ajb@elrepo.org> - 3.10.89-1
- Updated with the 3.10.89 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.89]

* Mon Sep 14 2015 Alan Bartlett <ajb@elrepo.org> - 3.10.88-1
- Updated with the 3.10.88 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.88]

* Mon Aug 17 2015 Alan Bartlett <ajb@elrepo.org> - 3.10.87-1
- Updated with the 3.10.87 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.87]

* Tue Aug 11 2015 Alan Bartlett <ajb@elrepo.org> - 3.10.86-1
- Updated with the 3.10.86 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.86]

* Tue Aug 04 2015 Alan Bartlett <ajb@elrepo.org> - 3.10.85-1
- Updated with the 3.10.85 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.85]

* Sat Jul 11 2015 Alan Bartlett <ajb@elrepo.org> - 3.10.84-1
- Updated with the 3.10.84 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.84]

* Sat Jul 04 2015 Alan Bartlett <ajb@elrepo.org> - 3.10.83-1
- Updated with the 3.10.83 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.83]

* Mon Jun 29 2015 Alan Bartlett <ajb@elrepo.org> - 3.10.82-1
- Updated with the 3.10.82 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.82]

* Tue Jun 23 2015 Alan Bartlett <ajb@elrepo.org> - 3.10.81-1
- Updated with the 3.10.81 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.81]

* Sun Jun 07 2015 Alan Bartlett <ajb@elrepo.org> - 3.10.80-1
- Updated with the 3.10.80 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.80]

* Mon May 18 2015 Alan Bartlett <ajb@elrepo.org> - 3.10.79-1
- Updated with the 3.10.79 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.79]

* Wed May 13 2015 Alan Bartlett <ajb@elrepo.org> - 3.10.78-1
- Updated with the 3.10.78 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.78]

* Thu May 07 2015 Alan Bartlett <ajb@elrepo.org> - 3.10.77-1
- Updated with the 3.10.77 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.77]
- CONFIG_SUNRPC_DEBUG=y [Jamie Bainbridge]

* Wed Apr 29 2015 Alan Bartlett <ajb@elrepo.org> - 3.10.76-1
- Updated with the 3.10.76 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.76]

* Sun Apr 19 2015 Alan Bartlett <ajb@elrepo.org> - 3.10.75-1
- Updated with the 3.10.75 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.75]

* Mon Apr 13 2015 Alan Bartlett <ajb@elrepo.org> - 3.10.74-1
- Updated with the 3.10.74 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.74]

* Thu Mar 26 2015 Alan Bartlett <ajb@elrepo.org> - 3.10.73-1
- Updated with the 3.10.73 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.73]

* Wed Mar 18 2015 Alan Bartlett <ajb@elrepo.org> - 3.10.72-1
- Updated with the 3.10.72 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.72]

* Sat Mar 07 2015 Alan Bartlett <ajb@elrepo.org> - 3.10.71-1
- Updated with the 3.10.71 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.71]

* Fri Feb 27 2015 Alan Bartlett <ajb@elrepo.org> - 3.10.70-1
- Updated with the 3.10.70 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.70]

* Wed Feb 11 2015 Alan Bartlett <ajb@elrepo.org> - 3.10.69-1
- Updated with the 3.10.69 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.69]

* Fri Feb 06 2015 Alan Bartlett <ajb@elrepo.org> - 3.10.68-1
- Updated with the 3.10.68 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.68]

* Fri Jan 30 2015 Alan Bartlett <ajb@elrepo.org> - 3.10.67-1
- Updated with the 3.10.67 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.67]

* Wed Jan 28 2015 Alan Bartlett <ajb@elrepo.org> - 3.10.66-1
- Updated with the 3.10.66 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.66]

* Sat Jan 17 2015 Alan Bartlett <ajb@elrepo.org> - 3.10.65-1
- Updated with the 3.10.65 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.65]

* Fri Jan 09 2015 Alan Bartlett <ajb@elrepo.org> - 3.10.64-1
- Updated with the 3.10.64 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.64]

* Tue Dec 16 2014 Alan Bartlett <ajb@elrepo.org> - 3.10.63-1
- Updated with the 3.10.63 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.63]

* Sun Dec 07 2014 Alan Bartlett <ajb@elrepo.org> - 3.10.62-1
- Updated with the 3.10.62 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.62]

* Sat Nov 22 2014 Alan Bartlett <ajb@elrepo.org> - 3.10.61-1
- Updated with the 3.10.61 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.61]

* Sat Nov 15 2014 Alan Bartlett <ajb@elrepo.org> - 3.10.60-1
- Updated with the 3.10.60 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.60]

* Fri Oct 31 2014 Alan Bartlett <ajb@elrepo.org> - 3.10.59-1
- Updated with the 3.10.59 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.59]

* Wed Oct 15 2014 Alan Bartlett <ajb@elrepo.org> - 3.10.58-1
- Updated with the 3.10.58 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.58]

* Fri Oct 10 2014 Alan Bartlett <ajb@elrepo.org> - 3.10.57-1
- Updated with the 3.10.57 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.57]

* Mon Oct 06 2014 Alan Bartlett <ajb@elrepo.org> - 3.10.56-1
- Updated with the 3.10.56 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.56]
- CONFIG_NUMA_BALANCING=y and CONFIG_NUMA_BALANCING_DEFAULT_ENABLED=y
- [http://elrepo.org/bugs/view.php?id=509]
- CONFIG_9P_FS=m, CONFIG_9P_FSCACHE=y and CONFIG_9P_FS_POSIX_ACL=y
- [http://elrepo.org/bugs/view.php?id=510]

* Thu Sep 18 2014 Alan Bartlett <ajb@elrepo.org> - 3.10.55-1
- Updated with the 3.10.55 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.55]

* Sat Sep 06 2014 Alan Bartlett <ajb@elrepo.org> - 3.10.54-1
- Updated with the 3.10.54 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.54]
- CONFIG_RCU_NOCB_CPU=y and CONFIG_RCU_NOCB_CPU_ALL=y
- [http://elrepo.org/bugs/view.php?id=505]

* Thu Aug 14 2014 Alan Bartlett <ajb@elrepo.org> - 3.10.53-1
- Updated with the 3.10.53 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.53]

* Fri Aug 08 2014 Alan Bartlett <ajb@elrepo.org> - 3.10.52-1
- Updated with the 3.10.52 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.52]
- CONFIG_ATH9K_DEBUGFS=y, CONFIG_ATH9K_MAC_DEBUG=y and
- CONFIG_ATH9K_HTC_DEBUGFS=y [http://elrepo.org/bugs/view.php?id=501]

* Fri Aug 01 2014 Alan Bartlett <ajb@elrepo.org> - 3.10.51-1
- Updated with the 3.10.51 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.51]

* Mon Jul 28 2014 Alan Bartlett <ajb@elrepo.org> - 3.10.50-1
- Updated with the 3.10.50 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.50]
- CONFIG_INTEL_MEI=m and CONFIG_INTEL_MEI_ME=m
- [http://elrepo.org/bugs/view.php?id=493]

* Fri Jul 18 2014 Alan Bartlett <ajb@elrepo.org> - 3.10.49-1
- Updated with the 3.10.49 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.49]

* Thu Jul 10 2014 Alan Bartlett <ajb@elrepo.org> - 3.10.48-1
- Updated with the 3.10.48 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.48]

* Mon Jul 07 2014 Alan Bartlett <ajb@elrepo.org> - 3.10.47-1
- Updated with the 3.10.47 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.47]

* Tue Jul 01 2014 Alan Bartlett <ajb@elrepo.org> - 3.10.46-1
- Updated with the 3.10.46 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.46]

* Fri Jun 27 2014 Alan Bartlett <ajb@elrepo.org> - 3.10.45-1
- Updated with the 3.10.45 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.45]

* Tue Jun 17 2014 Alan Bartlett <ajb@elrepo.org> - 3.10.44-1
- Updated with the 3.10.44 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.44]

* Thu Jun 12 2014 Alan Bartlett <ajb@elrepo.org> - 3.10.43-1
- Updated with the 3.10.43 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.43]

* Sun Jun 08 2014 Alan Bartlett <ajb@elrepo.org> - 3.10.42-1
- Updated with the 3.10.42 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.42]

* Sun Jun 01 2014 Alan Bartlett <ajb@elrepo.org> - 3.10.41-1
- Updated with the 3.10.41 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.41]

* Tue May 13 2014 Alan Bartlett <ajb@elrepo.org> - 3.10.40-1
- Updated with the 3.10.40 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.40]

* Tue May 06 2014 Alan Bartlett <ajb@elrepo.org> - 3.10.39-1
- Updated with the 3.10.39 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.39]

* Sun Apr 27 2014 Alan Bartlett <ajb@elrepo.org> - 3.10.38-1
- Updated with the 3.10.38 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.38]
- CONFIG_FANOTIFY=y [http://elrepo.org/bugs/view.php?id=470]

* Mon Apr 14 2014 Alan Bartlett <ajb@elrepo.org> - 3.10.37-1
- Updated with the 3.10.37 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.37]

* Fri Apr 04 2014 Alan Bartlett <ajb@elrepo.org> - 3.10.36-1
- Updated with the 3.10.36 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.36]

* Mon Mar 31 2014 Alan Bartlett <ajb@elrepo.org> - 3.10.35-1
- Updated with the 3.10.35 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.35]

* Mon Mar 24 2014 Alan Bartlett <ajb@elrepo.org> - 3.10.34-1
- Updated with the 3.10.34 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.34]

* Fri Mar 07 2014 Alan Bartlett <ajb@elrepo.org> - 3.10.33-1
- Updated with the 3.10.33 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.33]
- CONFIG_CIFS_SMB2=y [http://elrepo.org/bugs/view.php?id=461]

* Sun Feb 23 2014 Alan Bartlett <ajb@elrepo.org> - 3.10.32-1
- Updated with the 3.10.32 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.32]

* Fri Feb 21 2014 Alan Bartlett <ajb@elrepo.org> - 3.10.31-1
- Updated with the 3.10.31 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.31]
- CONFIG_ACPI_HOTPLUG_MEMORY=y [http://elrepo.org/bugs/view.php?id=454]

* Fri Feb 14 2014 Alan Bartlett <ajb@elrepo.org> - 3.10.30-1
- Updated with the 3.10.30 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.30]

* Fri Feb 07 2014 Alan Bartlett <ajb@elrepo.org> - 3.10.29-1
- Updated with the 3.10.29 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.29]

* Sun Jan 26 2014 Alan Bartlett <ajb@elrepo.org> - 3.10.28-1
- Updated with the 3.10.28 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.28]

* Thu Jan 16 2014 Alan Bartlett <ajb@elrepo.org> - 3.10.27-1
- Updated with the 3.10.27 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.27]

* Fri Jan 10 2014 Alan Bartlett <ajb@elrepo.org> - 3.10.26-1
- Updated with the 3.10.26 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.26]
- CONFIG_L2TP=m, CONFIG_PPPOL2TP=m [http://elrepo.org/bugs/view.php?id=443]

* Fri Dec 20 2013 Alan Bartlett <ajb@elrepo.org> - 3.10.25-1
- Updated with the 3.10.25 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.25]

* Thu Dec 12 2013 Alan Bartlett <ajb@elrepo.org> - 3.10.24-1
- Updated with the 3.10.24 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.24]

* Mon Dec 09 2013 Alan Bartlett <ajb@elrepo.org> - 3.10.23-1
- Updated with the 3.10.23 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.23]

* Thu Dec 05 2013 Alan Bartlett <ajb@elrepo.org> - 3.10.22-1
- Updated with the 3.10.22 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.22]

* Sat Nov 30 2013 Alan Bartlett <ajb@elrepo.org> - 3.10.21-1
- Updated with the 3.10.21 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.21]

* Thu Nov 21 2013 Alan Bartlett <ajb@elrepo.org> - 3.10.20-1
- Updated with the 3.10.20 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.20]
- CONFIG_HFS_FS=m and CONFIG_HFSPLUS_FS=m [http://elrepo.org/bugs/view.php?id=427]

* Wed Nov 13 2013 Alan Bartlett <ajb@elrepo.org> - 3.10.19-1
- Updated with the 3.10.19 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.19]

* Mon Nov 04 2013 Alan Bartlett <ajb@elrepo.org> - 3.10.18-1
- Updated with the 3.10.18 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.18]

* Fri Oct 18 2013 Alan Bartlett <ajb@elrepo.org> - 3.10.17-1
- Updated with the 3.10.17 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.17]

* Mon Oct 14 2013 Alan Bartlett <ajb@elrepo.org> - 3.10.16-1
- Updated with the 3.10.16 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.16]

* Sat Oct 05 2013 Alan Bartlett <ajb@elrepo.org> - 3.10.15-1
- Updated with the 3.10.15 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.15]

* Wed Oct 02 2013 Alan Bartlett <ajb@elrepo.org> - 3.10.14-1
- Updated with the 3.10.14 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.14]

* Fri Sep 27 2013 Alan Bartlett <ajb@elrepo.org> - 3.10.13-1
- Updated with the 3.10.13 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.13]

* Mon Sep 16 2013 Alan Bartlett <ajb@elrepo.org> - 3.10.12-1
- Updated with the 3.10.12 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.12]
- CONFIG_BCACHE=m [http://elrepo.org/bugs/view.php?id=407]

* Sun Sep 08 2013 Alan Bartlett <ajb@elrepo.org> - 3.10.11-1
- Updated with the 3.10.11 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.11]

* Thu Aug 29 2013 Alan Bartlett <ajb@elrepo.org> - 3.10.10-1
- Updated with the 3.10.10 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.10]

* Wed Aug 21 2013 Alan Bartlett <ajb@elrepo.org> - 3.10.9-1
- Updated with the 3.10.9 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.9]

* Tue Aug 20 2013 Alan Bartlett <ajb@elrepo.org> - 3.10.8-1
- Updated with the 3.10.8 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.8]

* Thu Aug 15 2013 Alan Bartlett <ajb@elrepo.org> - 3.10.7-1
- Updated with the 3.10.7 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.7]

* Mon Aug 12 2013 Alan Bartlett <ajb@elrepo.org> - 3.10.6-1
- Updated with the 3.10.6 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.6]

* Sun Aug 04 2013 Alan Bartlett <ajb@elrepo.org> - 3.10.5-1
- Updated with the 3.10.5 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.5]

* Mon Jul 29 2013 Alan Bartlett <ajb@elrepo.org> - 3.10.4-1
- Updated with the 3.10.4 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.4]

* Fri Jul 26 2013 Alan Bartlett <ajb@elrepo.org> - 3.10.3-1
- Updated with the 3.10.3 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.3]

* Mon Jul 22 2013 Alan Bartlett <ajb@elrepo.org> - 3.10.2-1
- Updated with the 3.10.2 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.2]

* Sun Jul 14 2013 Alan Bartlett <ajb@elrepo.org> - 3.10.1-1
- Updated with the 3.10.1 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.10.1]

* Mon Jul 01 2013 Alan Bartlett <ajb@elrepo.org> - 3.10.0-1
- Updated with the 3.10 source tarball.

* Thu Jun 27 2013 Alan Bartlett <ajb@elrepo.org> - 3.9.8-1
- Updated with the 3.9.8 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.9.8]

* Fri Jun 21 2013 Alan Bartlett <ajb@elrepo.org> - 3.9.7-1
- Updated with the 3.9.7 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.9.7]

* Thu Jun 13 2013 Alan Bartlett <ajb@elrepo.org> - 3.9.6-1
- Updated with the 3.9.6 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.9.6]

* Sat Jun 08 2013 Alan Bartlett <ajb@elrepo.org> - 3.9.5-1
- Updated with the 3.9.5 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.9.5]

* Fri May 24 2013 Alan Bartlett <ajb@elrepo.org> - 3.9.4-1
- Updated with the 3.9.4 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.9.4]

* Mon May 20 2013 Alan Bartlett <ajb@elrepo.org> - 3.9.3-1
- Updated with the 3.9.3 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.9.3]

* Sun May 12 2013 Alan Bartlett <ajb@elrepo.org> - 3.9.2-1
- Updated with the 3.9.2 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.9.2]

* Wed May 08 2013 Alan Bartlett <ajb@elrepo.org> - 3.9.1-1
- Updated with the 3.9.1 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.9.1]

* Mon Apr 29 2013 Alan Bartlett <ajb@elrepo.org> - 3.9.0-1
- Updated with the 3.9 source tarball.
- Added a BR for the bc package.

* Sat Apr 27 2013 Alan Bartlett <ajb@elrepo.org> - 3.8.10-1
- Updated with the 3.8.10 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.8.10]

* Fri Apr 26 2013 Alan Bartlett <ajb@elrepo.org> - 3.8.9-1
- Updated with the 3.8.9 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.8.9]
- CONFIG_NUMA=y for 32-bit.

* Wed Apr 17 2013 Alan Bartlett <ajb@elrepo.org> - 3.8.8-1
- Updated with the 3.8.8 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.8.8]
- CONFIG_NUMA disabled for 32-bit.
- CONFIG_REGULATOR_DUMMY disabled. [https://bugzilla.kernel.org/show_bug.cgi?id=50711]

* Sat Apr 13 2013 Alan Bartlett <ajb@elrepo.org> - 3.8.7-1
- Updated with the 3.8.7 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.8.7]

* Sat Apr 06 2013 Alan Bartlett <ajb@elrepo.org> - 3.8.6-1
- Updated with the 3.8.6 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.8.6]

* Thu Mar 28 2013 Alan Bartlett <ajb@elrepo.org> - 3.8.5-1
- Updated with the 3.8.5 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.8.5]

* Thu Mar 21 2013 Alan Bartlett <ajb@elrepo.org> - 3.8.4-1
- Updated with the 3.8.4 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.8.4]

* Fri Mar 15 2013 Alan Bartlett <ajb@elrepo.org> - 3.8.3-1
- Updated with the 3.8.3 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.8.3]

* Wed Mar 13 2013 Alan Bartlett <ajb@elrepo.org> - 3.8.2-2
- CONFIG_X86_X2APIC=y, CONFIG_X86_NUMACHIP disabled, CONFIG_X86_UV=y,
- CONFIG_SGI_XP=m, CONFIG_SGI_GRU=m, CONFIG_SGI_GRU_DEBUG disabled
- and CONFIG_UV_MMTIMER=m [http://elrepo.org/bugs/view.php?id=368]

* Tue Mar 04 2013 Alan Bartlett <ajb@elrepo.org> - 3.8.2-1
- Updated with the 3.8.2 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.8.2]

* Tue Feb 28 2013 Alan Bartlett <ajb@elrepo.org> - 3.8.1-1
- Updated with the 3.8.1 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.8.1]
- CONFIG_IPV6_SUBTREES=y and CONFIG_IPV6_MROUTE_MULTIPLE_TABLES=y [http://elrepo.org/bugs/view.php?id=354]

* Tue Feb 19 2013 Alan Bartlett <ajb@elrepo.org> - 3.8.0-1
- Updated with the 3.8 source tarball.

* Mon Feb 18 2013 Alan Bartlett <ajb@elrepo.org> - 3.7.9-1
- Updated with the 3.7.9 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.7.9]

* Fri Feb 15 2013 Alan Bartlett <ajb@elrepo.org> - 3.7.8-1
- Updated with the 3.7.8 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.7.8]

* Tue Feb 12 2013 Alan Bartlett <ajb@elrepo.org> - 3.7.7-1
- Updated with the 3.7.7 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.7.7]
- CONFIG_MEMCG=y, CONFIG_MEMCG_SWAP=y, CONFIG_MEMCG_SWAP_ENABLE disabled,
- CONFIG_MEMCG_KMEM=y and CONFIG_MM_OWNER=y [Dag Wieers]

* Mon Feb 04 2013 Alan Bartlett <ajb@elrepo.org> - 3.7.6-1
- Updated with the 3.7.6 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.7.6]

* Mon Jan 28 2013 Alan Bartlett <ajb@elrepo.org> - 3.7.5-1
- Updated with the 3.7.5 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.7.5]

* Sun Jan 27 2013 Alan Bartlett <ajb@elrepo.org> - 3.7.4-2
- Correcting an issue with the configuration files. [http://elrepo.org/bugs/view.php?id=347]

* Tue Jan 22 2013 Alan Bartlett <ajb@elrepo.org> - 3.7.4-1
- Updated with the 3.7.4 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.7.4]

* Sat Jan 19 2013 Alan Bartlett <ajb@elrepo.org> - 3.7.3-1
- Updated with the 3.7.3 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.7.3]
- Adjusted this specification file to ensure that the arch/%%{asmarch}/syscalls/
- directory is copied to the build/ directory. [http://elrepo.org/bugs/view.php?id=344]

* Sat Jan 12 2013 Alan Bartlett <ajb@elrepo.org> - 3.7.2-1
- Updated with the 3.7.2 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.7.2]

* Thu Jan 10 2013 Alan Bartlett <ajb@elrepo.org> - 3.7.1-3
- CONFIG_UFS_FS=m [http://elrepo.org/bugs/view.php?id=342]
- Further adjustments to this specification file. [http://elrepo.org/bugs/view.php?id=340]

* Mon Dec 31 2012 Alan Bartlett <ajb@elrepo.org> - 3.7.1-2
- Adjusted this specification file to ensure that a copy of the version.h file is
- present in the include/linux/ directory. [http://elrepo.org/bugs/view.php?id=340]

* Tue Dec 18 2012 Alan Bartlett <ajb@elrepo.org> - 3.7.1-1
- Updated with the 3.7.1 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.7.1]
- Added WERROR=0 to the perf 'make' line to enable the 32-bit
- perf package to be built. [http://elrepo.org/bugs/view.php?id=335]

* Wed Dec 12 2012 Alan Bartlett <ajb@elrepo.org> - 3.7.0-1
- Updated with the 3.7 source tarball.

* Tue Dec 11 2012 Alan Bartlett <ajb@elrepo.org> - 3.6.10-1
- Updated with the 3.6.10 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.6.10]

* Tue Dec 04 2012 Alan Bartlett <ajb@elrepo.org> - 3.6.9-1
- Updated with the 3.6.9 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.6.9]

* Mon Nov 26 2012 Alan Bartlett <ajb@elrepo.org> - 3.6.8-1
- Updated with the 3.6.8 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.6.8]
- CONFIG_MAC80211_DEBUGFS=y and CONFIG_ATH_DEBUG=y [http://elrepo.org/bugs/view.php?id=326]
- CONFIG_ATH9K_RATE_CONTROL disabled [http://elrepo.org/bugs/view.php?id=327]

* Sun Nov 18 2012 Alan Bartlett <ajb@elrepo.org> - 3.6.7-1
- Updated with the 3.6.7 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.6.7]

* Tue Nov 06 2012 Alan Bartlett <ajb@elrepo.org> - 3.6.6-1
- Updated with the 3.6.6 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.6.6]

* Wed Oct 31 2012 Alan Bartlett <ajb@elrepo.org> - 3.6.5-1
- Updated with the 3.6.5 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.6.5]

* Sun Oct 28 2012 Alan Bartlett <ajb@elrepo.org> - 3.6.4-1
- Updated with the 3.6.4 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.6.4]
- CONFIG_MAC80211_MESH=y [Jonathan Bither]
- CONFIG_LIBERTAS_MESH=y

* Mon Oct 22 2012 Alan Bartlett <ajb@elrepo.org> - 3.6.3-1
- Updated with the 3.6.3 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.6.3]

* Sat Oct 13 2012 Alan Bartlett <ajb@elrepo.org> - 3.6.2-1
- Updated with the 3.6.2 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.6.2]
- CONFIG_SCSI_SCAN_ASYNC disabled [http://elrepo.org/bugs/view.php?id=317]
- CONFIG_AIC79XX_REG_PRETTY_PRINT disabled and CONFIG_SCSI_AIC7XXX_OLD=m

* Mon Oct 08 2012 Alan Bartlett <ajb@elrepo.org> - 3.6.1-2
- Rebuilt with CONFIG_NFS_FS=m, CONFIG_NFS_V2=m, CONFIG_NFS_V3=m,
- CONFIG_NFS_V3_ACL=y, CONFIG_NFS_V4=m, CONFIG_NFS_FSCACHE=y,
- CONFIG_NFSD=m and CONFIG_NFS_ACL_SUPPORT=m [Akemi Yagi]

* Sun Oct 07 2012 Alan Bartlett <ajb@elrepo.org> - 3.6.1-1
- Updated with the 3.6.1 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.6.1]

* Fri Oct 05 2012 Alan Bartlett <ajb@elrepo.org> - 3.6.0-1
- Updated with the 3.6 source tarball.

* Thu Oct 04 2012 Alan Bartlett <ajb@elrepo.org> - 3.5.5-1
- Updated with the 3.5.5 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.5.5]

* Sat Sep 15 2012 Alan Bartlett <ajb@elrepo.org> - 3.5.4-1
- Updated with the 3.5.4 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.5.4]

* Sun Aug 26 2012 Alan Bartlett <ajb@elrepo.org> - 3.5.3-1
- Updated with the 3.5.3 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.5.3]

* Wed Aug 15 2012 Alan Bartlett <ajb@elrepo.org> - 3.5.2-1
- Updated with the 3.5.2 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.5.2]

* Thu Aug 09 2012 Alan Bartlett <ajb@elrepo.org> - 3.5.1-1
- Updated with the 3.5.1 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.5.1]

* Tue Jul 24 2012 Alan Bartlett <ajb@elrepo.org> - 3.5.0-2
- Rebuilt with RTLLIB support enabled. [http://elrepo.org/bugs/view.php?id=289]

* Mon Jul 23 2012 Alan Bartlett <ajb@elrepo.org> - 3.5.0-1
- Updated with the 3.5 source tarball.

* Fri Jul 20 2012 Alan Bartlett <ajb@elrepo.org> - 3.4.6-1
- Updated with the 3.4.6 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.4.6]

* Tue Jul 17 2012 Alan Bartlett <ajb@elrepo.org> - 3.4.5-1
- Updated with the 3.4.5 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.4.5]

* Fri Jun 22 2012 Alan Bartlett <ajb@elrepo.org> - 3.4.4-1
- Updated with the 3.4.4 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.4.4]

* Mon Jun 18 2012 Alan Bartlett <ajb@elrepo.org> - 3.4.3-1
- Updated with the 3.4.3 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.4.3]

* Sun Jun 10 2012 Alan Bartlett <ajb@elrepo.org> - 3.4.2-1
- Updated with the 3.4.2 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.4.2]

* Mon Jun 04 2012 Alan Bartlett <ajb@elrepo.org> - 3.4.1-1
- Updated with the 3.4.1 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.4.1]

* Sat May 26 2012 Alan Bartlett <ajb@elrepo.org> - 3.4.0-1
- Updated with the 3.4 source tarball.
- Added a BR for the bison package. [Akemi Yagi]
- Added a BR for the gtk2-devel package. [Akemi Yagi]

* Fri May 25 2012 Alan Bartlett <ajb@elrepo.org> - 3.3.7-2
- Rebuilt with CEPH support enabled.

* Thu May 24 2012 Alan Bartlett <ajb@elrepo.org> - 3.3.7-1
- Updated with the 3.3.7 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.3.7]

* Sun May 20 2012 Alan Bartlett <ajb@elrepo.org> - 3.3.6-2
- Corrected the corrupt configuration files.

* Sun May 13 2012 Alan Bartlett <ajb@elrepo.org> - 3.3.6-1
- Updated with the 3.3.6 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.3.6]

* Mon May 07 2012 Alan Bartlett <ajb@elrepo.org> - 3.3.5-1
- Updated with the 3.3.5 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.3.5]

* Fri Apr 27 2012 Alan Bartlett <ajb@elrepo.org> - 3.3.4-1
- Updated with the 3.3.4 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.3.4]
- Re-enabled the build of the perf packages.

* Mon Apr 23 2012 Alan Bartlett <ajb@elrepo.org> - 3.3.3-1
- Updated with the 3.3.3 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.3.3]
- Disabled the build of the perf packages due to an undetermined
- bug in the sources. With the 3.3.2 sources, the perf packages will
- build. With the 3.3.3 sources, the perf packages will not build.

* Fri Apr 13 2012 Alan Bartlett <ajb@elrepo.org> - 3.3.2-1
- Updated with the 3.3.2 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.3.2]

* Tue Apr 03 2012 Alan Bartlett <ajb@elrepo.org> - 3.3.1-1
- Updated with the 3.3.1 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.3.1]

* Mon Mar 19 2012 Alan Bartlett <ajb@elrepo.org> - 3.3.0-1
- Updated with the 3.3 source tarball.

* Tue Mar 13 2012 Alan Bartlett <ajb@elrepo.org> - 3.2.11-1
- Updated with the 3.2.11 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.2.11]

* Thu Mar 01 2012 Alan Bartlett <ajb@elrepo.org> - 3.2.9-1
- Updated with the 3.2.9 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.2.9]

* Tue Feb 28 2012 Alan Bartlett <ajb@elrepo.org> - 3.2.8-1
- Updated with the 3.2.8 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.2.8]

* Tue Feb 21 2012 Alan Bartlett <ajb@elrepo.org> - 3.2.7-1
- Updated with the 3.2.7 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.2.7]

* Tue Feb 14 2012 Alan Bartlett <ajb@elrepo.org> - 3.2.6-1
- Updated with the 3.2.6 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.2.6]

* Mon Feb 06 2012 Alan Bartlett <ajb@elrepo.org> - 3.2.5-1
- Updated with the 3.2.5 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.2.5]

* Sat Feb 04 2012 Alan Bartlett <ajb@elrepo.org> - 3.2.4-1
- Updated with the 3.2.4 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.2.4]

* Fri Feb 03 2012 Alan Bartlett <ajb@elrepo.org> - 3.2.3-1
- Updated with the 3.2.3 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.2.3]

* Fri Jan 27 2012 Alan Bartlett <ajb@elrepo.org> - 3.2.2-1
- Updated with the 3.2.2 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.2.2]
- Adjustments to Conflicts and Provides [Phil Perry]

* Mon Jan 16 2012 Alan Bartlett <ajb@elrepo.org> - 3.2.1-1
- Updated with the 3.2.1 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.2.1]
- General availability.
