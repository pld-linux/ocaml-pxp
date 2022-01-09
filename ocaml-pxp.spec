#
# Conditional build:
%bcond_without	ocaml_opt	# native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), update when upstream will support it
%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

Summary:	Polimorphic XML Parser for OCaml
Summary(pl.UTF-8):	Polimorficzny analizator składniowy XML-a dla OCamla
Name:		ocaml-pxp
Version:	1.2.9
Release:	3
License:	distributable
Group:		Libraries
Source0:	http://download.camlcity.org/download/pxp-%{version}.tar.gz
# Source0-md5:	8002253eade813b8355500f4c59f8da8
Patch0:		%{name}-debian-build-fix.patch
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
Conflicts:	ocaml-pxp-devel < 1.2.9-3
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
Summary(pl.UTF-8):	Polimorficzny analizator składniowy XML-a dla OCamla - część programistyczna
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

Pakiet ten zawiera pliki niezbędne do tworzenia programów w OCamlu
używających biblioteki PXP.

%prep
%setup -q -n pxp-%{version}
%patch0 -p1

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
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml

OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml \
%{__make} install

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -pr examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/README doc/SPEC
%dir %{_libdir}/ocaml/pxp
%{_libdir}/ocaml/pxp/META
%dir %{_libdir}/ocaml/pxp-engine
%{_libdir}/ocaml/pxp-engine/META
%{_libdir}/ocaml/pxp-engine/*.cma
%dir %{_libdir}/ocaml/pxp-lex-iso8859*
%{_libdir}/ocaml/pxp-lex-iso8859*/META
%{_libdir}/ocaml/pxp-lex-iso8859*/*.cma
%{_libdir}/ocaml/pxp-lex-utf8/META
%{_libdir}/ocaml/pxp-lex-utf8/*.cma
%dir %{_libdir}/ocaml/pxp-pp
%{_libdir}/ocaml/pxp-pp/META
%{_libdir}/ocaml/pxp-pp/*.cma
%dir %{_libdir}/ocaml/pxp-ulex-utf8
%{_libdir}/ocaml/pxp-ulex-utf8/META
%{_libdir}/ocaml/pxp-ulex-utf8/*.cma

%files devel
%defattr(644,root,root,755)
%doc doc/design.txt doc/manual/html
%{_libdir}/ocaml/pxp-engine/*.cmi
%{_libdir}/ocaml/pxp-engine/*.cmo
%{_libdir}/ocaml/pxp-engine/*.mli
%{_libdir}/ocaml/pxp-lex-iso8859*/*.cmi
%{_libdir}/ocaml/pxp-lex-iso8859*/*.cmo
%{_libdir}/ocaml/pxp-lex-utf8/*.cmi
%{_libdir}/ocaml/pxp-lex-utf8/*.cmo
%{_libdir}/ocaml/pxp-ulex-utf8/*.cmi
%{_libdir}/ocaml/pxp-ulex-utf8/*.cmo
%if %{with ocaml_opt}
%{_libdir}/ocaml/pxp-engine/*.a
%{_libdir}/ocaml/pxp-engine/*.cmxa
%{_libdir}/ocaml/pxp-lex-iso8859*/*.a
%{_libdir}/ocaml/pxp-lex-iso8859*/*.cmx
%{_libdir}/ocaml/pxp-lex-iso8859*/*.cmxa
%{_libdir}/ocaml/pxp-lex-iso8859*/*.o
%{_libdir}/ocaml/pxp-lex-utf8/*.a
%{_libdir}/ocaml/pxp-lex-utf8/*.cmx
%{_libdir}/ocaml/pxp-lex-utf8/*.cmxa
%{_libdir}/ocaml/pxp-lex-utf8/*.o
%{_libdir}/ocaml/pxp-ulex-utf8/*.a
%{_libdir}/ocaml/pxp-ulex-utf8/*.cmx
%{_libdir}/ocaml/pxp-ulex-utf8/*.cmxa
%{_libdir}/ocaml/pxp-ulex-utf8/*.o
%endif
%{_examplesdir}/%{name}-%{version}
