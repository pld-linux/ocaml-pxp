Summary:	Polimorphic XML Parser for OCaml
Summary(pl):	Polimorficzny Parser XML-a dla OCamla
Name:		ocaml-pxp
Version:	1.1.5
Release:	1
License:	distributable
Group:		Libraries
Vendor:		Gerd Stolpmann <gerd@gerd-stolpmann.de>
URL:		http://www.ocaml-programming.de/programming/pxp.html
# Source0-md5:	d462c59148db685309bf9a05f939c184
Source0:	http://www.ocaml-programming.de/packages/pxp-%{version}.tar.gz
BuildRequires:	ocaml >= 3.04
BuildRequires:	ocaml-net-netstring-devel
BuildRequires:	ocaml-wlex-devel
BuildRequires:	ocaml-findlib
%requires_eq	ocaml-wlex
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PXP is a validating parser for XML 1.0 which has been written entirely
in Objective Caml.

PXP means "Polymorphic XML parser" and emphasizes its most useful
property: that the API is polymorphic and can be configured such that
different objects are used to store different types of elements.

%description -l pl
PXP jest waliduj�cym parserem XML 1.0, napisanym w ca�o�ci w OCamlu.

PXP oznacza "Polimorficzny Parser XML", co podkre�la jego najbardziej
u�yteczn� w�asno��: API jest polimorficzne i mo�e by� skonfigurowane
tak, �e r�ne obiekty s� u�ywane do przechowywania r�nych typ�w
element�w.

%package devel
Summary:	Polimorphic XML Parser for OCaml - development part
Summary(pl):	Polimorficzny Parser XML-a dla OCamla - cze�� programistyczna
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

This package contains files needed to develop OCaml programs using
this library.

%description devel -l pl
PXP jest waliduj�cym parserem XML 1.0, napisanym w ca�o�ci w OCamlu.

PXP oznacza "Polimorficzny Parser XML", co podkre�la jego najbardziej
u�yteczn� w�asno��: API jest polimorficzne i mo�e by� skonfigurowane
tak, �e r�ne obiekty s� u�ywane do przechowywania r�nych typ�w
element�w.

Pakiet ten zawiera pliki niezb�dne do tworzenia program�w u�ywaj�cych
tej biblioteki.

%prep
%setup -q -n pxp-%{version}

%build
./configure \
	-with-lex-iso88591 \
	-with-lex-utf8 \
	-with-wlex

sed -e 's/-g//' Makefile.rules > Makefile.rules.tmp
mv -f Makefile.rules.tmp Makefile.rules
%{__make} all opt

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
%doc doc/DEV doc/EXTENSIONS doc/README doc/RELEASE-NOTES doc/SPEC
%doc doc/design.txt LICENSE doc/manual/html
%dir %{_libdir}/ocaml/pxp
%{_libdir}/ocaml/pxp/*
%{_examplesdir}/%{name}-%{version}
%{_libdir}/ocaml/site-lib/*
