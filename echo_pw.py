import password as pw

def main():
    while True:  # 무한 루프를 시작합니다.
        # 사용자 입력 받기
        password = input("비밀번호를 입력하세요: ")
        result = pw.validate_password(password)
        print(result)

        if password = "!quit":  # 종료 조건 확인
            print("프로그램을 종료합니다. 안녕히 가세요!")  
            break  # 루프를 종료하고 프로그램을 끝냅니다.
        

if __name__ == "__main__":
    main()