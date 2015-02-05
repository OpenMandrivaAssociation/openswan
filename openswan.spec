%{?build_selinux}%{?!build_selinux:%bcond_with selinux}

Summary:	An implementation of IPSEC & IKE for Linux
Name:		openswan
Version:	2.6.41
Release:	1
License:	GPLv2+
Group:		System/Servers
Url:		http://www.openswan.org/
Source0:	http://www.openswan.org/download/openswan-%{version}.tar.gz
Source1:	http://www.openswan.org/download/openswan-%{version}.tar.gz.asc
Source2:	openswan.service
Patch0:		openswan-2.6.28-manfix.patch
BuildRequires:	bison
BuildRequires:	docbook-dtd412-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	dos2unix
BuildRequires:	flex
BuildRequires:	xmlto
BuildRequires:	gmp-devel
BuildRequires:	openldap-devel
BuildRequires:	pam-devel
%if %{with selinux}
BuildRequires:	selinux-devel
%endif
BuildRequires:	pkgconfig(libcap-ng)
BuildRequires:	pkgconfig(libcurl)
Requires:	curl
Requires:	iproute2
Requires:	ipsec-tools
Requires:	lsof
Requires:	openldap
Requires(post,preun):	rpm-helper
Provides:	ipsec-userland
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

%preun
%_preun_service %{name}

%post
%_post_service %{name}

#----------------------------------------------------------------------------

%package doc
Summary:	An implementation of IPSEC & IKE for Linux
Group:		System/Servers
BuildArch:	noarch

%description doc
Openswan is a free implementation of IPSEC & IKE for Linux, a fork of the
FreeS/WAN project.

This is the documentation for Openswan.

%files doc
%doc docs/README.* docs/CREDITS.* docs/*.txt
%doc docs/quickstarts docs/html-old-need-merge-with-wiki

#----------------------------------------------------------------------------

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
    CONFDIR=%{_sysconfdir}/%{name} \
    FINALCONFDIR=%{_sysconfdir}/%{name} \
    FINALCONFFILE=%{_sysconfdir}/%{name}/ipsec.conf \
    FINALLIBEXECDIR=%{_libdir}/ipsec \
    FINALLIBDIR=%{_libdir}/ipsec \
    USE_LIBCAP_NG=true \
%if %{with selinux}
    USE_LABELED_IPSEC=true \
%endif
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
    FINALCONFDIR=%{_sysconfdir}/%{name} \
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


