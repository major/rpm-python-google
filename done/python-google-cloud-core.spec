# tests are enabled by default
%bcond_without tests

%global         srcname     google-cloud-core
%global         forgeurl    https://github.com/googleapis/python-cloud-core
Version:        1.7.1
%global         tag         v%{version}
%forgemeta

Name:           python-%{srcname}
Release:        1%{?dist}
Summary:        Core Helpers for Google Cloud Python Client Library

License:        ASL 2.0
URL:            %forgeurl
Source0:        %forgesource
# Fix mock > unittest.mock. Made PRs to upstream and they are aware but not
# accepting patches for this right now.
# Example: https://github.com/googleapis/python-api-core/pull/208
Patch0:         python-google-cloud-core-mock-fix.patch

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros

%if %{with tests}
BuildRequires:  python3dist(pytest)
%endif

%global _description %{expand:
This library is not meant to stand-alone. Instead it defines common helpers
(e.g. base Client classes) used by all of the google-cloud-* packages.}

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

# Build the grpc extras subpackage.
%pyproject_extras_subpkg -n python3-%{srcname} grpc


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
%pytest --import-mode importlib tests
%endif


%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc README.rst CHANGELOG.md
%{python3_sitelib}/google_cloud_core-%{version}-py%{python3_version}-nspkg.pth


%files -n python3-%{srcname}-doc
%license LICENSE
%doc html


%changelog
* Thu Jul 15 2021 Major Hayden <major@mhtx.net> - 1.7.1-1
- First package.
