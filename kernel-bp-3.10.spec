%global __spec_install_pre %{___build_pre}

# Define the version of the Linux Kernel Archive tarball.
%define RHKver 3.10.0
%define RHKrel 327.22.2

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
%define firmware_conflicts bfa-firmware, ql2100-firmware, ql2200-firmware, ql23xx-firmware, ql2400-firmware, ql2500-firmware, rt61pci-firmware, rt73usb-firmware, xorg-x11-drv-ati-firmware netxen-firmware

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
Source5: linux-firmware-20150904-43.git6ebf5d5.el7.noarch.rpm

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
%{__mv} usr/share/doc/linux-firmware-20150904 usr/share/doc/kernel-firmware-%{version}

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
* Mon Jul 11 2016 Jay Grizzard <elfchief-rpms@lupine.org>
- Updated with 3.10.0.327.22.2 CentOS kernel

* Tue May 20 2016 Jay Grizzard <elfchief-rpms@lupine.org>
- Updated with 3.10.0-327.18.2 CentOS kernel

* Tue Apr  5 2016 Jay Grizzard <elfchief-rpms@lupine.org>
- Updated with 3.10.0-327.13.1 CentOS kernel

* Wed Jan 13 2016 Jay Grizzard <elfchief-rpms@lupine.org>
- Updated with 3.10.0-327.4.4 CentOS kernel

* Mon Oct 26 2015 Jay Grizzard <elfchief-rpms@lupine.org>
- Initial build with 3.10.0-229.14.1 CentOS kernel
