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


## Player Ratings

Once the relevant data was collected, the next step was to understand the different positions within the groups. 

FBref groups every player using a simple position tag — `FW`, `MF`, `DF`, `GK`, or a combination like `FW,MF` for players who play across two roles. 
While useful as a starting point, these tags are often too broad to fairly compare players: a plain `FW` tag, for example, doesn't distinguish a penalty-box poacher from a wide, creative forward, even though the two do fundamentally different jobs on the pitch.

This was when I came up with these groups:

<img width="753" height="535" alt="Screenshot 2026-08-07 at 00 41 11" src="https://github.com/user-attachments/assets/bc704a63-dcd3-4442-95f9-f45b99a2c933" />







