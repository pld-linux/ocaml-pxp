Summary:	Polimorphic XML Parser for OCaml
Summary(pl):	Polimorficzny Parser XML-a dla OCamla
Name:		ocaml-pxp
Version:	1.1.4
Release:	1
License:	distributable
Group:		Libraries
Vendor:		Gerd Stolpmann <gerd@gerd-stolpmann.de>
URL:		http://www.ocaml-programming.de/programming/pxp.html
Source0:	http://www.ocaml-programming.de/packages/pxp-%{version}.tar.gz
Patch0:		%{name}-sub_lexeme.patch
BuildRequires:	ocaml >= 3.04
BuildRequires:	ocaml-net-netstring-devel
BuildRequires:	ocaml-wlex-devel
BuildRequires:	ocaml-findlib
%requires_eq	ocaml-wlex
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
No main package.

%package devel
Summary:	Polimorphic XML Parser for OCaml - development part
Summary(pl):	Polimorficzny Parser XML-a dla OCamla - cze¶æ programistyczna
Group:		Development/Libraries
%requires_eq	ocaml
%requires_eq	ocaml-net-netstring-devel
%requires_eq	ocaml-wlex-devel

%description devel
This package contains files needed to develop OCaml programs using
this library.

%description devel -l pl
Pakiet ten zawiera pliki niezbêdne do tworzenia programów u¿ywaj±cych
tej biblioteki.

%prep
%setup -q -n pxp-%{version}
%patch0 -p1

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

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -r examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

gzip -9nf doc/{DEV,EXTENSIONS,README,RELEASE-NOTES,SPEC,design.txt} LICENSE

%clean
rm -rf $RPM_BUILD_ROOT

%files devel
%defattr(644,root,root,755)
%doc doc/*.gz *.gz doc/manual/html
%dir %{_libdir}/ocaml/pxp
%{_libdir}/ocaml/pxp/*.cm[ixa]*
%{_libdir}/ocaml/pxp/*.a
%{_examplesdir}/%{name}-%{version}
%{_libdir}/ocaml/site-lib/*
