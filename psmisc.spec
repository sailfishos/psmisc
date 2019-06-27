Name:           psmisc
Version:        22.13
Release:        7
License:        GPLv2+
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

%package doc
Summary:   Documentation for %{name}
Group:     Documentation
Requires:  %{name} = %{version}-%{release}
Obsoletes: %{name}-docs

%description doc
Man pages for %{name}.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure --prefix=/usr --disable-nls
make %{?_smp_mflags}

%install
%make_install

mkdir -p %{buildroot}%{_sbindir}
mv %{buildroot}%{_bindir}/fuser %{buildroot}%{_sbindir}

pushd %{buildroot}%{_sbindir};
ln -s /usr/bin/killall pidof
popd

mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}
install -m0644 -t %{buildroot}%{_docdir}/%{name}-%{version} \
        AUTHORS ChangeLog NEWS README

%files
%defattr(-,root,root)
%license COPYING
%{_sbindir}/fuser
%{_bindir}/killall
%{_sbindir}/pidof
%{_bindir}/pstree
%{_bindir}/pstree.x11
%{_bindir}/prtstat
%ifnarch aarch64
%{_bindir}/peekfd
%endif

%files doc
%defattr(-,root,root)
%{_mandir}/man1/*.*
%{_docdir}/%{name}-%{version}
