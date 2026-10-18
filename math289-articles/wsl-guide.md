---
title: "WSL Guide for Windows Users"
source: https://web.stanford.edu/class/math289/wsl_guide.pdf
crawled: 2026-10-19
---

Installing WSL on Windows 10 and 11
Travor Liu
tzliu@stanford.edu
September 23, 2026
In Stanford Math 289, we will usecoding agents: AI tools that help us write and execute
code. These agents tend to work better in Unix-like environments (e.g. Linux and macOS)
than in Windows. We therefore prefer a Unix-like environment for the course. For Windows
users, it is still possible to have a Linux environment while continuing to use Windows as
usual. In this guide, we will help you set upUbuntu, a widely used version of Linux that
comes with a collection of useful programs. We will run Ubuntu throughWindows Subsystem
for Linux(WSL), a Windows feature that lets you use Linux without replacing Windows.
This guide works on Windows 10 and Windows 11. Most screenshots illustrate Windows 10;
Windows 11 may look different, and the relevant menu differences are noted below.
Throughout this guide,Windows+Rmeans hold down the key with the Windows logo, press
R, then release both keys. This opens theRundialog, a quick way to launch applications
by typing their names and pressingEnter. For example, enteringwinverin the Run dialog
(Figure 1) opens a window showing your Windows version.
Later, you will typecommands: instructions executed inside PowerShell or the Ubuntu
terminal. Each step specifies which application to use. Type or paste the command there
and pressEnter, then wait for it to finish before entering the next one.
Figure 1:Run dialog withwinverentered. Source: Southern Oregon University,https://supp
ort.sou.edu/kb/articles/how-to-check-your-version-of-windows-10.
1

Follow Section 1 through Section 6 in order: first check your computer and enable the
Windows features, then learn how to use PowerShell, install Ubuntu, create your Linux
account, and verify the installation. Section 7 covers everyday use and maintenance. If you
run into problems, consult Section 8; Section 9 provides an alternative installation method
if needed. Consulting AI models can also help you troubleshoot problems.
1 Check your computer
Save your work before starting: you will need to restart Windows. You also need an internet
connection and a Windows account with administrator permission to install software.
1. Check the Windows version. PressWindows+R, typewinver, and pressEnter. In the
window that opens, look for Version and OS Build (Figure 2). The main installation
method works on Windows 11, or Windows 10 version 2004 or later with build 19041
or later (https://learn.microsoft.com/en-us/windows/wsl/install). Close
the window after checking. If your Windows 10 version is older, check for updates under
Settings>Update&Security>WindowsUpdate, orusetheoptionalmanualinstructions
in Section 9.
Figure 2:Windows 10 Home 22H2 inwinver. Source: Sun City Texas Computer Club, p. 9,
https://www.sctexas.org/Files/Library/27409/SUNCITYCOMPUTERWINDOWSSIG11082022.
PDF.
2. Check the system type. Open Start, then Settings > System > About. Under System
2

type, look for a 64-bit operating system with an x64-based or ARM-based processor
(Figure 3).
Figure 3:System type in Settings. Source: Into Windows,https://www.intowindows.com/
how-to-check-if-your-pc-is-running-32-bit-or-64-bit-windows-10/.
3. Checkvirtualization. ThisisacomputerfeatureneededbyWSL2. PressCtrl+Shift+Esc
to open Task Manager. Select More details if necessary, then Performance > CPU. Look
for Virtualization: Enabled (Figure 4). If it says Disabled, follow your computer manufac-
turer’s instructions for enabling virtualization in the BIOS/UEFI settings (the computer’s
startup settings) (https://learn.microsoft.com/en-us/windows/wsl/troubleshoot
ing).
3

Figure 4:Virtualization status in Task Manager. Source: ASUS,https://www.asus.com/u
s/support/faq/1043181/.
2 Enable the Windows features
1. PressWindows+R, typeoptionalfeatures, and pressEnter. A window called Windows
Features opens.
2. Scroll down and check both Windows Subsystem for Linux and Virtual Machine Platform
(Figure 5). If either box is already checked, leave it checked.
3. Click OK. If Windows asks for permission to make changes, approve it. Wait for Windows
to finish.
4. If you checked either box in this step,restart Windowsbefore continuing. Save any
open documents first.
4

Figure 5:Windows Features on Windows 11, with both required items outlined. Source: Logic-
Monitor,https://www.logicmonitor.com/blog/install-pietrasanta-traceroute-on-windo
ws-11.
3 Using Windows PowerShell
Windows PowerShell is an application in which you type instructions for Windows. We will
tell you exactly what to type and whether you need an administrator window, which has
permission to change the computer’s settings. Figure 6 shows theWindows+Xmenu used
below.
•Administrator window: pressWindows+X, select Windows PowerShell (Admin) on Win-
dows 10 or Terminal (Admin) on Windows 11, and approve the administrator prompt.
Use this for installing WSL or whenever a step requests administrator access.
•Ordinary window: pressWindows+Xand select Windows PowerShell on Windows 10 or
Terminal on Windows 11. Use this for checking the installation or starting Ubuntu.
5

Figure 6:Windows+Xmenu. Source: WindowsLoop,https://windowsloop.com/how-to-run-p
owershell-as-administrator/.
On Windows 11, Terminal may be labeled Windows Terminal. It opens a window with tabs;
use a PowerShell tab. Figure 7 shows PowerShell in both a classic window and Windows
Terminal. If one is not already open, select Windows PowerShell from the arrow menu beside
the + button.
Figure 7:PowerShell in a classic window (left) and Windows Terminal (right). Source: Packt,
p. 1,https://static.packt-cdn.com/downloads/9781800207561_ColorImages.pdf.
If these options are missing, search for Windows PowerShell in Start. Click the app for
an ordinary window, or right-click it and select Run as administrator for an administrator
window.
Apromptis the text the computer displays when it is ready for you to type a command.
A PowerShell prompt usually begins withPS, followed by the current Windows folder. For
example:
PS C:\Users\alice>
Type commands after the prompt; do not copy the prompt itself. In an administrator
window, the title normally includes Administrator.
6

4 Install WSL and Ubuntu
Use an administrator PowerShell window as described in Section 3. Type the following line
exactly, including the spaces and hyphens, and pressEnter:
wsl --install -d Ubuntu
Windows will download and install the necessary software. Wait until it finishes, then restart
Windows. After signing in again, click Start, type Ubuntu, and click the Ubuntu app if it
has not opened automatically. Its first startup may take a few minutes. This method installs
WSL 2, the version used in this guide (https://learn.microsoft.com/en-us/windows/
wsl/install).
For another illustrated walkthrough, see Microsoft’s WSL tutorial (https://code.visua
lstudio.com/docs/remote/wsl-tutorial). It also covers optional Visual Studio Code
setup; use Section 9 here for the full manual WSL 2 installation sequence.
5 Getting started with Ubuntu
Use the Ubuntu window for this section. This window is called theUbuntu terminal: it lets
you type commands for Linux. You can open it by selecting Ubuntu from Start (Figure 8
for Windows 10 or Figure 9 for Windows 11).
Figure 8:Ubuntu in the Windows 10 Start menu. Source: Config Server Firewall,https:
//www.configserverfirewall.com/ubuntu-linux/install-ubuntu-on-windows-10/.
7

Figure 9:Ubuntu in Start search on Windows 11. Source: It’s FOSS,https://itsfoss.com/ru
n-linux-apps-windows-wsl/.
On its first launch, Ubuntu will ask you to choose a username and password. Use a simple
username with lowercase letters and no spaces, such asalice. This account is separate
from your Windows account. Remember the password: you will need it when installing or
updating Linux software.
Remark1.Nothing appears while you type a password, not even dots or asterisks. This is
normal. You can useBackspaceto delete the last character you typed. Type the password
and pressEnter, then type it again when asked to confirm it.
For example, the account setup may display the following prompts. Choose your own user-
name in place ofalice; password entry remains invisible.
Enter new UNIX username: alice
New password:
Retype new password:
After account setup, the terminal displays apromptwhen Ubuntu is ready for a command
(Figure 10). For example:
alice@DESKTOP:~$
Here,aliceis your Linux username,DESKTOPis your computer’s name, and~means your
home folder. Your names may differ. Type commands after the$; do not copy the prompt
itself. After a command finishes, the prompt returns so you can enter another.
8

Figure 10:Ubuntu terminal after account setup. Source: Microsoft,https://code.visualstu
dio.com/docs/remote/wsl-tutorial.
The three commands below display your username, your Ubuntu release, and the Linux
kernel version (the version of the core part of Linux). The following sample session uses
aliceon a computer namedDESKTOP. Type only the commands after the$prompt; the
other lines are example output. Your username, computer name, Ubuntu release, and kernel
version may differ. The/etc/os-releaseoutput is abbreviated.
alice@DESKTOP:~$ whoami
alice
alice@DESKTOP:~$ cat /etc/os-release
PRETTY_NAME="Ubuntu 24.04.1 LTS"
NAME="Ubuntu"
VERSION_ID="24.04"
VERSION="24.04.1 LTS (Noble Numbat)"
ID=ubuntu
...
alice@DESKTOP:~$ uname -r
5.15.167.4-microsoft-standard-WSL2
Enter the following commands one at a time to update Ubuntu’s software. Wait for the first
to finish before entering the second:
sudo apt update
sudo apt upgrade
The wordsudoasks Ubuntu for permission to change installed software. Enter the Linux
password you just created if asked. The first command checks for available updates; the
second installs them. If askedDo you want to continue? [Y/n], typeyand pressEnter.
Wait until the prompt returns.
Remark2.Windows Update does not update the software inside Ubuntu.
Microsoft’s illustrated setup guide covers accounts, updates, and Linux files (https://lear
n.microsoft.com/en-us/windows/wsl/setup/environment).
9

6 Verify your installation
Open an ordinary PowerShell window as described in Section 3. Run:
wsl --list --verbose
Look for Ubuntu with2in theVERSIONcolumn. For example:
NAME STATE VERSION
* Ubuntu Running 2
Remark3.Stoppedis also normal: it means Ubuntu is not currently open. TheVERSION
column should show2; this is the WSL version, not the Ubuntu release number. You can
ignore the asterisk. If the column shows1, see Section 8 (https://learn.microsoft.com/
en-us/windows/wsl/basic-commands).
Installation is complete whenwsl –list –verboselists Ubuntu with WSL version 2 and
the example commands in Section 5 work in Ubuntu. You can now close the PowerShell
window. For future work, simply open Ubuntu from Start; you do not need to repeat the
installation.
7 Everyday use and maintenance
In a PowerShell window, runwsl -d Ubuntuto enter Linux. Inside Ubuntu, runexitto
return. You can also launch Ubuntu directly from Start.
For work with Linux software, keep files in your Linuxhome folder, the personal folder be-
longing to your Ubuntu account. The symbol~means this folder. In Ubuntu, the commands
below create a folder namedprojects, switch to it, and open it in Windows File Explorer:
mkdir -p ~/projects
cd ~/projects
explorer.exe .
Remark4.Keep the final dot inexplorer.exe .: it means “the current folder.” Windows
drive C: is accessible from Linux at/mnt/c. See file storage guidance (https://learn.mi
crosoft.com/en-us/windows/wsl/setup/environment).
Routine maintenance
PowerShell: update WSL itself with:
wsl --update
Continue to runsudo apt updateandsudo apt upgradeinside Ubuntu for Linux pack-
ages. To restart WSL, save your work first, then run these commands in a PowerShell
10

window:
wsl --shutdown
wsl -d Ubuntu
Shutdown stopsallrunning WSL distributions. On older WSL installations, some newer op-
tions may be absent;wsl –helplists the options your installation supports. See maintenance
commands (https://learn.microsoft.com/en-us/windows/wsl/basic-commands).
8 Troubleshooting
If something goes wrong, copy the complete error message or take a photograph of it before
closing the window. The following suggestions cover common problems.
Ubuntu is listed with VERSION 1.
In an ordinary PowerShell window, run the following. If this Ubuntu installation
already contains work, save a backup copy of that work first. ReplaceUbuntuif the
NAME column shows a different name.
wsl --set-version Ubuntu 2
Wait for it to finish, then repeatwsl –list –verbose.
Installer prints help, or Ubuntu is missing.
In a PowerShell window, runwsl –list –online, thenwsl –install -d Ubuntu.
Launch Ubuntu once to finish initialization. Use the same Windows account in which
you installed it.
Download remains at 0.0%.
Trywsl –install –web-download -d Ubuntuin an administrator PowerShell win-
dow. If that option is unavailable, consultwsl –helpand use the manual fallback.
See installer troubleshooting (https://learn.microsoft.com/en-us/windows/wsl/
install).
Error0x80370102: virtual machine cannot start.
Repeat the virtualization check in Section 1 and the checkbox check in Section 2,
then restart Windows. If the error persists, look up the exact error in Microsoft’s
troubleshooting guide (https://learn.microsoft.com/en-us/windows/wsl/trou
bleshooting).
Error0x8007019e: WSL component disabled.
Return to the Windows Features check in Section 2, enable Windows Subsystem for
Linux, and restart Windows.
WSL 2 reports a missing or outdated kernel.
Trywsl –updatein a PowerShell window. For the legacy manual installation, install
the matching kernel update package from Section 9.
For more help, see Microsoft’s troubleshooting guide (https://learn.microsoft.com/en
11

-us/windows/wsl/troubleshooting).
9 Alternative installation (optional)
Skip this section if Ubuntu is already working. These older installation steps may be useful
when the command in Section 4 is unavailable. Microsoft’s manual guide lists the Windows
versions supported by this method and provides the downloads (https://learn.microsof
t.com/en-us/windows/wsl/install-manual).
Complete the Windows Features check and any required restart in Section 2 before proceed-
ing.
1. Download and run the x64 or ARM64 WSL 2 Linux kernel update package linked in step
4 of Microsoft’s manual guide. Choose x64 for an x64-based processor or ARM64 for an
ARM-based processor, using the System type you checked in Section 1. Download the
file, then double-click it to run the installer.
2. PowerShell: runwsl –set-default-version 2.
3. Install Ubuntu from the Microsoft Store (Figure 11) and launch it. If the Store is un-
available, use the direct distribution downloads and package instructions in the manual
guide.
Figure 11:Ubuntu in the Microsoft Store (appearance may vary). Source: manual installation
guide (https://learn.microsoft.com/en-us/windows/wsl/install-manual).
4. Complete the account setup and verification in Section 5 and Section 6.
12