set -e
f() { git fetch -q --depth 1 origin "$1" && mkdir -p "$2" && git archive FETCH_HEAD "${3:-.}" | tar -x -C "$2"; }
D=$1
f fnfd2-chars /tmp/d2chars out
for k in $(seq -w 0 19); do f fnfd2-k$k /tmp/d2her out || true; done
for b in $(git ls-remote origin | grep -oE "fnfd2-img(b)?-[a-z0-9_]+$"); do f $b /tmp/d2img out || true; done
for b in $(git ls-remote origin | grep -oE "fnfd2-fix8-d[0-9]+_n[0-9]+$"); do f $b /tmp/d2img out || true; done
for b in $(git ls-remote origin | grep -oE "fnf-out-img-d${D}_s[123]$"); do f $b /tmp/skimg/$b || true; done
for k in soft1 soft2 soft3 hymn2 hymn3 qa2 qa3 qa4 qa5 qa6; do f fnf-out-mu-$k /tmp/mus || true; done
for b in $(git ls-remote origin | grep -oE "fnf-out-(read-g0[4-9]|read-g10|r3-[0-9]+|r4-[a-z0-9_]+)$"); do f $b /tmp/oldread || true; done
