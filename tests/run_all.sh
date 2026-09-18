#!/bin/sh
# Plays every bot route through the real game. Usage: sh tests/run_all.sh [godot-binary]
G=${1:-godot}
fail=0
run() { # name map spawn flags
	printf '%-12s ' "$1"
	if SCP_MAP=$2 SCP_SPAWN=$3 SCP_FLAGS=$4 SCP_SAVE=user://test_$1.json timeout 1500 "$G" --path . \
		--script res://tools/playtest.gd -- "res://tests/routes/$1.json" 2>&1 | grep -q 'ROUTE COMPLETE'
	then echo ok; else echo FAILED; fail=1; fi
}
run sector_a    A01 start    ""
run sector_b    B01 ""       ""
run b02_contain B02 from_B11 ""
run sector_cd   C01 from_B15 "item:card_2,item:cheese,item:pistol,item:ammo:12,item:medkit:2"
run sector_efg  E01 from_C01 "item:card_4,item:bag096,item:pistol,item:ammo:24,item:medkit:3,ortega_went_hcz"
exit $fail
