# tests are enabled by default
%bcond_without tests

%global         srcname     google-cloud-testutils
%global         forgeurl    https://github.com/googleapis/python-test-utils
Version:        1.1.0
%global         tag         v%{version}
%forgemeta

Name:           python-%{srcname}
Release:        1%{?dist}
Summary:        Python test utilities for Google Cloud APIs

License:        ASL 2.0
URL:            %forgeurl
Source0:        %forgesource

BuildArch:      noarch

BuildRequires:  python3-devel

%if %{with tests}
BuildRequires:  python3dist(pytest)
%endif

%global _description %{expand:
This is a collection of common tools used in system tests of Python client
libraries for Google APIs.}

%description %{_description}


%package -n python3-%{srcname}
%py_provides    python3-test-utils
Summary:        %{summary}

%description -n python3-%{srcname} %{_description}


%prep
%forgesetup


%generate_buildrequires
%pyproject_buildrequires -r


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files test_utils

# Remove extra scripts and tests.
rm -rf %{buildroot}%{python3_sitelib}/{scripts,tests}
rm -f %{buildroot}%{_bindir}/lower-bound-checker


%if %{with tests}
%check
%python3 -m unittest discover tests/unit/
%endif


%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc README.rst CHANGELOG.md CODE_OF_CONDUCT.md SECURITY.md


%changelog
* Thu Aug 26 2021 Major Hayden <major@mhtx.net> - 1.1.0-1
- First package.
