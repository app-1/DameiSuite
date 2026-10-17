# Damei Instrument Bus Suites

## 1. Damei Vocal Sovereign (`Damei_VocalSuite.jsfx`)
* **Lead Vocal Pocket Sculpting**: Automatically creates frequency pocket carve-outs across competing instruments (guitars and synths).
* **Multi-Stage Sibilance Management**: Split-band de-esser targeted between 5.5 kHz and 8.0 kHz.
* **3D Ambience Halo**: Parallel stereo saturation and micro-pitch widening.
* **Telemetry**: Publishes vocal RMS and dynamic range to `gmem[880..899]`.

## 2. Damei Drum Bus Architect (`Damei_DrumSuite.jsfx`)
* **Atumpan Transient Matrix**: Independent transient attack snap and sustain tail control.
* **Kick-to-Sub Anchor**: Tight sub-bass alignment with phase synchronization.
* **Parallel Drum Crunch**: New York-style parallel compression bus.
* **Telemetry**: Publishes transient punch ratio and shell crest to `gmem[820..839]`.

## 3. Damei Bass Bus Engine (`Damei_BassSuite.jsfx`)
* **Hamidovic Crossover Architecture**: Low-end split isolating clean sub fundamentals (<90 Hz) while distorting mid-range grit (300 - 1500 Hz).
* **Kick-to-Sub Dynamic Ducking**: Ultra-fast sidechain ducking triggered whenever the kick strikes.
* **Telemetry**: Publishes kick/bass correlation and ducking GR to `gmem[860..879]`.

## 4. Damei Guitar Bus Alchemist (`Damei_GuitarSuite.jsfx`)
* **Quad-Wall Sculptor**: Stereo width expansion for double and quad-tracked heavy guitars.
* **Palm-Mute Chug Guard**: Dynamic narrow notch filter centered at 190 Hz to eliminate cabinet resonance during chugs without thinning sustained chords.
* **Center Vocal Donut-Hole**: Mid-channel notch carving room for the lead vocal.
* **Telemetry**: Publishes guitar wall width and chug energy to `gmem[840..859]`.

## 5. Damei Synth Bus Nebula (`Damei_SynthSuite.jsfx`)
* **Multiband Stereo Dimension**: Wide Haas-effect widening with strict mono compatibility below 200 Hz.
* **SynBass Handshake**: Coordinates sub-lows between synth bass lines and the main bass guitar.
* **Telemetry**: Publishes synth energy and stereo width to `gmem[800..819]`.

## 6. Damei Devastator Suite (`Damei_DevastatorSuite.jsfx`)
* **Cinematic Hybrid FX Co-Pilot**: Automated risers, sub-drops, and impact swells.
* **Chorus Drop Slam**: Delivers immediate dynamic impact at section boundaries.
* **Telemetry**: Publishes impact energy to `gmem[890..899]`.
