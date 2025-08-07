Summary:	Supplies technical and tag information about a video or audio file
Name:	mediainfo
Version:	25.07
Release:	1
License:	BSD-2-Clause-Patent
Group:	Sound
Url:		https://mediaarea.net/en/MediaInfo
Source0:	https://mediaarea.net/download/source/%{name}/%{version}/%{name}_%{version}.tar.bz2
BuildRequires:	dos2unix
BuildRequires:	imagemagick
BuildRequires:	ncurses
BuildRequires:	qmake-qt6
BuildRequires:qt6-qttools-linguist-tools
BuildRequires:	wxwidgets-devel
BuildRequires:	pkgconfig(libmediainfo) >= 25.07
BuildRequires:	pkgconfig(libzen) >= 0.4.41
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:	cmake(Qt6LinguistTools)
BuildRequires:	cmake(Qt6Network)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:	cmake(Qt6Xml)
BuildRequires:	cmake(Qt6WebEngineWidgets)
BuildRequires:	pkgconfig(pyside6)
BuildRequires:	pkgconfig(zlib)

%description
MediaInfo supplies technical and tag information about a video or audio file.
What information can I get from MediaInfo?
* General: title, author, director, album, track number, date, duration...
* Video: codec, aspect, fps, bitrate...
* Audio: codec, sample rate, channels, language, bitrate...
* Text: language of subtitle.
* Chapters: number of chapters, list of chapters.
* DivX, XviD, H263, H.263, H264, x264, ASP, AVC, iTunes, MPEG-1/2, MPEG1/2,
MPEG-4, MPEG4, MP4, M4A, M4V, QuickTime, RealVideo, RealAudio, RA, RM,
MSMPEG4v1, MSMPEG4v2, MSMPEG4v3, VOB, DVD, WMA, VMW, ASF, 3GP, 3GPP, 3GP2.
What format (container) does MediaInfo support?
* Video: MKV, OGM, AVI, DivX, WMV, QuickTime, Real, MPEG-1,
  MPEG-2, MPEG-4, DVD (VOB) (Codecs: DivX, XviD, MSMPEG4, ASP,
  H.264, AVC...).
* Audio: OGG, MP3, WAV, RA, AC3, DTS, AAC, M4A, AU, AIFF.
* Subtitles: SRT, SSA, ASS, SAMI.

%files
%doc Release/ReadMe_CLI_Linux.txt
%doc LICENSE History_CLI.txt
%{_bindir}/%{name}

#-----------------------------------------------------------------------------

%package gui-wx
Summary:	GUI for %{name}
Group:	Sound
Requires:	%{name}-gui-common = %{version}-%{release}
Provides:	%{name}-gui = %{version}-%{release}

%description gui-wx
Graphical user interface for %{name}.

%files gui-wx
%doc Release/ReadMe_GUI_Linux.txt
%doc License.html History_GUI.txt
%{_bindir}/%{name}-wx
%{_datadir}/applications/%{name}-wx.desktop
%{_datadir}/applications/%{name}-gui.desktop

#-----------------------------------------------------------------------------

%package gui-qt
Summary:		GUI for %{name}
Group:	Sound
Requires:	%{name}-gui-common = %{version}-%{release}
Provides:	%{name}-gui = %{version}-%{release}

%description gui-qt
Qt-based graphical user interface for %{name}.

%files gui-qt
%{_bindir}/%{name}-gui
%{_bindir}/%{name}-qt
%{_datadir}/applications/%{name}-qt.desktop

#-----------------------------------------------------------------------------

%package gui-common
Summary:		Common files for %{name} GUIs
Group:	Sound
BuildArch:	noarch

%description gui-common
Common files for %{name} GUI packages.

%files gui-common
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/metainfo/%{name}-gui.metainfo.xml
%{_datadir}/pixmaps/%{name}.xpm
%{_datadir}/icons/hicolor/*/apps/*.svg
%{_datadir}/kio/servicemenus/%{name}-gui.desktop

#-----------------------------------------------------------------------------

%prep
%autosetup -p1 -n MediaInfo

# Fix EOLs and rights
dos2unix License.html History_*.txt 
chmod 644 *.html *.txt Release/*.txt


%build
# Build CLI
pushd Project/GNU/CLI
	autoreconf -vfi
	%configure --disable-static
	%make_build
popd

# Build wxwidgets based GUI
pushd Project/GNU/GUI
	autoreconf -vfi
	%configure --disable-static
	%make_build
popd

# Build Qt based GUI
pushd Project/QMake/GUI
	qmake-qt6
	%make_build
popd


%install
pushd Project/GNU/CLI
	%make_install
popd

pushd Project/GNU/GUI
	%make_install
	# Fix binary name
	mv %{buildroot}%{_bindir}/%{name}-gui %{buildroot}%{_bindir}/%{name}-wx
popd

pushd Project/QMake/GUI
	%make_install INSTALL_ROOT=%{buildroot}
	mv %{buildroot}%{_bindir}/%{name}-gui %{buildroot}%{_bindir}/%{name}-qt
	ln -s %{name}-qt %{buildroot}%{_bindir}/%{name}-gui
popd

#  Provide more icons
for i in 16 32 48 64 128; do
	mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/
	convert -scale ${i} Source/Resource/Image/MediaInfo.png %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/%{name}.png
done

# Add menu entries for GUI apps
mkdir -p %{buildroot}%{_datadir}/applications/
cat > %{buildroot}%{_datadir}/applications/%{name}-wx.desktop << EOF
[Desktop Entry]
Type=Application
Name=MediaInfo
Comment=Supplies technical and tag information about a video or audio file
Icon=%{name}
Exec=%{name}-wx %f
Terminal=false
Categories=AudioVideo;AudioVideoEditing;
EOF

mkdir -p %{buildroot}%{_datadir}/applications/
cat > %{buildroot}%{_datadir}/applications/%{name}-qt.desktop << EOF
[Desktop Entry]
Type=Application
Name=MediaInfo
Comment=Supplies technical and tag information about a video or audio file
Icon=%{name}
Exec=%{name}-qt %f
Terminal=false
Categories=AudioVideo;AudioVideoEditing;
EOF

# Put the servicemenu file where dolphin can find it and remove older stuff
mkdir -p %{buildroot}%{_datadir}/kio/servicemenus
cp %{buildroot}%{_datadir}/kservices5/ServiceMenus/%{name}-gui.desktop %{buildroot}%{_datadir}/kio/servicemenus
rm -f %{buildroot}%{_datadir}/apps/konqueror/servicemenus/%{name}-gui.desktop
rm -f %{buildroot}%{_datadir}/kde4/services/ServiceMenus/%{name}-gui.desktop
rm -f %{buildroot}%{_datadir}/kservices5/ServiceMenus/%{name}-gui.desktop
