%global upstreamname hipFFT
%global rocm_release 6.0
%global rocm_patch 0
%global rocm_version %{rocm_release}.%{rocm_patch}

%global toolchain rocm
# hipcc does not support some clang flags
%global build_cxxflags %(echo %{optflags} | sed -e 's/-fstack-protector-strong/-Xarch_host -fstack-protector-strong/' -e 's/-fcf-protection/-Xarch_host -fcf-protection/')

# Tests are downloaded so this option is only good for local building
# Also need to
# export QA_RPATHS=0xff
%bcond_with test

# gfortran and clang rpm macros do not mix
%global build_fflags %{nil}

Name:           hipfft
Version:        %{rocm_version}
Release:        1%{?dist}
Summary:        ROCm FFT marshalling library
Url:            https://github.com/ROCmSoftwarePlatform/%{upstreamname}
License:        MIT

# Only x86_64 works right now:
ExclusiveArch:  x86_64

Source0:        %{url}/archive/refs/tags/rocm-%{rocm_version}.tar.gz#/%{upstreamname}-%{rocm_version}.tar.gz
Patch0:         0001-Use-system-s-rocfft-headers.patch

BuildRequires:  cmake
BuildRequires:  compiler-rt
BuildRequires:  clang-devel
BuildRequires:  gcc-gfortran
BuildRequires:  lld
BuildRequires:  llvm-devel
BuildRequires:  ninja-build
BuildRequires:  rocm-cmake
BuildRequires:  rocm-comgr-devel
BuildRequires:  rocm-hip-devel
BuildRequires:  rocm-runtime-devel
BuildRequires:  rocm-rpm-macros
BuildRequires:  rocprim-devel
BuildRequires:  rocfft-devel

%if %{with test}
BuildRequires:  gtest-devel
BuildRequires:  libomp-devel
BuildRequires:  rocblas-devel
%endif

%description
hipFFT is an FFT marshalling library. Currently, hipFFT supports
the rocFFT backends

hipFFT exports an interface that does not require the client to
change, regardless of the chosen backend. It sits between the
application and the backend FFT library, marshalling inputs into
the backend and results back to the application.

%package devel
Summary:        Libraries and headers for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
%{summary}

%if %{with test}
%package test
Summary:        Tests for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description test
%{summary}
%endif

%prep
%autosetup -p1 -n %{upstreamname}-rocm-%{version}

%build
%cmake -G Ninja \
       -DBUILD_FILE_REORG_BACKWARD_COMPATIBILITY=OFF \
       -DROCM_SYMLINK_LIBS=OFF \
       -DHIP_PLATFORM=amd \
       -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
       -DCMAKE_BUILD_TYPE=RelWithDebInfo

%cmake_build

%install
%cmake_install

%files
%license LICENSE.md
%exclude %{_docdir}/%{name}/LICENSE.md
%{_libdir}/lib%{name}.so.*

%files devel
%dir %{_libdir}/cmake/%{name}

%doc README.md
%{_includedir}/%{name}
%{_libdir}/cmake/%{name}/*.cmake
%{_libdir}/lib%{name}.so

%changelog
* Sat Jan 6 2024 Tom Rix <trix@redhat.com> - 6.0.0-1
- Update to 6.0.0

* Wed Dec 20 2023 Tom Rix <trix@redhat.com>  - 5.7.1-1
- Initial package

