Name:           libaccounts-qt
Version:        1.6
Release:        1
License:        LGPLv2.1
Summary:        Accounts framework (Qt binding)
Url:            https://code.google.com/p/accounts-sso.libaccounts-qt
Group:          System/Libraries
Source:         %{name}-%{version}.tar.bz2
Patch0:         libaccounts-qt-1.2-disable-multilib.patch
Patch1:         0001-libaccounts-qt-c++0x.patch
Patch2:         0002-libaccounts-qt-documentation-path.patch 
Patch3:         0003-Fix-test-service-MyService-to-include-messaging-tag.patch
BuildRequires:  doxygen
BuildRequires:  fdupes
BuildRequires:  pkgconfig(QtCore)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libaccounts-glib) >= 1.6

%description
Framework to provide the accounts.

%package devel
Summary:        Development files for accounts-qt
Group:          Development/Libraries
Requires:       %{name} = %{version}
Provides:       accounts-qt-dev

%description devel
Headers and static libraries for the accounts.

%package tests
Summary:        Tests for accounts-qt
Group:          System/Libraries
Requires:       %{name} = %{version}

%description tests
Tests for accounts-qt.

%package doc
Summary:        Documentation for accounts-qt
Group:          Documentation

%description doc
HTML documentation for the accounts.

%prep
%setup -q -n %{name}-%{version}/%{name}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
sed -i 's,DATA_PATH = .*,DATA_PATH = /opt/tests/%{name}/data,' tests/accountstest.pro
sed -i 's,/usr/bin/accountstest,/opt/tests/%{name}/accountstest,' tests/tests.xml

%build
%qmake CONFIG+=release
make %{?_smp_mflags}

%install
%qmake_install
rm %{buildroot}%{_datadir}/doc/accounts-qt/html/installdox
%fdupes %{buildroot}%{_includedir}
%fdupes %{buildroot}%{_docdir}
mkdir -p %{buildroot}/opt/tests/%{name}/test-definition
mv %{buildroot}/opt/tests/%{name}/data/tests.xml %{buildroot}/opt/tests/%{name}/test-definition
mv %{buildroot}/%{_bindir}/accountstest %{buildroot}/opt/tests/%{name}/

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libaccounts-qt.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/accounts-qt/Accounts/Account
%{_includedir}/accounts-qt/Accounts/AccountService
%{_includedir}/accounts-qt/Accounts/Application
%{_includedir}/accounts-qt/Accounts/AuthData
%{_includedir}/accounts-qt/Accounts/Error
%{_includedir}/accounts-qt/Accounts/Manager
%{_includedir}/accounts-qt/Accounts/Provider
%{_includedir}/accounts-qt/Accounts/Service
%{_includedir}/accounts-qt/Accounts/ServiceType
%{_includedir}/accounts-qt/Accounts/*.h
%{_libdir}/libaccounts-qt.so
%{_libdir}/pkgconfig/accounts-qt.pc

%files tests
%defattr(-,root,root,-)
/opt/tests/%{name}

%files doc
%defattr(-,root,root,-)
%doc README COPYING
%{_datadir}/doc/*
