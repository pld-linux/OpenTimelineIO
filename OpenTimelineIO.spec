#
# Conditional build:
%bcond_with	tests		# build with tests
%define		rjcommit	24b5e7a8b27f42fa16b96fc70aade9106cf7102f
Summary:	OpenTimelineIO
Name:		OpenTimelineIO
Version:	0.18.1
Release:	1
License:	Apache v2.0
Group:		X11/Libraries
Source0:	https://github.com/AcademySoftwareFoundation/OpenTimelineIO/archive/refs/tags/v%{version}.tar.gz
# Source0-md5:	7b13298f151ad5bd2d4a74c0c66bfa41
Source1:	https://github.com/Tencent/rapidjson/archive/%{rjcommit}/rapidjson-%{rjcommit}.tar.gz
# Source1-md5:	531f76775e11b09b28422bfa1d4d59b5
Patch0:		0002-CMake-fixes.patch
URL:		http://opentimeline.io/
BuildRequires:	Imath-devel
BuildRequires:	cmake >= 3.16
BuildRequires:	ninja
BuildRequires:	rapidjson-devel >= 1.1.1
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
OpenTimelineIO is an interchange format and API for editorial cut
information. OTIO contains information about the order and length of
cuts and references to external media. It is not however, a container
format for media.

%package devel
Summary:	Header files for %{name} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{name}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{name}.

%prep
%setup -q -a1
%patch -P0 -p1
# Imath: system version used via OTIO_FIND_MATH
# rapidjson: snapshot needed for APIs added since last release
find src/deps/{Imath,rapidjson} -delete
mv rapidjson-%{rjcommit} src/deps/rapidjson

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DOTIO_FIND_IMATH=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc *.md *.pdf *.txt
%ghost %{_libdir}/libopentime.so.18
%{_libdir}/libopentime.so.*.*
%ghost %{_libdir}/libopentimelineio.so.18
%{_libdir}/libopentimelineio.so.*.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/opentime
%{_includedir}/opentimelineio
%{_libdir}/cmake/opentime
%{_libdir}/cmake/opentimelineio
%{_libdir}/libopentime.so
%{_libdir}/libopentimelineio.so
