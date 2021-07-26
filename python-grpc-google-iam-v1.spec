# NOTE(mhayden): No tests are provided with the pypi package.
%global         srcname     grpc-google-iam-v1

Name:           python-%{srcname}
Version:        0.12.3
Release:        1%{?dist}
Summary:        GRPC library for the google-iam-v1 service

License:        ASL 2.0
URL:            https://pypi.org/project/%{srcname}/
Source0:        %pypi_source

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros


%global _description %{expand:
The IDL-derived library for the google-iam (v1) service in Google Cloud.}

%description %{_description}


%package -n python3-%{srcname}
Summary:        %{summary}

%description -n python3-%{srcname} %{_description}


%prep
%autosetup -n %{srcname}-%{version}


%generate_buildrequires
%pyproject_buildrequires -r


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files google


%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc README.rst
%{python3_sitelib}/grpc_google_iam_v1-%{version}-py%{python3_version}-nspkg.pth


%changelog
* Thu Jul 15 2021 Major Hayden <major@mhtx.net> - 1.0.0-1
- First package.
