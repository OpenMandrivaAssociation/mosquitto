%global _disable_ld_no_undefined 1

%define libname %mklibname mosquitto 1
%define pplibname %mklibname mosquittopp 1
%define devname %mklibname -d mosquitto
%define ppdevname %mklibname -d mosquittopp

Summary:	MQTT protocol message broker
Name:		mosquitto
Version:	2.0.15
Release:	1
Group:		System/Libraries
License:	EPL/EDL	
URL:		https://mosquitto.org/
Source0:	https://mosquitto.org/files/source/mosquitto-%{version}.tar.gz
BuildRequires:	cmake ninja
BuildRequires:	pkgconfig(libcares)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(systemd)
BuildRequires:	xsltproc
BuildRequires:	docbook-style-xsl

%description
Eclipse Mosquitto is an open source (EPL/EDL licensed) message broker that
implements the MQTT protocol versions 5.0, 3.1.1 and 3.1.
Mosquitto is lightweight and is suitable for use on all devices from low
power single board computers to full servers.

The MQTT protocol provides a lightweight method of carrying out messaging
using a publish/subscribe model. This makes it suitable for Internet of
Things messaging such as with low power sensors or mobile devices such
as phones, embedded computers or microcontrollers.

The Mosquitto project also provides a C library for implementing MQTT
clients, and the very popular mosquitto_pub and mosquitto_sub command line
MQTT clients.

%package -n %{libname}
Summary:	Library for handling the MQTT protocol

%description -n %{libname}
Library for handling the MQTT protocol

%files -n %{libname}
%{_libdir}/libmosquitto.so.*

%package -n %{pplibname}
Summary:	Library for handling the MQTT protocol in C++
Requires:	%{libname} = %{EVRD}

%description -n %{pplibname}
Library for handling the MQTT protocol in C++

%files -n %{pplibname}
%{_libdir}/libmosquittopp.so.*

%package -n %{devname}
Summary:	Development files for the Mosquitto MQTT library
Requires:	%{libname} = %{EVRD}

%description -n %{devname}
Development files for the Mosquitto MQTT library

%files -n %{devname}
%{_includedir}/mosquitto.h
%{_includedir}/mosquitto_broker.h
%{_includedir}/mosquitto_plugin.h
%{_includedir}/mqtt_protocol.h
%{_libdir}/libmosquitto.so
%{_libdir}/pkgconfig/libmosquitto.pc

%package -n %{ppdevname}
Summary:	Development files for the Mosquitto MQTT C++ library
Requires:	%{devname} = %{EVRD}
Requires:	%{pplibname} = %{EVRD}

%description -n %{ppdevname}
Development files for the Mosquitto MQTT C++ library

%files -n %{ppdevname}
%{_includedir}/mosquittopp.h
%{_libdir}/libmosquittopp.so
%{_libdir}/pkgconfig/libmosquittopp.pc

%prep
%autosetup -p1
%cmake -G Ninja \
	-DWITH_SRV:BOOL=ON \
	-DWITH_SYSTEMD:BOOL=ON \
	-DCMAKE_INSTALL_SYSCONFDIR=%{_sysconfdir}

# FIXME once we have the deps:
#	-DWITH_DLT:BOOL=ON \
#	-DWITH_WEBSOCKETS:BOOL=ON

%build
%ninja_build -C build

%install
%ninja_install -C build

%files
%{_bindir}/mosquitto_passwd
%{_bindir}/mosquitto_pub
%{_bindir}/mosquitto_rr
%{_bindir}/mosquitto_sub
%dir %{_sysconfdir}/mosquitto
%{_sysconfdir}/mosquitto/aclfile.example
%{_sysconfdir}/mosquitto/mosquitto.conf
%{_sysconfdir}/mosquitto/pskfile.example
%{_sysconfdir}/mosquitto/pwfile.example
%{_sbindir}/mosquitto
%{_mandir}/man1/mosquitto_ctrl.1*
%{_mandir}/man1/mosquitto_ctrl_dynsec.1*
%{_mandir}/man1/mosquitto_passwd.1*
%{_mandir}/man1/mosquitto_pub.1*
%{_mandir}/man1/mosquitto_rr.1*
%{_mandir}/man1/mosquitto_sub.1*
%{_mandir}/man3/libmosquitto.3*
%{_mandir}/man5/mosquitto.conf.5*
%{_mandir}/man7/mosquitto-tls.7*
%{_mandir}/man7/mqtt.7*
%{_mandir}/man8/mosquitto.8*
