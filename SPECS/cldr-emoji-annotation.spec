%global tag_version release-39
#%%global is_official 0%%(echo %%{tag_version} | egrep -q 'alpha|beta|final'; echo $?)
#%%global is_official 0
%global is_official 0

Name:       cldr-emoji-annotation
Version:    39
Release:    2%{?dist}
%if 0%{?fedora:1}%{?rhel:0}
Epoch:      1
%endif
# Annotation files are in Unicode license
Summary:    Emoji annotation files in CLDR
License:    Unicode
URL:        https://unicode.org/cldr
%if %is_official
Source0:    https://github.com/unicode-org/cldr/releases/download/%{tag_version}/cldr-common-%{version}.zip
Source1:    https://raw.githubusercontent.com/unicode-org/cldr/%{tag_version}/README.md#/cldr-README.md
%else
Source0:    https://github.com/unicode-org/cldr/archive/%{tag_version}.zip#/cldr-%{tag_version}.zip
%endif
#Patch0:     %%{name}-HEAD.patch
BuildRequires: autoconf
BuildRequires: automake
BuildArch:  noarch

%description
This package provides the emoji annotation file by language in CLDR.

%package devel
Summary:    Files for development using cldr-annotations
Requires:   %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:   pkgconfig
BuildArch:  noarch

%description devel
This package contains the pkg-config files for development
when building programs that use cldr-emoji-annotations.


%prep
%if %is_official
%autosetup -c -n cldr-%{tag_version}
cp %SOURCE1 README.md
%else
%autosetup -n cldr-%{tag_version}
%endif


%install
pushd $PWD
ANNOTATION_DIR=common/annotations
CLDR_DIR=%{_datadir}/unicode/cldr/$ANNOTATION_DIR
pushd $ANNOTATION_DIR
for xml in *.xml ; do
    install -pm 644 -D $xml $RPM_BUILD_ROOT$CLDR_DIR/$xml
done
popd

ANNOTATION_DIR=common/annotationsDerived
CLDR_DIR=%{_datadir}/unicode/cldr/$ANNOTATION_DIR
pushd $ANNOTATION_DIR
for xml in *.xml ; do
    install -pm 644 -D $xml $RPM_BUILD_ROOT$CLDR_DIR/$xml
done
popd

DTD_DIR=common/dtd
CLDR_DIR=%{_datadir}/unicode/cldr/$DTD_DIR
pushd $DTD_DIR
for dtd in *.dtd ; do
    install -pm 644 -D $dtd $RPM_BUILD_ROOT$CLDR_DIR/$dtd
done
popd

install -pm 755 -d $RPM_BUILD_ROOT%{_datadir}/pkgconfig
cat >> $RPM_BUILD_ROOT%{_datadir}/pkgconfig/%{name}.pc <<_EOF
prefix=/usr

Name: cldr-emoji-annotations
Description: annotation files in CLDR
Version: %{version}
_EOF


%check
ANNOTATION_DIR=common/annotations
CLDR_DIR=%{_datadir}/unicode/cldr/$ANNOTATION_DIR
for xml in $ANNOTATION_DIR/*.xml ; do
    xmllint --noout --valid --postvalid $xml
done

ANNOTATION_DIR=common/annotationsDerived
CLDR_DIR=%{_datadir}/unicode/cldr/$ANNOTATION_DIR
for xml in $ANNOTATION_DIR/*.xml ; do
    xmllint --noout --valid --postvalid $xml
done


%files
%doc README.md readme.html
%license unicode-license.txt
%dir %{_datadir}/unicode
%dir %{_datadir}/unicode/cldr
%dir %{_datadir}/unicode/cldr/common
%{_datadir}/unicode/cldr/common/dtd
%{_datadir}/unicode/cldr/common/annotations
%{_datadir}/unicode/cldr/common/annotationsDerived

%files devel
%{_datadir}/pkgconfig/*.pc

%changelog
* Mon Jun 14 2021 Takao Fujiwara <tfujiwar@gmail.com> - 39-2
- Add gating.yaml. Related: rhbz#1897540

* Mon May 24 2021 Takao Fujiwara <tfujiwar@gmail.com> - 39-1
- Bump to release-39. Related: rhbz#1897540

* Thu Jul 05 2018 Takao Fujiwara <tfujiwar@gmail.com> - 33.1.0_0-1
- Integrated release 33-1

* Wed Jun 20 2018 Takao Fujiwara <tfujiwar@gmail.com> - 33.0.0_2-1
- Changed COPYING

* Thu Apr 12 2018 Takao Fujiwara <tfujiwar@gmail.com> - 33.0.0_1-1
- Integrated release 33

* Fri Mar 09 2018 Takao Fujiwara <tfujiwar@gmail.com> - 32.90.0_1-2
- Removed gcc dependency

* Wed Mar 07 2018 Takao Fujiwara <tfujiwar@gmail.com> - 32.90.0_1-1
- Integrated release-33-alpha

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 32.0.0_1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 30 2017 Takao Fujiwara <tfujiwar@gmail.com> - 32.0.0_1-1
- Integrated release 32

* Thu Sep 28 2017 Takao Fujiwara <tfujiwar@gmail.com> - 31.90.0_1-1
- Integrated release-32-alpha

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 31.0.1_1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Apr 21 2017 Takao Fujiwara <tfujiwar@gmail.com> - 31.0.1_1-1
- Integrated release-31.0.1

* Wed Mar 22 2017 Takao Fujiwara <tfujiwar@gmail.com> - 31.0.0_1-1
- Integrated release-31

* Mon Mar 06 2017 Takao Fujiwara <tfujiwar@gmail.com> - 30.0.3_2-1
- Initial implementation
