https://forum.falcon-bms.com/topic/19901/ezboards-instant-single-click-briefing-to-kneeboards-conversion

## EZBoards - Instant single-click briefing to kneeboards conversion for Falcon BMS.

Version 12
For BMS 4.37
By "Logic", 2023-01-04.

### Introduction

EZBoards is a single-click solution to generate kneeboards from mission briefings for Falcon BMS.

EZBoards will generate kneeboard texture files based on data from your briefing.txt and callsign.ini files.
The following sections will be generated:
- Package Elements, with additional Pilot Roster info and fixed presets for IDM/TCN.
- Comm Ladder.
- Steerpoints.
- Targets: Target steerpoints with descriptions if they have been assigned.
- Weather report.

See example images.

All but the Targets data will be taken from birefing.txt, Targets data from callsign.ini.

EZBoards is intended for casual missions and does not intend to replace WDP or other tools for more thorough mission planning.
It has the advantage that the kneeboards are generated nearly instantly and with a single shortcut click.

### Prerequisites

In order to see kneeboards in 3D cockpit, you need to activate the 3D pilot model.
Pilot model can be activated in BMS settings Setup/Graphics/Pilot Model.
Or toggled by pressing Alt-C, P in the cockpit.

Falcon BMS must be configured to generate text briefing files (as opposed to HTML ones).
This is the default.
When in doubt, verify Configuration/General/Briefing/Debriefing/
Make sure "1\. Briefing Output to File" is selected.
Make sure "3\. HTML Briefings" is NOT selected.

### Installation

You can unzip the package to anywhere you want and run from there - It'll find the BMS folder and callsign via the Registry.
It is recommended to create a shortcut to EZBOARDS.BAT.

EZBoards requires .NET Core Runtime 3.1
You can download and install it from here: [https://dotnet.microsoft.com/download/dotnet-core/3.1](https://dotnet.microsoft.com/download/dotnet-core/3.1) .
(if not already present on your system)

### Usage

EZBoards should be run as the very last step in your mission planning, before comitting to 3D.
That is:
- Plan your mission as usual,
Make sure COMMS and IFF plans are loaded properly in your DTC,
Define target steerpoints if appropriate.
- Save your DTC.
(This will save the callsign.ini file which is the input for the target steerpoints)
- Go to the Briefing window. Push the "Print" button in the top-right corner.
(This will save the briefing.txt file which is the main input for EZBoards.)
- Run the EZBOARDS.BAT file. (You don't need to quit BMS!)
=> A console window opens, where information about the progress is shown.
The whole operation shouldn't last more than a few seconds.
When "Done." and "Press any key to continue" appears, you can close the window.
=> Your kneeboards have been generated and saved to the appropriate BMS texture file.
=> You can now commit to 3D and enjoy your kneeboards in the cockpit!

### Automated Usage with EZWatch

Since version 5, EZBoards can be run automatically whenever the briefing file content changes.
That is, whenever you press the "Print" button in BMS.
Just run EZWATCH.BAT.
It is self-explanatory.

### View briefing on other devices

Since version 6, EZBoards includes a small HTTP server that allows to view the generated briefing files on other device using a standard web server.
Just run EZSERVE.BAT and follow the instructions.
You need to allow network access to onehttpd-0.8.exe when Windows warns about it on first use.

### Notes, Known issues and limitations

- EZBoards should run on Windows 7 or higher. But i wasn't able to test. Tell me if you encounter any incompatibilities.

- EZBoards has been developed for the Korea KTO theater.
For use with other theaters, edit the TARGET variable in EZBOARDS.BAT accordingly.
(Ask on forums if you don't know how)

- Given the variable content of the Package-, Steerpoints- and Targets- sections, when these sections grow too big they will simply push the other sections down and out of the page.
EZBoards has been designed for reasonable content of these sections. (Up to 4 flights in package, some 20 steer- and target steerpoints)

- Don't like fonts, colors? They are configurable to some extent via the style.css sheet!

- The intermediate HTML and PNG files are preserved as well, you might want to use these for other purposes, like display on an external display device.

- Since v10 EZBoards looks into the Theaters.txt file to find the name of the texture file. This might be edited for other theaters.

### Acknowledgements

EZBoards uses
- wkhtmltoimage, a command line tools to render HTML into various image formats.
[https://wkhtmltopdf.org/](https://wkhtmltopdf.org/)
- Texconv, an external command-line tool to perform batched texture conversions.
[https://github.com/microsoft/DirectXTex/wiki/Texconv](https://github.com/microsoft/DirectXTex/wiki/Texconv)
- OneHTTPD, a minimalist web server.
[https://code.google.com/archive/p/onehttpd/](https://code.google.com/archive/p/onehttpd/)
- Ben Blamey's when_changed, a file watchdog for Windows.
[https://github.com/benblamey/when_changed](https://github.com/benblamey/when_changed)

### Example Images (full size)

[Briefing](https://drive.google.com/file/d/1c9ye1D0jLjY-LtuMmHz6R6FM2bAzDe1s/view?usp=sharing)  
[Kneeboards](https://drive.google.com/file/d/13wUOJ2H_GTJRhmTp-ETFSqBff4Joc192/view?usp=sharing)

Suggestions and feedback welcome!  
Contact Logic - scrontch@gmx.de
