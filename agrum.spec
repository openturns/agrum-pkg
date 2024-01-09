%{?__python3: %global __python %{__python3}}
%if 0%{?suse_version}
%global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%else
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Name:           agrum
Version:        1.11.0
Release:        0%{?dist}
Summary:        A GRaphical Universal Modeler
Group:          System Environment/Libraries
License:        LGPLv3+
URL:            http://agrum.gitlab.io/
Source0:        https://gitlab.com/agrumery/aGrUM/-/archive/%{version}/aGrUM-%{version}.tar.bz2
BuildRequires:  gcc-c++, cmake
BuildRequires:  python3-devel
BuildRequires:  python3-numpy
BuildRequires:  python3-six
BuildRequires:  python3-pydot
BuildRequires:  python3-matplotlib
Requires:       libagrum0

%description
aGrUM is a C++ library for graphical models.
It is designed for easily building applications using graphical models such as Bayesian networks,
influence diagrams, decision trees, GAI networks or Markov decision processes.

%package -n libagrum0
Summary:        AGrUM library files
Group:          Development/Libraries/C and C++

%description -n libagrum0
Dynamic libraries for aGrUM.

%package devel
Summary:        AGrUM development files
Group:          Development/Libraries/C and C++
Requires:       libagrum0 = %{version}

%description devel
Development files for aGrUM library.

%package examples
Summary:        AGrUM examples
Group:          Productivity/Scientific/Math

%description examples
Example files for aGrUM

%package -n python3-%{name}
Summary:        AGrUM Python module
Group:          Productivity/Scientific/Math
Requires:       python3-numpy
Requires:       python3-six
Requires:       python3-pydot
Requires:       python3-matplotlib
%description -n python3-%{name}
Python textual interface to aGrUM library

%prep
%setup -q -n aGrUM-%{version}
sed -i "s|sys.log|logging.warning|g" wrappers/pyAgrum/testunits/testsOnPython.py

%build
%cmake -DCMAKE_SKIP_INSTALL_RPATH:BOOL=ON -DBUILD_PYTHON=ON
%cmake_build

%install
%cmake_install

%check
LD_LIBRARY_PATH=%{buildroot}%{_libdir} PYTHONPATH=%{buildroot}%{python_sitearch} %{__python} ./wrappers/pyAgrum/testunits/gumTest.py

%post -n libagrum0 -p /sbin/ldconfig 
%postun -n libagrum0 -p /sbin/ldconfig 

%files -n libagrum0
%defattr(-,root,root,-)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_libdir}/*.so
%{_libdir}/cmake/
%{_libdir}/pkgconfig/

%files -n python3-%{name}
%defattr(-,root,root,-)
%{python_sitearch}/pyAgrum*


%changelog
* Mon Nov 05 2018 Julien Schueller <schueller at phimeca dot com> 0.13.3-1
- Initial package creation

