#!/usr/bin/env python3
"""Analyze round-trip diff for WP5.1."""
import re

original = open('scripts/confluence/_rt_tmp/original.html').read()
roundtrip = open('scripts/confluence/_rt_tmp/roundtrip.html').read()

# Check both have all 50 SHR rows
orig_shrs = re.findall(r'<p>SHR-(\d+)</p>', original)
rt_shrs = re.findall(r'<p>SHR-(\d+)</p>', roundtrip)
print(f'Original  SHR rows: {len(orig_shrs)} ({orig_shrs[0]}..{orig_shrs[-1]})')
print(f'RoundTrip SHR rows: {len(rt_shrs)} ({rt_shrs[0]}..{rt_shrs[-1]})')

# Normalize: strip macro-ids, showSummary param, content-wrapper divs, whitespace
def normalize(html):
    html = re.sub(r' ac:macro-id="[^"]+"', '', html)
    html = re.sub(r'<ac:parameter ac:name="showSummary">[^<]+</ac:parameter>', '', html)
    html = re.sub(r'<div class="content-wrapper">(.*?)</div>', r'\1', html, flags=re.DOTALL)
    html = re.sub(r'\s+', ' ', html)
    return html.strip()

n_orig = normalize(original)
n_rt = normalize(roundtrip)

print(f'\nNormalized sizes: orig={len(n_orig)}, rt={len(n_rt)}')

if n_orig == n_rt:
    print('CONTENT IDENTICAL after normalization — only cosmetic diffs!')
else:
    # Find and show first real difference
    for i, (a, b) in enumerate(zip(n_orig, n_rt)):
        if a != b:
            print(f'First content diff at char {i}:')
            print(f'  Orig: ...{repr(n_orig[max(0,i-80):i+80])}...')
            print(f'  RT:   ...{repr(n_rt[max(0,i-80):i+80])}...')
            break
    else:
        print(f'Same chars but different lengths: orig={len(n_orig)}, rt={len(n_rt)}')
        longer = 'orig' if len(n_orig) > len(n_rt) else 'rt'
        print(f'{longer} has extra tail: {repr((n_orig if longer=="orig" else n_rt)[-100:])}')
