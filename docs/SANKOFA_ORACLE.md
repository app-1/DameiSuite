# Damei Sankofa Oracle (`Damei_AssessmentMatrix.jsfx`)

## Overview
The **Damei Sankofa Oracle** is a reference match analyzer and closed-loop auto-correction brain. Inserted on the mix master, audio passes through 100% untouched while the engine performs continuous 7-band spectral analysis, stereo imaging audits, and loudness metrics against reference fingerprints.

## Key Features

### 1. 7-Band Spectral Divergence Analysis
The spectrum is segmented into 7 standard critical listening bands:
* **Band 0 (20 - 60 Hz)**: Sub-bass fundamental
* **Band 1 (60 - 250 Hz)**: Bass punch & kick body
* **Band 2 (250 - 800 Hz)**: Low-mid body / mud zone
* **Band 3 (800 - 2.5 kHz)**: Vocal core & guitar bite
* **Band 4 (2.5 - 6.0 kHz)**: High-mid presence & vocal clarity
* **Band 5 (6.0 - 10.0 kHz)**: Highs & drum cymbals
* **Band 6 (10.0 - 18.0 kHz)**: Air & sheen

### 2. Multi-Metric Scoring Engine
* **Tonal Score (0 - 100%)**: Weighted spectral match against the reference target curve.
* **Stereo Score (0 - 100%)**: Correlation and width per band.
* **Dynamics Score (0 - 100%)**: Peak-to-Loudness Ratio (PLR), Crest Factor, and Integrated LUFS.
* **Overall Score (0 - 100%)**: Composite production readiness index.

### 3. Closed-Loop Auto-Correction Trim Lane
When enabled (`Slider 7: Apply`), the Oracle continuously calculates the exact trim needed across the 7 bands and publishes correction offsets over `gmem:DameiMixMetering` directly to:
* Drums (`1300`)
* Guitars (`1316`)
* Bass (`1332`)
* Vocals (`1348`)
* Synths (`1364`)
* Devastator FX (`1380`)

Trims are rate-limited and dead-banded to prevent integrator windup and ensure transparent sonic adjustments.
