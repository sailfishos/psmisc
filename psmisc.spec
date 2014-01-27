#
# Please submit bugfixes or comments via http://bugs.meego.com/
#

Name:           psmisc
Version:        22.13
Release:        6
License:        BSD/GPLv2+
Summary:        Utilities for managing processes on your system
Url:            http://psmisc.sourceforge.net
Group:          Applications/System
Source:         http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

# rhbz #651794 - incorrect exit code of fuser -m -s
Patch0:         psmisc-22.13-fuser-silent.patch
# rhbz #666213 - uninitialized memory leading to `killall -g name` failure
Patch1:         psmisc-22.13-killall-pgid.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  pkgconfig(ncurses)

%description
The psmisc package contains utilities for managing processes on your
system: pstree, killall and fuser.  The pstree command displays a tree
structure of all of the running processes on your system.  The killall
command sends a specified signal (SIGTERM if nothing is specified) to
processes identified by name.  The fuser command identifies the PIDs
of processes that are using specified files or filesystems.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure --prefix=/usr --disable-nls
make %{?_smp_mflags}

%install
%make_install

mkdir -p %{buildroot}/sbin
mv %{buildroot}%{_bindir}/fuser %{buildroot}/sbin

pushd %{buildroot}/sbin;
ln -s ../usr/bin/killall pidof
popd

%docs_package

%files 
%defattr(-,root,root)
/sbin/fuser
%{_bindir}/killall
/sbin/pidof
%{_bindir}/pstree
%{_bindir}/pstree.x11
%{_bindir}/prtstat
%ifnarch aarch64
%{_bindir}/peekfd
%endif
