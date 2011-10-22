%define _enable_debug_packages %{nil}
%define debug_package %{nil}

Summary:	An implementation of IPSEC & IKE for Linux
Name:		openswan
Version:	2.6.36
Release:	%mkrel 1
License:	GPLv2+
Group:		System/Servers
URL:		http://www.openswan.org/
Source0:	http://www.openswan.org/download/openswan-%{version}.tar.gz
Source1:	http://www.openswan.org/download/openswan-%{version}.tar.gz.asc
Patch0:		openswan-2.6.28-manfix.patch
Patch1:		openswan-2.6.21-format_not_a_string_literal_and_no_format_arguments.diff
Requires(post): rpm-helper
Requires(preun): rpm-helper
Provides:	ipsec-userland
Requires:	lsof
Requires:	iproute2
Requires:	ipsec-tools
Conflicts:	freeswan
BuildRequires:	bison
BuildRequires:	gmp-devel
BuildRequires:	pam-devel
BuildRequires:	dos2unix
BuildRequires:	flex
BuildRequires:  xmlto
BuildRequires:	docbook-dtd412-xml
BuildRoot:	%{_tmppath}/%{name}-buildroot

%description
Openswan is a free implementation of IPSEC & IKE for Linux, a fork of the
FreeS/WAN project.

IPSEC is Internet Protocol Security and uses strong cryptography to
provide both authentication and encryption services.  These services
allow you to build secure tunnels through untrusted networks.
Everything passing through the untrusted net is encrypted by the ipsec
gateway machine and decrypted by the gateway at the other end of the
tunnel.  The resulting tunnel is a virtual private network or VPN.

This package contains the daemons and userland tools for setting up
Openswan on a kernel with either the 2.6 native IPsec code, or
FreeS/WAN's KLIPS.

%package	doc
Summary:	An implementation of IPSEC & IKE for Linux
Group:		System/Servers

%description	doc
Openswan is a free implementation of IPSEC & IKE for Linux, a fork of the
FreeS/WAN project.

This is the documentation for Openswan.

%prep

%setup -q -n openswan-%{version}
%patch0 -p0 -b .manfix
# %patch1 -p0 -b .format_not_a_string_literal_and_no_format_arguments

find . -type f -name "*.html" -exec dos2unix -U {} \;

%build

%serverbuild

find . -name "Makefile*" | xargs perl -pi -e "s|libexec|%{_lib}|g"
export CLFAGS=$(echo %{optflags} -fno-strict-aliasing)
# the %make macro doesn't seem to work
make \
    USERCOMPILE="-g $CLFAGS" \
    INC_USRLOCAL=%{_prefix} \
    MANTREE=%{_mandir} \
    INC_RCDEFAULT=%{_initrddir} \
    CONFDIR=%{_sysconfdir}/%name \
    FINALCONFDIR=%{_sysconfdir}/%name \
    FINALCONFFILE=%{_sysconfdir}/%name/ipsec.conf \
    FINALLIBEXECDIR=%{_libdir}/ipsec \
    FINALLIBDIR=%{_libdir}/ipsec \
    programs

%install
rm -rf %{buildroot}

%{make} \
    DESTDIR=%{buildroot} \
    INC_USRLOCAL=%{_prefix} \
    MANTREE=%{buildroot}%{_mandir} \
    INC_RCDEFAULT=%{_initrddir} \
    INC_USRLOCAL=%{_prefix} \
    INC_RCDEFAULT=%{_initrddir} \
    FINALCONFDIR=%{_sysconfdir}/%name \
    FINALLIBEXECDIR=%{_libdir}/ipsec \
    FINALLIBDIR=%{_libdir}/ipsec \
    install

install -d -m700 %{buildroot}%{_localstatedir}/lib/run/pluto
install -d %{buildroot}%{_sbindir}

# Remove old documentation for the time being.
rm -rf %{buildroot}%{_defaultdocdir}/freeswan

# cleanup
rm -rf %{buildroot}%{_sysconfdir}/rc.d/rc*
rm -rf %{buildroot}%{_sysconfdir}/rc.d/init.d/setup
rm -rf %{buildroot}%{_docdir}/%{name}

%preun
%_preun_service ipsec

%post
%_post_service ipsec

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc BUGS CHANGES COPYING CREDITS README
%attr(0755,root,root) %{_initrddir}/ipsec
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/ipsec.conf
%attr(0700,root,root) %dir %{_sysconfdir}/%{name}/ipsec.d
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/ipsec.d/*/*
%{_sbindir}/ipsec
%dir %{_libdir}/ipsec
%{_libdir}/ipsec/*
%{_localstatedir}/lib/run/pluto
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
