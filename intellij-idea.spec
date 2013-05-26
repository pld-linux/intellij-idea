%include	/usr/lib/rpm/macros.java
Summary:	IntelliJ IDEA 12 - The Most Intelligent Java IDE
Name:		intellij-idea
Version:	12.1.2
Release:	0.1
License:	Apache v2.0
Group:		Development/Tools
Source0:	http://download.jetbrains.com/idea/ideaIC-%{version}-src.tar.bz2
# Source0-md5:	68cf6340a3ce985cab659944e3ddf926
Source1:	%{name}.desktop
URL:		http://www.jetbrains.org/
BuildRequires:	ant
BuildRequires:	desktop-file-utils
BuildRequires:	jdk >= 1.6
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.596
Requires:	desktop-file-utils
Requires:	jdk >= 1.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# disable debuginfo package, not useful
%define		_enable_debug_packages	0

# use /usr/lib, 64bit files do not conflict with 32bit files (64 suffix)
# this allows to install both arch files and to use 32bit jdk on 64bit os
%define		_appdir		%{_prefix}/lib/%{name}

# rpm5 is so damn slow, so i use this for development:
%define		_noautoreqfiles	.*\.jar

%description
IntelliJ IDEA is a code-centric IDE focused on developer productivity.
The editor deeply understands your code and knows its way around the
codebase, makes great suggestions right when you need them, and is
always ready to help you shape your code.

%prep
%setup -qn ideaIC-129.354

%build
%ant

# keep only single arch files (don't want to pull 32bit deps by default),
# if you want to mix, install rpm from both arch
cd out/dist.unix.ce
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
cd ../..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_bindir},%{_pixmapsdir},%{_desktopdir}}

cd out
cp -l dist.all.ce/build.txt $RPM_BUILD_ROOT/cp-test && l=l && rm -f $RPM_BUILD_ROOT/cp-test
cp -a$l dist.all.ce/{bin,lib,license,plugins} $RPM_BUILD_ROOT%{_appdir}

cp -p dist.unix.ce/bin/idea.png $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png
cp -a$l dist.unix.ce/bin $RPM_BUILD_ROOT%{_appdir}

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
ln -s %{_appdir}/bin/idea.sh $RPM_BUILD_ROOT%{_bindir}/idea

desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database

%files
%defattr(644,root,root,755)
%doc LICENSE.txt README.md
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
