# tests are enabled by default
%bcond_without tests

%global         srcname     google-cloud-spanner
%global         forgeurl    https://github.com/googleapis/python-spanner
Version:        3.11.0
%global         tag         v%{version}
%forgemeta

Name:           python-%{srcname}
Release:        1%{?dist}
Summary:        Python Client for Google Cloud Spanner

License:        ASL 2.0
URL:            %forgeurl
Source0:        %forgesource
Patch0:         python-google-cloud-spanner-mock.patch

BuildArch:      noarch

BuildRequires:  pyproject-rpm-macros

%if %{with tests}
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-asyncio)
%endif

%global _description %{expand:
Python Client for Google Cloud Spanner}

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


%if %{with tests}
%check
# Work around an unusual pytest/PEP 420 issue where pytest can't import the
# installed module. Thanks to mhroncok for the help!
# NOTE(mhayden): Skip the cursor tests since most of them require credentials
# which are not included in the source repo.
mv google{,_}
%pytest --disable-warnings --ignore=tests/unit/spanner_dbapi/test_cursor.py tests/unit
mv google{_,}
%endif


%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc README.rst CHANGELOG.md
%{python3_sitelib}/google_cloud_spanner-%{version}-py%{python3_version}-nspkg.pth


%files -n python3-%{srcname}-doc
%license LICENSE
%doc html


%changelog
* Thu Aug 26 2021 Major Hayden <major@mhtx.net> - 3.11.0-1
- First package.
