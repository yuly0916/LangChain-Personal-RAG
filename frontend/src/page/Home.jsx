import { HiOutlineLightBulb } from "react-icons/hi";
import "./Home.css";
import api from "../api";
import { useEffect } from "react";

function Home() {
  const test = async () => {
    const res = await api.get('/test');
    console.log(res);
    
  }
  useEffect(()=>{
    test();
  },[])
  return (
    <div className="home-container">
      {/* Animated Background */}
      <div className="orb orb-1"></div>
      <div className="orb orb-2"></div>
      <div className="orb orb-3"></div>

      {/* Glassmorphism Card */}
      <div className="glass-card">
        <div className="icon-wrapper">
          <HiOutlineLightBulb />
        </div>
        <h1 className="title">홈페이지 준비 중입니다</h1>
        <p className="subtitle">
          안녕하세요! 현재 최고의 사용자 경험을 위한 <br />
          <strong>AI RAG 웹 서비스</strong> 기반을 다지고 있습니다.<br />
          놀라운 비주얼과 완벽한 기능으로 곧 찾아뵙겠습니다.
        </p>

        {/* Loading Indicator */}
        <div className="loading-dots">
          <div className="dot"></div>
          <div className="dot"></div>
          <div className="dot"></div>
        </div>
      </div>
    </div>
  )
}

export default Home