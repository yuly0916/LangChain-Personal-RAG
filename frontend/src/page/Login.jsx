
const Login = () => {
        const moveToLogin = () => {
        window.location.href = `https://kauth.kakao.com/oauth/authorize?client_id=${import.meta.env.VITE_CLIENT_ID}&redirect_uri=${import.meta.env.VITE_REDIRECT_URI}&response_type=code&prompt=login`;
    }
    console.log(import.meta.env.VITE_CLIENT_ID);
    
    return (
        <>
            <button onClick={moveToLogin}>로그인</button>
        </>
    )
}

export default Login;