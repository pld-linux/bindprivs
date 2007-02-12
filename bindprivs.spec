#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
#
Summary:	Little silly kernel module and utility to restrict virtual hosts
Summary(pl.UTF-8):   Proste narzędzie do ustawiania restrykcji używania wirtualnych hostów
Name:		bindprivs
Version:	0.6
Release:	1
License:	GPL v2
Group:		Networking/Utilities
Source0:	http://toxygen.net/bindprivs/%{name}-%{version}.tar.gz
# Source0-md5:	0846e1094480728440ec46d273cc0815
%{?with_dist_kernel:BuildRequires: kernel-headers}
URL:		http://toxygen.net/bindprivs/
BuildRequires:	%{kgcc_package}
BuildRequires:	rpmbuild(macros) >= 1.118
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
bindprivs is a little silly kernel module can be used to restrict
virtual host to some particular users. Read bindprivs.conf(5) and
bpset(8) for more details.

%description -l pl.UTF-8
bindprivs to prosty moduł jądra służący do ograniczenia używania
wirtualnych hostów dla poszczególnych użytkowników. Informacje na
temat używania go można znaleźć w bindprivs.conf(5) oraz bpset(8).

%package -n kernel-misc-bindprivs
Summary:	bindprivs Linux kernel module
Summary(pl.UTF-8):   Moduł jądra Linuksa bindprivs
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod

%description -n kernel-misc-bindprivs
bindprivs Linux kernel module - a little silly kernel module which can
be used to restrict virtual host to some particular users.

%description -n kernel-misc-bindprivs -l pl.UTF-8
Moduł jądra Linuksa bindprivs - prosty moduł jądra służący do
ograniczenia używania wirtualnych hostów dla poszczególnych
użytkowników.

%package -n kernel-smp-misc-bindprivs
Summary:	bindprivs Linux SMP kernel module
Summary(pl.UTF-8):   Moduł jądra Linuksa SMP bindprivs
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-misc-bindprivs
bindprivs Linux SMP kernel module - a little silly kernel module which
can be used to restrict virtual host to some particular users.

%description -n kernel-smp-misc-bindprivs -l pl.UTF-8
Moduł jądra Linuksa SMP bindprivs - prosty moduł jądra służący do
ograniczenia używania wirtualnych hostów dla poszczególnych
użytkowników.

%prep
%setup -q

%build
%{__make} bindprivs.o \
	CC="%{kgcc}" \
	CFLAGS="%{rpmcflags} -fomit-frame-pointer -Wall -D__SMP__"
mv -f bindprivs.o bindprivs-smp.o

%{__make} bindprivs.o \
	CC="%{kgcc}" \
	CFLAGS="%{rpmcflags} -fomit-frame-pointer -Wall"

%{__make} bpset \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Wall"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man{5,8},%{_sysconfdir}} \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc

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
/sbin/insmod bindprivs
EOF

cat > $RPM_BUILD_ROOT%{_bindir}/bpremove << EOF
bpset -u
/sbin/rmmod bindprivs
EOF

install bindprivs-smp.o	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/bindprivs.o
install bindprivs.o	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc

install bpset		$RPM_BUILD_ROOT%{_bindir}
install bindprivs.conf.5 $RPM_BUILD_ROOT%{_mandir}/man5
install bpset.8		$RPM_BUILD_ROOT%{_mandir}/man8

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel-misc-bindprivs
%depmod %{_kernel_ver}

%postun	-n kernel-misc-bindprivs
%depmod %{_kernel_ver}

%post	-n kernel-smp-misc-bindprivs
%depmod %{_kernel_ver}smp

%postun	-n kernel-smp-misc-bindprivs
%depmod %{_kernel_ver}smp

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/bp*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bindprivs.conf
%{_mandir}/man?/*

%files -n kernel-misc-bindprivs
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/bindprivs.o*

%files -n kernel-smp-misc-bindprivs
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/bindprivs.o*
