#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

Summary:	OAuthlib authentication support for Requests
Summary(pl.UTF-8):	Obsługa uwierzytelniania przez OAuthlib dla Requests
Name:		python3-requests-oauthlib
Version:	2.0.0
Release:	1
License:	ISC
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/requests-oauthlib/
Source0:	https://files.pythonhosted.org/packages/source/r/requests-oauthlib/requests-oauthlib-%{version}.tar.gz
# Source0-md5:	713dc7856f9ff625d75335c10d332a1b
Patch0:		requests-oauthlib-oauthlib3.3.0.patch
URL:		https://github.com/requests/requests-oauthlib
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-cryptography
BuildRequires:	python3-oauthlib >= 3.0.0
BuildRequires:	python3-pyjwt >= 1.0.0
BuildRequires:	python3-requests >= 2.0.0
BuildRequires:	python3-requests-mock
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%{?with_doc:BuildRequires:	sphinx-pdg-3}
Requires:	python3-modules >= 1:3.4
Obsoletes:	python3-requests_oauthlib < 0.6.1-3
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This project provides first-class OAuth library support for Requests.

%description -l pl.UTF-8
Ten pakiet zapewnia obsługę biblioteki OAuth dla Requests.

%package apidocs
Summary:	API documentation for requests-oauthlib module
Summary(pl.UTF-8):	Dokumentacja API biblioteki requests-oauthlib
Group:		Documentation

%description apidocs
API documentation for requests-oauthlib module.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki requests-oauthlib.

%prep
%setup -q -n requests-oauthlib-%{version}
%patch -P0 -p1

# selenium-based, downloads chrome webdriver (x86_64 only anyway)
%{__rm} -r tests/examples

%build
%py3_build

%if %{with tests}
%{__python3} -m unittest discover -s tests
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS.rst HISTORY.rst LICENSE README.rst
%{py3_sitescriptdir}/requests_oauthlib
%{py3_sitescriptdir}/requests_oauthlib-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,examples,*.html,*.js}
%endif
