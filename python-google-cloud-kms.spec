# tests are enabled by default
%bcond_without tests

%global         srcname     google-cloud-kms
%global         forgeurl    https://github.com/googleapis/python-kms
Version:        2.4.0
%global         tag         v%{version}
%forgemeta

Name:           python-%{srcname}
Release:        1%{?dist}
Summary:        Python Client for Google Cloud Key Management Service (KMS) API

License:        ASL 2.0
URL:            %forgeurl
Source0:        %forgesource
# Fix mock > unittest.mock. Made PRs to upstream and they are aware but not
# accepting patches for this right now.
Patch0:         python-google-cloud-kms-mock-fix.patch

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros

%if %{with tests}
BuildRequires:  python3dist(cryptography)
BuildRequires:  python3dist(pem)
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-asyncio)
%endif

%global _description %{expand:
Manages keys and performs cryptographic operations in a central cloud service,
for direct use by other cloud resources and applications via the Google
Cloud Key Management Service (KMS) API.}

%description %{_description}


%package -n python3-%{srcname}
Summary:        %{summary}

%description -n python3-%{srcname} %{_description}


%package -n python3-%{srcname}-doc
Requires:       python3-docs
BuildRequires:  python3-docs
BuildRequires:  python3dist(recommonmark)
BuildRequires:  python3dist(sphinx)
BuildRequires:  python3dist(sphinx-rtd-theme)
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

# Remove unneeded executable.
rm -f %{buildroot}/%{_bindir}/fixup_kms_v1_keywords.py


%if %{with tests}
%check
%pytest --ignore=samples --ignore tests/system
%endif


%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc README.rst CHANGELOG.md
%{python3_sitelib}/google_cloud_kms-%{version}-py%{python3_version}-nspkg.pth


%files -n python3-%{srcname}-doc
%license LICENSE
%doc html


%changelog
* Thu Jul 15 2021 Major Hayden <major@mhtx.net> - 2.4.0-1
- First package.
