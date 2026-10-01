import "./Login.css";

const Login = () => {
  const handleKakaoLogin = () => {
    const params = new URLSearchParams({
      client_id: import.meta.env.VITE_CLIENT_ID,
      redirect_uri: import.meta.env.VITE_REDIRECT_URI,
      response_type: "code",
      prompt: "login",
    });

        window.location.href = `https://kauth.kakao.com/oauth/authorize?${params.toString()}`;
  };
  const guestLogin = () => {
    const url = new URL(import.meta.env.VITE_REDIRECT_URI);
    url.searchParams.set("mode","guest");
    window.location.href = url.toString();
};

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="login-profile">
          <div className="login-profile-icon">
            <img src="/favicon.ico" alt="서비스 아이콘" />
          </div>

          <div>
            <h1>로그인 해주세요!</h1>
            <p>
              궁금한 내용을
              <br />
              편하게 질문해보세요.
            </p>
          </div>
        </div>

        <div className="login-message-box">
          <p>
            로그인하면 대화를 저장하고
            <br />
            다음에도 이어갈 수 있어요.
          </p>
        </div>

        <button
          type="button"
         className="kakao-login-button"
          onClick={handleKakaoLogin}
        >
          <img src="/kakao_login.png" alt="카카오 로그인" />
        </button>

        <p className="login-sub-text">
          카카오 계정으로 간편하게 시작하세요.
        </p>
        <div className="login-divider">
          <span>먼저 써보고 싶다면</span>
        </div>

        <button
          type="button"
          className="guest-login-button"
          onClick={guestLogin}>
            <span>로그인 없이 체험하기</span>
            <span aria-hidden="true">→</span>
            </button>
        <p className="guest-login-description">
          체험 중에는 이전 대화를 기억하지 않으며,
          <br />
          새로고침하면 대화 내역이 사라져요.
        </p>
      </div>
    </div>
  );
};

export default Login;