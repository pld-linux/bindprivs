#
# TODO: use standard scheme for kernel module
#
Summary:	Little silly kernel module can be used to restrict virtual hosts
Summary(pl):	Proste narzêdzie do ustawiania restrykcji u¿ywania wirtualnych hostów
Name:		bindprivs
Version:	0.6
Release:	1
License:	GPL
Group:		Networking/Utilities
Source0:	ftp://bzium.eu.org/pub/%{name}-%{version}.tar.gz
# Source0-md5:	0846e1094480728440ec46d273cc0815
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This little silly kernel module can be used to restrict virtual host
to some particular users. Read bindprivs.conf(5) and bpset(8) for more
details.

%description -l pl
To prosty modu³ j±dra s³u¿±cy do ograniczenia u¿ywania wirtualnych
hostów dla poszczególnych u¿ytkowników. Informacje na temat u¿ywania
go mo¿na znale¼æ w bindprivs.conf(5) oraz bpset(8).

%prep
%setup -q

%build
%{__make} CC="%{__cc} %{rpmcflags} -Wall"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man{5,8},%{_libdir}/bindprivs,%{_sysconfdir}}

cat > $RPM_BUILD_ROOT%{_sysconfdir}/bindprivs.conf << EOF
# Sample configuration

## let's allow ,,root'' and ,,jack'' using 10.0.2.5
#allow 10.0.2.5 root jack
#deny 10.0.2.5 all

## only the group ,,irc'' can use our IPv6 class
#allowgroup 3ffe:1281:102:ffff::/48 irc
#deny 3ffe:1281:102:ffff::/48 all

## reject all network connections from group ,,nonetwork''
#deny all all
EOF

cat > $RPM_BUILD_ROOT%{_bindir}/bpload << EOF
/sbin/insmod /usr/lib/bindprivs/bindprivs.o
EOF

cat > $RPM_BUILD_ROOT%{_bindir}/bpremove << EOF
bpset -u
/sbin/rmmod bindprivs
EOF

install bpset		$RPM_BUILD_ROOT%{_bindir}
install bindprivs.o	$RPM_BUILD_ROOT%{_libdir}/bindprivs
install bindprivs.conf.5 $RPM_BUILD_ROOT%{_mandir}/man5
install bpset.8		$RPM_BUILD_ROOT%{_mandir}/man8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/bp*
%{_libdir}/bindprivs
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/bindprivs.conf
%{_mandir}/man?/*
