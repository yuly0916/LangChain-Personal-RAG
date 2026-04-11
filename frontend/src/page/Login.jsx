
const Login = () => {
    window.location.href = `https://kauth.kakao.com/oauth/authorize?client_id=${import.meta.env.VITE_CLIENT_ID}&redirect_uri=${import.meta.env.VITE_REDIRECT_URI}&response_type=code&prompt=login`;

    return (
        <>
        </>
    )
}

export default Login;