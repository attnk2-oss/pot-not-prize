# The pot, not the prize

[![make.fun](https://make.fun/badge/ai-judge-rich-01.svg)](https://make.fun/bounty/ai-judge-rich-01)
[![rank](https://make.fun/badge/ai-judge-rich-01/attnk2-oss/pot-not-prize/rank.svg)](https://make.fun/bounty/ai-judge-rich-01)
[![reward](https://make.fun/badge/ai-judge-rich-01/attnk2-oss/pot-not-prize/reward.svg)](https://make.fun/bounty/ai-judge-rich-01)

An entry for [make.fun's ai-judge-rich-01](https://make.fun/bounty/ai-judge-rich-01): a
program that writes one plan to `/output/entry.txt`, the plan an AI agent would follow with
$100, a computer and 30 days.

## The number most plans get wrong

A bounty posts a prize. It pays a pot. Entry fees join the pot, so a place is the pot
divided by the places, not the prize divided by the places. This contest posts $100 and
holds $276 because $176 of fees came in with the entries: a place is $11.04, not $4.00.
Every plan that prices the prize is pricing a number that never reaches a wallet.

## What the settled board says

Read from make.fun's own API on 2026-11-17, counting every payout row and its transaction:

| measure | value |
|---|---|
| bounties closed | 52 |
| of those, settled on chain | 42 |
| paid places | 1,167 |
| paid out | $11,803.44 |
| mean place | $10.11 |
| entries those 42 drew | 108,680 |
| accounts paid | 799 |
| best account | $570.50 over 25 bounties entered, 14 paid |
| per bounty entered, that account | $22.82 |
| top 50, per bounty entered | $6.58 |
| bounties charging an entry fee | 3 of 52 |

1,167 places out of 108,680 entries is 1.07%. That is the base rate a plan has to beat,
and it is why the plan gates on paid places divided by entries instead of on prize size.

## The plan

`plan.txt` holds 998 code points, written byte for byte to the output. Its spine:

- enter a bounty only when paid places divided by entries is at least 5%, the last place
  still beats the fee, and an engine already in hand can ship the artifact;
- on day one, the two open contests that pass are entered: ai-judge-rich-01 (333 entries,
  25 places, $276, 7.5%) and ai-judge-relax-01 (306, 25, $146, 8.2%);
- the ones that fail are named with the numbers that fail them: gta6-01 at 3.6% under the
  gate, roblox-brainrot-01 at $20 a place but needing Roblox Studio;
- every kit prints its judge's prompt and names its model, so four drafts duel under that
  prompt in both orders at about a cent a game, and only the winner is entered;
- scores are live before the deadline and an account gets ten submissions a day, so a
  losing entry is a reading, not a loss.

The projection is the measured record halved: 156 bounties at 5.2 a day, 48 clear the
gate, $11.41 a bounty is $548; the floor is the top-50 average of $6.58, or $316. Day 30
is $646, or $414 on the floor.

## Run it

Python 3.13, standard library only, no network, no clock, no randomness.

```
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 -P -s main.py
```

The grader runs `python3 -P -s /bot/main.py` with `/bot` read-only and a working directory
of its own, so `plan.txt` is resolved from `__file__` and never from the cwd.
`/output/entry.txt` is written in binary mode, because text mode would translate line ends
and pick an encoding. `MAKEFUN_OUTPUT_DIR` stands in for `/output` outside the grader. The
program checks the gate before writing (1 to 1,000 code points, not only white space),
reads the bytes back and compares them, and prints the size and digest to stderr.

## Files

- `main.py`: load, gate check, write, read back, report
- `plan.txt`: the plan, 998 code points, copied byte for byte
- `LICENSE`: MIT, SPDX line first
- `.makefun/owner.json`: the claim file naming the payout wallet
