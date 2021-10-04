# tests are enabled by default
%bcond_without tests

%global         srcname     google-cloud-firestore
%global         forgeurl    https://github.com/googleapis/python-firestore
Version:        2.3.1
%global         tag         v%{version}
%forgemeta

Name:           python-%{srcname}
Release:        1%{?dist}
Summary:        Python Client for Google Cloud Firestore API

License:        ASL 2.0
URL:            %forgeurl
Source0:        %forgesource
# Use unittest.mock instead of PyPI backport package mock
# https://github.com/googleapis/python-firestore/issues/445
Patch0:         python-google-cloud-firestore-mock.patch
# Fix intersphinx mappings.
Patch1:         python-google-cloud-firestore-intersphinx-mappings.patch

BuildArch:      noarch

BuildRequires:  python3-devel

# Documentation
BuildRequires:  grpc-doc
BuildRequires:  python3-proto-plus-doc

%if %{with tests}
BuildRequires:  python3dist(aiounittest)
BuildRequires:  python3dist(google-cloud-testutils)
BuildRequires:  python3dist(pytest)
%endif

%global _description %{expand:
The Google Cloud Firestore API is a flexible, scalable database for mobile,
web, and server development from Firebase and Google Cloud Platform.}

%description %{_description}


%package -n python3-%{srcname}
Summary:        %{summary}

%description -n python3-%{srcname} %{_description}


%package -n python3-%{srcname}-doc
Requires:       python3-docs
Requires:       python3-proto-plus-doc
Requires:       grpc-doc
BuildRequires:  python3dist(recommonmark)
BuildRequires:  python3dist(sphinx)
Summary:        Documentation for python-%{srcname}

%description -n python3-%{srcname}-doc
Documentation for python-%{srcname}


%prep
%forgeautosetup -p1


%generate_buildrequires
%pyproject_buildrequires -r


%build
%pyproject_wheel

# Generate documentation.
PYTHONPATH="${PWD}:${PWD}/docs/" sphinx-build docs html %{?_smp_mflags}
rm -rf html/.{doctrees,buildinfo}


%install
%pyproject_install
%pyproject_save_files google

# Remove unnecessary script.
rm -f %{buildroot}%{_bindir}/fixup_firestore*.py


%if %{with tests}
%check
# Some of the tests here have unusual relative imports, so we need to add the
# tests to PYTHONPATH.
mkdir /tmp/testpath
cp -ar tests /tmp/testpath

# The test_bulk_writer file has lots of tests that require connectivity with
# Google's API endpoints.
PYTHONPATH=%{buildroot}%{python3_sitelib}:/tmp/testpath \
    %pytest --import-mode importlib --disable-warnings \
        --ignore tests/unit/v1/test_bulk_writer.py tests/unit
%endif


%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc README.rst CHANGELOG.md
%{python3_sitelib}/google_cloud_firestore-%{version}-py%{python3_version}-nspkg.pth


%files -n python3-%{srcname}-doc
%license LICENSE
%doc html


%changelog
* Thu Aug 26 2021 Major Hayden <major@mhtx.net> - 2.3.1-1
- First package.
