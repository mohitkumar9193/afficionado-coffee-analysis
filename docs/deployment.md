# Deployment plan

## Decision for Step 1

Use one GitHub repository with two deployment targets:

1. Streamlit Community Cloud hosts the required interactive Python dashboard.
2. Vercel hosts a companion project page with links to the dashboard, research paper, executive summary, and repository.

Streamlit runs a Python server with persistent sessions. Community Cloud provides a documented deployment flow from a GitHub repository. We are selecting that supported route rather than designing a custom Streamlit hosting adapter for Vercel.

This satisfies the requested Vercel presence while retaining the specified Streamlit application. If the internship requires the analytics application itself to run on a Vercel URL, confirm that condition before dashboard development; a companion page alone would not meet that additional rule.

## Planned settings

| Target | Setting |
| --- | --- |
| GitHub repository | afficionado-coffee-analysis |
| Default branch | main |
| Streamlit app path | dashboard/app.py (to be created in Step 9) |
| Python dependencies | Root requirements.txt, added and pinned after validation |
| Vercel root directory | website |
| Vercel framework/build settings | Selected when the companion page is implemented |

No repository remote, cloud project, account connection, or live URL has been created during Step 1.

## Data availability

Local raw and processed transaction files are ignored by Git. Before deploying, decide whether an authorized dataset can be packaged with the app, loaded from approved storage, or supplied through an upload widget. Local ignored files will not automatically appear on the cloud host. Publish only approved report content and data.

## Publishing sequence for Step 12

1. Verify dashboard calculations and report consistency.
2. Prepare the approved data-loading method and pinned dependencies.
3. Push the completed project to GitHub.
4. Deploy dashboard/app.py on Streamlit Community Cloud and test the live app.
5. Insert verified dashboard, report, and repository links in the Vercel page.
6. Deploy website/ on Vercel and verify the submission links.

## Official references checked during setup

- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
- https://docs.streamlit.io/develop/concepts/architecture/architecture
