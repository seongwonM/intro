import requests

def get_github_user_info_and_repos(username):
    """ GitHub 사용자 정보 및 저장소 목록 가져오는 함수 """
    base_url = "https://api.github.com/users"
    user_url = f"{base_url}/{username}"
    repos_url = f"{base_url}/{username}/repos?per_page=5"  # 최대 5개 저장소 조회

    try:
        # 사용자 정보 요청
        user_response = requests.get(user_url, timeout=5)
        if user_response.status_code == 404:
            return {"error": "사용자를 찾을 수 없습니다."}
        elif user_response.status_code != 200:
            return {"error": f"사용자 정보 요청 실패 (상태 코드: {user_response.status_code})"}

        # 저장소 목록 요청
        repos_response = requests.get(repos_url, timeout=5)
        if repos_response.status_code != 200:
            return {"error": f"저장소 목록 요청 실패 (상태 코드: {repos_response.status_code})"}

        # 사용자 정보 및 저장소 데이터 반환
        user_data = user_response.json()
        repos_data = repos_response.json()

        return {
            "user": {
                "login": user_data.get("login"),
                "name": user_data.get("name"),
                "bio": user_data.get("bio"),
                "public_repos": user_data.get("public_repos"),
                "followers": user_data.get("followers"),
                "following": user_data.get("following"),
                "created_at": user_data.get("created_at"),
                "updated_at": user_data.get("updated_at"),
            },
            "repositories": [
                {
                    "name": repo["name"],
                    "html_url": repo["html_url"],
                    "description": repo["description"],
                    "stargazers_count": repo["stargazers_count"],
                    "forks_count": repo["forks_count"],
                    "language": repo["language"]
                }
                for repo in repos_data
            ]
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"네트워크 오류: {e}"}

# 테스트 코드
def test_github_user_info_and_repos():
    """ GitHub 사용자 정보 및 저장소 목록 테스트 """

    # ✅ 정상적인 사용자 검증 (GitHub 공식 계정 'octocat')
    valid_user = "octocat"
    result = get_github_user_info_and_repos(valid_user)
    assert "user" in result and "login" in result["user"], f"테스트 실패: {result}"
    assert "repositories" in result, f"테스트 실패: 저장소 정보 없음 - {result}"
    print(f"✅ 정상 사용자 테스트 통과: {result['user']['login']} (저장소 {len(result['repositories'])}개)")

    # ❌ 존재하지 않는 사용자 검증
    invalid_user = "thisuserdoesnotexist12345"
    result = get_github_user_info_and_repos(invalid_user)
    assert "error" in result and result["error"] == "사용자를 찾을 수 없습니다.", f"테스트 실패: {result}"
    print("✅ 비정상 사용자 테스트 통과: 사용자 없음 확인")

    # ❌ 빈 문자열 입력 검증
    empty_user = ""
    result = get_github_user_info_and_repos(empty_user)
    assert "error" in result, f"테스트 실패: {result}"
    print("✅ 빈 사용자명 테스트 통과")

# 테스트 실행
if __name__ == "__main__":
    test_github_user_info_and_repos()
