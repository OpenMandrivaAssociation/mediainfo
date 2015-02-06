Name:		mediainfo
Version:	0.7.45
Release:	2
Summary:	Supplies technical and tag information about a video or audio file
Group:		Sound
License:	GPL
URL:		http://mediainfo.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}_%{version}.tar.bz2
Patch0:		mediainfo_0.7.44-fix-qtgui-build.patch
BuildRequires:	dos2unix
BuildRequires:	mediainfo-devel
BuildRequires:	libzen-devel
BuildRequires:	pkgconfig
BuildRequires:	wxgtku2.8-devel
BuildRequires: 	zlib-devel
BuildRequires:	qt4-devel
BuildRequires:	imagemagick

%description
MediaInfo supplies technical and tag information about a video or audio file.

What information can I get from MediaInfo?
* General: title, author, director, album, track number, date, duration...
* Video: codec, aspect, fps, bitrate...
* Audio: codec, sample rate, channels, language, bitrate...
* Text: language of subtitle
* Chapters: number of chapters, list of chapters

DivX, XviD, H263, H.263, H264, x264, ASP, AVC, iTunes, MPEG-1,
MPEG1, MPEG-2, MPEG2, MPEG-4, MPEG4, MP4, M4A, M4V, QuickTime,
RealVideo, RealAudio, RA, RM, MSMPEG4v1, MSMPEG4v2, MSMPEG4v3,
VOB, DVD, WMA, VMW, ASF, 3GP, 3GPP, 3GP2

What format (container) does MediaInfo support?
* Video: MKV, OGM, AVI, DivX, WMV, QuickTime, Real, MPEG-1,
  MPEG-2, MPEG-4, DVD (VOB) (Codecs: DivX, XviD, MSMPEG4, ASP,
  H.264, AVC...)
* Audio: OGG, MP3, WAV, RA, AC3, DTS, AAC, M4A, AU, AIFF
* Subtitles: SRT, SSA, ASS, SAMI

%package gui-wx
Summary:	GUI for %{name}
Group:		Sound
Requires:	%{name}-gui-common = %{version}-%{release}
Provides:	%{name}-gui = %{version}-%{release}

%description gui-wx
Graphical user interface for %{name}.

%package gui-qt
Summary:        GUI for %{name}
Group:          Sound
Requires:	%{name}-gui-common = %{version}-%{release}
Provides:	%{name}-gui = %{version}-%{release}

%description gui-qt
Qt-based graphical user interface for %{name}.

%package gui-common
Summary:        Common files for %{name} GUIs
Group:          Sound
BuildArch:	noarch

%description gui-common
Common files for %{name} GUI packages.

%prep
%setup -q -n MediaInfo
%patch0 -p0 -b .buildfix

# fix EOLs and rights
dos2unix License.html History_*.txt 
chmod 644 *.html *.txt Release/*.txt

%build
# build CLI
pushd Project/GNU/CLI
	autoreconf -vfi
	%configure2_5x --disable-static
	%make
popd

# build GUI
pushd Project/GNU/GUI
	autoreconf -vfi
	%configure2_5x --disable-static
	%make
popd

# build Qt based GUI
pushd Project/QMake/GUI
	%qmake_qt4
	%make
popd

%install
pushd Project/GNU/CLI
	%makeinstall_std
popd

pushd Project/GNU/GUI
	%makeinstall_std
popd

pushd Project/QMake/GUI
	%makeinstall_std INSTALL_ROOT=%{buildroot}
popd

# icon
install -Dm 644 Source/Ressource/Image/MediaInfo.png \
	%{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{name}.png

for i in 16 32 48 64 128; do
	mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/
	convert -scale ${i} Source/Ressource/Image/MediaInfo.png %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/%{name}.png
done

# menu-entry
mkdir -p %{buildroot}/%{_datadir}/applications/
cat > %{buildroot}/%{_datadir}/applications/%{vendor}-%{name}-wx.desktop << EOF
[Desktop Entry]
Type=Application
Name=MediaInfo
Comment=Supplies technical and tag information about a video or audio file
Icon=%{name}
Exec=%{name}-wx %f
Terminal=false
Categories=AudioVideo;AudioVideoEditing;
EOF

mkdir -p %{buildroot}/%{_datadir}/applications/
cat > %{buildroot}/%{_datadir}/applications/%{vendor}-%{name}-qt.desktop << EOF
[Desktop Entry]
Type=Application
Name=MediaInfo
Comment=Supplies technical and tag information about a video or audio file
Icon=%{name}
Exec=%{name}-qt %f
Terminal=false
Categories=AudioVideo;AudioVideoEditing;
EOF

#fix binary name
mv %{buildroot}%{_bindir}/%{name}-gui %{buildroot}%{_bindir}/%{name}-wx

%files
%defattr(-,root,root)
%doc Release/ReadMe_CLI_Linux.txt
%doc License.html History_CLI.txt
%{_bindir}/mediainfo

%files gui-wx
%defattr(-,root,root)
%doc Release/ReadMe_GUI_Linux.txt
%doc License.html History_GUI.txt
%{_bindir}/%{name}-wx
%{_datadir}/applications/%{vendor}-%{name}-wx.desktop

%files gui-common
%{_datadir}/icons/hicolor/*/apps/*.png

%files gui-qt
%defattr(-,root,root)
%{_bindir}/%{name}-qt
%{_datadir}/applications/%{vendor}-%{name}-qt.desktop


%changelog
* Sat Jun 18 2011 Jani Välimaa <wally@mandriva.org> 0.7.45-1mdv2011.0
+ Revision: 685928
- import mediainfo

