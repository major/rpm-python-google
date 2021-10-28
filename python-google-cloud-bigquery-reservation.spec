# tests are enabled by default
%bcond_without tests

%global         srcname     google-cloud-bigquery-reservation
%global         forgeurl    https://github.com/googleapis/python-bigquery-reservation
Version:        1.4.0
%global         tag         v%{version}
%forgemeta

Name:           python-%{srcname}
Release:        1%{?dist}
Summary:        Python SDK for Google Cloud BigQuery Reservation API

License:        ASL 2.0
URL:            %forgeurl
Source0:        %forgesource
# Use unittest.mock instead of PyPI mock
# (https://fedoraproject.org/wiki/Changes/DeprecatePythonMock).
#
# This simple patch cannot be submitted upstream because they support
# Python 3.6 and 3.7, but use AsyncMock, which was introduced to
# unittest.mock in Python 3.8.
Patch0:         python-google-cloud-bigquery-reservation-mock.patch

BuildArch:      noarch

BuildRequires:  python3-devel

%if %{with tests}
BuildRequires:  python3dist(grpcio-testing)
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-asyncio)
%endif

%global _description %{expand:
BigQuery Reservation API: Modify BigQuery flat-rate reservations.}

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


%if %{with tests}
%check
%pytest --disable-warnings tests/unit
%endif


%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc README.rst CHANGELOG.md CODE_OF_CONDUCT.md CONTRIBUTING.rst SECURITY.md samples
%{python3_sitelib}/google_cloud_bigquery_reservation-%{version}-py%{python3_version}-nspkg.pth


%changelog
* Mon Oct 11 2021 Major Hayden <major@mhtx.net> - 1.3.1-1
- First package.
