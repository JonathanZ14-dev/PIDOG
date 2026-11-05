"""A tiny supervised model: learn a blue-area threshold for OBSTACLE labels.
Synthetic demonstration intentionally exposes a color shortcut, not general vision.
"""
import argparse
import csv
import json
import math
from pathlib import Path


def load_rows(path):
    """Read CSV and reject malformed labels, empty splits or scene leakage."""
    with Path(path).open(newline='') as stream:
        rows = list(csv.DictReader(stream))
    scene_splits = {}
    for row in rows:
        row['blue_ratio'] = float(row['blue_ratio'])
        row['obstacle'] = int(row['obstacle'])
        if not math.isfinite(row['blue_ratio']) or not 0 <= row['blue_ratio'] <= 1 or row['obstacle'] not in (0,1) or row['split'] not in ('train','validation','test') or not row['scene_id']:
            raise ValueError('Invalid dataset row')
        if row['scene_id'] in scene_splits and scene_splits[row['scene_id']] != row['split']:
            raise ValueError('Scene leakage across splits')
        scene_splits[row['scene_id']] = row['split']
    if any(not any(r['split']==s for r in rows) for s in ('train','validation','test')):
        raise ValueError('Need nonempty train, validation and test splits')
    return rows


def evaluate(rows, threshold):
    """Return counts; positive means obstacle present, not a blue pixel."""
    counts = {'TP':0, 'TN':0, 'FP':0, 'FN':0}
    for r in rows:
        prediction = r['blue_ratio'] >= threshold
        key = ('TP' if r['obstacle'] else 'FP') if prediction else ('FN' if r['obstacle'] else 'TN')
        counts[key] += 1
    counts['n'] = len(rows)
    counts['accuracy'] = (counts['TP']+counts['TN'])/len(rows) if rows else None
    return counts


def fit_threshold(train):
    """Minimize train mistakes; tie-break by largest threshold. No test rows."""
    if not train or {r['obstacle'] for r in train} != {0,1}:
        raise ValueError('Training needs both classes')
    values = sorted({r['blue_ratio'] for r in train})
    candidates = [0.0]+[(a+b)/2 for a,b in zip(values, values[1:])]+[1.000001]
    def score(t):
        c = evaluate(train, t)
        return c['FP']+c['FN'], -t
    return min(candidates, key=score)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('csv')
    args = p.parse_args()
    rows = load_rows(args.csv)
    threshold = fit_threshold([r for r in rows if r['split']=='train'])
    print(json.dumps({'threshold':threshold, 'target':'obstacle presence; dataset labels',
                      'results':{s:evaluate([r for r in rows if r['split']==s],threshold) for s in ('train','validation','test')}},indent=2))


if __name__ == '__main__':
    main()
