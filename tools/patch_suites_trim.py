"""Insert the Matrix Trim module into the six Damei suites (idempotent, backs up originals first)."""
import os, re, shutil
D = r"C:\Dev\DameiAPI\reaper_scripts"
BK = os.path.join(D, "backups_pretrim")
os.makedirs(BK, exist_ok=True)
SUITES = {  # file -> lane index (must match WT rows in the Matrix)
    "Damei_DrumSuite.jsfx": 0, "Damei_GuitarSuite.jsfx": 1, "Damei_BassSuite.jsfx": 2,
    "Damei_VocalSuite.jsfx": 3, "Damei_SynthSuite.jsfx": 4, "Damei_DevastatorSuite.jsfx": 5,
}

INIT = r'''
// ===== MATRIX TRIM BEGIN (auto-correction lane published by Damei_AssessmentMatrix) =====
// Final-stage 7-band + side-shelf trim. Targets arrive on gmem[1300 + lane*16 ...]; ramped (~1 s), capped by the Matrix.
mtrim_lane = 1300 + __IDX__*16;
mtrim_mem  = 2096000;
mtrim_on = 0; mtrim_cnt = 0;
mtrim_cur = mtrim_mem + 200;   // 8 current gains (7 bands + side shelf)
i = 0; loop(8, mtrim_cur[i] = 0; i += 1; );
i = 0; loop(100, mtrim_mem[i] = 0; i += 1; );

function mtrim_bq(c, s, x) local(y) (
  y = c[0]*x + s[0];
  s[0] = c[1]*x - c[3]*y + s[1];
  s[1] = c[2]*x - c[4]*y;
  y;
);

// kind: 0 peaking, 1 low shelf, 2 high shelf
function mtrim_design(c, kind, fc, q, gdb) local(A, w0, cs, sn, al, sa, a0, b0, b1, b2, a1, a2) (
  A = pow(10, gdb/40); w0 = 2*$pi*fc/srate; cs = cos(w0); sn = sin(w0);
  kind == 0 ? (
    al = sn/(2*q);
    b0 = 1 + al*A; b1 = -2*cs; b2 = 1 - al*A; a0 = 1 + al/A; a1 = -2*cs; a2 = 1 - al/A;
  ) : (
    sa = 2*sqrt(A)*(sn*0.70710678);
    kind == 1 ? (
      b0 = A*((A+1) - (A-1)*cs + sa); b1 = 2*A*((A-1) - (A+1)*cs); b2 = A*((A+1) - (A-1)*cs - sa);
      a0 = (A+1) + (A-1)*cs + sa;     a1 = -2*((A-1) + (A+1)*cs);  a2 = (A+1) + (A-1)*cs - sa;
    ) : (
      b0 = A*((A+1) + (A-1)*cs + sa); b1 = -2*A*((A-1) + (A+1)*cs); b2 = A*((A+1) + (A-1)*cs - sa);
      a0 = (A+1) - (A-1)*cs + sa;     a1 = 2*((A-1) - (A+1)*cs);    a2 = (A+1) - (A-1)*cs - sa;
    );
  );
  c[0] = b0/a0; c[1] = b1/a0; c[2] = b2/a0; c[3] = a1/a0; c[4] = a2/a0;
);

function mtrim_block() local(ok, b, tg, any, g) (
  ok = (slider__SL__ == 1) && (gmem[mtrim_lane] == 1) && ((time_precise() - gmem[mtrim_lane + 15]) < 5);
  any = 0; b = 0;
  loop(8,
    tg = ok ? gmem[mtrim_lane + 1 + b] : 0;
    mtrim_cur[b] += (tg - mtrim_cur[b]) * 0.012;
    abs(mtrim_cur[b]) > 0.02 ? ( any = 1; );
    b += 1;
  );
  mtrim_on = any;
  any ? (
    mtrim_design(mtrim_mem + 0,  1, 70,    0.7, mtrim_cur[0]);
    mtrim_design(mtrim_mem + 5,  0, 130,   0.8, mtrim_cur[1]);
    mtrim_design(mtrim_mem + 10, 0, 450,   0.8, mtrim_cur[2]);
    mtrim_design(mtrim_mem + 15, 0, 1400,  0.8, mtrim_cur[3]);
    mtrim_design(mtrim_mem + 20, 0, 3800,  0.8, mtrim_cur[4]);
    mtrim_design(mtrim_mem + 25, 0, 7800,  0.8, mtrim_cur[5]);
    mtrim_design(mtrim_mem + 30, 2, 11000, 0.7, mtrim_cur[6]);
    mtrim_design(mtrim_mem + 35, 2, 3000,  0.7, mtrim_cur[7]);
  );
);

function mtrim_process() local(k, yl, yr, mm, ss) (
  mtrim_on ? (
    yl = spl0; yr = spl1; k = 0;
    loop(7,
      yl = mtrim_bq(mtrim_mem + k*5, mtrim_mem + 50 + k*2, yl);
      yr = mtrim_bq(mtrim_mem + k*5, mtrim_mem + 70 + k*2, yr);
      k += 1;
    );
    mm = (yl + yr)*0.5; ss = (yl - yr)*0.5;
    ss = mtrim_bq(mtrim_mem + 35, mtrim_mem + 90, ss);
    spl0 = mm + ss; spl1 = mm - ss;
  );
);
// ===== MATRIX TRIM END =====
'''

def patch(fn, idx):
    p = os.path.join(D, fn)
    raw = open(p, encoding="utf-8", newline="").read()
    if "MATRIX TRIM BEGIN" in raw:
        return f"{fn}: already patched"
    shutil.copyfile(p, os.path.join(BK, fn))
    crlf = "\r\n" in raw
    L = raw.replace("\r\n", "\n").split("\n")
    maxs = max(int(m.group(1)) for l in L for m in [re.match(r"slider(\d+):", l)] if m)
    sl = maxs + 1

    def find(prefix, start=0):
        for i in range(start, len(L)):
            if L[i].startswith(prefix):
                return i
        return -1

    def next_section(i):
        for j in range(i + 1, len(L)):
            if L[j].startswith("@"):
                return j
        return len(L)

    snippet = INIT.replace("__IDX__", str(idx)).replace("__SL__", str(sl)).split("\n")
    # work bottom-up so earlier indexes stay valid
    s_i = find("@sample")
    s_end = next_section(s_i)
    L[s_end:s_end] = ["  mtrim_process();", ""]
    b_i = find("@block")
    if b_i >= 0:
        b_end = next_section(b_i)
        L[b_end:b_end] = ["  mtrim_block();", ""]
    else:
        L[s_i:s_i] = ["@block", "mtrim_block();", ""]
    i_i = find("@init")
    i_end = next_section(i_i)
    L[i_end:i_end] = snippet
    o_i = find("options:gmem")
    L[o_i:o_i] = [f"slider{sl}:1<0,1,1{{Off,On}}>Matrix Trim (applies Assessment Matrix auto-correct lane)"]
    out = "\n".join(L)
    if crlf:
        out = out.replace("\n", "\r\n")
    open(p, "w", encoding="utf-8", newline="").write(out)
    return f"{fn}: patched (lane {idx}, slider{sl}, block={'existing' if b_i >= 0 else 'new'})"

for fn, idx in SUITES.items():
    print(patch(fn, idx))
