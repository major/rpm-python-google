# Tests disabled by default since they require network access.
%bcond_with tests

%global         srcname     grafeas
%global         forgeurl    https://github.com/googleapis/python-grafeas
Version:        1.3.0
%global         tag         v%{version}
%forgemeta

Name:           python-%{srcname}
Release:        1%{?dist}
Summary:        Python SDK for Google Cloud Grafeas API

License:        ASL 2.0
URL:            %forgeurl
Source0:        %forgesource
# Use unittest.mock instead of PyPI mock
# (https://fedoraproject.org/wiki/Changes/DeprecatePythonMock).
#
# This simple patch cannot be submitted upstream because they support
# Python 3.6 and 3.7, but use AsyncMock, which was introduced to
# unittest.mock in Python 3.8.
Patch0:         python-grafeas-mock.patch

BuildArch:      noarch

BuildRequires:  python3-devel

%if %{with tests}
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-asyncio)
%endif

%global _description %{expand:
Grafeas API: An implementation of the Grafeas API, which stores, and enables
querying and retrieval of critical metadata about all of your software
artifacts.}

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
%pyproject_save_files grafeas

# Remove unnecessary scripts.
rm -f %{buildroot}%{_bindir}/fixup*


%if %{with tests}
%check
%pytest --disable-warnings tests/unit
%endif


%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.rst CHANGELOG.md CODE_OF_CONDUCT.md CONTRIBUTING.rst SECURITY.md UPGRADING.md samples
%{python3_sitelib}/grafeas-%{version}-py%{python3_version}-nspkg.pth


%changelog
* Mon Oct 11 2021 Major Hayden <major@mhtx.net> - 1.3.0-1
- First package.
