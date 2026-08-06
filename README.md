# A 2nd-teir Football Scouting Project

## Overview

I had the aim of building a scouting tool that could identify up and coming talentwithin major 2nd-teir leagues across the world, and decided on:
  - **Championship** — England (2nd tier) — 2025-26 season
  - **2. Bundesliga** — Germany (2nd tier) — 2025-26 season
  - **Ligue 2** — France (2nd tier) — 2025-26 season
  - **Serie B** — Italy (2nd tier) — 2025-26 season
  - **Série B** — Brazil (2nd tier) — 2026 season

## Getting Data

The first step was finding data. I used FBref.com, Whoscored.com, and fotmob.com as the 3 major sources of data across these leagues, since their data readiness topped others. 
The data was formatted using Python and Pandas, with custom parsers built for each site's specific export format — FBref's tab-separated tables, WhoScored's browser-automation exports, and FotMob's individually-scraped stat leaderboards. 
Each dataset covered player and team-level statistics including standard performance metrics (goals, assists, minutes), defensive actions (tackles, interceptions), shooting data (shots, shot accuracy), and sometimes passing and creativity metrics (key passes, chances created). 
In total, the combined dataset spans 3,145 outfield players, 212 goalkeepers, and 100 teams across all five leagues.

This data is labelled all_players.csv.


## First Analysis

In this project, you will also find first time analysis for data using just FBref.com, these come in the form of:
  - **forward_analysis.ipynb**
  - **defender_analysis.ipynb**
  - **goalkeeper_analysis.ipynb**

These 3 use the ready-available data on FBref.com to analyse patterns between players and teams across the five leagues — things like goal-scoring efficiency, team reliance, tackling and interception rates, and shot quality. 
Each notebook focuses on one position group specifically, using per-90-minute normalization to fairly compare players across leagues of different lengths, alongside a custom "team-share" metric showing how much of a team's total output (goals, assists, tackles) comes from a single player.
The analysis moves from simple ranked leaderboards through to more advanced visualizations — violin plots comparing distributions across leagues, pairplots showing relationships between multiple stats at once, and a custom correlation matrix — building toward the player rating system covered in the next stage of the project.


** But there was one main issue when trying to do midfielders **

One of the biggest attributes of the midfielder position is their passing- and this data wasnt readily available in the same way as before. 
It required webscraping using software Octoparse, and retreiving one statistic at a time using Fotmob- not the fastest way I was used to. But it meeant that I was able to get the correct passing data such as Big chances, Key passes, Interceptions and various more. 


## Player Grouping

Once the relevant data was collected, the next step was to understand the different positions within the groups. 

FBref groups every player using a simple position tag — `FW`, `MF`, `DF`, `GK`, or a combination like `FW,MF` for players who play across two roles. 
While useful as a starting point, these tags are often too broad to fairly compare players: a plain `FW` tag, for example, doesn't distinguish a penalty-box poacher from a wide, creative forward, even though the two do fundamentally different jobs on the pitch.

This was when I came up with these groups:

<img width="753" height="535" alt="Screenshot 2026-08-07 at 00 41 11" src="https://github.com/user-attachments/assets/bc704a63-dcd3-4442-95f9-f45b99a2c933" />

To get real analysis on these positions, I had to first understand understand how to seperate the players into their groups.
Rather than relying solely on FBref's broad tags, K-means clustering was used to discover genuine sub-roles within each position group. Given real playing statistics (goals, assists, crossing volume, tackles, creative output), the algorithm groups players based purely on how similar their actual numbers are, without being told in advance what the groups should represent.



## Player Rating System 

While researching how to actually turn all these stats into one meaningful number, I came across a research paper — *A multi-criteria system for performance assessment and support decision-making based on the example of Premier League top football strikers* (Kolbowicz, Nowak & Więckowski, 2024) — which used a method called **TOPSIS** to rate Premier League forwards. This felt like exactly what I needed: a proper, published way to combine multiple stats into a single rating, rather than just making up my own weightings.

TOPSIS stands for **Technique for Order Preference by Similarity to Ideal Solution**. The idea is genuinely simple once you get past the name: build an imaginary "perfect player" using the best real value of every stat across the whole dataset, and an imaginary "worst-case player" using the worst value of every stat. Then, for every real player, measure how close they are to each of these two — the closer to the ideal and further from the worst-case, the higher the rating.

Here's how it actually works, step by step:

1. Normalize every stat to a 0–1 scale. For stats where higher is better (like goals per 90), the best real value becomes 1 and the worst becomes 0. For stats where lower is better (like red cards), it's flipped — the lowest value becomes 1.

2. Weight every stat equally. I followed the same approach as the paper this is based on — rather than deciding myself that goals matter more than assists, every stat in a player's criteria list counts the same amount.

3. Build the ideal and worst-case players. Take the best normalized value of every stat and combine them into one "player" — this doesn't exist in real life, it's just a reference point built from real data.

4. Measure the distance. For every real player, calculate how far they are from the ideal player and from the worst-case player, using Euclidean distance — the same maths you'd use to measure distance on a map, just done across many stats at once instead of two.

5. Calculate the final score. A player's rating is their distance from the worst-case player, divided by the total of both distances combined. This gets multiplied by 100 to give a score out of 100.

One thing I found genuinely interesting while working through this: TOPSIS doesn't just reward high totals — it rewards being *well-rounded*. Two players with the exact same combined output across their stats can end up with different ratings depending on how balanced they are across each individual stat. A player who's great at one thing and poor at another will actually score lower than someone who's decent across the board with the same overall total.



## Mathematical Formulation of the Rating System

**Step 1 — Decision Matrix**

Let $x_{ij}$ represent the raw value of criterion $i$ for player $j$, where $i = 1, \dots, n$ (the number of criteria) and $j = 1, \dots, m$ (the number of players).

**Step 2 — Normalization**

Each criterion is normalized to a range between 0 and 1. For **profit** criteria (higher is better):

$$v_{ij} = \frac{x_{ij} - \min(x_i)}{\max(x_i) - \min(x_i)}$$

For **cost** criteria (lower is better, e.g. red cards):

$$v_{ij} = \frac{\max(x_i) - x_{ij}}{\max(x_i) - \min(x_i)}$$

**Step 3 — Weighting**

Since criteria are weighted equally, each weight is:

$$w_i = \frac{1}{n}$$

giving the weighted normalized value:

$$u_{ij} = w_i \cdot v_{ij}$$

**Step 4 — Ideal and Worst-Case Solutions**

$$u_i^* = \max_j(u_{ij}), \qquad u_i^- = \min_j(u_{ij})$$

**Step 5 — Euclidean Distance to Ideal and Worst-Case**

$$D_j^* = \sqrt{\sum_{i=1}^{n} \left(u_{ij} - u_i^*\right)^2}$$

$$D_j^- = \sqrt{\sum_{i=1}^{n} \left(u_{ij} - u_i^-\right)^2}$$

**Step 6 — Relative Closeness (Final Rating)**

$$C_j^* = \frac{D_j^-}{D_j^* + D_j^-}$$

The final rating is $C_j^* \times 100$, bounded between 0 and 100.









