---
title: "GitHub Pages와 Jenkins로 테마를 배포하는 방법"
description: "공식 Pages artifact workflow와 Jenkins의 독립 배포 경로, 검증 지점을 정리합니다."
date: 2026-03-29 09:00:00 +0900
updated_at: 2026-08-04 20:00:00 +0900
thumbnail: /assets/images/posts/deployment-guide-cover.png
series: theme-operations
tags:
  - GitHub Pages
  - Jenkins
  - Deployment
  - Open Source
---

기본 배포는 `gh-pages` 브랜치에 산출물을 다시 커밋하지 않습니다. GitHub의 공식 Pages Actions로 빌드 artifact를 전달하고 `github-pages` environment에 배포합니다.

## 배포 흐름

```text
main push
  ↓
저장소 URL·base path 계산
  ↓
Jekyll production build
  ↓
HTML 구조·내부 링크·placeholder 검증
  ↓
Pages artifact 업로드
  ↓
github-pages environment 배포
```

pull request에서는 빌드와 검증까지만 실행합니다. merge되지 않은 코드가 라이브 사이트를 바꾸지 않습니다.

## GitHub Pages 설정

1. 저장소 **Settings → Pages**로 이동합니다.
2. **Build and deployment → Source**를 `GitHub Actions`로 선택합니다.
3. `main`에 push합니다.
4. **Actions → Pages**의 build와 deploy job을 확인합니다.

프로젝트 페이지와 사용자 페이지 모두 `_config.yml`의 로컬 URL을 유지할 수 있습니다. workflow가 실제 저장소 주소와 하위 경로를 빌드에 전달합니다.

```yaml
url: "http://localhost:4000"
baseurl: ""
```

커스텀 도메인은 Pages 설정에서 도메인을 등록한 뒤 `url`만 명시합니다.

```yaml
url: "https://blog.example.com"
baseurl: ""
```

## 실패 지점 확인

| 단계 | 확인할 것 |
|---|---|
| Configure Pages | Pages source가 GitHub Actions인지 |
| Build | YAML 문법, Gemfile.lock, 미래 날짜 포스트 |
| Verify | 중첩 landmark, 깨진 내부 링크, 미치환 설정값 |
| Deploy | `pages: write`, `id-token: write`, environment 보호 규칙 |

배포 성공 뒤에는 사이트 주소, CSS·이미지, 글 상세, `feed.xml`, `sitemap.xml`을 확인합니다.

## 커스텀 도메인

1. **Settings → Pages → Custom domain**에 도메인을 입력합니다.
2. DNS에서 apex 도메인은 GitHub Pages A/AAAA 레코드, subdomain은 `username.github.io` CNAME을 설정합니다.
3. DNS 검증 후 **Enforce HTTPS**를 켭니다.

IP 주소는 변경될 수 있으므로 GitHub Pages 공식 문서의 현재 값을 사용합니다.

## Jenkins 경로

`Jenkinsfile`은 사내 Jenkins처럼 GitHub Actions를 사용할 수 없는 환경을 위한 별도 예시입니다.

```text
bundle install
  → profile cache
  → jekyll build
  → output 검증
  → gh-pages branch push
```

요구사항:

- Ruby 3.4.x, Bundler, Git
- `github-pages` credential
- Pages source `gh-pages / (root)`

기본 Actions 배포와 Jenkins 배포를 동시에 켜면 배포 기준이 둘로 나뉩니다. 한 저장소에서는 하나의 경로만 선택합니다.

## 다음 단계

→ **[GitHub 프로필 동기화와 기여 그래프를 붙이는 방법]({{ site.baseurl }}/github-profile-sync-and-contribution-graph/)**
