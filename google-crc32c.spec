%global         srcname     google-crc32c
%global         reponame    crc32c
%global         forgeurl    https://github.com/google/%{reponame}
Version:        1.1.1
%global         tag         %{version}
%forgemeta -a

Name:           %{srcname}
Release:        1%{?dist}
License:        BSD
Summary:        CRC32C implementation with support for CPU-specific acceleration instructions
Url:            %forgeurl
Source0:        %forgesource

BuildRequires:  cmake
BuildRequires:  gcc-c++

%description
This project collects a few CRC32C implementations under an umbrella that
dispatches to a suitable implementation based on the host computer's hardware
capabilities. CRC32C is specified as the CRC that uses the iSCSI polynomial in
RFC 3720. The polynomial was introduced by G. Castagnoli, S. Braeuer and M.
Herrmann. CRC32C is used in software such as Btrfs, ext4, Ceph and leveldb.


%package devel
Summary:        Development files for google-crc32c
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use google-crc32c.


%prep
%autosetup -n %{reponame}-%{version}


%build
# NOTE(mhayden): Thanks to the Arch Linux developers for providing ideas on how
# to compile this properly. https://aur.archlinux.org/packages/google-crc32c/
%cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DCRC32C_BUILD_BENCHMARKS=OFF \
    -DCRC32C_BUILD_TESTS=OFF \
    -DCRC32C_USE_GLOG=OFF \
    .
%cmake_build


%install
%cmake_install


%files
%license LICENSE
%doc README.md
%{_libdir}/lib%{reponame}.so.1*


%files devel
%license LICENSE
%doc README.md
%{_libdir}/lib%{reponame}.so
%{_libdir}/cmake/Crc32c/
%{_includedir}/%{reponame}


%changelog
* Fri Jul 16 2021 Major Hayden <major@mhtx.net> - 1.1.1-1
- First package.
