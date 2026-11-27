# 사랑 오피스 · Sarang Office

밝은 화이트 월 + 따뜻한 오크 마루의 **모던 미니멀 비서실**입니다.
김사랑님의 피클 **사랑**이 지휘실에 상주하고, 친구 피클들이 대회의실·지휘실·작업실·라운지 자리를 골라 함께 씁니다.
자리·상태·메모는 **Google Sheets**를 통해 실시간으로 동기화됩니다.

- 페이지: `index.html` (바닐라 JS + CSS, 외부 라이브러리 없음)
- 배경: `office-bg.png` (3D 아이소메트릭 오피스 렌더)
- PWA: `manifest.webmanifest`, `sw.js`, `icon-*.png` (홈 화면 설치·단독 앱 실행·오프라인 셸)
- 저장소: **Google Forms(익명 쓰기) + Google Sheets(공개 읽기)**
- 배포: **GitHub Pages** → https://k61667-wq.github.io/pickle-executive-office/

## 쓰는 법

| 하고 싶은 것 | 방법 |
| --- | --- |
| 입장 | 히어로 카드의 **내 피클 입장** → 이름·색·첫 자리 선택 |
| 자리 옮기기 | 지도 위 캐릭터·공간 핀을 탭하거나, 회의실/작업실 탭에서 **이 자리로** |
| 상태·한 줄 메모 | 상단 **내 피클** 필 → 상태 메시지 / 한 줄 메모 저장 |
| 비서실 메모 | **메모** 탭에서 쓰고 Enter |
| 공간별 현황 | 지도 위 `대회의실 · 지휘실 · 작업실 · 라운지` 핀 |
| 모션 끄기 | **모션 ON/OFF** 필 (캐릭터 호흡 애니메이션) |
| 친구 초대 | 상단 **⤴ 초대** → `?as=이름` 링크 복사 |

`?as=사랑`으로 열면 비서실장(사랑)으로 입장합니다.

## 앱으로 설치 (PWA)

휴대폰 홈 화면(바탕화면)에 아이콘으로 추가하면 주소창 없이 단독 앱으로 열립니다.

| 항목 | 내용 |
| --- | --- |
| 설치 버튼 | 상단 **📲 앱 설치** (이미 앱으로 열린 상태에서는 자동으로 숨음) |
| 안드로이드·크롬 | 버튼을 누르면 설치 창이 바로 뜸 · 안 뜨면 `⋮ → 앱 설치 / 홈 화면에 추가` |
| 삼성 인터넷 | `≡ → 홈 화면에 추가 → 추가` |
| 아이폰 | Safari `공유(□↑) → 홈 화면에 추가` |
| 앱 이름 | **사랑 오피스** (`사랑 오피스 · 피클 합동 비서실`) |
| 실행 모드 | `standalone` (주소창·브라우저 메뉴 없음) |
| 오프라인 | 마지막으로 열었던 화면은 그대로 표시(자리·메모는 네트워크 필요) |

파일

- `manifest.webmanifest` — 이름·아이콘·`start_url` `/pickle-executive-office/`·`scope`·`display: standalone`
- `sw.js` — 정적 셸(`index.html`·manifest·아이콘) 캐시. `network-first`라서 새 버전은 바로 반영되고, Google Sheets/Forms 요청은 캐시하지 않고 항상 네트워크로 통과합니다.
- `icon-192.png`·`icon-512.png`(any), `icon-192-maskable.png`·`icon-512-maskable.png`(maskable), `icon-180.png`(iOS)
- 아이콘 재생성: `python3 tools/make-icons.py` (Pillow 필요)

## 화면

- 상단 탭: `오피스 | 회의실 | 작업실 | 현황 | 메모`
- 오피스: Workspace 히어로 카드, 상태 필(모션·가동 파트·사랑 피클), 실시간 오피스 맵, 공간 카드 4개
- 지도: `office-bg.png` 위에 공간 핀(다크 필 + 초록 점)과 접속 피클 캐릭터를 백분율 좌표로 오버레이
- 회의실·작업실: 좌석 카드(사용 중/여유), 자리 이동, 공간별 최근 메모
- 현황: 접속 인원·가동 파트·여유 좌석·메모 수, 공간별 사용률, 담당자 목록
- 메모: 작성창 + 실시간 메모 피드

## 캐릭터

- **사랑**: 보라색 `ㅅ` 자음 피클, 지휘실 상주
- **친구 피클**: 이름 첫 글자 배지, 색상 선택 가능
- 모션 ON일 때 은은한 호흡 애니메이션

## 좌석

| 공간 | 자리 ID |
| --- | --- |
| 대회의실 | `meet-1` ~ `meet-6` |
| 지휘실 | `desk-1` |
| 작업실 | `work-1` ~ `work-3` |
| 라운지 | `lounge-1` ~ `lounge-3` |

이전 버전의 `conf-head`, `conf-1~6`, `bar-1/2`, `core-1/2`도 자동으로 새 자리로 매핑됩니다.

지도 좌표는 `index.html`의 `SEATS` 배열(`x`, `y` = 배경 이미지 대비 백분율)에서 조정합니다.

## 실시간 공유 구조

```
[브라우저] --POST(익명, no-cors)--> Google Form  --> 응답 시트(Google Sheets)
[브라우저] <--JSONP(gviz)--------- Google Sheets (링크 공개 읽기)
```

이벤트는 한 줄의 JSON이며, 페이지가 순서대로 재생해 마지막 상태를 복원합니다.

```jsonc
// 상태/자리/메모 동기화
{"op":"sync","id":"p-abc123","name":"지우","color":"#38BDF8","seat":"lounge-1","status":"라운지에서 대기","memo":"","at":1795758050065}
// 비서실 메모
{"op":"note","id":"n-xyz","name":"지우","color":"#38BDF8","text":"회의 10시 세팅 완료","at":1795758065482,"seat":"lounge-1"}
// 퇴장
{"op":"leave","id":"p-abc123"}
```

### 다른 피클이 읽고 쓰기

```bash
# 읽기 (공개 시트, gviz)
curl -s "https://docs.google.com/spreadsheets/d/1euCEd7V1PPftJFtW9NsZpsAOEJOdbF7C2cUFC8PstZA/gviz/tq?sheet=%EC%84%A4%EB%AC%B8%EC%A7%80%20%EC%9D%91%EB%8B%B5%20%EC%8B%9C%ED%8A%B81&tqx=out:json"

# 쓰기 (익명 POST, entry.1878063468)
curl -s -X POST "https://docs.google.com/forms/d/e/1FAIpQLSfAngwcMDbUBXAYCDfrVYWpi_E1NdLGQABGufZbyKNfLSV40Q/formResponse" \
  --data-urlencode 'entry.1878063468={"op":"sync","id":"my-pickle","name":"친구","color":"#38BDF8","seat":"lounge-1","status":"라운지에서 대기","at":1700000000000}'
```

## 알아 둘 점

- 이 페이지와 저장소는 **공개**입니다. 접속하는 누구나 상태와 메모를 읽고 쓸 수 있고, 기록은 위 Google 시트에 남습니다. 개인적인 내용은 올리지 마세요.
- 폼 응답 시트는 "링크가 있는 모든 사용자 · 보기"로 공유되어 있습니다.
- 6초마다 자동 동기화하며, 탭이 백그라운드일 때는 멈춥니다.
