Summary:	Little silly kernel module can be used to restrict virtual host.
Summary(pl):	Proste narzêdzie do ustawiania restrykcji u¿ywania na vhosty.
Name:		bindprivs
Version:	0.5
Release:	1
License:	GPL
Group:		Networking/Utilities
Source0:	ftp://bzium.eu.org/pub/%{name}-%{version}.tar.gz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This little silly kernel module can be used to restrict virtual host
to some particular users. read bindprivs.conf(5) and bpset(8) for more
details.

%description -l pl
To prosty modu³ kernelowy s³u¿±cy do ograniczenia u¿ywania vhostów.
Jak go u¿ywaæ przeczytaj bindprivs.conf(5) oraz bpset(8). 

%prep
%setup -q

%build
%{__make} CC="gcc %{rpmcflags} -Wall"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man{5,8},%{_libdir}/bindprivs,%{_sysconfdir}}

cat > $RPM_BUILD_ROOT%{_sysconfdir}/bindprivs.conf.sample << EOF
# let's allow ,,root'' and ,,jack'' using 10.0.2.5
allow 10.0.2.5 root jack
deny 10.0.2.5 all

# only the group ,,irc'' can use our IPv6 class
allowgroup 3ffe:1281:102:ffff::/48 irc
deny 3ffe:1281:102:ffff::/48 all

# reject all network connections from group ,,nonetwork''
deny all all
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
%attr(755,root,root) %{_bindir}/bp*
%{_libdir}/bindprivs
%{_sysconfdir}/bindprivs.conf.sample
%{_mandir}/man?/*
%doc README
