# AutoResearch Eval — Review Rubric

Tracks the validity and calibration of the review rubric over time.

## Methodology

For each rubric dimension, track:
- **True positive rate:** Finding flagged → human agreed it was a real issue
- **False positive rate:** Finding flagged → human disagreed
- **Suppression error rate:** Finding suppressed → human later identified it as real

Update counters when a review cycle completes and human provides feedback.

## Dimension Calibration

| Dimension | TP | FP | Suppressed errors | Notes |
|-----------|----|----|-------------------|-------|
| Naming quality | 0 | 0 | 0 | |
| Domain language | 0 | 0 | 0 | |
| Function responsibility | 0 | 0 | 0 | |
| Architectural fit | 0 | 0 | 0 | |
| Unnecessary duplication | 0 | 0 | 0 | |
| Refactoring avoidance | 0 | 0 | 0 | |
| Cognitive load | 0 | 0 | 0 | |

## Threshold Adjustment

Current threshold: **80/100**

Adjust threshold based on false positive rate:
- FP rate > 30% on a dimension → raise threshold for that dimension
- Suppression error rate > 20% on a dimension → lower threshold

## Notes

_Record calibration decisions and rationale here._
