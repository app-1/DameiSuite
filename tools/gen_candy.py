"""Ear-Candy Director kernel generator + patcher for Vocal Sovereign and Guitar Bus Alchemist.

Run once (idempotent only from the pre-candy backups in backups_precandy / or current v2 vocal state).
"""
import re, sys

DIR = r'C:\Dev\DameiAPI\reaper_scripts'

TR = ['THROW', 'BLOOM', 'ECHO', 'SLAP', 'HALL', 'RISE', 'CHOP', 'TELE', 'BREATH',
      'GHOSTUP', 'GHOSTDN', 'DIVE', 'GRIT', 'WIDE', 'TREM', 'SWEEP']
BIT = {n: 1 << i for i, n in enumerate(TR)}

NAMES_V = ['Phrase Throw', 'Reverse Bloom', 'Ducked Echo', 'Tape Slap', 'Hall Tail', 'Filter Rise',
           'Stutter Chop', 'Telephone Choke', 'Breath Air', 'Octave Halo', 'Sub Shadow', 'Pitch Dive',
           'Grit Layer', 'Wide Double', 'Tremolo', 'Sweep']
NAMES_G = ['Chord Throw', 'Reverse Swell', 'Dotted Echo', 'Slapback', 'Plate Tail', 'Filter Rise',
           'Killswitch Chop', 'Radio Choke', 'Sparkle Air', 'Octave Shimmer', 'Sub-Octave Weight', 'Whammy Dive',
           'Fuzz Layer', 'Haas Widener', 'Tremolo Pulse', 'Filter Sweep']
HINTS = ['last phrase thrown ping-pong into the drop', 'reversed phrase swells into the drop',
         'dotted echo blooms in gaps after phrases', 'short slap on phrase ends in sparse parts',
         'hall tail on big phrase ring-outs', 'high-pass rise across the last bar',
         '16th gate chop on the final beat', 'bandpass choke before drops / bridge lo-fi',
         'high-band shadow in loud choruses', 'octave halo late in loud choruses',
         'octave-down weight on breakdowns / peaks', 'pitch dive over the last 0.4 s of a section',
         'parallel grit when energy peaks', 'Haas widen in choruses',
         'tempo-synced tremolo on sparse parts', 'slow filter sweep through verses and builds']
TYPE_NAMES = ['Open (energy only)', 'Intro', 'Verse', 'Pre-Chorus', 'Chorus', 'Bridge', 'Outro', 'Other']

PRODUCERS = ['Default Neutral Wire', 'Lance Prenc', 'Scott Seigel', 'Jonathan Dolese', 'Buster Odeholm',
             'Kel Pinchin', 'Sam Guaiana', 'Forrester Savell', 'Jens Bogren', 'Nolly Getgood', 'Will Putney',
             'George Lever', 'Sam Bassal', 'Henrik Udd', 'Joey Sturgis', 'Dan Braunstein', 'Zakk Cervini']

# (tricks, signature, density, gain)
VOC = [
 (['ECHO', 'HALL', 'THROW'], 'ECHO', 1, 0.80),
 (['THROW', 'SLAP', 'TELE', 'GRIT', 'WIDE', 'CHOP'], 'TELE', 2, 1.00),
 (['CHOP', 'TELE', 'GRIT', 'DIVE', 'SLAP'], 'CHOP', 2, 1.00),
 (['RISE', 'TELE', 'SLAP', 'GRIT', 'ECHO', 'THROW'], 'RISE', 2, 1.00),
 (['TELE', 'CHOP', 'DIVE', 'GHOSTDN', 'SLAP'], 'DIVE', 1, 1.00),
 (['ECHO', 'BLOOM', 'WIDE', 'BREATH', 'HALL', 'RISE'], 'BLOOM', 2, 0.95),
 (['THROW', 'ECHO', 'WIDE', 'BREATH', 'SLAP'], 'THROW', 2, 0.95),
 (['BLOOM', 'HALL', 'ECHO', 'RISE', 'GHOSTUP', 'BREATH'], 'BLOOM', 2, 1.05),
 (['HALL', 'ECHO', 'BREATH', 'WIDE', 'BLOOM'], 'HALL', 1, 0.80),
 (['THROW', 'RISE', 'SLAP', 'WIDE', 'GHOSTUP', 'CHOP'], 'WIDE', 2, 0.95),
 (['CHOP', 'TELE', 'GRIT', 'DIVE', 'SLAP'], 'GRIT', 2, 1.00),
 (['BLOOM', 'HALL', 'ECHO', 'GHOSTUP', 'TELE', 'WIDE', 'BREATH'], 'GHOSTUP', 2, 1.05),
 (['BLOOM', 'RISE', 'ECHO', 'WIDE', 'THROW', 'BREATH'], 'RISE', 2, 1.00),
 (['TELE', 'RISE', 'BLOOM', 'BREATH', 'GHOSTUP', 'CHOP', 'GHOSTDN'], 'TELE', 2, 1.05),
 (['CHOP', 'TELE', 'SLAP', 'BREATH', 'GRIT', 'WIDE'], 'CHOP', 2, 1.00),
 (['THROW', 'BLOOM', 'ECHO', 'BREATH', 'WIDE', 'GHOSTUP'], 'THROW', 2, 1.00),
 (['TELE', 'RISE', 'CHOP', 'BREATH', 'WIDE', 'ECHO'], 'TELE', 2, 1.00),
]
GTR = [
 (['ECHO', 'BLOOM', 'HALL'], 'ECHO', 1, 0.80),
 (['CHOP', 'GRIT', 'GHOSTDN', 'DIVE', 'RISE', 'WIDE'], 'GHOSTDN', 2, 1.00),
 (['CHOP', 'DIVE', 'GHOSTDN', 'GRIT', 'TELE'], 'DIVE', 2, 1.00),
 (['RISE', 'SWEEP', 'TELE', 'GRIT', 'SLAP', 'WIDE'], 'SWEEP', 2, 1.00),
 (['GHOSTDN', 'DIVE', 'CHOP', 'GRIT', 'TELE'], 'GHOSTDN', 1, 1.00),
 (['GHOSTUP', 'BLOOM', 'ECHO', 'WIDE', 'SWEEP', 'TREM'], 'GHOSTUP', 2, 0.95),
 (['ECHO', 'WIDE', 'BREATH', 'SLAP', 'BLOOM'], 'WIDE', 2, 0.95),
 (['BLOOM', 'HALL', 'ECHO', 'GHOSTUP', 'SWEEP', 'TREM'], 'BLOOM', 2, 1.05),
 (['HALL', 'WIDE', 'BLOOM', 'ECHO', 'SWEEP'], 'WIDE', 1, 0.80),
 (['CHOP', 'WIDE', 'RISE', 'GHOSTDN', 'ECHO', 'SLAP'], 'CHOP', 2, 0.95),
 (['CHOP', 'GHOSTDN', 'DIVE', 'GRIT', 'TELE'], 'GRIT', 2, 1.00),
 (['BLOOM', 'HALL', 'GHOSTUP', 'TREM', 'SWEEP', 'ECHO'], 'TREM', 2, 1.05),
 (['BLOOM', 'RISE', 'ECHO', 'WIDE', 'GHOSTUP', 'SLAP'], 'GHOSTUP', 2, 1.00),
 (['RISE', 'BLOOM', 'SWEEP', 'GHOSTUP', 'TELE', 'GHOSTDN'], 'SWEEP', 2, 1.05),
 (['CHOP', 'GRIT', 'WIDE', 'SLAP', 'RISE'], 'GRIT', 2, 1.00),
 (['ECHO', 'BLOOM', 'WIDE', 'GHOSTUP', 'SLAP', 'HALL'], 'ECHO', 2, 1.00),
 (['RISE', 'CHOP', 'TELE', 'WIDE', 'SLAP', 'BREATH'], 'RISE', 2, 1.00),
]
GTIPS = [
 ["Transparent wall: the Director adds only the odd touch.",
  "Dotted echo and plate tails only in the gaps between riffs.",
  "No colour on verses; one swell into each chorus.",
  "Restraint wins: if you can hear it, lower the amount."],
 ["Tight, aggressive chugs: killswitch chop on the last beat.",
  "Sub-octave shadow under breakdown chugs for extra weight.",
  "Whammy dive over the last 0.4 s of a section, barely there.",
  "Grit layer only when the riff peaks above the section average."],
 ["Precision hardcore: gate chops and dive tails, nothing washy.",
  "Sub-octave weight on breakdown hits, dry everywhere else.",
  "Radio choke before the drop, snap back to full range.",
  "Parallel grit at peaks keeps the heavy parts hostile."],
 ["Nu-metal movement: slow filter sweeps through the verses.",
  "High-pass rise across the pre-chorus bar, released on the drop.",
  "Slapback on sparse single-note lines for a warm vintage edge.",
  "Haas widener opens up the chorus wall."],
 ["Weight is everything: sub-octave shadow under the low chugs.",
  "Whammy dive into dead silence before the drop.",
  "Killswitch chop on the final beat, hard cut, then impact.",
  "Almost no ambience: the heavy parts stay dry and dense."],
 ["Ethereal layers: octave shimmer rises late in big choruses.",
  "Reverse swell into the chorus plus dotted echo in the gaps.",
  "Slow filter sweep and a gentle tremolo pulse on clean parts.",
  "Haas widener gives the lead lines a halo."],
 ["Punchy post-hardcore: sparkle air in the loud choruses.",
  "Dotted echo only when the riff stops; slapback on sparse parts.",
  "Widener opens the chorus; verses stay tight and centred.",
  "Reverse swell into the big hooks, short and tasteful."],
 ["Expansive prog: reverse swell into the chorus, long plate tail.",
  "Octave shimmer late in loud sections, very quiet.",
  "Tremolo pulse and slow sweep colour the clean passages.",
  "Dotted echo blooms between phrases, never over the riff."],
 ["Dense wall: keep it natural, plate tail on big ring-outs.",
  "Haas widener in choruses for size, nothing flashy.",
  "A single reverse swell into the biggest section only.",
  "Slow filter sweep in verses adds quiet movement."],
 ["Crystalline precision: killswitch chop on the last beat.",
  "Widener plus sub-octave weight for tight, huge chorus riffs.",
  "Short slapback on lead lines in sparse verses.",
  "High-pass rise on the pre-chorus bar for lift."],
 ["Raw hardcore girth: grit layer when the riff peaks.",
  "Sub-octave shadow on breakdowns, chop before the hit.",
  "Whammy dive tails on section ends. Dry, mean, short.",
  "Radio choke before the drop; no ambience."],
 ["Atmospheric weight: tremolo pulse on the cleans.",
  "Reverse swell + plate tail into the biggest chorus.",
  "Octave shimmer late in loud parts, tucked way back.",
  "Slow filter sweep, then dotted echo in the gaps."],
 ["Polished nu-metalcore: rise into the chorus, widener on top.",
  "Octave shimmer on late choruses for gloss.",
  "Slapback on sparse parts, dotted echo at riff stops.",
  "Reverse swell leads into the big hooks."],
 ["Arena wall: sweep movement through builds, rise into drops.",
  "Octave shimmer late; sub-octave weight on the heaviest peaks.",
  "Radio choke on the final bar, fully open on the drop.",
  "Reverse swell blends with the filter rise into the chorus."],
 ["Scooped 2010s crunch: killswitch chop and grit layer.",
  "Widener for the big chorus; slapback on sparse parts.",
  "High-pass rise into the drop, short and bright.",
  "Keep it punchy: no long tails."],
 ["Ethereal space: dotted echo in the gaps, reverse swell at drops.",
  "Octave shimmer late in the biggest choruses, very quiet.",
  "Haas widener opens the chorus wall; plate tail on ring-outs.",
  "Slapback only on sparse single-note passages."],
 ["Pop-punk lift: filter rise then killswitch chop before the drop.",
  "Radio choke on the final bar, explosive open on the downbeat.",
  "Widener and sparkle air make the chorus gloss.",
  "Short slapback on sparse verse guitars."],
]

def mask_of(lst):
    m = 0
    for n in lst:
        m |= BIT[n]
    return m

def kernel(sfx, names, tips, recipes, vis_bits, tag, prods=None, hints=None):
    """Return the JSFX text of the shared Director kernel (init-section only)."""
    prods = prods or PRODUCERS
    hints = hints or HINTS
    np_ = len(prods)
    s = KERNEL_TEMPLATE.replace('min(16, ', 'min(%d, ' % (np_ - 1))
    # tables
    tbl = []
    for k in range(16):
        tbl.append('dk_nm[%d] = "%s";' % (k, names[k]))
        tbl.append('dk_hint[%d] = "%s";' % (k, hints[k]))
    for k, nm in enumerate(TYPE_NAMES):
        tbl.append('dk_tn[%d] = "%s";' % (k, nm))
    for p in range(np_):
        tl, sig, dn, gn = recipes[p]
        tbl.append('dk_pn[%d] = "%s"; dk_pm[%d] = %d; dk_ps[%d] = %d; dk_pd[%d] = %d; dk_pg[%d] = %s;' %
                   (p, prods[p], p, mask_of(tl), p, TR.index(sig), p, dn, p, repr(gn)))
        for n in range(4):
            ln = tips[p][n]
            assert len(ln) <= 66, (len(ln), ln)
            tbl.append('dk_tip[%d] = "%s";' % (p*4 + n, ln))
    s = s.replace('@@TABLES@@', '\n'.join(tbl))
    s = s.replace('@@VIS@@', str(vis_bits))
    for key, val in sfx.items():
        s = s.replace('@@%s@@' % key, val)
    return s

KERNEL_TEMPLATE = r'''
// ===== EAR-CANDY DIRECTOR BEGIN (shared region + energy aware producer tricks) =====
// Reads REAPER regions (gmem 100-109) AND the measured energy of this bus. Per region it picks a small,
// producer-specific set of tricks, then fires them only inside the right musical window. Every wet
// signal is derived from the performance itself and capped, so it stays barely audible.
dk_bm = 780000;
dk_rv = dk_bm;            dk_rv_sz = 400000;      // reverse-bloom capture
dk_dA = dk_bm + 400000;   dk_dB = dk_bm + 600000; dk_dA_sz = 200000;   // ping-pong throw
dk_ec = dk_bm + 800000;   dk_ec_sz = 200000;      // ducked echo
dk_hl = dk_bm + 1000000;                          // hall (4 combs x 8000 + 2 allpass x 3000)
dk_sh = dk_bm + 1060000;  dk_sh_sz = 16384;       // shifter / tap ring
dk_sl = dk_bm + 1080000;  dk_sl_sz = 30000;       // slap
memset(dk_bm, 0, 1110000);

dk_tip = 1900000; dk_pn = 1900080; dk_pm = 1900100; dk_ps = 1900120; dk_pd = 1900140; dk_pg = 1900160;
dk_nm = 1900180; dk_hint = 1900200; dk_tn = 1900220;
dk_tbl = 1900240; dk_env = dk_tbl; dk_hold = dk_tbl + 16; dk_tg = dk_tbl + 32; dk_ga = dk_tbl + 48; dk_tgp = dk_tbl + 64;
dk_hp = 1900330; dk_hd = 1900340; dk_sp = 1900350; dk_bs = 1900360;
dk_i = 0; loop(80, dk_tbl[dk_i] = 0; dk_i += 1; );
dk_i = 0; loop(8, dk_hp[dk_i] = 0; dk_hd[dk_i] = 0; dk_i += 1; );
dk_sp[0] = 0.0; dk_sp[1] = 0.33; dk_sp[2] = 0.66;
dk_vis = @@VIS@@;
dk_susm = 63232;   // sustained tricks: BREATH GHOSTUP GHOSTDN GRIT WIDE TREM SWEEP
dk_boot = 1;

dk_bs[0] = 0.22; dk_bs[1] = 0.30; dk_bs[2] = 0.30; dk_bs[3] = 0.20; dk_bs[4] = 0.45; dk_bs[5] = 0.55;
dk_bs[6] = 0.60; dk_bs[7] = 0.50; dk_bs[8] = 0.50; dk_bs[9] = 0.12; dk_bs[10] = 0.15; dk_bs[11] = 0.22;
dk_bs[12] = 0.30; dk_bs[13] = 0.14; dk_bs[14] = 0.18; dk_bs[15] = 0.20;

@@TABLES@@

dk_isr = 1.0 / srate;
dk_c_slow = 1.0 - exp(-1.0 / (srate * 0.6));
dk_c_fast = 1.0 - exp(-1.0 / (srate * 0.003));
dk_rel_c = exp(-1.0 / (srate * 0.9));
dk_dr_c = exp(-1.0 / (srate * 0.12));
dk_W = floor(srate * 0.045);
dk_kb = 1.0 - exp(-6.2831853 * 4000.0 * dk_isr);
dk_kw = 1.0 - exp(-6.2831853 * 250.0 * dk_isr);
dk_kg = 1.0 - exp(-6.2831853 * 1200.0 * dk_isr);
dk_k5 = 1.0 - exp(-6.2831853 * 500.0 * dk_isr);
dk_k3 = 1.0 - exp(-6.2831853 * 3000.0 * dk_isr);
dk_cl0 = floor(1557.0 * srate / 44100.0); dk_cl1 = floor(1617.0 * srate / 44100.0);
dk_cl2 = floor(1491.0 * srate / 44100.0); dk_cl3 = floor(1422.0 * srate / 44100.0);
dk_al0 = floor(225.0 * srate / 44100.0);  dk_al1 = floor(556.0 * srate / 44100.0);
dk_wd1 = floor(srate * 0.011); dk_wd2 = floor(srate * 0.017); dk_bd = floor(srate * 0.0073);

dk_rv_w = 0; dk_rv_rd = 0; dk_swp = 0; dk_bl_lp = 0; dk_bg = 0;
dk_dA_w = 0; dk_ec_w = 0; dk_ec_lp = 0; dk_sh_w = 0; dk_sl_w = 0;
dk_ef = 0; dk_ed = 0; dk_gs = 1; dk_ri_l = 0; dk_ri_r = 0; dk_t1 = 0; dk_t2 = 0;
dk_trp = 0; dk_sv_lo = 0; dk_sv_bd = 0; dk_svf = 0.1; dk_swph = 0;
dk_b_l1 = 0; dk_b_l2 = 0; dk_g_lp = 0; dk_w_l1 = 0; dk_w_l2 = 0;
dk_acc = 0; dk_tc = -1; dk_lf = -1; dk_wsel = 0; dk_beat = 0.5; dk_bpm = 120;
dk_bllen = 3.0; dk_rilen = 2.0; dk_thd = 24000; dk_ecd = 18000; dk_sld = 4500; dk_trr = 4;
dk_fast_db = -90; dk_slow_db = -40; dk_song_db = -40; dk_rg_db = -40; dk_seen = 0;
dk_act_t = 0; dk_gap_t = 0; dk_dens = 0; dk_ctx = 0.5; dk_hot = 0; dk_pe_len = 0; dk_pe_cnt = 0;
dk_key_last = -999; dk_mask_last = -1; dk_clock = 0; dk_t_pe = -99; dk_ch_win = 0; dk_ch_sus = 0;
dk_prod = 0; dk_seed = 0; dk_et = 0; dk_amt = 0.9; dk_dn = 1; dk_sigk = 0; dk_pseudo = 0; dk_en = 0;
strcpy(#dk_l1, "Director idle - press play. Region + energy decisions appear here.");
strcpy(#dk_l2, "");

function dk_hash(a, b) local(x) (
  x = sin(a * 12.9898 + b * 78.233 + dk_seed) * 43758.5453;
  x - floor(x);
);

// top-n tricks from cand ranked by a deterministic per-region hash (+ signature boost)
function dk_choose(cand, n, salt) local(res, best, bk, k, sc) (
  res = 0;
  loop(n,
    best = -1; bk = -1; k = 0;
    loop(16,
      ((cand & (1 << k)) && !(res & (1 << k))) ? (
        sc = dk_hash(salt, k) + (k == dk_sigk ? 0.35 : 0.0);
        (sc > best) ? ( best = sc; bk = k; );
      );
      k += 1;
    );
    (bk >= 0) ? ( res = res | (1 << bk); );
  );
  res;
);

function dk_names(m) local(k, c) (
  strcpy(#dk_tmp, "");
  k = 0; c = 0;
  loop(16,
    (m & (1 << k)) ? (
      (c > 0) ? ( strcat(#dk_tmp, " + "); );
      strcat(#dk_tmp, dk_nm[k]);
      c += 1;
    );
    k += 1;
  );
  (c == 0) ? ( strcpy(#dk_tmp, "none"); );
  #dk_tmp;
);

function dk_preset_changed(p) (
  ((@@FOLLOW@@ == 1) && (dk_boot == 0)) ? ( @@MASK@@ = dk_pm[max(0, min(16, p))]; );
);

function dk_off() (
  dk_i = 0;
  loop(16, dk_tg[dk_i] = 0; dk_hold[dk_i] = 0; dk_env[dk_i] *= 0.9; dk_i += 1; );
);

// ---------------- pitch shifter taps (two crossfaded delay taps) ----------------
function dk_tap(d) local(p, i0, fr, a, b) (
  p = dk_sh_w - d;
  (p < 0) ? ( p += dk_sh_sz; );
  i0 = floor(p); fr = p - i0;
  a = dk_sh[i0]; b = dk_sh[(i0 + 1) % dk_sh_sz];
  a + (b - a) * fr;
);

function dk_shift(slot, ratio) local(ph, d1, d2, y1, y2, w1) (
  ph = dk_sp[slot];
  ph += (1.0 - ratio) / dk_W;
  (ph >= 1.0) ? ( ph -= 1.0; );
  (ph < 0.0) ? ( ph += 1.0; );
  dk_sp[slot] = ph;
  d1 = ph * dk_W + 2.0;
  d2 = (ph >= 0.5 ? ph - 0.5 : ph + 0.5) * dk_W + 2.0;
  y1 = dk_tap(d1);
  y2 = dk_tap(d2);
  w1 = sin(3.14159265 * ph); w1 = w1 * w1;
  y1 * w1 + y2 * (1.0 - w1);
);

// ---------------- small hall (Schroeder): returns left, right in dk_hlL / dk_hlR ----------------
function dk_comb(k, len, x) local(base, p, y) (
  base = dk_hl + k * 8000;
  p = dk_hp[k];
  y = base[p];
  dk_hd[k] += (y - dk_hd[k]) * 0.35;
  base[p] = x + dk_hd[k] * 0.80;
  p += 1; (p >= len) ? ( p = 0; );
  dk_hp[k] = p;
  y;
);

function dk_ap(k, len, x) local(base, p, z, w, y) (
  base = dk_hl + 32000 + (k - 4) * 3000;
  p = dk_hp[k];
  z = base[p];
  w = x + 0.5 * z;
  y = z - 0.5 * w;
  base[p] = w;
  p += 1; (p >= len) ? ( p = 0; );
  dk_hp[k] = p;
  y;
);

function dk_hall(x) local(c0, c1, c2, c3) (
  c0 = dk_comb(0, dk_cl0, x);
  c1 = dk_comb(1, dk_cl1, x);
  c2 = dk_comb(2, dk_cl2, x);
  c3 = dk_comb(3, dk_cl3, x);
  dk_hlL = dk_ap(4, dk_al0, (c0 + c2) * 0.25);
  dk_hlR = dk_ap(5, dk_al1, (c1 + c3) * 0.25);
);

// ---------------- the per-block director (regions + energy -> decisions) ----------------
function dk_block() local(k, w0, w1b, w5, w6, w7, w11, recent, cand, big, hc, pk, pm_) (
  dk_dt = samplesblock * dk_isr;
  dk_prod = max(0, min(16, floor(@@PROD@@ + 0.5)));
  dk_seed = dk_prod * 7.77;
  dk_sigk = dk_ps[dk_prod];
  dk_dn = dk_pd[dk_prod];
  dk_mask = floor(@@MASK@@ + 0.5);
  dk_en = ((play_state & 1) && !(play_state & 2));
  dk_amt = (0.4 + 1.2 * @@SUB@@ * 0.01) * dk_pg[dk_prod];
  dk_bpm = (tempo > 20) ? tempo : 120;
  dk_beat = 60.0 / dk_bpm;
  dk_bllen = min(3.4, 8.0 * dk_beat);
  dk_rilen = min(2.0, 4.0 * dk_beat);
  dk_thd = max(2, min(dk_dA_sz - 2, floor(srate * min(0.9, dk_beat))));
  dk_ecd = max(floor(srate * 0.08), min(dk_ec_sz - 2, floor(srate * min(0.7, dk_beat * 0.75))));
  dk_sld = max(2, min(dk_sl_sz - 2, floor(srate * 0.095)));
  dk_trr = dk_bpm / 60.0 * 2.0;
  k = 0; loop(16, dk_ga[k] = dk_bs[k] * dk_amt; k += 1; );

  dk_en ? (
    // ---- structure (regions from the REAPER bridge; heartbeat optional for older bridge scripts)
    dk_br = (gmem[100] == 1) && (gmem[107] == 1) && ((gmem[109] == 0) || ((time_precise() - gmem[109]) < 2.0));
    dk_rt = dk_br ? gmem[106] : 0;
    dk_sec = dk_br ? gmem[101] : 0;
    dk_et = ((dk_rt >= 1) && (dk_rt <= 6)) ? dk_rt :
            (dk_sec == 3 ? 4 : (dk_sec == 4 ? 5 : (dk_sec == 1 ? 3 : (dk_sec == 5 ? 2 : (dk_sec == 2 ? 3 : 0)))));
    dk_idx = dk_br ? gmem[104] : -1;
    dk_prog = dk_br ? gmem[105] : 0.5;
    dk_lf = (dk_br && gmem[108] > 0) ? gmem[108] : -1;
    dk_tc = (dk_br && gmem[102] > 0) ? gmem[102] : -1;
    dk_wsel = ((dk_tc > 0.06) && (dk_tc < 4.0)) ? 0 : 1;

    // ---- energy (this bus): fast / slow / song-long dB, activity, phrase ends, density
    dk_p = dk_acc / max(1, samplesblock); dk_acc = 0;
    dk_pdb = (dk_p > 0.000000001) ? 10.0 * log10(dk_p) : -90.0;
    dk_fast_db += (dk_pdb - dk_fast_db) * (1.0 - exp(-dk_dt / 0.35));
    ((dk_seen == 0) && (dk_pdb > -52)) ? ( dk_seen = 1; dk_slow_db = dk_pdb; dk_song_db = dk_pdb; dk_rg_db = dk_pdb; );
    dk_act = (dk_pdb > max(-52.0, dk_slow_db - 16.0));
    dk_act ? (
      dk_slow_db += (dk_pdb - dk_slow_db) * (1.0 - exp(-dk_dt / 6.0));
      dk_song_db += (dk_pdb - dk_song_db) * (1.0 - exp(-dk_dt / 40.0));
      dk_rg_db += (dk_pdb - dk_rg_db) * (1.0 - exp(-dk_dt / 8.0));
      dk_act_t += dk_dt; dk_gap_t = 0;
    ) : ( dk_gap_t += dk_dt; );
    dk_pe = 0;
    ((dk_gap_t >= 0.10) && (dk_gap_t - dk_dt < 0.10) && (dk_act_t > 0.45)) ? ( dk_pe = 1; dk_pe_len = dk_act_t; );
    (dk_gap_t > 0.30) ? ( dk_act_t = 0; );
    dk_dens += ((dk_act ? 1.0 : 0.0) - dk_dens) * (1.0 - exp(-dk_dt / 4.0));
    dk_hot = dk_fast_db - dk_rg_db;
    dk_int = max(0.0, min(1.0, (dk_slow_db - dk_song_db + 6.0) / 12.0));
    pm_ = (dk_et == 4) ? 0.85 : ((dk_et == 3) ? 0.55 : ((dk_et == 2) ? 0.40 : ((dk_et == 5) ? 0.30 : ((dk_et == 1) ? 0.25 : ((dk_et == 6) ? 0.30 : 0.5)))));
    dk_ctx = dk_br ? (0.5 * pm_ + 0.5 * dk_int) : dk_int;
    dk_clock += dk_dt;
    recent = (dk_gap_t < 0.5);

    // ---- new region (or palette edited): choose this region's window tricks + sustained layers
    dk_key = dk_br ? ((dk_idx + 1) * 16 + dk_et) : -1;
    ((dk_key != dk_key_last) || (dk_mask != dk_mask_last)) ? (
      dk_key_last = dk_key; dk_mask_last = dk_mask;
      dk_rg_db = dk_slow_db; dk_pe_cnt = 0; dk_t_pe = -99;
      dk_pseudo += 1;
      dk_salt = dk_br ? dk_idx * 3.7 + 1.0 : dk_pseudo;
      dk_ch_win = dk_choose(dk_mask & 2275, dk_dn, dk_salt);
      dk_ch_sus = dk_choose(dk_mask & 63232, (dk_dn >= 2 ? 2 : 1), dk_salt + 41.0);
      strcpy(#dk_n1, dk_names(dk_ch_win));
      strcpy(#dk_n2, dk_names(dk_ch_sus));
      strcpy(#dk_l2, #dk_l1);
      sprintf(#dk_l1, "%s %d | ctx %.2f | into-next: %s | layers: %s", dk_tn[dk_et], dk_idx, dk_ctx, #dk_n1, #dk_n2);
    );

    // ---- window tricks (once per region transition, only inside the right window)
    w0 = ((dk_tc > 0.1) && (dk_tc < 1.6)) || ((dk_lf > 0.1) && (dk_lf < 1.6) && (dk_et == 2 || dk_et == 3));
    w1b = ((dk_tc > 0.06) && (dk_tc < dk_bllen)) || ((dk_lf > 0.06) && (dk_lf < dk_bllen) && (dk_et == 2 || dk_et == 3 || dk_et == 5));
    w5 = ((dk_tc > 0.06) && (dk_tc < dk_rilen)) || ((dk_lf > 0.06) && (dk_lf < dk_rilen) && (dk_et == 2 || dk_et == 3));
    w6 = ((dk_tc > 0.06) && (dk_tc < dk_beat)) || ((dk_lf > 0.06) && (dk_lf < dk_beat) && (dk_et == 3));
    w7 = ((dk_tc > 0.06) && (dk_tc < 4.0 * dk_beat)) || ((dk_et == 5) && (dk_prog < 0.35) && recent);
    w11 = (dk_lf > 0.06) && (dk_lf < 0.45) && (dk_et == 2 || dk_et == 3 || dk_et == 5) && recent;
    dk_tg[0]  = ((dk_ch_win & dk_mask & 1)    && w0  && recent) ? 1 : 0;
    dk_tg[1]  = ((dk_ch_win & dk_mask & 2)    && w1b && (dk_ctx < 0.85)) ? 1 : 0;
    dk_tg[5]  = ((dk_ch_win & dk_mask & 32)   && w5) ? 1 : 0;
    dk_tg[6]  = ((dk_ch_win & dk_mask & 64)   && w6 && (dk_ctx > 0.3)) ? 1 : 0;
    dk_tg[7]  = ((dk_ch_win & dk_mask & 128)  && w7) ? 1 : 0;
    dk_tg[11] = ((dk_ch_win & dk_mask & 2048) && w11) ? 1 : 0;

    // ---- sustained layers (follow the measured energy of the region, slow fades)
    big = ((dk_et == 4) && (dk_ctx > 0.45)) || ((dk_et == 0) && (dk_ctx > 0.7));
    dk_tg[8]  = ((dk_ch_sus & dk_mask & 256)   && big && (dk_ctx > 0.55)) ? 1 : 0;
    dk_tg[9]  = ((dk_ch_sus & dk_mask & 512)   && big && (dk_ctx > 0.60) && ((dk_et == 0) || (dk_prog > 0.45))) ? 1 : 0;
    dk_tg[10] = ((dk_ch_sus & dk_mask & 1024)  && ((dk_et == 5) || (big && (dk_ctx > 0.85))) && recent) ? 1 : 0;
    dk_tg[12] = ((dk_ch_sus & dk_mask & 4096)  && (dk_ctx > 0.78) && (dk_hot > -1.0)) ? 1 : 0;
    dk_tg[13] = ((dk_ch_sus & dk_mask & 8192)  && big) ? 1 : 0;
    dk_tg[14] = ((dk_ch_sus & dk_mask & 16384) && (dk_ctx < 0.5) && ((dk_et == 0) || (dk_et == 1) || (dk_et == 2) || (dk_et == 6)) && (dk_dens > 0.15)) ? 1 : 0;
    dk_tg[15] = ((dk_ch_sus & dk_mask & 32768) && (dk_ctx < 0.7) && ((dk_et == 0) || (dk_et == 1) || (dk_et == 2) || (dk_et == 3)) && ((dk_et == 0) || ((dk_prog > 0.15) && (dk_prog < 0.9)))) ? 1 : 0;

    // ---- phrase-end tricks: one per phrase end at most, and not every phrase (variety, restraint)
    k = 2; loop(3, (dk_hold[k] > 0) ? ( dk_hold[k] -= dk_dt; ); k += 1; );
    (dk_pe && ((dk_mask & 28) != 0)) ? (
      dk_pe_cnt += 1;
      hc = dk_hash(dk_idx * 13.0 + dk_pe_cnt, 99.0);
      ((hc < 0.30 + 0.20 * dk_dn) && ((dk_clock - dk_t_pe) > 3.0) && (dk_pe_len > 0.7) && !((dk_tc > 0) && (dk_tc < 1.6))) ? (
        cand = dk_mask & 28;
        (dk_ctx > 0.6) ? ( cand = cand & 20; );
        pk = dk_choose(cand, 1, dk_idx * 17.0 + dk_pe_cnt);
        (pk & 4)  ? ( dk_hold[2] = 2.2; strcpy(#dk_pk, dk_nm[2]); );
        (pk & 8)  ? ( dk_hold[3] = 0.6; strcpy(#dk_pk, dk_nm[3]); );
        (pk & 16) ? ( dk_hold[4] = 2.4; strcpy(#dk_pk, dk_nm[4]); );
        (pk != 0) ? (
          dk_t_pe = dk_clock;
          strcpy(#dk_l2, #dk_l1);
          sprintf(#dk_l1, "phrase end %.1fs | %s r%d | ctx %.2f | fired %s", dk_pe_len, dk_tn[dk_et], dk_idx, dk_ctx, #dk_pk);
        );
      );
    );
    dk_tg[2] = (dk_hold[2] > 0) ? 1 : 0;
    dk_tg[3] = (dk_hold[3] > 0) ? 1 : 0;
    dk_tg[4] = (dk_hold[4] > 0) ? 1 : 0;

    // ---- log window tricks as they start
    k = 0;
    loop(16,
      ((dk_tg[k] > 0.5) && (dk_tgp[k] < 0.5) && !(dk_susm & (1 << k)) && (k != 2) && (k != 3) && (k != 4)) ? (
        strcpy(#dk_l2, #dk_l1);
        sprintf(#dk_l1, "%s r%d | ctx %.2f | window: %s", dk_tn[dk_et], dk_idx, dk_ctx, dk_nm[k]);
      );
      dk_tgp[k] = dk_tg[k];
      k += 1;
    );
    // slow free-running filter-sweep LFO (one cycle per two bars)
    dk_swph += dk_dt * (dk_bpm / 60.0) / 8.0;
    (dk_swph >= 1.0) ? ( dk_swph -= 1.0; );
    dk_svf = min(0.45, 2.0 * sin(3.14159265 * 450.0 * pow(4.5, 0.5 + 0.5 * sin(6.2831853 * dk_swph)) * dk_isr));
  ) : (
    k = 0; loop(16, dk_tg[k] = 0; dk_hold[k] = 0; dk_tgp[k] = 0; k += 1; );
    dk_acc = 0;
  );
);

// ---------------- the per-sample engine ----------------
function dk_process() (
  dk_m = (out_l + out_r) * 0.5;
  dk_acc += dk_m * dk_m;
  (dk_tc > 0) ? ( dk_tc -= dk_isr; );
  (dk_lf > 0) ? ( dk_lf -= dk_isr; );
  dk_wl = dk_wsel ? dk_lf : dk_tc;

  dk_i = 0;
  loop(16, dk_env[dk_i] += (dk_tg[dk_i] - dk_env[dk_i]) * ((dk_susm & (1 << dk_i)) ? dk_c_slow : dk_c_fast); dk_i += 1; );

  dk_ef = max(abs(dk_m), dk_ef * dk_rel_c);
  dk_ed = max(abs(dk_m), dk_ed * dk_dr_c);
  dk_duck = max(0.0, 1.0 - dk_ed * 9.0);
  dk_cap = dk_ef * 0.5 + 0.0003;
  dk_xl = 0; dk_xr = 0;

  // sends are always open so the last phrase is ready when a tail opens
  dk_rv[dk_rv_w] = dk_m; dk_rv_w = (dk_rv_w + 1) % dk_rv_sz;
  dk_sh[dk_sh_w] = dk_m; dk_sh_w = (dk_sh_w + 1) % dk_sh_sz;
  dk_sl[dk_sl_w] = dk_m;

  // THROW: ping-pong capture only inside its window, returns until the downbeat
  dk_sg = (dk_env[0] > 0.5) ? 1.0 : 0.0;
  dk_ra = dk_dA[(dk_dA_w - dk_thd + dk_dA_sz) % dk_dA_sz];
  dk_rb = dk_dB[(dk_dA_w - dk_thd + dk_dA_sz) % dk_dA_sz];
  dk_dA[dk_dA_w] = out_l * dk_sg + dk_rb * 0.46;
  dk_dB[dk_dA_w] = out_r * dk_sg + dk_ra * 0.46;
  dk_dA_w = (dk_dA_w + 1) % dk_dA_sz;
  dk_xl += dk_ra * dk_ga[0] * dk_env[0];
  dk_xr += dk_rb * dk_ga[0] * dk_env[0];

  // BLOOM: replay the phrase before the transition backwards, swelling into the downbeat
  dk_bw = (dk_tg[1] > 0.5);
  (dk_bw && !dk_swp) ? ( dk_rv_rd = dk_rv_w; );
  dk_swp = dk_bw;
  dk_bw ? (
    dk_rv_rd = (dk_rv_rd - 1 + dk_rv_sz) % dk_rv_sz;
    dk_bl_lp += (dk_rv[dk_rv_rd] - dk_bl_lp) * 0.28;
    dk_bgt = sqr(max(0.0, min(1.0, 1.0 - dk_wl / dk_bllen)));
  ) : ( dk_bl_lp *= 0.995; dk_bgt = 0.0; );
  dk_bg += (dk_bgt - dk_bg) * 0.004;
  dk_xl += dk_bl_lp * dk_bg * dk_ga[1];
  dk_xr += dk_bl_lp * dk_bg * dk_ga[1];

  // ECHO: tempo-synced dotted echo, ducked by the performance so it lives in the gaps
  dk_er = dk_ec[(dk_ec_w - dk_ecd + dk_ec_sz) % dk_ec_sz];
  dk_er2 = dk_ec[(dk_ec_w - dk_ecd - 211 + dk_ec_sz * 2) % dk_ec_sz];
  dk_ec_lp += (dk_er - dk_ec_lp) * 0.35;
  dk_ec[dk_ec_w] = dk_m * 0.8 + dk_ec_lp * 0.40;
  dk_ec_w = (dk_ec_w + 1) % dk_ec_sz;
  dk_xl += dk_ec_lp * dk_ga[2] * dk_env[2] * dk_duck;
  dk_xr += dk_er2 * dk_ga[2] * dk_env[2] * dk_duck * 0.9;

  // SLAP
  dk_sr = dk_sl[(dk_sl_w - dk_sld + dk_sl_sz) % dk_sl_sz];
  dk_sr2 = dk_sl[(dk_sl_w - dk_sld - 160 + dk_sl_sz * 2) % dk_sl_sz];
  dk_sl_w = (dk_sl_w + 1) % dk_sl_sz;
  dk_xl += dk_sr * dk_ga[3] * dk_env[3] * dk_duck;
  dk_xr += dk_sr2 * dk_ga[3] * dk_env[3] * dk_duck;

  // HALL
  dk_hall(dk_m * 0.5);
  dk_xl += dk_hlL * dk_ga[4] * dk_env[4] * dk_duck;
  dk_xr += dk_hlR * dk_ga[4] * dk_env[4] * dk_duck;

  // BREATH / sparkle: saturated high-band shadow, decorrelated between sides
  (dk_env[8] > 0.0005) ? (
    dk_b_l1 += (dk_m - dk_b_l1) * dk_kb;
    dk_hb = dk_tap(dk_bd);
    dk_b_l2 += (dk_hb - dk_b_l2) * dk_kb;
    dk_y1 = (dk_m - dk_b_l1) * 5.0; dk_y2 = (dk_hb - dk_b_l2) * 5.0;
    dk_xl += (dk_y1 / (1.0 + abs(dk_y1))) * 0.35 * dk_ga[8] * dk_env[8];
    dk_xr += (dk_y2 / (1.0 + abs(dk_y2))) * 0.35 * dk_ga[8] * dk_env[8];
  );

  // GHOSTUP / GHOSTDN / DIVE: octave-up halo, octave-down shadow, pitch dive tail
  (dk_env[9] > 0.0005) ? (
    dk_u = dk_shift(0, 2.0);
    dk_xl += dk_u * dk_ga[9] * dk_env[9]; dk_xr += dk_u * dk_ga[9] * dk_env[9] * 0.9;
  );
  (dk_env[10] > 0.0005) ? (
    dk_d = dk_shift(1, 0.5);
    dk_xl += dk_d * dk_ga[10] * dk_env[10]; dk_xr += dk_d * dk_ga[10] * dk_env[10];
  );
  (dk_env[11] > 0.0005) ? (
    dk_dv = dk_shift(2, 1.0 - 0.45 * max(0.0, min(1.0, 1.0 - dk_lf / 0.45)));
    dk_xl += dk_dv * dk_ga[11] * dk_env[11]; dk_xr += dk_dv * dk_ga[11] * dk_env[11];
  );

  // GRIT: clipped mid/high layer
  (dk_env[12] > 0.0005) ? (
    dk_g_lp += (dk_m - dk_g_lp) * dk_kg;
    dk_gy = max(-0.5, min(0.5, (dk_m - dk_g_lp) * 6.0));
    dk_xl += dk_gy * 0.5 * dk_ga[12] * dk_env[12]; dk_xr += dk_gy * 0.5 * dk_ga[12] * dk_env[12];
  );

  // WIDE: two decorrelated micro-doubles, high-passed so the low end stays mono
  (dk_env[13] > 0.0005) ? (
    dk_wa = dk_tap(dk_wd1); dk_wb = dk_tap(dk_wd2);
    dk_w_l1 += (dk_wa - dk_w_l1) * dk_kw; dk_w_l2 += (dk_wb - dk_w_l2) * dk_kw;
    dk_xl += (dk_wa - dk_w_l1) * dk_ga[13] * dk_env[13];
    dk_xr -= (dk_wb - dk_w_l2) * dk_ga[13] * dk_env[13];
  );

  // SWEEP: slow band-pass movement blended in parallel
  (dk_env[15] > 0.0005) ? (
    dk_sv_lo += dk_svf * dk_sv_bd;
    dk_sv_hi = dk_m - dk_sv_lo - 0.45 * dk_sv_bd;
    dk_sv_bd += dk_svf * dk_sv_hi;
    dk_xl += dk_sv_bd * dk_ga[15] * dk_env[15]; dk_xr += dk_sv_bd * dk_ga[15] * dk_env[15];
  );

  // ---- inline (dry) modifiers ----
  (dk_env[14] > 0.0005) ? (
    dk_trp += dk_trr * dk_isr; (dk_trp >= 1.0) ? ( dk_trp -= 1.0; );
    dk_tm = 1.0 - min(0.35, dk_ga[14]) * dk_env[14] * (0.5 + 0.5 * sin(6.2831853 * dk_trp));
    out_l *= dk_tm; out_r *= dk_tm;
  );
  (dk_env[5] > 0.0005) ? (
    dk_ri_p = max(0.0, min(1.0, 1.0 - dk_wl / dk_rilen));
    dk_ri_k = 1.0 - exp(-6.2831853 * 90.0 * pow(10.0, dk_ri_p) * dk_isr);
    dk_ri_l += (out_l - dk_ri_l) * dk_ri_k; dk_ri_r += (out_r - dk_ri_r) * dk_ri_k;
    dk_rm = dk_env[5] * min(0.8, dk_ga[5]);
    out_l -= dk_ri_l * dk_rm; out_r -= dk_ri_r * dk_rm;
  );
  (dk_env[7] > 0.0005) ? (
    dk_t1 += (dk_m - dk_t1) * dk_k5;
    dk_t2 += ((dk_m - dk_t1) - dk_t2) * dk_k3;
    dk_tmx = min(0.6, dk_env[7] * dk_ga[7]);
    out_l += (dk_t2 * 1.3 - out_l) * dk_tmx; out_r += (dk_t2 * 1.3 - out_r) * dk_tmx;
  );
  dk_cph = dk_wl / (dk_beat * 0.25);
  dk_cfr = dk_cph - floor(dk_cph);
  dk_ct = ((dk_env[6] > 0.5) && (dk_cfr < 0.45)) ? (1.0 - min(0.9, dk_ga[6])) : 1.0;
  dk_gs += (dk_ct - dk_gs) * 0.03;
  out_l *= dk_gs; out_r *= dk_gs;

  // ---- add the (capped) wet bed ----
  out_l += max(-dk_cap, min(dk_cap, dk_xl));
  out_r += max(-dk_cap, min(dk_cap, dk_xr));
);
// ---------------- GUI (called from @gfx only) ----------------
// ===== EAR-CANDY DIRECTOR END =====
'''

GUI_TEMPLATE = r'''// ===== EAR-CANDY DIRECTOR GUI BEGIN =====
function dk_gui(gx, gy, gw, gh, ar, ag, ab) (
  gfx_r = 0.024; gfx_g = 0.026; gfx_b = 0.036; gfx_rect(gx, gy, gw, gh);
  gfx_r = ar; gfx_g = ag; gfx_b = ab; gfx_rect(gx, gy, gw, gh, 0);
  gfx_setfont(1, "Orbitron", 15, 'b'); gfx_x = gx + 18; gfx_y = gy + 12;
  gfx_drawstr("EAR-CANDY DIRECTOR  //  PRODUCER PLAYBOOK");
  gfx_setfont(1, "Consolas", 12, 'b'); gfx_r = 0.62; gfx_g = 0.68; gfx_b = 0.78;
  gfx_x = gx + 18; gfx_y = gy + 34;
  gfx_drawstr("Reads regions + live energy, then adds one subtle producer trick at a time.");

  dg_cw = floor((gw - 48) / 2);
  dg_lx = gx + 16; dg_rx = dg_lx + dg_cw + 16; dg_ty = gy + 58;

  // director on / off
  dg_on = (@@DIR@@ == 1);
  dg_hv = (mouse_x >= dg_lx && mouse_x <= dg_lx + dg_cw && mouse_y >= dg_ty && mouse_y <= dg_ty + 28);
  dg_on ? ( gfx_r = ar * 0.28; gfx_g = ag * 0.28; gfx_b = ab * 0.28; ) : ( gfx_r = 0.07; gfx_g = 0.07; gfx_b = 0.10; );
  gfx_rect(dg_lx, dg_ty, dg_cw, 28);
  dg_on ? ( gfx_r = ar; gfx_g = ag; gfx_b = ab; ) : ( gfx_r = 0.35; gfx_g = 0.35; gfx_b = 0.42; );
  gfx_rect(dg_lx, dg_ty, dg_cw, 28, 0);
  gfx_setfont(1, "Orbitron", 12, 'b');
  dg_s = dg_on ? "DIRECTOR ON: REGION + ENERGY AWARE" : "DIRECTOR OFF: CLASSIC FIXED-TIMING";
  gfx_measurestr(dg_s, dg_w, dg_h); gfx_x = dg_lx + (dg_cw - dg_w) * 0.5; gfx_y = dg_ty + 8; gfx_drawstr(dg_s);
  (mouse_clicked && dg_hv) ? ( @@DIR@@ = !@@DIR@@; slider_automate(); );

  // amount slider
  dg_sy = dg_ty + 36;
  gfx_setfont(1, "Orbitron", 12, 'b'); gfx_r = 0.95; gfx_g = 0.90; gfx_b = 0.95;
  gfx_x = dg_lx; gfx_y = dg_sy; gfx_drawstr("EAR-CANDY AMOUNT");
  sprintf(#dg_v, "%d %%", floor(@@SUB@@ + 0.5));
  gfx_measurestr(#dg_v, dg_w, dg_h); gfx_r = ar; gfx_g = ag; gfx_b = ab;
  gfx_x = dg_lx + dg_cw - dg_w; gfx_y = dg_sy; gfx_drawstr(#dg_v);
  gfx_r = 0.03; gfx_g = 0.03; gfx_b = 0.06; gfx_rect(dg_lx, dg_sy + 20, dg_cw, 14);
  gfx_r = ar * 0.4; gfx_g = ag * 0.4; gfx_b = ab * 0.4; gfx_rect(dg_lx, dg_sy + 20, dg_cw, 14, 0);
  gfx_r = ar; gfx_g = ag; gfx_b = ab; gfx_rect(dg_lx + 1, dg_sy + 21, floor(@@SUB@@ * 0.01 * (dg_cw - 2)), 12);
  ((mouse_cap & 1) && mouse_x >= dg_lx && mouse_x <= dg_lx + dg_cw && mouse_y >= dg_sy + 18 && mouse_y <= dg_sy + 36) ? (
    @@SUB@@ = max(0, min(100, floor((mouse_x - dg_lx) / dg_cw * 100 + 0.5))); slider_automate();
  );

  // trick palette: toggle = in the palette; bar = live activity
  dg_gy = dg_sy + 46; dg_mv = floor(@@MASK@@ + 0.5);
  dg_nv = 0; dg_k = 0; loop(16, ((dk_vis & (1 << dg_k)) ? ( dg_nv += 1; ); ); dg_k += 1; );
  dg_rows = ceil(dg_nv / 2);
  dg_rh = max(20, min(28, floor((gh - 58 - 82 - 80 - 12) / dg_rows) - 4));
  dg_n = 0; dg_k = 0;
  loop(16,
    (dk_vis & (1 << dg_k)) ? (
      dg_pw = floor(dg_cw * 0.5) - 3;
      dg_px = dg_lx + (dg_n % 2) * (floor(dg_cw * 0.5) + 2);
      dg_py = dg_gy + floor(dg_n / 2) * (dg_rh + 4);
      dg_mon = (dg_mv & (1 << dg_k)) ? 1 : 0;
      dg_hv = (mouse_x >= dg_px && mouse_x <= dg_px + dg_pw && mouse_y >= dg_py && mouse_y <= dg_py + dg_rh);
      dg_mon ? ( gfx_r = 0.07; gfx_g = 0.09; gfx_b = 0.12; ) : ( gfx_r = 0.03; gfx_g = 0.03; gfx_b = 0.05; );
      dg_hv ? ( gfx_r += 0.05; gfx_g += 0.05; gfx_b += 0.05; );
      gfx_rect(dg_px, dg_py, dg_pw, dg_rh);
      gfx_r = ar; gfx_g = ag; gfx_b = ab; gfx_a = 0.55;
      gfx_rect(dg_px + 1, dg_py + 1, floor(dk_env[dg_k] * (dg_pw - 2)), dg_rh - 2);
      gfx_a = 1.0;
      dg_mon ? ( gfx_r = ar; gfx_g = ag; gfx_b = ab; ) : ( gfx_r = 0.22; gfx_g = 0.22; gfx_b = 0.30; );
      gfx_rect(dg_px, dg_py, dg_pw, dg_rh, 0);
      gfx_setfont(1, "Consolas", 12, 'b');
      dg_mon ? ( gfx_r = 0.95; gfx_g = 0.95; gfx_b = 0.98; ) : ( gfx_r = 0.42; gfx_g = 0.45; gfx_b = 0.52; );
      sprintf(#dg_l, "%s%s", (dg_k == dk_ps[dk_prod] && dg_mon) ? "* " : "", dk_nm[dg_k]);
      gfx_x = dg_px + 8; gfx_y = dg_py + floor((dg_rh - 12) * 0.5); gfx_drawstr(#dg_l);
      (mouse_clicked && dg_hv) ? (
        @@MASK@@ = (dg_mv & (1 << dg_k)) ? dg_mv - (1 << dg_k) : dg_mv + (1 << dg_k);
        slider_automate();
      );
      dg_n += 1;
    );
    dg_k += 1;
  );

  // director reasoning log
  dg_ly = dg_gy + dg_rows * (dg_rh + 4) + 4;
  gfx_r = 0.016; gfx_g = 0.018; gfx_b = 0.026; gfx_rect(dg_lx, dg_ly, dg_cw, 62);
  gfx_r = ar * 0.5; gfx_g = ag * 0.5; gfx_b = ab * 0.5; gfx_rect(dg_lx, dg_ly, dg_cw, 62, 0);
  gfx_setfont(1, "Consolas", 11.5, 'b');
  gfx_r = ar; gfx_g = ag; gfx_b = ab; gfx_x = dg_lx + 8; gfx_y = dg_ly + 6; gfx_drawstr(#dk_l1);
  gfx_r = 0.60; gfx_g = 0.64; gfx_b = 0.72; gfx_x = dg_lx + 8; gfx_y = dg_ly + 24; gfx_drawstr(#dk_l2);
  sprintf(#dg_st, "%s | ctx %.2f | energy %.1f dB (song %.1f) | density %d%%", dk_tn[dk_et], dk_ctx, dk_slow_db, dk_song_db, floor(dk_dens * 100));
  gfx_r = 0.42; gfx_g = 0.46; gfx_b = 0.54; gfx_x = dg_lx + 8; gfx_y = dg_ly + 42; gfx_drawstr(#dg_st);

  // ---- right column: producer playbook ----
  (dg_last_prod != @@PROD@@) ? ( dg_pbi = max(0, min(16, floor(@@PROD@@ + 0.5))); dg_last_prod = @@PROD@@; );
  gfx_r = 0.018; gfx_g = 0.020; gfx_b = 0.028; gfx_rect(dg_rx, dg_ty, dg_cw, gh - 66);
  gfx_r = ar * 0.7; gfx_g = ag * 0.7; gfx_b = ab * 0.7; gfx_rect(dg_rx, dg_ty, dg_cw, gh - 66, 0);
  gfx_r = 0.08; gfx_g = 0.07; gfx_b = 0.12; gfx_rect(dg_rx + 8, dg_ty + 8, 32, 26); gfx_rect(dg_rx + dg_cw - 40, dg_ty + 8, 32, 26);
  gfx_r = ar; gfx_g = ag; gfx_b = ab; gfx_rect(dg_rx + 8, dg_ty + 8, 32, 26, 0); gfx_rect(dg_rx + dg_cw - 40, dg_ty + 8, 32, 26, 0);
  gfx_setfont(1, "Orbitron", 14, 'b'); gfx_r = 1.0; gfx_g = 1.0; gfx_b = 1.0;
  gfx_x = dg_rx + 19; gfx_y = dg_ty + 13; gfx_drawstr("<");
  gfx_x = dg_rx + dg_cw - 29; gfx_y = dg_ty + 13; gfx_drawstr(">");
  gfx_measurestr(dk_pn[dg_pbi], dg_w, dg_h);
  gfx_r = ar; gfx_g = ag; gfx_b = ab; gfx_x = dg_rx + (dg_cw - dg_w) * 0.5; gfx_y = dg_ty + 13; gfx_drawstr(dk_pn[dg_pbi]);
  (mouse_clicked && mouse_x >= dg_rx + 8 && mouse_x <= dg_rx + 40 && mouse_y >= dg_ty + 8 && mouse_y <= dg_ty + 34) ? ( dg_pbi = (dg_pbi + 16) % 17; );
  (mouse_clicked && mouse_x >= dg_rx + dg_cw - 40 && mouse_x <= dg_rx + dg_cw - 8 && mouse_y >= dg_ty + 8 && mouse_y <= dg_ty + 34) ? ( dg_pbi = (dg_pbi + 1) % 17; );

  gfx_setfont(1, "Consolas", 11, 'b'); gfx_r = 0.50; gfx_g = 0.54; gfx_b = 0.62;
  gfx_x = dg_rx + 12; gfx_y = dg_ty + 40; gfx_drawstr("Craft heuristics inspired by each producer's sound, not session notes.");
  gfx_setfont(1, "Consolas", 12, 'b');
  dg_n = 0;
  loop(4,
    dg_n == 0 ? ( gfx_r = 0.00; gfx_g = 0.85; gfx_b = 1.00; ) :
    dg_n == 1 ? ( gfx_r = 0.15; gfx_g = 0.95; gfx_b = 0.45; ) :
    dg_n == 2 ? ( gfx_r = 1.00; gfx_g = 0.75; gfx_b = 0.20; ) : ( gfx_r = 0.95; gfx_g = 0.55; gfx_b = 0.90; );
    gfx_x = dg_rx + 12; gfx_y = dg_ty + 62 + dg_n * 20;
    gfx_drawstr("- ");
    gfx_drawstr(dk_tip[dg_pbi * 4 + dg_n]);
    dg_n += 1;
  );

  gfx_setfont(1, "Orbitron", 12, 'b'); gfx_r = ar; gfx_g = ag; gfx_b = ab;
  gfx_x = dg_rx + 12; gfx_y = dg_ty + 150; gfx_drawstr("SIGNATURE PALETTE  (* = signature)");
  gfx_setfont(1, "Consolas", 11.5, 'b');
  dg_pm_v = floor(dk_pm[dg_pbi] + 0.5);
  dg_n = 0; dg_k = 0;
  loop(16,
    ((dg_pm_v & (1 << dg_k)) && (dg_n < 7)) ? (
      (dg_k == dk_ps[dg_pbi]) ? ( gfx_r = 1.0; gfx_g = 0.9; gfx_b = 0.5; ) : ( gfx_r = 0.78; gfx_g = 0.82; gfx_b = 0.90; );
      sprintf(#dg_l, "%s%s: %s", (dg_k == dk_ps[dg_pbi]) ? "* " : "  ", dk_nm[dg_k], dk_hint[dg_k]);
      gfx_x = dg_rx + 12; gfx_y = dg_ty + 172 + dg_n * 18; gfx_drawstr(#dg_l);
      dg_n += 1;
    );
    dg_k += 1;
  );
  dg_by = dg_ty + 304;
  dg_hv = (mouse_x >= dg_rx + 12 && mouse_x <= dg_rx + dg_cw - 12 && mouse_y >= dg_by && mouse_y <= dg_by + 30);
  dg_hv ? ( gfx_r = ar * 0.35; gfx_g = ag * 0.35; gfx_b = ab * 0.35; ) : ( gfx_r = ar * 0.18; gfx_g = ag * 0.18; gfx_b = ab * 0.18; );
  gfx_rect(dg_rx + 12, dg_by, dg_cw - 24, 30);
  gfx_r = ar; gfx_g = ag; gfx_b = ab; gfx_rect(dg_rx + 12, dg_by, dg_cw - 24, 30, 0);
  gfx_setfont(1, "Orbitron", 12, 'b');
  dg_s = "LOAD THIS PALETTE INTO THE DIRECTOR";
  gfx_measurestr(dg_s, dg_w, dg_h); gfx_x = dg_rx + (dg_cw - dg_w) * 0.5; gfx_y = dg_by + 8; gfx_drawstr(dg_s);
  (mouse_clicked && dg_hv) ? ( @@MASK@@ = dk_pm[dg_pbi]; slider_automate(); );

  dg_fy = dg_by + 38;
  dg_hv = (mouse_x >= dg_rx + 12 && mouse_x <= dg_rx + dg_cw - 12 && mouse_y >= dg_fy && mouse_y <= dg_fy + 26);
  (@@FOLLOW@@ == 1) ? ( gfx_r = ar * 0.25; gfx_g = ag * 0.25; gfx_b = ab * 0.25; ) : ( gfx_r = 0.06; gfx_g = 0.06; gfx_b = 0.09; );
  gfx_rect(dg_rx + 12, dg_fy, dg_cw - 24, 26);
  (@@FOLLOW@@ == 1) ? ( gfx_r = ar; gfx_g = ag; gfx_b = ab; ) : ( gfx_r = 0.30; gfx_g = 0.30; gfx_b = 0.38; );
  gfx_rect(dg_rx + 12, dg_fy, dg_cw - 24, 26, 0);
  gfx_setfont(1, "Orbitron", 11, 'b');
  dg_s = (@@FOLLOW@@ == 1) ? "PALETTE FOLLOWS PRODUCER PRESET: ON" : "PALETTE FOLLOWS PRODUCER PRESET: OFF";
  gfx_measurestr(dg_s, dg_w, dg_h); gfx_x = dg_rx + (dg_cw - dg_w) * 0.5; gfx_y = dg_fy + 7; gfx_drawstr(dg_s);
  (mouse_clicked && dg_hv) ? ( @@FOLLOW@@ = !@@FOLLOW@@; slider_automate(); );
);
// ===== EAR-CANDY DIRECTOR GUI END =====
'''

def rd(path):
    raw = open(path, 'rb').read().decode('utf-8')
    return raw.replace('\r\n', '\n'), ('\r\n' in raw)

def wr(path, t, crlf):
    open(path, 'wb').write((t.replace('\n', '\r\n') if crlf else t).encode('utf-8'))

def sub1(t, old, new):
    assert t.count(old) == 1, (old[:70], t.count(old))
    return t.replace(old, new)

def cut(t, start, end, new):
    a = t.index(start); b = t.index(end, a)
    return t[:a] + new + t[b:]

# =============================== VOCAL ===============================
def patch_vocal():
    P = DIR + r'\Damei_VocalSuite.jsfx'
    t, crlf = rd(P)
    # curated tips parsed from the current file
    tips = [[None]*4 for _ in range(17)]
    for m in re.finditer(r'pb_t\[(\d+)\] = "(.*?)";', t):
        i = int(m.group(1)); tips[i // 4][i % 4] = m.group(2)
    assert all(all(x for x in r) for r in tips)
    vis = 0xFFFF & ~BIT['TREM'] & ~BIT['SWEEP']
    sfx = dict(DIR='slider39', SUB='slider40', MASK='slider41', FOLLOW='slider42', PROD='slider18')
    kern = kernel(sfx, NAMES_V, tips, VOC, vis, 'v')
    gui = GUI_TEMPLATE
    for k, v in sfx.items():
        gui = gui.replace('@@%s@@' % k, v)

    # sliders
    t = re.sub(r'slider36:.*\n', '', t); t = re.sub(r'slider37:.*\n', '', t); t = re.sub(r'slider38:.*\n', '', t)
    defmask = mask_of(VOC[15][0])
    t = sub1(t, 'slider34:2.0<0.5,4.0,0.5>-Reverse Swell Duration (Bars)\n',
             'slider34:2.0<0.5,4.0,0.5>-Reverse Swell Duration (Bars)\n'
             'slider39:1<0,1,1{Classic Fixed-Timing Automators,Ear-Candy Director (Region + Energy Aware)}>-Ear-Candy Director\n'
             'slider40:40<0,100,1>-Ear-Candy Amount (%%)\n'
             'slider41:%d<0,65535,1>-Ear-Candy Trick Palette (bitmask)\n'
             'slider42:1<0,1,1{Manual Palette,Follow Producer Preset}>-Ear-Candy Palette Follows Producer\n' % defmask)
    # init block (replace the v2 init + apply_candy_for)
    t = cut(t, '// ---- Producer Ear-Candy v2:', 'function apply_vocal_preset(p_idx) (', kern + 'dk_boot = 0;\n\n')
    t = sub1(t, 'apply_candy_for(p_idx);', 'dk_preset_changed(p_idx);')
    # block
    t = cut(t, 'is_play = ((play_state & 1)', 'is_pre_drop_throw = (slider30 && is_play && g_to_chorus_sec',
            'is_play = ((play_state & 1) && !(play_state & 2));\n(slider39 == 1) ? ( dk_block(); ) : ( dk_off(); );\n')
    t = sub1(t, 'is_pre_drop_throw = (slider30 && is_play && g_to_chorus_sec',
             'is_pre_drop_throw = (slider39 == 0 && slider30 && is_play && g_to_chorus_sec')
    # sample
    t = sub1(t, 'cd_mono = (out_l + out_r) * 0.5;\ngtc_s > 0.0 ? gtc_s -= 1.0 / srate;\n', '')
    t = cut(t, '\n// 6b. Ear-Candy v2', '\n// Contextual Distorted Ad-Lib / Megaphone Choke', '')
    t = sub1(t, 'slider32 == 0 ? tel_trigger = 0;', 'slider32 == 0 ? tel_trigger = 0;\nslider39 == 1 ? tel_trigger = 0;')
    t = cut(t, '\n// Pre-chorus filter rise:', '// 7. Headroom Clipper & Output Trim',
            '\n// Ear-Candy Director (region + energy aware; replaces the fixed-timing automators)\n(slider39 == 1) ? ( dk_process(); );\n\n')
    # gui helper
    t = cut(t, '// Pill toggle used by the Ear-Candy tab.', '// Helper function for Imperial Magenta Param Sliders', gui + '\n')
    # tab 1 body
    a = t.index('// TAB 1: PRODUCER EAR-CANDY')
    a = t.index('slider1 == 1 ? (', a)
    b = t.index('// =============================================================================\n// TAB 2: DUAL-STAGE', a)
    t = t[:a] + 'slider1 == 1 ? (\n  dk_gui(disp_x, disp_y, disp_w, disp_h, 1.00, 0.16, 0.52);\n);\n\n' + t[b:]
    wr(P, t, crlf)
    print('vocal ok')

# =============================== GUITAR ===============================
def patch_guitar():
    P = DIR + r'\Damei_GuitarSuite.jsfx'
    t, crlf = rd(P)
    vis = 0xFFFF
    sfx = dict(DIR='slider48', SUB='slider49', MASK='slider50', FOLLOW='slider51', PROD='slider23')
    kern = kernel(sfx, NAMES_G, GTIPS, GTR, vis, 'g')
    gui = GUI_TEMPLATE
    for k, v in sfx.items():
        gui = gui.replace('@@%s@@' % k, v)
    defmask = mask_of(GTR[0][0])

    # tab list + sliders
    t = sub1(t, 'slider1:0<0,5,1{Guitar Wall Overview', 'slider1:0<0,6,1{Guitar Wall Overview')
    t = sub1(t, ',Producer Matrix & Session Tips}>', ',Producer Matrix & Session Tips,Ear-Candy Director}>')
    t = re.sub(r'(slider46:30<0,100,5>[^\n]*\n)', lambda m: m.group(1) +
               'slider48:1<0,1,1{Classic Fixed-Timing Automators,Ear-Candy Director (Region + Energy Aware)}>-Ear-Candy Director\n'
               'slider49:40<0,100,1>-Ear-Candy Amount (%%)\n'
               'slider50:' + str(defmask) + '<0,65535,1>-Ear-Candy Trick Palette (bitmask)\n'
               'slider51:1<0,1,1{Manual Palette,Follow Producer Preset}>-Ear-Candy Palette Follows Producer\n', t, count=1)
    assert 'slider50:' in t
    # kernel before the preset matrix
    m = re.search(r'// [─]+\n// PRODUCER PRESET MATRIX \(0 to 16\)', t)
    assert m
    t = t[:m.start()] + kern + '\n' + t[m.start():]
    t = sub1(t, 'update_guitar_filters();\napply_guitar_preset(slider23);\n',
             'update_guitar_filters();\napply_guitar_preset(slider23);\ndk_boot = 0;\n')
    t = sub1(t, 'slider28 = 1; slider37 = 0.4; slider38 = -0.2; slider39 = -0.6;\n  );\n\n  update_guitar_filters();\n);',
             'slider28 = 1; slider37 = 0.4; slider38 = -0.2; slider39 = -0.6;\n  );\n\n  dk_preset_changed(p_idx);\n  update_guitar_filters();\n);')
    # block
    t = sub1(t, '  mtrim_block();\n\n@sample',
             '  gk_play = ((play_state & 1) && !(play_state & 2));\n  (slider48 == 1) ? ( dk_block(); ) : ( dk_off(); );\n\n  mtrim_block();\n\n@sample')
    # legacy automators: only when Director is off, and only while the transport is playing
    t = sub1(t, 'slider42 && (is_pre_drop || slider42 == 2) ? (', 'slider48 == 0 && gk_play && slider42 && (is_pre_drop || slider42 == 2) ? (')
    t = sub1(t, 'slider43 && ((is_pre_drop &&', 'slider48 == 0 && gk_play && slider43 && ((is_pre_drop &&')
    t = sub1(t, 'slider44 && ((is_pre_drop &&', 'slider48 == 0 && gk_play && slider44 && ((is_pre_drop &&')
    t = sub1(t, 'slider45 && (is_breakdown || slider45 == 2) ? (', 'slider48 == 0 && gk_play && slider45 && (is_breakdown || slider45 == 2) ? (')
    t = sub1(t, 'spl0 = out_l; spl1 = out_r;\n\n// Telemetry Buffer Fill',
             '// E. Ear-Candy Director (region + energy aware producer tricks)\n'
             'slider48 == 1 ? (\n'
             '  dk_process();\n'
             '  scrape_active = (dk_env[5] > 0.2 || dk_env[1] > 0.2);\n'
             '  stutter_active = (dk_env[6] > 0.2);\n'
             '  radio_active = (dk_env[7] > 0.2 || dk_env[15] > 0.2);\n'
             '  tape_active = (dk_env[11] > 0.2 || dk_env[10] > 0.2);\n'
             ');\n\n'
             'spl0 = out_l; spl1 = out_r;\n\n// Telemetry Buffer Fill')
    # gui: tabs
    t = sub1(t, 'tab_w = floor((crt_w - 24) / 6);', 'tab_w = floor((crt_w - 24) / 7);')
    t = sub1(t, 'ti = 0;\nloop(6,\n  tx = crt_x + 8 + ti * tab_w;', 'ti = 0;\nloop(7,\n  tx = crt_x + 8 + ti * tab_w;')
    t = sub1(t, '"Analog Glue" : "Producer Matrix")', '"Analog Glue" : (ti==5 ? "Producer Matrix" : "Ear-Candy"))')
    # gui: overview strip labels in Director mode
    def lab(n, old_pref, a, b):
        nonlocal t
        i = t.index('b%d_txt = ' % n)
        j = t.index(';\n', i)
        expr = t[i + len('b%d_txt = ' % n): j]
        t = t[:i] + 'b%d_txt = slider48 == 1 ? (b%d_trig ? "%s" : "%s") : (%s)' % (n, n, a, b, expr) + t[j:]
    lab(1, '', '! SWELL !', 'SWELL [DIR]')
    lab(2, '', '! CHOP !', 'CHOP [DIR]')
    lab(3, '', '! FILTER !', 'FILTER [DIR]')
    lab(4, '', '! DIVE !', 'DIVE [DIR]')
    t = sub1(t, 'mouse_clicked ? (\n    (mouse_y >= ec_btn_y && mouse_y <= ec_btn_y + ec_btn_h) ? (',
             'mouse_clicked && slider48 == 0 ? (\n    (mouse_y >= ec_btn_y && mouse_y <= ec_btn_y + ec_btn_h) ? (')
    t = sub1(t, '  // 3. Bottom Row: 5 Luxury Studio Hardware Channel Strips',
             '  (mouse_clicked && slider48 == 1 && mouse_y >= ec_btn_y && mouse_y <= ec_btn_y + ec_btn_h && mouse_x >= b1_x && mouse_x <= b4_x + ec_btn_w) ? (\n'
             '    slider1 = 6; slider_automate();\n  );\n\n'
             '  // 3. Bottom Row: 5 Luxury Studio Hardware Channel Strips')
    # gui: new tab + function
    t = sub1(t, '// Scanlines Overlay (Subtle Luxury Studio Glow)',
             gui + '\nslider1 == 6 ? (\n  dk_gui(disp_x + 10, disp_y + 12, disp_w - 20, disp_h - 24, 0.85, 0.68, 0.20);\n);\n\n'
             '// Scanlines Overlay (Subtle Luxury Studio Glow)')
    wr(P, t, crlf)
    print('guitar ok')


if __name__ == '__main__':
    import sys as _s
    which = _s.argv[1:] or ['synth']
    if 'vocal' in which: patch_vocal()
    if 'guitar' in which: patch_guitar()
    if 'synth' in which:
        from gen_candy_synth import patch_synth
        patch_synth()
