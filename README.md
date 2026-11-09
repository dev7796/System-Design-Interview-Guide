# System Design Interview Guide

36 system design interview questions, each answered the same way, from requirements to a final architecture. Built as one PDF (about 540 pages) and one web page with moving diagrams.

- `System_Design_Interview_Guide.pdf`: the book.
- `System_Design_Interview_Guide_web.html`: the same book in a browser. Arrows flow, icons pulse, a Pause button at the top. Needs internet for the icon packs.

## The questions

Easy: Bitly, Dropbox, Yelp, Local Delivery Service.
Medium: Ticketmaster, Instagram, FB News Feed, Tinder, LeetCode, WhatsApp, Strava, Distributed Cache, Rate Limiter, Online Auction, YouTube, Job Scheduler, FB Live Comments, News Aggregator, Price Tracking, Notification System, Food Review App, Game Leaderboard.
Hard: YouTube Top K, Uber, Robinhood, Google Docs, Web Crawler, Ad Click Aggregator, FB Post Search, Payment System, Metrics Monitoring, Online Chess, ChatGPT, Flash Sale, Donations Website, GitHub Actions.

## Every chapter has

1. Functional requirements
2. Non-functional requirements
3. Back-of-the-envelope estimates
4. Core entities
5. API design
6. High-level design, as "how will users do X?" questions, with an icon diagram and a sequence diagram
7. Deep dives: fast, correct, scalable
8. Final architecture: icon diagram with tiers, component table, AWS deployment map
9. Common mistakes and interviewer follow-ups
10. One-page cheat sheet

Plain words, real numbers, and code where code is clearer than prose.

## Build it yourself

Needs `pandoc`, `playwright-cli` (Chromium), and Python 3.

```bash
python3 build_pdf.py
```

Reads `questions/*.md`, writes `book.md` and `book.html`, draws the Mermaid diagrams in Chromium, prints the PDF, and writes the web edition. Takes about two minutes.

Edit a chapter in `questions/`, run the build again.

## Layout

```
questions/        36 markdown chapters, one per question
build_pdf.py      the build
book.css          print and web styles
BRIEF.md          the shape every chapter follows
DIAGRAM_BRIEF.md  Mermaid diagram rules
ICONS.md          icon vocabulary for the architecture diagrams
CLOUDMAP.md       rules for the AWS deployment maps
```
