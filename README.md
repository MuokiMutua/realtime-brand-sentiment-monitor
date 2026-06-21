## Real-Time PR Command Center & Sentiment Monitor 
<img width="1891" height="786" alt="image" src="https://github.com/user-attachments/assets/3fdab385-f317-43f3-9446-4fc513fd3be5" />
<img width="1825" height="938" alt="image" src="https://github.com/user-attachments/assets/418c33bd-1eec-45fd-977f-5ecac1c5f7f4" />

An end-to-end streaming data pipeline and live dashboard built to monitor brand perception in real-time. This system simulates a social media firehose, applies Natural Language Processing (NLP) to incoming mentions, and triggers PR crisis alerts the moment sentiment drops.

## The Problem

In the modern financial landscape, a system outage, a blocked card, or a hidden fee can spark a social media wildfire in minutes. Traditional reporting is historical (e.g., weekly reports). By the time a Chief Communications Officer or CTO reads a PDF report about an app outage, the PR crisis has already done its damage.

## Background

To effectively manage brand reputation and system reliability, banks and fintechs need active social listening. They need to know immediately when the volume of negative chatter spikes so they can deploy engineering fixes or PR damage control in real-time.

## Objective

* To build a fully automated, real-time streaming system that:

* Simulates a live, continuous feed of unstructured social media mentions.

* Evaluates the emotional sentiment of each mention instantaneously using a specialized NLP model.

* Visualizes the live data stream on an auto-refreshing command center dashboard.

* Automatically calculates thresholds and triggers a "PR Crisis" alert if the global sentiment score plummets.

## How We Solve It (System Architecture)

This project consists of two concurrently running processes:

**data_streamer.py (The Live Firehose)**

* Simulates an ongoing stream of social media posts referencing target financial brands.

* Utilizes VADER (Valence Aware Dictionary and sEntiment Reasoner)—an NLP model specifically tuned to understand social media context, including capitalization, slang, and emojis.

* Calculates a continuous compound sentiment score (-1.0 to 1.0) and dynamically appends the data to a live CSV database.

## live_dashboard.py (The Command Center)

* A Streamlit application engineered with an auto-rerun loop (time.sleep + st.rerun).

* Reads the tail of the streaming database and continuously updates the UI.

* Uses Plotly to render a moving sentiment trajectory chart.

* Features a dynamic logic gate that changes the system status to "CRITICAL: PR CRISIS" if the rolling average sentiment drops into the red zone.

## Tech Stack

* Language: Python 3.x

* NLP Model: vaderSentiment

* Data Processing: pandas

* Visualization & UI: streamlit, plotly

* Architecture: Concurrent processes (Producer/Consumer model via live CSV polling)

## Dashboard Highlights

The "Heartbeat": The dashboard autonomously refreshes every 3 seconds to pull in the latest data from the streaming engine.

Live Sentiment Trajectory: A moving line chart tracking the 10-mention rolling average to smooth out the noise and show clear trending direction.

Competitor Overview: An actively updating horizontal bar chart comparing the aggregate sentiment scores of competing brands.

Live Mention Feed: A scrolling, color-coded feed showing the raw, unedited text of the latest incoming mentions.
