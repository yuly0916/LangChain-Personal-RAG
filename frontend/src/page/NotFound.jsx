import { useNavigate } from "react-router-dom";
import "./Home.css";

const NotFound = () => {
    const navigate = useNavigate();

    return (
        <div className="home-container">

            <div className="glass-card" style={{ padding: "60px 40px" }}>
                <h1 style={{ fontSize: "6rem", margin: "0", background: "linear-gradient(135deg, var(--color-primary-light), var(--color-primary))", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent", textShadow: "0 10px 20px rgba(0,0,0,0.05)" }}>
                    404
                </h1>
                <h2 style={{ fontSize: "1.5rem", marginTop: "10px", marginBottom: "20px", color: "var(--color-text-main)" }}>
                    길을 잃으신 것 같아요.
                </h2>
                <p style={{ color: "var(--color-text-muted)", marginBottom: "40px", fontSize: "1rem" }}>
                    요청하신 페이지를 찾을 수 없어요.
                </p>

                <button
                    onClick={() => navigate("/", { replace: true })}
                    className="chat-send-btn"
                    style={{ padding: "12px 30px", fontSize: "1rem" }}
                >
                    홈으로 돌아가기
                </button>
            </div>
        </div>
    )
}

export default NotFound;