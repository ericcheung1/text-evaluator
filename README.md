## Word-Processor-Dot-Com - Text Processing Web App

Early Prototype Live On: https://www.word-processor-dot-com.site/

A lightweight frontend‑for‑backend (BFF) web application that serves as one client of the WPaaS NLP Inference API. The site currently supports real-time sentiment analysis of Reddit posts fetched via PRAW, using the sentiment endpoint of the [WPaaS](https://github.com/ericcheung1/WPaaS) API. And supports sentiment analysis on individual sentences. 

## Architecture & Deployment

- Deployed on a VPS using Nginx as a static file server and TLS termination layer
- Secured with HTTPS via Let’s Encrypt (Certbot) & Served through a custom domain
- Communicates directly with the WPaaS API over HTTP


## Current Limitations

- Early prototype UI with basic HTML layout with no styling
- Limited number of comments sentiment analyzed

## APIs & Services Used

- PRAW (Python Reddit API Wrapper) for fetching Reddit posts and comments
- [WPaaS](https://github.com/ericcheung1/WPaaS) NLP Inference API for real‑time sentiment analysis
