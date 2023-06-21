%global kf5_version 5.107.0

%global wayland_min_version 1.3

Name: opt-kf5-kwayland
Version: 5.107.0
Release: 3%{?dist}
Summary: KDE Frameworks 5 library that wraps Client and Server Wayland libraries

License: GPLv2+
URL:     https://invent.kde.org/frameworks/kwayland
Source0: %{name}-%{version}.tar.bz2

Patch1: 0001-Use-pkg-config-to-find-EGL.patch

%{?opt_kf5_default_filter}

BuildRequires: make
BuildRequires: opt-extra-cmake-modules >= %{version}
BuildRequires: opt-kf5-rpm-macros >= %{version}
BuildRequires: opt-qt5-qtbase-devel
# https://bugs.kde.org/show_bug.cgi?id=365569#c8 claims this is needed
BuildRequires: opt-qt5-qtbase-private-devel
BuildRequires: opt-qt5-qtbase-static

BuildRequires: wayland-devel >= %{wayland_min_version}
BuildRequires: wayland-protocols-devel
BuildRequires: opt-qt5-qttools-devel

# cmake(Qt5WaylandClient)
BuildRequires: opt-qt5-qtwayland-devel
# cmake(PlasmaWaylandProtocols) > 1.1
BuildRequires: plasma-wayland-protocols-devel > 1.1
BuildRequires: pkgconfig(egl)

%{?_opt_qt5:Requires: %{_opt_qt5}%{?_isa} = %{_opt_qt5_version}}
Requires: opt-qt5-qtbase-gui
Requires: opt-qt5-qtwayland

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       opt-qt5-qtbase-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -n %{name}-%{version}/upstream -p1


%build
export QTDIR=%{_opt_qt5_prefix}
touch .git

mkdir -p build
pushd build

%_opt_cmake_kf5 ../ \
  -DBUILD_TESTING:BOOL=OFF
%make_build

popd

%install
pushd build
make DESTDIR=%{buildroot} install
popd

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSES/*.txt
%{_opt_kf5_datadir}/qlogging-categories5/*categories
%{_opt_kf5_libdir}/libKF5WaylandClient.so.5*
%{_opt_kf5_libdir}/libKF5WaylandServer.so.5*

%files devel
%{_opt_kf5_includedir}/KF5/KWayland/
%{_opt_kf5_libdir}/cmake/KF5Wayland/
%{_opt_kf5_libdir}/libKF5WaylandClient.so
%{_opt_kf5_libdir}/libKF5WaylandServer.so
%{_opt_kf5_libdir}/pkgconfig/KF5WaylandClient.pc
%{_opt_kf5_archdatadir}/mkspecs/modules/qt_KWaylandClient.pri
%{_opt_kf5_archdatadir}/mkspecs/modules/qt_KWaylandServer.pri
%{_opt_kf5_libexecdir}/org-kde-kf5-kwayland-testserver
