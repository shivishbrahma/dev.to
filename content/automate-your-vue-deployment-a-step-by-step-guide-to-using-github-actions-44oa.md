---
cover_image: https://media.dev.to/cdn-cgi/image/width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fm52zorn1uiwo74k84rx7.png
created_at: 2024-08-01 17:31:43+00:00
description: Deploying a Vue application can be a tedious and error-prone process,
    especially when done manually....
edited_at: 2024-08-02 04:54:50+00:00
id: 1944047
published: true
published_at: 2024-08-01 17:31:43+00:00
slug: automate-your-vue-deployment-a-step-by-step-guide-to-using-github-actions-44oa
tags:
- github
- vue
- deployment
title: 'Automate Your Vue Deployment: A Step-by-Step Guide to Using GitHub Actions'
---
Deploying a Vue application can be a tedious and error-prone process, especially when done manually. But what if you could automate this process, ensuring that your app is deployed quickly, reliably, and with minimal effort? Enter GitHub Actions, a powerful tool that allows you to automate your deployment workflow directly within your GitHub repository.

In this blog post, we'll take you through a step-by-step guide on how to deploy your Vue application using GitHub Actions. We'll cover the benefits of automation, the basics of GitHub Actions, and provide a hands-on tutorial on setting up your first workflow. By the end of this article, you'll be able to streamline your deployment process, focus on building amazing Vue apps, and take your development workflow to the next level.

## Getting Started

We start with a VueJS project already pushed to GitHub and use GitHub Actions to deploy it.

### Understanding workflow structure

All workflow files should be stored in the `.github/workflows` directory. To achieve this, utilize the `actions/checkout` and `actions/setup-node` actions.

```yaml
name: Vue app deployment

on:
    push:
        branches: ["vuetify"]
    pull_request:
        branches: ["vuetify"]

jobs:
    build:
        runs-on: ubuntu-latest

        strategy:
            matrix:
                node-version: [18.x, 20.x]

        steps:
            - uses: actions/checkout@v3
              with:
                token: ${{ secrets.GH_TOKEN }}
            - name: Use Node.js ${{ matrix.node-version }}
              uses: actions/setup-node@v3
              with:
                  node-version: ${{ matrix.node-version }}
            - name: Build the dist
              run: |
                  npm ci
                  npm run build --if-present
            - name: Commit build to gp-vue
              run: |
                  git config user.name github-actions
                  git config user.email github-actions@github.com
                  git --work-tree dist add --all 
                  git commit -m "Vue deployment run by github-actions"
                  git push origin HEAD:gp-vue --force
              shell: bash
```

Defining the workflow name and the actions to be used. Using a node version of 20.x. and we are welcome to rename the user name and email. The branch name for the deployment is **gp-vue**, you can change it too.

### Create a vuetify branch and push to github

We don't have a branch named **vuetify**, let's create one

```bash
git branch vuetify

git checkout vuetify

git push -u origin vuetify
```

After successful push, we go to **Actions** tab in the repo of Github.

![Location of Actions tab in Github](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ujc1xc3pvm97laegcchh.png)

Select the recent workflow, to see details if there is a green tick ✅ then the run is successful else check FAQ section of articles for list of errors in details. The details of workflow page is similar to image below:

![Workflow details page](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/pzpflbm1vfo0nm7bwd83.png)

### Setting up the root folder

The final setup for the github pages is selecting the branch and root folder.

Select the **Settings** tab and click on **Pages** option in sidebar.
Select branch `gp-vue` in *Source* option and `/root` as root folder.

![Location of Setting tab in Github](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/mn91rso0xt79d9wy1jd3.png)

![Pages page in Settings tab](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/tvomrxqe7nggrjokldsj.png)

The url for the site is available in the same page as visible above.

There is a custom workflow for github-pages deployment that is also available in **Actions** tab.

## FAQs

1. Why using multiple versions for node-setup?
    Ans: We are using 18.x and 20.x node versions, because there might be some new or old packages that won't be compiled in one of the 2. But it is advisable to use the node version that you are using in the local setup.
2. What are the possible reasons for failing react compilation in Github Workflow?
    Ans: Here a list of reasons where react compilation might fail:
    - If there are depreciation warnings or any other react warnings showing in terminal after `npm start` in local.
    - If you miss to create the same branch name mentioned as trigger on push or pull_request.
    - If the node packages being used doesn't support node versions mentioned in the node versions array.

## References

- [Github actions/checkout](https://github.com/actions/checkout)
- [Github actions/setup-node](https://github.com/actions/setup-node)
