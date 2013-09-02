Summary:	An implementation of IPSEC & IKE for Linux
Name:		openswan
Version:	2.6.39
Release:	1
License:	GPLv2+
Group:		System/Servers
URL:		http://www.openswan.org/
Source0:	http://www.openswan.org/download/openswan-%{version}.tar.gz
Source1:	http://www.openswan.org/download/openswan-%{version}.tar.gz.asc
Source2:	openswan.service
Patch0:		openswan-2.6.28-manfix.patch
Requires(post): rpm-helper
Requires(preun): rpm-helper
Provides:	ipsec-userland
BuildRequires:	bison
BuildRequires:	curl-devel
BuildRequires:	docbook-dtd412-xml
BuildRequires:	dos2unix
BuildRequires:	flex
BuildRequires:	gmp-devel
BuildRequires:	libcap-ng-devel
BuildRequires:	openldap-devel
BuildRequires:	pam-devel
BuildRequires:  xmlto
Requires:	curl
Requires:	iproute2
Requires:	ipsec-tools
Requires:	lsof
Requires:	openldap
Conflicts:	freeswan

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
BuildArch:	noarch

%description	doc
Openswan is a free implementation of IPSEC & IKE for Linux, a fork of the
FreeS/WAN project.

This is the documentation for Openswan.

%prep

%setup -q -n openswan-%{version}
%patch0 -p0 -b .manfix

find . -type f -name "*.html" -exec dos2unix {} \;

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
    USE_LIBCAP_NG=true \
    USE_LDAP=true \
    USE_LIBCURL=true \
    HAVE_THREADS=true \
    programs

%install

make \
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

install -Dm644 %{SOURCE2} %{buildroot}%{_unitdir}/openswan.service
mkdir -p %{buildroot}%{_prefix}/lib/systemd/scripts/
mv %{buildroot}/%{_initrddir}/ipsec %{buildroot}/%{_prefix}/lib/systemd/scripts/


%preun
%_preun_service %{name}

%post
%_post_service %{name}

%files
%doc BUGS CHANGES COPYING CREDITS README
%{_unitdir}/%{name}.service
%{_prefix}/lib/systemd/scripts/ipsec
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/ipsec.conf
%attr(0700,root,root) %dir %{_sysconfdir}/%{name}/ipsec.d
%attr(0700,root,root) %dir %{_sysconfdir}/%{name}/ipsec.d/examples
%attr(0700,root,root) %dir %{_sysconfdir}/%{name}/ipsec.d/policies
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/ipsec.d/*/*
%{_sbindir}/ipsec
%dir %{_libdir}/ipsec
%{_libdir}/ipsec/*
%{_localstatedir}/lib/run/pluto
%{_mandir}/*/*

%files doc
%doc docs/README.* docs/CREDITS.* docs/*.txt
%doc docs/quickstarts docs/html-old-need-merge-with-wiki


%changelog
* Tue Jul 17 2012 Oden Eriksson <oeriksson@mandriva.com> 2.6.38-1
+ Revision: 809978
- 2.6.38
- sync deps slipthly with fedora
- various fixes

* Tue Nov 08 2011 Alexander Khrukin <akhrukin@mandriva.org> 2.6.37-1
+ Revision: 729094
- update to 2.6.37 upstream release

* Sat Oct 22 2011 Zombie Ryushu <ryushu@mandriva.org> 2.6.36-1
+ Revision: 705678
- fix docdir
- fix deprecated patch
- Upgrade to 2.6.36

* Fri Sep 03 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 2.6.28-2mdv2011.0
+ Revision: 575574
- lsof as require
- 2.6.28
  P0 rediffed

* Wed Feb 10 2010 Funda Wang <fwang@mandriva.org> 2.6.24-2mdv2010.1
+ Revision: 503615
- rebuild for new gmp

* Tue Jan 19 2010 Frederik Himpe <fhimpe@mandriva.org> 2.6.24-1mdv2010.1
+ Revision: 493791
- Update to new version 2.6.24

* Sat Nov 07 2009 Frederik Himpe <fhimpe@mandriva.org> 2.6.23-1mdv2010.1
+ Revision: 462705
- Update to new version 2.6.23

* Thu Jun 25 2009 Frederik Himpe <fhimpe@mandriva.org> 2.6.22-1mdv2010.0
+ Revision: 389267
- BuildRequires docbook-dtd412-xml for documentation
- Update to new version 2.6.22
- Build with -fno-strict-aliasing, otherwise it fails

* Tue Mar 31 2009 Oden Eriksson <oeriksson@mandriva.com> 2.6.21-1mdv2009.1
+ Revision: 362883
- 2.6.21 (fixes CVE-2009-0790)
- rediffed P0
- added P1 to fix build with -Werror=format-security

* Wed Dec 03 2008 Jérôme Soyer <saispo@mandriva.org> 2.6.19-1mdv2009.1
+ Revision: 309656
- Add BuildRequires
- New release 2.6.19

* Mon Nov 10 2008 Michael Scherer <misc@mandriva.org> 2.6.18-1mdv2009.1
+ Revision: 301689
- upgrade to 2.6.18
- clean end of line ( automatic with vim )

* Mon Sep 01 2008 Olivier Blin <blino@mandriva.org> 2.6.16-1mdv2009.0
+ Revision: 278117
- 2.6.16

* Tue Jul 15 2008 Funda Wang <fwang@mandriva.org> 2.6.14-1mdv2009.0
+ Revision: 235755
- drop unneeded setup file
- BR flex
- New version 2.6.14
- rediff man-fix patch

  + Pixel <pixel@mandriva.com>
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

* Sat Mar 01 2008 Olivier Blin <blino@mandriva.org> 2.4.12-1mdv2008.1
+ Revision: 177431
- 2.4.12
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri May 25 2007 Olivier Blin <blino@mandriva.org> 2.4.8-1mdv2008.0
+ Revision: 31108
- 2.4.8 (from Zombie Ryushu)

