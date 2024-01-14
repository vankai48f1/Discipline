# VLU

Crack expiration:
Step 1: director ==> ..\enterprise\web_enterprise\static\src\webclient\home_menu\expiration_panel.js
Step 2:
_computeDiffDays(date) {
const today = DateTime.utc();
const duration = date.diff(today, "days");
return 1000;
}

# CI/CD

Running apt-get update... curl
-L "https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh" | sudo bash
gitlab-runner register --url https://gitlab.com  --token glrt-XqzYLGDzz7jCwowDLy9G
sudo gitlab-runner start
sudo gitlab-runner status
sudo gitlab-runner verify

# List account

*-Teacher-*
1. tam.dt@vanlang.vn - 1
2. danh.hp@vanlang.vn - 1

*-Student-*
3. khai.2174801030038@vanlang.vn - 1
4. tuan.2174801030037@vanlang.vn - 1

*-Staff-*
5. uyen.btm@vanlang.vn - 1

# API keys: 
1. Access API: 323c031f47e302e59baa9e0f5fc22e12fd26de64
## Integrate with your tools

- [ ] [Set up project integrations](https://gitlab.com/buiductuan12081995/vlu/-/settings/integrations)

## Collaborate with your team

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Automatically merge when pipeline succeeds](https://docs.gitlab.com/ee/user/project/merge_requests/merge_when_pipeline_succeeds.html)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/index.html)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing(SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***
