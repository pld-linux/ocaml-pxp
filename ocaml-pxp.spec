%define		ocaml_ver	1:3.09.2
Summary:	Polimorphic XML Parser for OCaml
Summary(pl.UTF-8):	Polimorficzny analizator składniowy XML-a dla OCamla
Name:		ocaml-pxp
Version:	1.1.6
Release:	9
License:	distributable
Group:		Libraries
Source0:	http://www.ocaml-programming.de/packages/pxp-%{version}.tar.gz
# Source0-md5:	8f1c26e348405fb7f064b4bc2584ab59
URL:		http://www.ocaml-programming.de/programming/pxp.html
BuildRequires:	ocaml >= %{ocaml_devel}
BuildRequires:	ocaml-findlib
BuildRequires:	ocaml-net-netstring-devel >= 1.1.1-2
BuildRequires:	ocaml-wlex-devel
BuildRequires:	sed >= 4.0
%requires_eq	ocaml-wlex
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
%requires_eq	ocaml-wlex-devel

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
	-with-lex-iso88591 \
	-with-lex-utf8 \
	-with-wlex

sed -i -e 's/-g//' Makefile.rules
%{__make} -j1 \
	all opt

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
rm $RPM_BUILD_ROOT%{_libdir}/ocaml/pxp/*.{o,mli}

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -r examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files devel
%defattr(644,root,root,755)
%doc doc/ABOUT-FINDLIB doc/EXTENSIONS doc/README doc/RELEASE-NOTES doc/SPEC
%doc doc/design.txt LICENSE doc/manual/html
%dir %{_libdir}/ocaml/pxp
%{_libdir}/ocaml/pxp/*
%{_examplesdir}/%{name}-%{version}
%{_libdir}/ocaml/site-lib/*
