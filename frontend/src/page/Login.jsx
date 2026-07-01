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
              토끼에게 물어보려면
              <br />
              카카오 로그인이 필요해요.
            </p>
          </div>
        </div>

        <div className="login-message-box">
          <p>
            로그인 후 서비스를
            <br />
            바로 이용할 수 있어요.
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
      </div>
    </div>
  );
};

export default Login;