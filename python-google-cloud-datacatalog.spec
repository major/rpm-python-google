# tests are enabled by default
%bcond_without tests

%global         srcname     google-cloud-datacatalog
%global         forgeurl    https://github.com/googleapis/python-datacatalog
Version:        3.4.3
%global         tag         v%{version}
%forgemeta

Name:           python-%{srcname}
Release:        1%{?dist}
Summary:        Python SDK for Google Cloud Data Catalog API

License:        ASL 2.0
URL:            %forgeurl
Source0:        %forgesource
# Use unittest.mock instead of PyPI mock
# (https://fedoraproject.org/wiki/Changes/DeprecatePythonMock).
#
# This simple patch cannot be submitted upstream because they support
# Python 3.6 and 3.7, but use AsyncMock, which was introduced to
# unittest.mock in Python 3.8.
Patch0:         python-google-cloud-datacatalog-mock.patch

BuildArch:      noarch

BuildRequires:  python3-devel

%if %{with tests}
BuildRequires:  python3dist(fastavro)
BuildRequires:  python3dist(freezegun)
BuildRequires:  python3dist(pandas)
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-asyncio)
%endif

%global _description %{expand:
Google Cloud Data Catalog API: Google Cloud Data Catalog API provides features
to attach metadata to Google Cloud Platform resources like BigQuery Tables. Key
critical resources include: Entries (Data Catalog representation of a cloud
resource).}

%description %{_description}


%package -n python3-%{srcname}
Summary:        %{summary}

%description -n python3-%{srcname} %{_description}


%prep
%forgeautosetup -p1


%generate_buildrequires
%pyproject_buildrequires -r


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files google

# Remove unnecessary scripts.
rm -f %{buildroot}%{_bindir}/fixup*


%if %{with tests}
%check
%pytest --disable-warnings tests/unit
%endif


%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.rst CHANGELOG.md CODE_OF_CONDUCT.md CONTRIBUTING.rst SECURITY.md UPGRADING.md samples
%{python3_sitelib}/google_cloud_datacatalog-%{version}-py%{python3_version}-nspkg.pth


%changelog
* Mon Oct 11 2021 Major Hayden <major@mhtx.net> - 3.4.3-1
- First package.
