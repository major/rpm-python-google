# 🔥 Requires tensorflow, which requires a complicated build w/Bazel.

# tests are enabled by default
%bcond_without tests

%global         srcname     google-cloud-aiplatform
%global         forgeurl    https://github.com/googleapis/python-aiplatform
Version:        1.5.0
%global         tag         v%{version}
%forgemeta

Name:           python-%{srcname}
Release:        1%{?dist}
Summary:        Python SDK for Vertex AI on Google Cloud

License:        ASL 2.0
URL:            %forgeurl
Source0:        %forgesource
Patch0:         python-google-cloud-aiplatform-mock.patch

BuildArch:      noarch

BuildRequires:  pyproject-rpm-macros

%if %{with tests}
BuildRequires:  python3dist(grpcio-testing)
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-asyncio)
%endif

%global _description %{expand:
A Python SDK for Vertex AI, a fully managed, end-to-end platform for data
science and machine learning.}

%description %{_description}


%package -n python3-%{srcname}
Summary:        %{summary}

%description -n python3-%{srcname} %{_description}


%package -n python3-%{srcname}-doc
BuildRequires:  python3dist(recommonmark)
BuildRequires:  python3dist(sphinx)
BuildRequires:  python3dist(sphinx-rtd-theme)
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
%pytest --disable-warnings tests/unit
%endif


%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc README.rst CHANGELOG.md


%files -n python3-%{srcname}-doc
%license LICENSE
%doc html


%changelog
* Mon Oct 11 2021 Major Hayden <major@mhtx.net> - 1.5.0-1
- First package.
