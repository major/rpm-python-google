# tests are enabled by default
%bcond_without tests

# https://pypi.org/project/pyarrow not yet packaged
%bcond_with pyarrow

%global         srcname     google-cloud-bigquery-storage
%global         forgeurl    https://github.com/googleapis/python-bigquery-storage
Version:        2.9.1
%global         tag         v%{version}
%forgemeta

Name:           python-%{srcname}
Release:        1%{?dist}
Summary:        Python SDK for Google Cloud BigQuery Storage API

License:        ASL 2.0
URL:            %forgeurl
Source0:        %forgesource
# Use unittest.mock instead of PyPI mock
# (https://fedoraproject.org/wiki/Changes/DeprecatePythonMock).
#
# This simple patch cannot be submitted upstream because they support
# Python 3.6 and 3.7, but use AsyncMock, which was introduced to
# unittest.mock in Python 3.8.
Patch0:         python-google-cloud-bigquery-storage-mock.patch

# The base package is arched because extras metapackages requiring fastavro are
# not available on 32-bit architectures
# (https://bugzilla.redhat.com/show_bug.cgi?id=1943932).
%ifnarch %{arm32} %{ix86}
%global fastavro_arch 1
%endif
# Of the binary RPMs, only the conditionally-enabled extras metapackage
# python3-google-cloud-bigquery-storage+fastavro is arched.
#
# Since there is no compiled code, there are no debugging symbols.
%global debug_package %{nil}

BuildRequires:  python3-devel

%if %{with tests}
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-asyncio)
%endif

%global _description %{expand:
Python SDK for Google Cloud BigQuery Storage API}

%description %{_description}


%package -n python3-%{srcname}
Summary:        %{summary}
BuildArch:      noarch

%description -n python3-%{srcname} %{_description}

# We would have to write out the extras metapackage definitions manually if
# we wanted them to be noarch, since the base package is arched.
%pyproject_extras_subpkg -n python3-%{srcname} pandas %{?with_pyarrow:pyarrow}

%if 0%{?fastavro_arch}
# Note that this metapackage is arched because it is not available on 32-bit
# architectures.
%pyproject_extras_subpkg -n python3-%{srcname} fastavro
%endif


%prep
%forgeautosetup -p1


%generate_buildrequires
%pyproject_buildrequires -x pandas%{?with_pyarrow:,pyarrow}%{?fastavro_arch:,fastavro},tests


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files google

# Remove unnecessary scripts.
rm -f %{buildroot}%{_bindir}/fixup*.py


%if %{with tests}
%check
%pytest %{?!fastavro_arch:--ignore=tests/unit/test_reader_v1.py} \
    --disable-warnings tests/unit
%endif


%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.rst CHANGELOG.md CODE_OF_CONDUCT.md CONTRIBUTING.rst SECURITY.md UPGRADING.md samples
%{python3_sitelib}/google_cloud_bigquery_storage-%{version}-py%{python3_version}-nspkg.pth


%changelog
* Mon Oct 11 2021 Major Hayden <major@mhtx.net> - 2.9.1-1
- First package.
