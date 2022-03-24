# tests are enabled by default
%bcond_without tests

%global         srcname     google-cloud-bigquery-datatransfer
%global         forgeurl    https://github.com/googleapis/python-bigquery-datatransfer
Version:        3.4.0
%global         tag         v%{version}
%forgemeta

Name:           python-%{srcname}
Release:        1%{?dist}
Summary:        Python SDK for Google Cloud BigQuery Data Transfer API

License:        ASL 2.0
URL:            %forgeurl
Source0:        %forgesource
# Use unittest.mock instead of PyPI mock
# (https://fedoraproject.org/wiki/Changes/DeprecatePythonMock).
#
# This simple patch cannot be submitted upstream because they support
# Python 3.6 and 3.7, but use AsyncMock, which was introduced to
# unittest.mock in Python 3.8.
Patch0:         python-google-cloud-bigquery-datatransfer-mock.patch

BuildArch:      noarch

BuildRequires:  python3-devel

%if %{with tests}
BuildRequires:  python3dist(grpcio-testing)
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-asyncio)
%endif

%global _description %{expand:
The BigQuery Data Transfer API allows users to transfer data from partner SaaS
applications to Google BigQuery on a scheduled, managed basis.}

%description %{_description}


%package -n python3-%{srcname}
Summary:        %{summary}

%description -n python3-%{srcname} %{_description}

%pyproject_extras_subpkg -n python3-%{srcname} libcst


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
rm -f %{buildroot}%{_bindir}/fixup_bigquery_datatransfer_v1_keywords.py

%if %{with tests}
%check
%pytest --disable-warnings tests/unit
%endif


%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.rst CHANGELOG.md CODE_OF_CONDUCT.md CONTRIBUTING.rst SECURITY.md UPGRADING.md samples
%{python3_sitelib}/google_cloud_bigquery_datatransfer-%{version}-py%{python3_version}-nspkg.pth


%changelog
* Mon Oct 11 2021 Major Hayden <major@mhtx.net> - 3.4.0-1
- First package.
