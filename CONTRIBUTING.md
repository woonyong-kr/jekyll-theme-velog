# 기여 방법

버그 재현, 문서 교정, 접근성·반응형 개선과 설정 일반화를 받는다. 개인 블로그에만 필요한 콘텐츠와 비밀값은 포함하지 않는다.

## 시작

Ruby `3.2.9`와 Bundler `2.5.23`을 사용한다.

```bash
git clone https://github.com/woonyong-kr/jekyll-theme-velog.git
cd jekyll-theme-velog
BUNDLE_FORCE_RUBY_PLATFORM=true bundle install
BUNDLE_FORCE_RUBY_PLATFORM=true bundle exec jekyll doctor
BUNDLE_FORCE_RUBY_PLATFORM=true bundle exec jekyll build
```

로컬 미리보기는 다음 명령으로 실행한다.

```bash
BUNDLE_FORCE_RUBY_PLATFORM=true bundle exec jekyll serve
```

## 변경 범위

- 사용자 설정은 `_config.yml`과 `_data/*.yml`에 둔다.
- 개인 계정, 저장소 이름, URL과 추적 ID를 레이아웃에 하드코딩하지 않는다.
- 라이트·다크 모드와 모바일 폭을 함께 확인한다.
- 기능 변경은 README의 설정·사용법과 함께 수정한다.
- 빌드 결과물 `_site/`과 로컬 캐시는 커밋하지 않는다.

## Pull Request

PR에는 문제, 변경 범위와 검증 명령을 적는다. 화면 변경은 전후 이미지를 포함한다.

```bash
BUNDLE_FORCE_RUBY_PLATFORM=true bundle exec jekyll doctor
BUNDLE_FORCE_RUBY_PLATFORM=true bundle exec jekyll build
```

두 명령이 통과하고 `_site/index.html`이 생성돼야 한다.
