# tests are enabled by default
%bcond_without tests

%global         srcname     google-resumable-media
%global         forgeurl    https://github.com/googleapis/google-resumable-media-python
Version:        1.3.1
%global         tag         v%{version}
%forgemeta

Name:           python-%{srcname}
Release:        1%{?dist}
Summary:        Utilities for Google media downloads and resumable uploads

License:        ASL 2.0
URL:            %forgeurl
Source0:        %forgesource
Patch0:         python-google-resumable-media-mock-fix.patch

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros

%if %{with tests}
BuildRequires:  python3dist(google-auth)
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(aiohttp)
%endif

%global _description %{expand:
Utilities for Google media downloads and resumable uploads}

%description %{_description}


%package -n python3-%{srcname}
Summary:        %{summary}

%description -n python3-%{srcname} %{_description}


%package -n python3-%{srcname}-doc
Requires:       python3-docs
BuildRequires:  python3-docs
BuildRequires:  python3dist(recommonmark)
BuildRequires:  python3dist(sphinx)
Summary:        Documentation for python-%{srcname}

%description -n python3-%{srcname}-doc
Documentation for python-%{srcname}


%prep
%forgesetup
%patch0 -p0

# Use local inventory in intersphinx mapping.
sed -r -i -e \
    's|https://docs.python.org/3|/%{_docdir}/python3-docs/html|' \
    docs/conf.py


%generate_buildrequires
%pyproject_buildrequires -r


%build
%pyproject_wheel

# Generate documentation.
PYTHONPATH="${PWD}:${PWD}/docs/" sphinx-build docs html
rm -rf html/.{doctrees,buildinfo}


%install
%pyproject_install
%pyproject_save_files google


%if %{with tests}
%check
# Some of the tests import code from other tests, so we need to copy them
# elsewhere and add them to PYTHONPATH.
mkdir temp_tests
cp -r tests temp_tests/

PYTHONPATH=%{buildroot}%{python3_sitelib}:$(pwd)/temp_tests \
    %pytest --import-mode importlib tests/unit tests_async/unit
%endif


%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc README.rst CHANGELOG.md
%{python3_sitelib}/google_resumable_media-%{version}-py%{python3_version}-nspkg.pth


%files -n python3-%{srcname}-doc
%license LICENSE
%doc html


%changelog
* Thu Jul 15 2021 Major Hayden <major@mhtx.net> - 1.3.1-1
- First package.
