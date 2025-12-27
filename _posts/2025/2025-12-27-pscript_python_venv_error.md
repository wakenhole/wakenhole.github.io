---
title: "[개발팁] 파이썬 가상환경 오류 해결: '이 시스템에서 스크립트를 실행할 수 없으므로...' 완벽 가이드"
date: 2025-12-27 19:00:00 +0900
categories: [Tech, Software Guides]
tags:
  - venv
  - PowerShell
  - ExecutionPolicy
  - 오류해결
toc: true
toc_sticky: true
tagline: "DevEnvironment"
image:
  path: https://images.unsplash.com/photo-1526379095098-d400fd0bf935?ixlib=rb-4.0.3&auto=format&fit=crop&w=1474&q=80
---

새로운 프로젝트를 시작하려는 설레는 마음으로 파이썬 가상환경(Virtual Environment)을 생성하고 `activate` 명령어를 입력하는 순간, 예상치 못한 붉은색 에러 메시지와 마주하게 되는 경우가 있습니다. 특히 윈도우(Windows) 환경에서 VS Code나 PowerShell을 사용할 때 빈번하게 발생하는 이 문제는 개발 입문자들을 당혹스럽게 만드는 첫 번째 관문이기도 합니다. 오늘은 `.\Scripts\Activate` 실행 시 발생하는 보안 오류의 원인을 명확히 짚어보고, 이를 안전하게 해결하는 표준적인 절차를 다루어 보겠습니다.

{% include ad-inpost.html %}

### 1. 문제 상황 인식: 무엇이 실행을 막고 있는가?

![Error Message Analysis](https://images.unsplash.com/photo-1594322436404-5a0526db4d13?ixlib=rb-4.0.3&auto=format&fit=crop&w=1470&q=80){: width="400px"}

가상환경을 활성화하기 위해 `.\Scripts\Activate` 명령어를 입력했을 때, 다음과 같은 에러 메시지가 출력된다면 이는 **PowerShell의 실행 정책(Execution Policy)** 때문입니다.

```
& : 이 시스템에서 스크립트를 실행할 수 없으므로 C:\Users\...\.venv\Scripts\Activate.ps1 파일을 로드할 수 없습니다. 자세한 내용은 about_Executi
on_Policies(https://go.microsoft.com/fwlink/?LinkID=135170)를 참조하십시오.
위치 줄:1 문자:3
+ & C:/Users/.../.venv/Scripts/Activate.ps1
+   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : 보안 오류: (:) [], PSSecurityException
    + FullyQualifiedErrorId : UnauthorizedAccess
```

> "이 시스템에서 스크립트를 실행할 수 없으므로 C:\Users\...\activate.ps1 파일을 로드할 수 없습니다. 자세한 내용은 about_Execution_Policies를 참조하십시오."

이 메시지는 시스템의 오류라기보다는, 윈도우가 악성 스크립트의 무분별한 실행을 방지하기 위해 기본적으로 설정해 둔 **보안 기능**이 작동하고 있음을 의미합니다. 마이크로소프트는 PowerShell의 기본 실행 정책을 `Restricted`(제한됨)로 설정하여, 서명되지 않은 스크립트가 실행되는 것을 차단하고 있습니다. 즉, 우리가 생성한 가상환경 실행 파일인 `Activate.ps1` 역시 시스템 입장에서는 '신뢰할 수 없는 외부 스크립트'로 간주되어 실행이 거부된 것입니다.

{% include ad-inpost.html %}

### 2. 해결 방법: 실행 정책 변경 (Set-ExecutionPolicy)

이 문제를 해결하기 위해서는 PowerShell의 실행 정책을 변경해야 합니다. 가장 널리 권장되는 설정은 **`RemoteSigned`** 입니다. 이는 로컬 컴퓨터에서 작성한 스크립트는 실행을 허용하되, 인터넷에서 다운로드한 스크립트는 신뢰할 수 있는 배포자의 서명이 있어야만 실행할 수 있도록 하는 '타협점'과 같은 설정입니다.

![Powershell Administrator](https://images.unsplash.com/photo-1629654297299-c8506221ca97?ixlib=rb-4.0.3&auto=format&fit=crop&w=1470&q=80)

해결 절차는 다음과 같습니다.

1.  **관리자 권한으로 PowerShell 실행:**
    * 시작 메뉴에서 'PowerShell'을 검색한 후, 마우스 오른쪽 버튼을 클릭하여 **[관리자 권한으로 실행]**을 선택합니다. (일반 권한으로는 정책을 변경할 수 없습니다.)

2.  **현재 정책 확인 (선택 사항):**
    * 아래 명령어를 입력하여 현재 상태를 확인합니다. 아마도 `Restricted`라고 출력될 것입니다.
    ```powershell
    Get-ExecutionPolicy
    ```

3.  **정책 변경 명령어 입력:**
    * 가장 핵심적인 단계입니다. 아래 명령어를 입력하여 정책을 `RemoteSigned`로 변경합니다.
    ```powershell
    Set-ExecutionPolicy RemoteSigned
    ```
    * 만약 `RemoteSigned`로도 해결되지 않는 특수한 경우라면 `Unrestricted`(모든 제한 해제)를 사용할 수 있으나, 보안상 권장하지 않습니다.

4.  **변경 사항 승인:**
    * 명령어 입력 후 실행 정책 변경 여부를 묻는 메시지가 나오면 **`Y`** (또는 `A`)를 입력하고 엔터(Enter)를 누릅니다.

{% include ad-inpost.html %}

### 3. 결과 검증 및 가상환경 재실행

정책 변경이 완료되었다면, 다시 원래 작업하던 VS Code나 터미널로 돌아가 가상환경 활성화를 시도해 봅니다.

![Success Code](https://images.unsplash.com/photo-1517694712202-14dd9538aa97?ixlib=rb-4.0.3&auto=format&fit=crop&w=1470&q=80)

```powershell
# 가상환경 활성화 재시도
.\Scripts\Activate.ps1
```


{% include ad-inpost.html %}