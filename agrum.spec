# norootforbuild
%global __python %{__python2}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

%define __cmake %{_bindir}/cmake
%define _cmake_lib_suffix64 -DLIB_SUFFIX=64
%define cmake \
CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ; \
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ; \
FFLAGS="${FFLAGS:-%optflags}" ; export FFLAGS ; \
%__cmake \\\
-DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \\\
%if "%{?_lib}" == "lib64" \
%{?_cmake_lib_suffix64} \\\
%endif \
-DBUILD_SHARED_LIBS:BOOL=ON

Name:           agrum
Version:        0.14.1
Release:        0%{?dist}
Summary:        A GRaphical Universal Modeler
Group:          System Environment/Libraries
License:        GPLv3+
URL:            http://agrum.gitlab.io/
Source0:        https://gitlab.com/agrumery/aGrUM/-/archive/%{version}/aGrUM-%{version}.tar.bz2
Patch0:         cmake28.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:  gcc-c++, cmake
BuildRequires:  python-devel
%if 0%{?centos_version}
BuildRequires:  numpy
%else
BuildRequires:  python-numpy
%endif
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

%package -n python-%{name}
Summary:        AGrUM Python module
Group:          Productivity/Scientific/Math
%if 0%{?centos_version}
Requires:       numpy
%else
Requires:       python-numpy
%endif
%description -n python-%{name}
Python textual interface to aGrUM library

%prep
%setup -q -n aGrUM-%{version}
%patch0 -p1

%build
%cmake -DINSTALL_DESTDIR:PATH=%{buildroot} \
       -DCMAKE_SKIP_INSTALL_RPATH:BOOL=ON \
       -DPYTHON_EXECUTABLE=%{__python} \
       .
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -r %{buildroot}%{python_sitearch}/pyAgrum/causal

%check
LD_LIBRARY_PATH=%{buildroot}%{_libdir} PYTHONPATH=%{buildroot}%{python_sitearch} %{__python} ./wrappers/pyAgrum/testunits/gumTest.py

%clean
rm -rf %{buildroot}

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

%files -n python-%{name}
%defattr(-,root,root,-)
%{python_sitearch}/pyAgrum*


%changelog
* Mon Nov 05 2018 Julien Schueller <schueller at phimeca dot com> 0.13.3-1
- Initial package creation

