# CIP colour tokens (Jira-inspired blue and neutral)

This is our own Jira-inspired palette. It is not a claim of exact current Atlassian tokens.
Figma file `nW0n4I3aarR2CqvEt9d9ZY`. The file has no variable collections, so tokens are the
local paint and effect styles. They were edited in place (no duplicate collections), which
retints every component that references them.

## Semantic mapping (before to after)

| Role | Style(s) | Before | After |
| --- | --- | --- | --- |
| Primary / action | Brand/500, Brand/600 | #0D9488 / #0F766E | #0C66E4 |
| Primary hover | Brand/700 | #115E59 | #0055CC |
| Primary pressed | Brand/800 | #134E4A | #09326C |
| Selected / subtle blue | Brand/50, Blue/50 | #F0FDFA | #E9F2FF |
| Focus ring (border) | Brand/300 | #5EEAD4 | #388BFF |
| Focus halo | Brand/100, `Focus ring/4px primary-100` | #CCFBF1 | #CCE0FF |
| Focus ring (solid) | `Focus ring/4px primary-600` | #0F766E | #388BFF |
| Page background | Neutral/50 | #FAFAFA | #F7F8F9 |
| Surface | Base/White | #FFFFFF | #FFFFFF |
| Disabled background | Neutral/100 | #F5F5F5 | #F1F2F4 |
| Divider / card border | Neutral/200 | #E5E5E5 | #DCDFE4 |
| Control boundary | Neutral/300 | #D4D4D4 | #8590A2 |
| Disabled text, icons | Neutral/400 | #A3A3A3 | #8993A4 |
| Muted text | Neutral/500 | #737373 | #626F86 |
| Secondary text | Neutral/600, Neutral/700 | #525252 / #404040 | #44546F |
| Primary text | Neutral/800, Neutral/900 | #262626 / #171717 | #172B4D |
| Success | Green/700, Green/50 | #15803D, #F0FDF4 | #216E4E, #DCFFF1 |
| Warning | Yellow/700, Yellow/50 | #A16207, #FEFCE8 | #974F0C, #FFF7D6 |
| Error | Red/700, Red/50 | #B91C1C, #FEF2F2 | #AE2A19, #FFECEB |
| Information | Blue/700, Blue/50 | #1D4ED8, #EFF6FF | #0055CC, #E9F2FF |

Full ramps (Brand, Blue, Neutral, Green, Red, Yellow) and the Gradient/Brand and
Gradient/Neutral stops were retinted to match. Red/300 and Red/400 were darkened so the
destructive input border reaches 3:1. Disabled button and input variants and the error hint
text in the Input field component were re-pointed at Neutral/100, Neutral/400 and Red/700.

## Contrast (WCAG 2.2 AA)

Text needs 4.5:1. Control boundaries and focus indicators need 3:1.

| Pair | Ratio |
| --- | --- |
| #172B4D on white | 14.1 |
| #44546F on #F7F8F9 | 7.2 |
| #626F86 on white / #F7F8F9 / #F1F2F4 | 5.1 / 4.8 / 4.5 |
| White on #0C66E4 / #0055CC / #09326C | 5.2 / 6.6 / 12.5 |
| #0C66E4 link on white / #F7F8F9 | 5.2 / 4.9 |
| #0055CC on #E9F2FF | 5.9 |
| Success #216E4E on #DCFFF1 | 5.8 |
| Warning #974F0C on #FFF7D6 | 5.7 |
| Error #AE2A19 on #FFECEB | 5.9 |
| Boundary #8590A2 on white / #F7F8F9 | 3.2 / 3.0 |
| Focus #388BFF on white / #F7F8F9 | 3.3 / 3.1 |
| Error border #F15B50 or #E2483D on white | 3.3 or 4.0 |
| Divider #DCDFE4 on white | 1.3 (decorative only, never a control boundary) |
| Disabled text #8993A4 on #F1F2F4 | 2.8 (exempt as disabled) |

## Unresolved

- The kit has no Pressed variant for buttons. The pressed token (#09326C, Brand/800) exists but is not shown on a component.
- `A1 — Authentication` and the two `Welcome - Jobber` frames on the CIP page were added by someone else. They use hardcoded Jira-style hex (not styles) and Jobber teal (#15A4C1, #0E6171). They were not edited.
- Other kit ramps (Orange, Sky, Indigo, Purple, Pink, Rose, Slate) and kit pages were not retinted. Only kit hardcoded teal was searched on the CIP page; the kit pages bind to styles.
- Mixed or image fills and 0.10 to 0.14 alpha shadows were left as they were.
- Status is never colour alone in CIP screens (icon plus text). Information and Brand now share blue, so info states must keep their icon and label.
