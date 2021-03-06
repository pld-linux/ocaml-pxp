#
# Conditional build:
%bcond_without	ocaml_opt	# skip building native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), remove when upstream will support it
%ifnarch %{ix86} %{x8664} arm aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

Summary:	Polimorphic XML Parser for OCaml
Summary(pl.UTF-8):	Polimorficzny analizator składniowy XML-a dla OCamla
Name:		ocaml-pxp
Version:	1.2.9
Release:	2
License:	distributable
Group:		Libraries
Source0:	http://download.camlcity.org/download/pxp-%{version}.tar.gz
# Source0-md5:	8002253eade813b8355500f4c59f8da8
URL:		http://projects.camlcity.org/projects/pxp.html
BuildRequires:	ocaml >= 1:3.09.2
BuildRequires:	ocaml-camlp4
BuildRequires:	ocaml-findlib
BuildRequires:	ocaml-ocamldoc-devel
BuildRequires:	ocaml-net-netstring-devel >= 3.6-2
BuildRequires:	ocaml-net-netsys-devel >= 3.6-2
BuildRequires:	ocaml-net-netunidata-devel
BuildRequires:	ocaml-ulex
BuildRequires:	sed >= 4.0
BuildConflicts:	ocaml-wlex-devel
%requires_eq	ocaml-ulex
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PXP is a validating parser for XML 1.0 which has been written entirely
in Objective Caml.

PXP means "Polymorphic XML Parser" and emphasizes its most useful
property: that the API is polymorphic and can be configured such that
different objects are used to store different types of elements.

%description -l pl.UTF-8
PXP jest walidującym analizatorem składniowym XML-a 1.0, napisanym w
całości w OCamlu.

PXP oznacza "Polymorphic XML Parser" (polimorficzny analizator
składniowy XML-a), co podkreśla jego najbardziej użyteczną własność:
API jest polimorficzne i może być skonfigurowane tak, że różne obiekty
są używane do przechowywania różnych typów elementów.

%package devel
Summary:	Polimorphic XML Parser for OCaml - development part
Summary(pl.UTF-8):	Polimorficzny analizator składniowy XML-a dla OCamla - cześć programistyczna
Group:		Development/Libraries
%requires_eq	ocaml
%requires_eq	ocaml-net-netstring-devel

%description devel
PXP is a validating parser for XML 1.0 which has been written entirely
in Objective Caml.

PXP means "Polymorphic XML parser" and emphasizes its most useful
property: that the API is polymorphic and can be configured such that
different objects are used to store different types of elements.

This package contains files needed to develop OCaml programs using the
PXP library.

%description devel -l pl.UTF-8
PXP jest walidującym analizatorem składniowym XML-a 1.0, napisanym w
całości w OCamlu.

PXP oznacza "Polymorphic XML Parser" (polimorficzny analizator
składniowy XML-a), co podkreśla jego najbardziej użyteczną własność:
API jest polimorficzne i może być skonfigurowane tak, że różne obiekty
są używane do przechowywania różnych typów elementów.

Pakiet ten zawiera pliki niezbędne do tworzenia programów używających
biblioteki PXP.

%prep
%setup -q -n pxp-%{version}

%build
./configure \
	-with-lex \
	-with-ulex \
	-without-wlex \
	-with-pp

sed -i -e 's/-g//' Makefile.rules
%{__make} -j1 \
	all %{?with_ocaml_opt:opt}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/{site-lib,pxp}
OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib %{__make} install
dir=`pwd`
cd $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib
for f in * ; do
	echo 'directory = "+pxp"' >> $f/META
	if [ "`echo $f/*.*`" != "$f/*.*" ]; then
		mv $f/*.* $RPM_BUILD_ROOT%{_libdir}/ocaml/pxp
	fi
done
cd $dir

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -r examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files devel
%defattr(644,root,root,755)
%doc doc/README doc/SPEC
%doc doc/design.txt doc/manual/html
%dir %{_libdir}/ocaml/pxp
%{_libdir}/ocaml/pxp/*.cm[xi]
%{_libdir}/ocaml/pxp/*.cma
%{_libdir}/ocaml/pxp/*.cmo
%{_libdir}/ocaml/pxp/*.mli
%if %{with ocaml_opt}
%{_libdir}/ocaml/pxp/*.[ao]
%{_libdir}/ocaml/pxp/*.cmxa
%endif
%{_examplesdir}/%{name}-%{version}
%{_libdir}/ocaml/site-lib/*
