# tests are enabled by default
%bcond_without tests

%global         srcname     google-cloud-build
%global         forgeurl    https://github.com/googleapis/python-cloudbuild
Version:        3.5.0
%global         tag         v%{version}
%forgemeta

Name:           python-%{srcname}
Release:        1%{?dist}
Summary:        Python Client for Google Cloud Build API

License:        ASL 2.0
URL:            %forgeurl
Source0:        %forgesource
Patch0:         python-google-cloud-build-mock.patch

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros

%if %{with tests}
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-asyncio)
%endif

%global _description %{expand:
Creates and manages builds on Google Cloud Platform.}

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
%patch0 -p1

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
rm -rf html/.{doctrees,buildinfo} html/objects.inv


%install
%pyproject_install
%pyproject_save_files google

# Remove unnecessary script.
rm -f %{buildroot}%{_bindir}/fixup_cloudbuild*.py


%if %{with tests}
%check
%pytest --import-mode importlib tests/unit
%endif


%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc README.rst CHANGELOG.md
%{python3_sitelib}/google_cloud_build-%{version}-py%{python3_version}-nspkg.pth


%files -n python3-%{srcname}-doc
%license LICENSE
%doc html


%changelog
* Thu Aug 26 2021 Major Hayden <major@mhtx.net> - 3.5.0-1
- First package.
