# 🏏 IPL Analytics API 🚀

**IPL Analytics API** is a dynamic platform built using Flask that provides insightful statistics and data analysis of the Indian Premier League. From head-to-head comparisons of IPL teams to individual player statistics, our API uncovers the excitement and depth of one of the world's most popular cricket leagues.

## 🌟 Features

- **Team-Centric Statistics:**<br>
📊 Get a comprehensive overview of any team's performance during a season.<br>
🤼‍♂️ Dive into head-to-head stats between two IPL giants.<br>
📅 Traverse through a team's journey across different IPL seasons.

- **Batsman Breakdown:**<br>
🏃‍♂️ Track the performance of your favorite batsman across IPL seasons.<br>
🌟 Discover seasonal highlights, from total runs to strike rates.<br>
🏏 Check out season-specific performance metrics.

- **Bowler Bonanza:**<br>
🎯 Unravel the mastery of a bowler throughout the IPL's illustrious history.<br>
⚡ Fetch detailed metrics, including economy, total wickets, and best figures.<br>
🔍 Analyze a bowler's performance during a particular season.

## 🔍 Detailed Overview

- **Team Analysis:**
  * Seasonal overview, including matches played, super overs, and title conquests.
  * Comprehensive head-to-head comparisons.
  * Highlights like top batsmen and bowlers for the season.

- **Batsman Deep Dive:**
  * Overview across all IPL seasons including total runs, average, and strike rate.
  * Seasonal breakdown: total runs, fours, sixes, and much more.

- **Bowler Breakdown:**
  * Career IPL statistics, including total wickets, economy, and best figures.
  * Seasonal insights: wickets, economy, and notable achievements.

## 💾 Usage

1. Team Specific API
   - `**teamAllSeasonsAPI(team)**`: Fetch details for a team for over all seasons.
   - `**teamSeasonAPI(team, season)**`: Fetch details for a team for a given season.
Team vs. Team API

teamVsTeamAllSeasonsAPI(team1, team2): Compare two teams over all seasons.
teamVsTeamSeasonAPI(team1, team2, season): Compare two teams for a specific season.
Batsman Specific API

batsmanAllSeasonsAPI(batsman): Fetch overall statistics of a batsman over all seasons.
batsmanSeasonAPI(batsman, season): Fetch statistics of a batsman for a specific season.
Bowler Specific API

bowlerAllSeasonsAPI(bowler): Fetch overall statistics of a bowler over all seasons.
bowlerSeasonAPI(bowler, season): Fetch statistics of a bowler for a specific season.
 
