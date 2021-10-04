# tests are enabled by default
%bcond_without tests

%global         srcname     google-cloud-automl
%global         forgeurl    https://github.com/googleapis/python-automl
Version:        2.4.2
%global         tag         v%{version}
%forgemeta

Name:           python-%{srcname}
Release:        1%{?dist}
Summary:        Python Client for Google Cloud AutoML API

License:        ASL 2.0
URL:            %forgeurl
Source0:        %forgesource
Patch0:         python-google-cloud-automl-mock.patch

BuildArch:      noarch

BuildRequires:  pyproject-rpm-macros

%if %{with tests}
BuildRequires:  python3dist(google-cloud-storage)
BuildRequires:  python3dist(pandas)
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-asyncio)
%endif

%global _description %{expand:
The Cloud AutoML API is a suite of machine learning products that enables
developers with limited machine learning expertise to train high-quality
models specific to their business needs, by leveraging Google’s
state-of-the-art transfer learning, and Neural Architecture Search technology.}

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

# Remove extra scripts.
rm -f %{buildroot}%{_bindir}/fixup_automl*.py


%if %{with tests}
%check
# Work around an unusual pytest/PEP 420 issue where pytest can't import the
# installed module. Thanks to mhroncok for the help!
# NOTE(mhayden): The test_prediction_client_client_info requires some
# credentials which are not included in the source repo.
mv google{,_}
%pytest --disable-warnings -k "not test_prediction_client_client_info" tests/unit
mv google{_,}
%endif


%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc README.rst CHANGELOG.md
%{python3_sitelib}/google_cloud_automl-%{version}-py%{python3_version}-nspkg.pth


%files -n python3-%{srcname}-doc
%license LICENSE
%doc html


%changelog
* Thu Aug 26 2021 Major Hayden <major@mhtx.net> - 2.4.2-1
- First package.
