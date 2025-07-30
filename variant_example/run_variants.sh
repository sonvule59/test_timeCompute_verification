#!/bin/bash

OUTDIR=build_saxpy_variants
echo "Running baseline (base)..."
BASE_OUTPUT=$($OUTDIR/base)
echo "Base output: $BASE_OUTPUT"

declare -A scores

for variant in "variant1" "variant2" "variant3"; do
    echo "Testing $variant..."
    START=$(date +%s%N)
    OUTPUT=$($OUTDIR/$variant)
    END=$(date +%s%N)
    RUNTIME_NS=$((END - START))
    RUNTIME_MS=$((RUNTIME_NS / 1000000))

    echo "Output: $OUTPUT"
    echo "Runtime: ${RUNTIME_MS}ms"

    if [ "$OUTPUT" == "$BASE_OUTPUT" ]; then
        SCORE=$((100 + 1000 / (RUNTIME_MS + 1)))
        scores[$variant]=$SCORE
        echo "Score: $SCORE"
    else
        scores[$variant]=0
        echo "Output mismatch. Score: 0"
    fi
    echo ""
done

echo "----- Summary -----"
for v in "${!scores[@]}"; do
    echo "$v: Score = ${scores[$v]}"
done
