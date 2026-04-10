import axios from "axios";

const api = axios.create({
    baseURL: import.meta.env.VITE_IP
});
function get_cookie(name) {
    var value = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');    
    return value? value[2] : null;
}

api.interceptors.request.use(
    (config)=>{
        config.headers.Authorization = `Bearer ${get_cookie("jwt_token")}`;
        return config;
},
(err) => {
    console.log('요청 중 에러 ',err);
    return Promise.reject(err);
}
)

export default api;