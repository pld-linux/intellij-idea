# TODO
# - build from source: http://www.jetbrains.org/
%include	/usr/lib/rpm/macros.java
Summary:	IntelliJ IDEA 11 - The Most Intelligent Java IDE
Name:		intellij-idea
Version:	11.1.4
Release:	0.1
License:	Apache v2.0
Group:		Development/Tools
Source0:	http://download-ln.jetbrains.com/idea/ideaIC-%{version}.tar.gz
# NoSource0-md5:	3c85588bb0b89ff565c64b38da1eddc0
NoSource:	0
Source1:	%{name}.desktop
URL:		https://www.jetbrains.com/idea/
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	jdk >= 1.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# disable debuginfo package, not useful
%define		_enable_debug_packages	0

# use /usr/lib, 64bit files do not conflict with 32bit files (64 suffix)
# this allows to install both arch files and to use 32bit jdk on 64bit os
%define		_appdir		%{_prefix}/lib/%{name}
%define		_noautoreqfiles	.*

%description
IntelliJ IDEA is a code-centric IDE focused on developer productivity.
The editor deeply understands your code and knows its way around the
codebase, makes great suggestions right when you need them, and is
always ready to help you shape your code.

%prep
%setup -qn idea-IC-117.963

# keep only single arch files (don't want to pull 32bit deps by default),
# if you want to mix, install rpm from both arch
%ifarch %{ix86}
rm bin/fsnotifier64
rm bin/libbreakgen64.so
rm bin/idea64.vmoptions
%endif
%ifarch %{x8664}
rm bin/fsnotifier
rm bin/libbreakgen.so
rm bin/idea.vmoptions
%endif
chmod a+rx bin/*.so bin/fsnotifier*
mv bin/idea.png .

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_bindir},%{_pixmapsdir},%{_desktopdir}}
cp -l build.txt $RPM_BUILD_ROOT/cp-test && l=l && rm -f $RPM_BUILD_ROOT/cp-test
cp -p idea.png $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png
cp -a$l bin lib license plugins $RPM_BUILD_ROOT%{_appdir}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
ln -s %{_appdir}/bin/idea.sh $RPM_BUILD_ROOT%{_bindir}/idea

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/idea
%dir %{_appdir}
%{_appdir}/lib
%{_appdir}/license
%{_appdir}/plugins
%dir %{_appdir}/bin
%{_appdir}/bin/idea*.vmoptions
%{_appdir}/bin/appletviewer.policy
%{_appdir}/bin/idea.properties
%{_appdir}/bin/log.xml
%attr(755,root,root) %{_appdir}/bin/idea.sh
%attr(755,root,root) %{_appdir}/bin/inspect.sh
%attr(755,root,root) %{_appdir}/bin/fsnotifier*
%attr(755,root,root) %{_appdir}/bin/libbreakgen*.so
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/%{name}.png
