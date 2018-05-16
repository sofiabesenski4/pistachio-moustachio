#!/bin/bash
#Script written by Umair <umair@noobslab.com> Mon, 08 Sep 2014 02:24:08 +0200
#Updated on Tue, 18 Oct 2016 10:31:08 +0200
#Site: http://www.NoobsLab.com
if [ $EUID -ne 0 ]; then
   echo "AdobeAir installation script must be run as root. (Hint: use sudo)" 1>&2
   exit 1
fi
echo "
This script is only for Ubuntu `printf "\e[32m16.04 Xenial"``echo -e "\033[0m"`/`printf "\e[32m15.10 Wily"``echo -e "\033[0m"`/`printf "\e[32m15.04 Vivid"``echo -e "\033[0m"`/`printf "\e[32m14.04 Trusty"``echo -e "\033[0m"`/`printf "\e[32m12.04 Precise"``echo -e "\033[0m"` and Linux Mint `printf "\e[32m17.x"``echo -e "\033[0m"`/`printf "\e[32m17"``echo -e "\033[0m"`/`printf "\e[32m13"``echo -e "\033[0m"`
"
CHKVer=`/usr/bin/lsb_release -rs`
TVer=`/usr/bin/lsb_release -rs`
echo "Checking your OS version..."
CHKArch=`uname -m`
echo "Checking your system architecture"
sleep 1
echo ""
if [ $CHKVer = "14.04" ] || [ $CHKVer = "17" ]; then
	#For Ubuntu 14.04 64bit
	if [ $CHKArch = "x86_64" ]; then
		if [ $TVer = "14.04" ]; then
		echo "You are running Ubuntu `printf "\e[32m14.04 Trusty"``echo -e "\033[0m"`"
		elif [ $TVer = "17" ]; then
		echo "You are running Linux Mint `printf "\e[32m17 Qiana"``echo -e "\033[0m"`"
		fi
		echo "Installing dependencies..."
		sleep 1
		apt-get install libxt6:i386 libnspr4-0d:i386 libgtk2.0-0:i386 libstdc++6:i386 libnss3-1d:i386 lib32nss-mdns libxml2:i386 libxslt1.1:i386 libcanberra-gtk-module:i386 gtk2-engines-murrine:i386 libgnome-keyring0:i386 libxaw7
		echo "Linking files..."
		echo "."
		ln -sf /usr/lib/x86_64-linux-gnu/libgnome-keyring.so.0 /usr/lib/libgnome-keyring.so.0
		echo ".."
		ln -sf /usr/lib/x86_64-linux-gnu/libgnome-keyring.so.0.2.0 /usr/lib/libgnome-keyring.so.0.2.0
	#Ubuntu 14.04 32bit
	elif [ $CHKArch = "i686" ]; then
		if [ $TVer = "14.04" ]; then
		echo "You are running Ubuntu `printf "\e[32m14.04 Trusty"``echo -e "\033[0m"`"
		elif [ $TVer = "17" ]; then
		echo "You are running Linux Mint `printf "\e[32m17 Qiana"``echo -e "\033[0m"`"
		fi
		echo "Installing dependencies..."
		sleep 1
		apt-get install libgtk2.0-0 libxslt1.1 libxml2 libnss3 libxaw7 libgnome-keyring0
		echo "Linking files..."
		echo "."
		ln -sf /usr/lib/i386-linux-gnu/libgnome-keyring.so.0 /usr/lib/libgnome-keyring.so.0
		echo ".."
		ln -sf /usr/lib/i386-linux-gnu/libgnome-keyring.so.0.2.0 /usr/lib/libgnome-keyring.so.0.2.0
	fi

elif [ $CHKVer = "14.04.1" ] || [ $CHKVer = "17.1" ]; then
	#For Ubuntu 14.04.1 64bit
	if [ $CHKArch = "x86_64" ]; then
		if [ $TVer = "14.04.1" ]; then
		echo "You are running Ubuntu `printf "\e[32m14.04.1 Trusty"``echo -e "\033[0m"`"
		elif [ $TVer = "17.1" ]; then
		echo "You are running Linux Mint `printf "\e[32m17.1 Rebecca"``echo -e "\033[0m"`"
		fi
		echo "Installing dependencies..."
		sleep 1
		apt-get install libxt6:i386 libnspr4-0d:i386 libgtk2.0-0:i386 libstdc++6:i386 libnss3-1d:i386 lib32nss-mdns libxml2:i386 libxslt1.1:i386 libcanberra-gtk-module:i386 gtk2-engines-murrine:i386 libgnome-keyring0:i386 libxaw7
		echo "Linking files..."
		echo "."
		ln -sf /usr/lib/x86_64-linux-gnu/libgnome-keyring.so.0 /usr/lib/libgnome-keyring.so.0
		echo ".."
		ln -sf /usr/lib/x86_64-linux-gnu/libgnome-keyring.so.0.2.0 /usr/lib/libgnome-keyring.so.0.2.0
	#Ubuntu 14.04.1 32bit
	elif [ $CHKArch = "i686" ]; then
		if [ $TVer = "14.04.1" ]; then
		echo "You are running Ubuntu `printf "\e[32m14.04.1 Trusty"``echo -e "\033[0m"`"
		elif [ $TVer = "17.1" ]; then
		echo "You are running Linux Mint `printf "\e[32m17.1 Rebecca"``echo -e "\033[0m"`"
		fi
		echo "Installing dependencies..."
		sleep 1
		apt-get install libgtk2.0-0 libxslt1.1 libxml2 libnss3 libxaw7 libgnome-keyring0
		echo "Linking files..."
		echo "."
		ln -sf /usr/lib/i386-linux-gnu/libgnome-keyring.so.0 /usr/lib/libgnome-keyring.so.0
		echo ".."
		ln -sf /usr/lib/i386-linux-gnu/libgnome-keyring.so.0.2.0 /usr/lib/libgnome-keyring.so.0.2.0
	fi

elif [ $CHKVer = "14.04.2" ] || [ $CHKVer = "17.2" ]; then
	#For Ubuntu 14.04.2 64bit
	if [ $CHKArch = "x86_64" ]; then
		if [ $TVer = "14.04.2" ]; then
		echo "You are running Ubuntu `printf "\e[32m14.04.2 Trusty"``echo -e "\033[0m"`"
		elif [ $TVer = "17.2" ]; then
		echo "You are running Linux Mint `printf "\e[32m17.2"``echo -e "\033[0m"`"
		fi
		echo "Installing dependencies..."
		sleep 1
		apt-get install libxt6:i386 libnspr4-0d:i386 libgtk2.0-0:i386 libstdc++6:i386 libnss3-1d:i386 lib32nss-mdns libxml2:i386 libxslt1.1:i386 libcanberra-gtk-module:i386 gtk2-engines-murrine:i386 libgnome-keyring0:i386 libxaw7
		echo "Linking files..."
		echo "."
		ln -sf /usr/lib/x86_64-linux-gnu/libgnome-keyring.so.0 /usr/lib/libgnome-keyring.so.0
		echo ".."
		ln -sf /usr/lib/x86_64-linux-gnu/libgnome-keyring.so.0.2.0 /usr/lib/libgnome-keyring.so.0.2.0
	#Ubuntu 14.04.2 32bit
	elif [ $CHKArch = "i686" ]; then
		if [ $TVer = "14.04.2" ]; then
		echo "You are running Ubuntu `printf "\e[32m14.04.2 Trusty"``echo -e "\033[0m"`"
		elif [ $TVer = "17.2" ]; then
		echo "You are running Linux Mint `printf "\e[32m17.2"``echo -e "\033[0m"`"
		fi
		echo "Installing dependencies..."
		sleep 1
		apt-get install libgtk2.0-0 libxslt1.1 libxml2 libnss3 libxaw7 libgnome-keyring0
		echo "Linking files..."
		echo "."
		ln -sf /usr/lib/i386-linux-gnu/libgnome-keyring.so.0 /usr/lib/libgnome-keyring.so.0
		echo ".."
		ln -sf /usr/lib/i386-linux-gnu/libgnome-keyring.so.0.2.0 /usr/lib/libgnome-keyring.so.0.2.0
	fi


elif [ $CHKVer = "14.04.3" ] || [ $CHKVer = "17.3" ]; then
	#For Ubuntu 14.04.3 64bit
	if [ $CHKArch = "x86_64" ]; then
		if [ $TVer = "14.04.3" ]; then
		echo "You are running Ubuntu `printf "\e[32m14.04.3 Trusty"``echo -e "\033[0m"`"
		elif [ $TVer = "17.3" ]; then
		echo "You are running Linux Mint `printf "\e[32m17.3"``echo -e "\033[0m"`"
		fi
		echo "Installing dependencies..."
		sleep 1
		apt-get install libxt6:i386 libnspr4-0d:i386 libgtk2.0-0:i386 libstdc++6:i386 libnss3-1d:i386 lib32nss-mdns libxml2:i386 libxslt1.1:i386 libcanberra-gtk-module:i386 gtk2-engines-murrine:i386 libgnome-keyring0:i386 libxaw7
		echo "Linking files..."
		echo "."
		ln -sf /usr/lib/x86_64-linux-gnu/libgnome-keyring.so.0 /usr/lib/libgnome-keyring.so.0
		echo ".."
		ln -sf /usr/lib/x86_64-linux-gnu/libgnome-keyring.so.0.2.0 /usr/lib/libgnome-keyring.so.0.2.0
	#Ubuntu 14.04.3 32bit
	elif [ $CHKArch = "i686" ]; then
		if [ $TVer = "14.04.3" ]; then
		echo "You are running Ubuntu `printf "\e[32m14.04.3 Trusty"``echo -e "\033[0m"`"
		elif [ $TVer = "17.3" ]; then
		echo "You are running Linux Mint `printf "\e[32m17.3"``echo -e "\033[0m"`"
		fi
		echo "Installing dependencies..."
		sleep 1
		apt-get install libgtk2.0-0 libxslt1.1 libxml2 libnss3 libxaw7 libgnome-keyring0
		echo "Linking files..."
		echo "."
		ln -sf /usr/lib/i386-linux-gnu/libgnome-keyring.so.0 /usr/lib/libgnome-keyring.so.0
		echo ".."
		ln -sf /usr/lib/i386-linux-gnu/libgnome-keyring.so.0.2.0 /usr/lib/libgnome-keyring.so.0.2.0
	fi

elif [ $CHKVer = "16.04" ] || [ $CHKVer = "18" ]; then
	#For Ubuntu 16.04 64bit and Linux Mint 18
	if [ $CHKArch = "x86_64" ]; then

		if [ $TVer = "16.04" ]; then
		echo "You are running Ubuntu `printf "\e[32m16.04 Xenial"``echo -e "\033[0m"`"
		elif [ $TVer = "18" ]; then
		echo "You are running Linux Mint `printf "\e[32m18"``echo -e "\033[0m"`"
		fi
		#echo "You are running Ubuntu `printf "\e[32m16.04 Xenial"``echo -e "\033[0m"`"

		echo "Installing dependencies..."
		sleep 1
		apt-get install libxt6:i386 libnspr4-0d:i386 libgtk2.0-0:i386 libstdc++6:i386 libnss3-1d:i386 libnss-mdns:i386 libxml2:i386 libxslt1.1:i386 libcanberra-gtk-module:i386 gtk2-engines-murrine:i386 libgnome-keyring0:i386 libxaw7
		echo "Linking files..."
		echo "."
		ln -sf /usr/lib/x86_64-linux-gnu/libgnome-keyring.so.0 /usr/lib/libgnome-keyring.so.0
		echo ".."
		ln -sf /usr/lib/x86_64-linux-gnu/libgnome-keyring.so.0.2.0 /usr/lib/libgnome-keyring.so.0.2.0
	#Ubuntu 16.04 32bit and Linux Mint 18
	elif [ $CHKArch = "i686" ]; then
		echo "You are running Ubuntu `printf "\e[32m16.04 Xenial"``echo -e "\033[0m"`"
		echo "Installing dependencies..."
		sleep 1
		apt-get install libgtk2.0-0 libxslt1.1 libxml2 libnss3 libxaw7 libgnome-keyring0
		echo "Linking files..."
		echo "."
		ln -sf /usr/lib/i386-linux-gnu/libgnome-keyring.so.0 /usr/lib/libgnome-keyring.so.0
		echo ".."
		ln -sf /usr/lib/i386-linux-gnu/libgnome-keyring.so.0.2.0 /usr/lib/libgnome-keyring.so.0.2.0
	fi


elif [ $CHKVer = "16.04.1" ] || [ $CHKVer = "18.1" ]; then
	#For Ubuntu 16.04.1 64bit and Linux Mint 18.1
	if [ $CHKArch = "x86_64" ]; then

		if [ $TVer = "16.04.1" ]; then
		echo "You are running Ubuntu `printf "\e[32m16.04 Xenial"``echo -e "\033[0m"`"
		elif [ $TVer = "18.1" ]; then
		echo "You are running Linux Mint `printf "\e[32m18"``echo -e "\033[0m"`"
		fi
		#echo "You are running Ubuntu `printf "\e[32m16.04 Xenial"``echo -e "\033[0m"`"

		echo "Installing dependencies..."
		sleep 1
		apt-get install libxt6:i386 libnspr4-0d:i386 libgtk2.0-0:i386 libstdc++6:i386 libnss3-1d:i386 libnss-mdns:i386 libxml2:i386 libxslt1.1:i386 libcanberra-gtk-module:i386 gtk2-engines-murrine:i386 libgnome-keyring0:i386 libxaw7
		echo "Linking files..."
		echo "."
		ln -sf /usr/lib/x86_64-linux-gnu/libgnome-keyring.so.0 /usr/lib/libgnome-keyring.so.0
		echo ".."
		ln -sf /usr/lib/x86_64-linux-gnu/libgnome-keyring.so.0.2.0 /usr/lib/libgnome-keyring.so.0.2.0
	#Ubuntu 16.04.1 32bit and Linux Mint 18.1
	elif [ $CHKArch = "i686" ]; then
		echo "You are running Ubuntu `printf "\e[32m16.04 Xenial"``echo -e "\033[0m"`"
		echo "Installing dependencies..."
		sleep 1
		apt-get install libgtk2.0-0 libxslt1.1 libxml2 libnss3 libxaw7 libgnome-keyring0
		echo "Linking files..."
		echo "."
		ln -sf /usr/lib/i386-linux-gnu/libgnome-keyring.so.0 /usr/lib/libgnome-keyring.so.0
		echo ".."
		ln -sf /usr/lib/i386-linux-gnu/libgnome-keyring.so.0.2.0 /usr/lib/libgnome-keyring.so.0.2.0
	fi


elif [ $CHKVer = "15.10" ]; then
	#For Ubuntu 15.10 64bit
	if [ $CHKArch = "x86_64" ]; then
		echo "You are running Ubuntu `printf "\e[32m15.10 Wily"``echo -e "\033[0m"`"
		echo "Installing dependencies..."
		sleep 1
		apt-get install libxt6:i386 libnspr4-0d:i386 libgtk2.0-0:i386 libstdc++6:i386 libnss3-1d:i386 lib32nss-mdns libxml2:i386 libxslt1.1:i386 libcanberra-gtk-module:i386 gtk2-engines-murrine:i386 libgnome-keyring0:i386 libxaw7
		echo "Linking files..."
		echo "."
		ln -sf /usr/lib/x86_64-linux-gnu/libgnome-keyring.so.0 /usr/lib/libgnome-keyring.so.0
		echo ".."
		ln -sf /usr/lib/x86_64-linux-gnu/libgnome-keyring.so.0.2.0 /usr/lib/libgnome-keyring.so.0.2.0
	#Ubuntu 15.10 32bit
	elif [ $CHKArch = "i686" ]; then
		echo "You are running Ubuntu `printf "\e[32m15.10 Wily"``echo -e "\033[0m"`"
		echo "Installing dependencies..."
		sleep 1
		apt-get install libgtk2.0-0 libxslt1.1 libxml2 libnss3 libxaw7 libgnome-keyring0
		echo "Linking files..."
		echo "."
		ln -sf /usr/lib/i386-linux-gnu/libgnome-keyring.so.0 /usr/lib/libgnome-keyring.so.0
		echo ".."
		ln -sf /usr/lib/i386-linux-gnu/libgnome-keyring.so.0.2.0 /usr/lib/libgnome-keyring.so.0.2.0
	fi

elif [ $CHKVer = "15.04" ]; then
	#For Ubuntu 15.04 Vivid 64bit
	if [ $CHKArch = "x86_64" ]; then
		echo "You are running Ubuntu `printf "\e[32m15.04 Vivid"``echo -e "\033[0m"`"
		echo "Installing dependencies..."
		sleep 1
		apt-get install libxt6:i386 libnspr4-0d:i386 libgtk2.0-0:i386 libstdc++6:i386 libnss3-1d:i386 lib32nss-mdns libxml2:i386 libxslt1.1:i386 libcanberra-gtk-module:i386 gtk2-engines-murrine:i386 libgnome-keyring0:i386 libxaw7
		echo "Linking files..."
		echo "."
		ln -sf /usr/lib/x86_64-linux-gnu/libgnome-keyring.so.0 /usr/lib/libgnome-keyring.so.0
		echo ".."
		ln -sf /usr/lib/x86_64-linux-gnu/libgnome-keyring.so.0.2.0 /usr/lib/libgnome-keyring.so.0.2.0
	#Ubuntu 15.04 Vivid 32bit
	elif [ $CHKArch = "i686" ]; then
		echo "You are running Ubuntu `printf "\e[32m15.04 Vivid"``echo -e "\033[0m"`"
		echo "Installing dependencies..."
		sleep 1
		apt-get install libgtk2.0-0 libxslt1.1 libxml2 libnss3 libxaw7 libgnome-keyring0
		echo "Linking files..."
		echo "."
		ln -sf /usr/lib/i386-linux-gnu/libgnome-keyring.so.0 /usr/lib/libgnome-keyring.so.0
		echo ".."
		ln -sf /usr/lib/i386-linux-gnu/libgnome-keyring.so.0.2.0 /usr/lib/libgnome-keyring.so.0.2.0
	fi

elif [ $CHKVer = "12.04" ] || [ $CHKVer = "13" ]; then
	#Ubuntu 12.04 32bit
	if [ $CHKArch = "i686" ]; then
		if [ $TVer = "12.04" ]; then
		echo "You are running Ubuntu `printf "\e[32m12.04 Precise"``echo -e "\033[0m"`"
		elif [ $TVer = "13" ]; then
		echo "You are running Linux Mint `printf "\e[32m13 Maya"``echo -e "\033[0m"`"
		fi
		echo "Installing dependencies..."
		sleep 1
		apt-get install libhal-storage1 libgnome-keyring0 libgnome-keyring0 libgtk2.0-0 libxslt1.1 libxml2
		echo "Linking files..."
		echo "."
		ln -sf /usr/lib/i386-linux-gnu/libgnome-keyring.so.0 /usr/lib/libgnome-keyring.so.0
		echo ".."
		ln -sf /usr/lib/i386-linux-gnu/libgnome-keyring.so.0.2.0 /usr/lib/libgnome-keyring.so.0.2.0
	#Ubuntu 12.04 64bit
	elif [ $CHKArch = "x86_64" ]; then
		if [ $TVer = "12.04" ]; then
		echo "You are running Ubuntu `printf "\e[32m12.04 Precise"``echo -e "\033[0m"`"
		elif [ $TVer = "13" ]; then
		echo "You are running Linux Mint `printf "\e[32m13 Maya"``echo -e "\033[0m"`"
		fi
		echo "Installing dependencies..."
		sleep 1
		apt-get install ia32-libs lib32nss-mdns libhal-storage1 libgnome-keyring0 libgnome-keyring0 libgtk2.0-0 libxslt1.1 libxml2
		echo "Symbolic linking files..."
		echo "."
		ln -sf /usr/lib/x86_64-linux-gnu/libgnome-keyring.so.0 /usr/lib/libgnome-keyring.so.0
		echo ".."
		ln -sf /usr/lib/x86_64-linux-gnu/libgnome-keyring.so.0.2.0 /usr/lib/libgnome-keyring.so.0.2.0
	fi

else
echo "You are not running Ubuntu `printf "\e[32m16.04 Xenial"``echo -e "\033[0m"`/`printf "\e[32m15.10 Wily"``echo -e "\033[0m"`/`printf "\e[32m15.04 Vivid"``echo -e "\033[0m"`/`printf "\e[32m14.04 Trusty"``echo -e "\033[0m"`/`printf "\e[32m12.04 Precise"``echo -e "\033[0m"`, or Linux Mint `printf "\e[31m17.x"``echo -e "\033[0m"`/`printf "\e[31m13 Maya"``echo -e "\033[0m"`"
sleep 1
echo "Exiting..."
exit 1
fi

echo "Downloading AdobeAir Installer from Adobe site"
	sleep 1
	wget -O AdobeAIRInstaller.bin http://airdownload.adobe.com/air/lin/download/2.6/AdobeAIRInstaller.bin
	echo "Making installer executable"
	sleep 1
	chmod +x AdobeAIRInstaller.bin
	echo "Now running AdobeAir installer"
	./AdobeAIRInstaller.bin
	echo "Removing installer file and unlinking symbolic files"
	rm AdobeAIRInstaller.bin
	rm /usr/lib/libgnome-keyring.so.0
	rm /usr/lib/libgnome-keyring.so.0.2.0
echo ""
echo "Keep visit on http://www.NoobsLab.com
"
sleep 1
exit 1
