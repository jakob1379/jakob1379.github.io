// Import the rendercv function and all the refactored components
#import "@preview/rendercv:0.1.0": *

// Apply the rendercv template with custom configuration
#show: rendercv.with(
  name: "Jakob Stender Guldberg",
  footer: context { [#emph[Jakob Stender Guldberg -- #str(here().page())\/#str(counter(page).final().first())]] },
  top-note: [ #emph[Last updated in Jan 2026] ],
  locale-catalog-language: "en",
  page-size: "us-letter",
  page-top-margin: 0.7in,
  page-bottom-margin: 0.7in,
  page-left-margin: 0.7in,
  page-right-margin: 0.7in,
  page-show-footer: true,
  page-show-top-note: true,
  colors-body: rgb(0, 0, 0),
  colors-name: rgb(0, 79, 144),
  colors-headline: rgb(0, 79, 144),
  colors-connections: rgb(0, 79, 144),
  colors-section-titles: rgb(0, 79, 144),
  colors-links: rgb(0, 79, 144),
  colors-footer: rgb(128, 128, 128),
  colors-top-note: rgb(128, 128, 128),
  typography-line-spacing: 0.6em,
  typography-alignment: "justified",
  typography-date-and-location-column-alignment: right,
  typography-font-family-body: "Fontin",
  typography-font-family-name: "Fontin",
  typography-font-family-headline: "Fontin",
  typography-font-family-connections: "Fontin",
  typography-font-family-section-titles: "Fontin",
  typography-font-size-body: 10pt,
  typography-font-size-name: 25pt,
  typography-font-size-headline: 10pt,
  typography-font-size-connections: 10pt,
  typography-font-size-section-titles: 1.4em,
  typography-small-caps-name: false,
  typography-small-caps-headline: false,
  typography-small-caps-connections: false,
  typography-small-caps-section-titles: false,
  typography-bold-name: false,
  typography-bold-headline: false,
  typography-bold-connections: false,
  typography-bold-section-titles: false,
  links-underline: true,
  links-show-external-link-icon: false,
  header-alignment: left,
  header-photo-width: 4.15cm,
  header-space-below-name: 0.7cm,
  header-space-below-headline: 0.7cm,
  header-space-below-connections: 0.7cm,
  header-connections-hyperlink: true,
  header-connections-show-icons: true,
  header-connections-display-urls-instead-of-usernames: false,
  header-connections-separator: "",
  header-connections-space-between-connections: 0.5cm,
  section-titles-type: "moderncv",
  section-titles-line-thickness: 0.15cm,
  section-titles-space-above: 0.55cm,
  section-titles-space-below: 0.3cm,
  sections-allow-page-break: true,
  sections-space-between-text-based-entries: 0.3em,
  sections-space-between-regular-entries: 1.2em,
  entries-date-and-location-width: 4.15cm,
  entries-side-space: 0cm,
  entries-space-between-columns: 0.3cm,
  entries-allow-page-break: false,
  entries-short-second-row: false,
  entries-summary-space-left: 0cm,
  entries-summary-space-above: 0.1cm,
  entries-highlights-bullet:  "•" ,
  entries-highlights-nested-bullet:  "•" ,
  entries-highlights-space-left: 0cm,
  entries-highlights-space-above: 0.15cm,
  entries-highlights-space-between-items: 0.1cm,
  entries-highlights-space-between-bullet-and-text: 0.3em,
  date: datetime(
    year: 2026,
    month: 1,
    day: 14,
  ),
)


= Jakob Stender Guldberg

#connections(
  [#link("mailto:jakob1379@gmail.com", icon: false, if-underline: false, if-color: false)[#connection-with-icon("envelope")[jakob1379\@gmail.com]]],
  [#link("https://jgalabs.dk/", icon: false, if-underline: false, if-color: false)[#connection-with-icon("link")[jgalabs.dk]]],
  [#link("https://linkedin.com/in/jakobguldberg", icon: false, if-underline: false, if-color: false)[#connection-with-icon("linkedin")[jakobguldberg]]],
  [#link("https://github.com/jakob1379", icon: false, if-underline: false, if-color: false)[#connection-with-icon("github")[jakob1379]]],
)


== Profile

Software & Data Platform Engineer specializing in \"industrializing\" scientific code. I bridge the gap between complex physical domains and reliable software by transforming experimental PoCs into robust production systems. I strive to develop \"simple solutions to complex problems\" through expertise in Developer Experience (DevEx), Modernization, and Operational Compliance (NIS2\/ISO).

== Experience

#regular-entry(
  [
    #strong[Software Consultant], Stealth Mode Startup (Compliance\/RegTech) -- Copenhagen

  ],
  [
    Nov 2025 – present

  ],
  main-column-second-row: [
    #summary[Engineered a secure data platform for regulated markets, achieving readiness for NIS2 and ISO 27001 audits by architecting a strictly typed FastAPI\/React system with granular Role-Based Access Control (RBAC).]

  ],
)

#regular-entry(
  [
    #strong[Special Consultant], DIKU (University of Copenhagen) & Darerl -- Copenhagen

  ],
  [
    Nov 2024 – Nov 2025

  ],
  main-column-second-row: [
    #summary[Increased research tool adoption by modernizing the \"RootPainter\" ML installer using uv and PEP standards, significantly lowering entry barriers for non-technical users. Accelerated Digital Twin workflows by refactoring experimental mesh-generation code into production-ready Prefect pipelines for reliable execution.]

  ],
)

#regular-entry(
  [
    #strong[Data Platform Engineer], RES (formerly Anemo Analytics) -- Copenhagen

  ],
  [
    Apr 2024 – Sept 2024

  ],
  main-column-second-row: [
    #summary[Validated real-time Edge Analytics feasibility to replace physical hard-drive shipping, achieving on-device Asset Health monitoring of wind turbines by architecting a high-performance Redpanda (Kafka) and DuckDB time-series pipeline on constrained hardware.]

  ],
)

#regular-entry(
  [
    #strong[IT Developer], Evaxion Biotech A\/S -- Copenhagen

  ],
  [
    Apr 2022 – Apr 2024

  ],
  main-column-second-row: [
    #summary[Delivered critical tooling for a 70-person biotech organization, focusing on automation and data velocity.]

    - Accelerated literature review (20,000 articles in 3 hours vs 800\/week for a five-person team) by engineering an automated LLM pipeline using LlamaIndex and Snakemake.

    - Eliminated manual data entry bottlenecks, reducing process time from weeks to minutes, by replacing fragile Excel workflows with a validated Streamlit application.

    - Optimized compute resources by setting up a 9-node on-prem HPC cluster (Ansible\/Slurm) and implementing NIS2-compliant security controls (Least Privilege\/Azure AD).

    - Reduced IT request cycle time from weeks to days by implementing GitLab Service Desk and converting inbound emails into assignable issues with standardized triage.

  ],
)

#regular-entry(
  [
    #strong[Student Developer], Evaxion Biotech A\/S -- Copenhagen

  ],
  [
    Jan 2021 – Dec 2022

  ],
  main-column-second-row: [
    #summary[Streamlined internal operations by developing robust RESTful integrations and database management tools using Django, FastAPI, and PostgreSQL.]

  ],
)

#regular-entry(
  [
    #strong[Teaching Assistant — Applied Programming], University of Copenhagen

  ],
  [
    June 2020 – June 2021

  ],
  main-column-second-row: [
    #summary[Mentored students in the Master's course in performance-critical C++ programming, focusing on memory management and optimization for data-intensive applications.]

  ],
)

#regular-entry(
  [
    #strong[Student Developer], DIKU (University of Copenhagen) -- Copenhagen

  ],
  [
    Jan 2020 – Dec 2020

  ],
  main-column-second-row: [
    #summary[Reduced Teaching Assistant workload by 50\% by engineering \"Canvas Code Correction,\" an automated grading platform integrating with the Canvas LMS API (Python\/Bash).]

  ],
)

#regular-entry(
  [
    #strong[Software Developer], Obital (Acquired by GN) -- Copenhagen

  ],
  [
    Jan 2018 – Dec 2020

  ],
  main-column-second-row: [
    #summary[Enabled hands-free smart home control for users with motor disabilities by developing a deep-learning eye-tracking solution running on low-powered mobile devices.]

  ],
)

== Education

#education-entry(
  [
    #strong[University of Copenhagen], M.Sc. in Bioinformatics (Thesis Submitted) in Machine Learning & Medical Image Analysis

  ],
  [
    Sept 2018 – June 2022

  ],
  main-column-second-row: [
    #summary[Thesis (Grade 12\/A): Developed an end-to-end pipeline to model tumor regression from longitudinal CT scans, enabling survival analysis (Kaplan-Meier) based on estimated volume changes over time. Implemented the high-performance workflow on a Slurm-managed HPC cluster. Transferred to industry to specialize in Data and Software Engineering.]

  ],
)

#education-entry(
  [
    #strong[University of Copenhagen], B.Sc. in Science and IT in Scientific Computing (Physics Specialization)

  ],
  [
    Sept 2014 – June 2018

  ],
  main-column-second-row: [
    #summary[Interdisciplinary foundation in Mathematical Modeling, Computer Science, and Physics.]

  ],
)

== Extra Curricular Activities

#regular-entry(
  [
    #strong[Canvas Code Correction v2]

  ],
  [
    Nov 2025 – present

  ],
  main-column-second-row: [
    #summary[Re-architecting grading platform for cloud scalability using Prefect and Pydantic to implement modern observability and security practices.]

  ],
)

#regular-entry(
  [
    #strong[NixOS & Flakes Guide]

  ],
  [
    2024

  ],
  main-column-second-row: [
    #summary[Mastered reproducible and immutable system configuration using NixOS and Nix Flakes. Full declarative configuration and implementation patterns are available in my \# link(\"https:\/\/github.com\/jakob1379\/nix-config\")\[nix-config\] repository.]

  ],
)

#regular-entry(
  [
    #strong[Continuous Learning (Talk Python)]

  ],
  [
    2023

  ],
  main-column-second-row: [
    #summary[Advanced coursework in FastAPI, Ansible, and Pytest to maintain cutting-edge Python proficiency.]

  ],
)

#regular-entry(
  [
    #strong[Open-source contributions]

  ],
  [
    2020–Present

  ],
  main-column-second-row: [
    #summary[Contribute via PRs to public repositories by reading issues and identifying possible pain-points I can help with through a review-first workflows by giving and receiving actionable feedback, and using AI-assisted development in PR scrutiny (tests, edge cases, refactor opportunities).]

  ],
)

== Technologies

#strong[Languages & Core:] Python (11y): FastAPI, Django, Pydantic, Typer, AnyIO. Data: Polars, DuckDB, SQLAlchemy, NumPy. Other: Bash, SQL, C++

#strong[Infrastructure:] DevOps: Docker, Ansible, Nix, Terraform. CI\/CD: GitHub Actions, GitLab CI. Observability: Prometheus, Grafana, Loki.

#strong[Data & Domain:] IoT\/Edge: Redpanda (Kafka), MQTT, Edge Analytics. Orchestration: Airflow, Prefect, Slurm (HPC). Compliance: NIS2, GDPR, ISO 27001.

== Languages

#strong[Danish:] Native

#strong[English:] Fluent
