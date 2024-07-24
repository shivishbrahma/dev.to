---
cover_image: https://media.dev.to/cdn-cgi/image/width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F0mqmsf3owvhv3fea72wf.png
created_at: 2022-03-06 07:33:46+00:00
description: Developing a React App has always been a fascinating experience as a
    Frontend Developer. To build...
edited_at: 2024-07-21 19:15:30+00:00
id: 1012218
published: true
published_at: 2022-03-06 07:33:46+00:00
slug: deploying-react-app-in-github-pages-4jfd
tag_list: github, react, deployment
title: Deploying React App in GitHub Pages
---
Developing a React App has always been a fascinating experience as a Frontend Developer. To build exotic components and embed them in our websites that we develop as a part of job or hobby, is an adventure in itself. When the time comes to share with friends and family, nothing is best than to host it over a website. There are quite a lot of options for free hosting, but for an open-source developer, Github Pages has separate place. In this article, we will try to learn to deploy an React App in Github Pages.

## Getting Started

Everything starts with the React project already pushed into a Github repo.

The best way of using Github architecture is by writing workflows in .yml files where we use predefined actions to perform command functionalities in Github server.

## Understanding workflow structure

All workflow files needs to be placed in `.github/workflows`. The action to be used for this objective is `actions/checkout` and `actions/setup-node`.


```yml
name: React app deployment

on:
  push:
    branches: [ 'reactify' ]
  pull_request:
    branches: [ 'reactify' ]

jobs:
  build:

    runs-on: ubuntu-latest

    strategy:
      matrix:
        node-version: [12.x, 14.x, 16.x]

    steps:
    - uses: actions/checkout@v2
    - name: Use Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v1
      with:
        node-version: ${{ matrix.node-version }}
    - run: npm ci
      shell: bash
    - run: npm run build --if-present
      shell: bash
    
    - run : git config user.name github-actions
      shell: bash
    - run : git config user.email github-actions@github.com
      shell: bash
    - run : git --work-tree build add --all
      shell: bash
    - run : git commit -m "Automatic Deploy action run by github-actions"
      shell: bash
    - run : git push origin HEAD:gp-react --force
      shell: bash
```

First defining the name of the workflow, and selecting the trigger for workflow as push or pull_request on certain branches like **reactify** in this case. Furthermore, defining the job with ubuntu-latest as os and selecting node version as 12.x, 14.x, 16.x. In the steps, we use checkout action to checkout in the repo. Next, we setup node with npm for versions. Install the node modules from package.json and create the build with the build script if present. Change user.name and user.email and add *build* in the work tree and commit as *github-actions* user to a **gp-react** branch with force.

## Create a reactify branch and push to github

Since we don't have a branch named **reactify**, let's create one

```bash
git branch reactify

git checkout reactify

git commit -m "Added github actions for gh pages"

# Set the upstream so that from the next time we can only do git push for updating repo
git push --set-upstream origin reactify
```

After successful push, we go to **Actions** tab in the repo of Github.

![Location of Actions tab in Github](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ujc1xc3pvm97laegcchh.png)

Select the recent workflow, to see details if there is a green tick ✅ then the run is successful else check FAQ section of articles for list of errors in details. The details of workflow page is similar to image below: 

![Workflow details page](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/xxjobo4dtsu3azc2rcsx.png)

## Setting up the root folder 

The final setup for the github pages is selecting the branch and root folder. 

Select the **Settings** tab and click on **Pages** option in sidebar.
Select branch `gp-react` in *Source* option and `/root` as root folder.

![Location of Setting tab in Github](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/mn91rso0xt79d9wy1jd3.png)

![Pages page in Settings tab](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/d92hyz89eriq5wegame7.png)

The url for the site is available in the same page as visible above.

There is a custom workflow for github-pages deployment that is also available in **Actions** tab.

## FAQ

1.  Why using multiple versions for node-setup?
    Ans: We are using 12, 14, 16 node versions, because there might be some new or old packages that won't be compiled in one of the 3. But it is advisable to use the node version that you are using in the local setup.
2.  What are the possible reasons for failing react compilation in Github Workflow?
    Ans: Here a list of reasons where react compilation might fail:
    - If there are depreciation warnings or any other react warnings showing in terminal after `npm start` in local.
    - If you miss to create the same branch name mentioned as trigger on push or pull_request.
    - If the node packages being used doesn't support node versions mentioned in the node versions array.

## Reference

- [Github actions/checkout](https://github.com/actions/checkout)
- [Github actions/setup-node](https://github.com/actions/setup-node)![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/vyg1bd0k2qgaat5suhz2.png)
 