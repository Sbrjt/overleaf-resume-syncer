Overleaf is a popular LaTeX editor used for writing resumes. But the free-tier plan lacks Git and cloud drive integration. So every time you update your resume, you have to manually download the latest pdf for sharing - which quickly becomes tedious.

This GitHub action solves this by automatically fetching the latest pdf from overleaf and commits it to your GitHub repo, from where it can be easily hosted and shared.

> [!NOTE]
> Privacy: If you prefer not to store your resume in a public repo, use a private repo and Google Drive Sync to keep your shareable resume link up to date.

## Example Usage

```yaml
name: Sync Overleaf PDF

permissions:
  contents: write

on:
  schedule:
    - cron: '0 0 * * *' # Daily at midnight
  workflow_dispatch: # For manual trigger

jobs:
  get-pdf:
    runs-on: ubuntu-latest
    steps:
      - uses: Sbrjt/overleaf-resume-syncer@main
        with:
          overleaf_url: 'https://www.overleaf.com/read/your-project-id' # Replace with your overleaf sharing link (not your project url!)
          github_token: ${{ secrets.GITHUB_TOKEN }}

          # Optional:
          gdrive_link: ${{ vars.GDRIVE_LINK }}
          gdrive_service_account_key: ${{ secrets.GDRIVE_SERVICE_ACCOUNT_KEY }}
```

<details>
<summary>
Detailed Steps
</summary>

### Step 1: Get the Overleaf Share Link

1. Open your project on Overleaf.
1. Click **Share** in the top-right corner.
1. Enable **Link Sharing** and copy the **view-only link**.

### Step 2: Create the Repo

1. Create a repo to host your resume (or fork [this](https://github.com/Sbrjt/resume) template).
   Create a workflow at `.github/workflows/update-resume.yml` using the example above.
1. Provide the `overleaf_url` (or you can use a repo Variable).
1. Run the workflow once (Actions > Fetch Overleaf Resume > Run workflow).
1. (Optional) Enable GitHub Pages to host your resume.

### Step 3: (Optional) Enable Google Drive Sync

> [!NOTE]
> This setup is a pain in the ass—but you only have to do it once.

1. Go to [Google Cloud Console](https://console.cloud.google.com/). See [video](https://www.embedlite.com/embed/mCZRICueLX0?&start=7&end=110).
1. Create a project and enable the **Google Drive API**.
1. Create a **Service Account** under **IAM & Admin > Service Accounts**.
1. Generate a **JSON** service account key (**Keys > Add Key > Create new key > JSON**) and download it.
1. Create a blank `resume.pdf` file in Google Drive.
1. Share the file with the service account's email address (eg `your-uploader@...iam.gserviceaccount.com`) with **Editor** permission, then copy its share link.
1. Navigate to **Settings > Secrets and variables > Actions**:
   - Under **Variables**, add:
     - `GDRIVE_LINK`: eg, `https://drive.google.com/file/d/.../view?...`
   - Under **Secrets**, add:
     - `GDRIVE_SERVICE_ACCOUNT_KEY`: The **entire** JSON content of the downloaded service account key file.

</details>

<details>
<summary>
How it works
</summary>

<br>

This is a GitHub composite action, which can be imported as `Sbrjt/overleaf-resume-syncer@v1` in any other GitHub Action. (See `action.yml` file.) The action takes in 2 inputs: your overleaf url and a github token.

First, it checks out the repo, installs python and selenium, and runs a python script to fetch the pdf.

`download_from_overleaf.py` get the latex code from overleaf by inspecting websockets frames and compares it with the existing `resume.tex`. If there are changes, it finds the download button and clicks it to get the new pdf. Otherwise, the action skips the next step.

Then it uses the GitHub token provided in the inputs to push the updated code on your behalf (as GitHub Actions bot).

The action is intended to run on a scheduled cron job (eg, daily or weekly).

</details>

#

The most trivial solution might seem like having some latex previewer/builder and editing the `.tex` file locally. But TeX distributions like TeX-live are huge and can be a hassle to set up. More info [here](https://mark-wang.com/blog/2022/latex/).

Using Selenium sidesteps Overleaf's protections (which block curl and unauthenticated scrapers) by simulating an actual user session.
