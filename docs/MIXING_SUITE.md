# Damei Mixing Suite (`Damei_MixingSuite.jsfx`)

## Overview
The **Damei Mixing Suite** sits on the pre-master mix bus, providing complete console color, bus glue, dynamic resonance mitigation, commercial headroom leveling, and producer signature topologies.

## Key Modules

### 1. Auto-Headroom Gain Leveler
* **Slider 3**: Headroom Target Ceiling (-18.0 to 0.0 dBTP, default: `-6.0 dBTP`).
* **Slider 4**: Auto-Headroom Leveler mode (Off / Strict -6 dBTP Auto-Trim).
* Maintains continuous optimal headroom into the mastering chain without inter-sample clipping.

### 2. Console Bus Compressor
* **Slider 8**: Topology selector:
  * `British VCA`: Classic punchy VCA bus glue with aggressive snap.
  * `Opto 2A`: Smooth, musical program compression.
  * `FET 76`: Fast peak-catching limiter.
* **Sliders 9 - 15**: Threshold, Ratio (1.5:1 up to All-Buttons-In), Attack (0.1 to 100 ms), Release (Auto or stepped), Sidechain HPF (20 - 250 Hz), Make-up gain, and Dry/Wet blend.

### 3. Dynamic Spectral Balancers
* **Dynamic De-Box Mud Gain** (Slider 17 & 18): Dynamically attenuates boxiness and mud in the 150 - 600 Hz range only when build-up occurs.
* **Dynamic De-Harsh Gain** (Slider 19 & 20): Dynamically suppresses metallic screech and harshness in the 2 - 7 kHz range.
* **Spectral Tilt**: Quick high-shelf/low-shelf tilt pivot for balancing overall darkness vs brightness.

### 4. 22 Producer Signature Presets (Slider 39)
Includes finely calibrated mix bus starting topologies for top modern metal and rock producers:
1. `Default Modern Metal Clean`
2. `Lance Prenc (Alpha Wolf / Polaris)`
3. `Scott Seigel (DIESECT)`
4. `Jonathan Dolese (Mirrorcell / Cane Hill)`
5. `Buster Odeholm (thrown / Northlane)`
6. `Lewis Johns (Love Is Noise / blanket)`
7. `Kel Pinchin (Split Chain)`
8. `Dan Lancaster & Jason Perry (Don Broco / BMTH)`
9. `Erik Bickerstaffe (Static Dress / Loathe)`
10. `Sam Guaiana (Shyeye / Silverstein)`
11. `Zach Tuch (Heavenward / Hundredth)`
12. `Forrester Savell (City Of Souls / Karnivool)`
13. `Leon Schmidt (SUNBORN - Nebula)`
14. `Ermin Hamidovic Systematic Reference`
15. `Will Putney (Fit For An Autopsy / Knocked Loose)`
16. `George Lever (Loathe / Sleep Token)`
17. `Sam Bassal (Thornhill - nerv / Ocean Grove)`
18. `Henrik Udd (Architects - Gravity / Bleed From Within)`
19. `Dan Braunstein (Spiritbox - Keep Sweet)`
20. `Zakk Cervini & Erik Ron (Bad Omens - THE DEATH OF PEACE OF MIND)`
21. `Jens Bogren (Fascination Street Studios)`
22. `Adam Nolly Getgood (Periphery / GGD)`

### 5. Song Structure & Chorus Impact AI
* Detects song sections (Verse, Pre-Chorus, Chorus, Bridge) via REAPER markers/regions or autonomous audio analysis.
* Automatically increases stereo width (+0.10x to +0.16x) and punch (+0.8 to +1.4 dB) exactly when the chorus hits.
