#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	6.16
%define		qtver		6.5.0
%define		kfname		kwindowsystem

Summary:	Access to the windowing system
Name:		kf6-%{kfname}
Version:	6.16.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	257e0f9177950df8f9380d8b7cfe25a8
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6Qml-devel >= %{qtver}
BuildRequires:	Qt6WaylandClient-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	libstdc++-devel
BuildRequires:	libxcb-devel
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	plasma-wayland-protocols-devel >= 1.15.0
BuildRequires:	qt6-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	wayland-protocols >= 1.21
BuildRequires:	xcb-util-keysyms-devel
BuildRequires:	xcb-util-wm-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXfixes-devel
BuildRequires:	xorg-lib-libxkbcommon-devel
BuildRequires:	xz
Requires:	Qt6Core >= %{qtver}
Requires:	Qt6Gui >= %{qtver}
Requires:	Qt6Qml >= %{qtver}
Requires:	Qt6WaylandClient >= %{qtver}
Requires:	kf6-dirs
#Obsoletes:	kf5-%{kfname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
Convenience access to certain properties and features of the windowing
system.

KWindowSystem provides information about the windowing system and
allows interaction with the windowing system. It provides an high
level API which is windowing system independent and has platform
specific implementations. This API is inspired by X11 and thus not all
functionality is available on all windowing systems.

In addition to the high level API, this framework also provides
several more low level classes for interaction with the X Windowing
System.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt6Widgets-devel >= %{qtver}
#Obsoletes:	kf5-%{kfname}-devel < %{version}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kfname}5_qt --with-qm --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kfname}5_qt.lang
%defattr(644,root,root,755)
%doc README.md
%ghost %{_libdir}/libKF6WindowSystem.so.6
%attr(755,root,root) %{_libdir}/libKF6WindowSystem.so.*.*
%dir %{_libdir}/qt6/plugins/kf6/kwindowsystem
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/kwindowsystem/KF6WindowSystemX11Plugin.so
%{_datadir}/qlogging-categories6/kwindowsystem.renamecategories
%{_datadir}/qlogging-categories6/kwindowsystem.categories
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/kwindowsystem/KF6WindowSystemKWaylandPlugin.so
%dir %{_libdir}/qt6/qml/org/kde/kwindowsystem
%{_libdir}/qt6/qml/org/kde/kwindowsystem/KWindowSystem.qmltypes
%{_libdir}/qt6/qml/org/kde/kwindowsystem/kde-qmlmodule.version
%attr(755,root,root) %{_libdir}/qt6/qml/org/kde/kwindowsystem/libKWindowSystem.so
%{_libdir}/qt6/qml/org/kde/kwindowsystem/qmldir

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF6/KWindowSystem
%{_libdir}/cmake/KF6WindowSystem
%{_libdir}/libKF6WindowSystem.so
%{_pkgconfigdir}/KF6WindowSystem.pc
