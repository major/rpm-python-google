# tests are enabled by default
%bcond_without tests

%global         srcname     google-cloud-containeranalysis
%global         forgeurl    https://github.com/googleapis/python-containeranalysis
Version:        2.6.0
%global         tag         v%{version}
%forgemeta

Name:           python-%{srcname}
Release:        1%{?dist}
Summary:        Python SDK for Google Cloud Container Analysis API

License:        ASL 2.0
URL:            %forgeurl
Source0:        %forgesource
# Use unittest.mock instead of PyPI mock
# (https://fedoraproject.org/wiki/Changes/DeprecatePythonMock).
#
# This simple patch cannot be submitted upstream because they support
# Python 3.6 and 3.7, but use AsyncMock, which was introduced to
# unittest.mock in Python 3.8.
Patch0:         python-google-cloud-containeranalysis-mock.patch
# Upstream has a bug that prevents the libcst exta from installing properly.
# PR made: https://github.com/googleapis/python-containeranalysis/pull/202
Patch1:         python-google-cloud-containeranalysis-libcst.patch

BuildArch:      noarch

BuildRequires:  python3-devel

%if %{with tests}
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-asyncio)
%endif

%global _description %{expand:
Container Analysis API: An implementation of the Grafeas API, which stores, and
enables querying and retrieval of critical metadata about all of your software
artifacts.}

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

# Remove unnecessary files.
rm -f %{buildroot}%{_bindir}/fixup* samples/snippets/.gitignore


%if %{with tests}
%check
# Disable two tests that require network connectivity.
%pytest --disable-warnings tests/unit \
    -k "not test_get_grafeas_client and not test_get_grafeas_client_async"
%endif


%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.rst CHANGELOG.md CODE_OF_CONDUCT.md CONTRIBUTING.rst SECURITY.md UPGRADING.md samples
%{python3_sitelib}/google_cloud_containeranalysis-%{version}-py%{python3_version}-nspkg.pth


%changelog
* Mon Oct 11 2021 Major Hayden <major@mhtx.net> - 2.6.0-1
- First package.
