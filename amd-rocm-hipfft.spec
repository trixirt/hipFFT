%global commit0 1d01f7c47069c2b6dc8f936ab0dcc793aa308987
%global _lto_cflags %{nil}
%global build_cxxflags %{nil}
%global build_ldflags %{nil}
%global _name amd-rocm-hipfft
%global rocm_path /opt/rocm
%global hipcc %{rocm_path}/bin/hipcc
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global toolchain clang
%global up_name hipFFT

%define patch_level 1
%bcond_with debug
%bcond_with static

%if %{without debug}
  %if %{without static}
    %global suf %{nil}
  %else
    %global suf -static
  %endif
%else
  %if %{without static}
    %global suf -debug
  %else
    %global suf -static-debug
  %endif
%endif

Name: %{_name}%{suf}

Version:        5.6
Release:        %{patch_level}.git%{?shortcommit0}%{?dist}
Summary:        TBD
License:        TBD

URL:            https://github.com/trixirt/%{up_name}
Source0:        %{url}/archive/%{commit0}/%{up_name}-%{shortcommit0}.tar.gz

BuildRequires:  cmake

%global debug_package %{nil}

%description
TBD

%package devel
Summary:        TBD

%description devel
%{summary}

%prep
%autosetup -p1 -n %{up_name}-%{commit0}

%build
%cmake \
%if %{with static}
       -DBUILD_SHARED_LIBS=OFF \
%endif
%if %{without debug}
       -DCMAKE_BUILD_TYPE=RELEASE \
%else
       -DCMAKE_BUILD_TYPE=DEBUG \
%endif
       -DCMAKE_C_COMPILER=%{hipcc} \
       -DCMAKE_CXX_COMPILER=%{hipcc} \
       -DCMAKE_EXE_LINKER_FLAGS=-L%{rocm_path}/lib64 \
       -DCMAKE_INSTALL_PREFIX=%{rocm_path} \
       -DCMAKE_SHARED_LINKER_FLAGS=-L%{rocm_path}/lib64

export LD_LIBRARY_PATH=%{rocm_path}/lib64
%cmake_build

%install
%cmake_install

%files devel
%{rocm_path}

%changelog
* Mon Aug 07 2023 Tom Rix <trix@redhat.com>
- Stub something together
