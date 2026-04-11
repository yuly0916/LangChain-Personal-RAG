import { useEffect, useState, useRef, useLayoutEffect } from "react"
import { useNavigate } from "react-router-dom"
import api from "../api"
import { jwtDecode } from "jwt-decode"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import "./Home.css"

function Home() {
  const navigate = useNavigate();
  const [chats, setChats] = useState([]);
  const [chatInput, setChatInput] = useState("")
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [models, setModels] = useState([]);
  const [selectedModel, setSelectedModel] = useState({});
  const [userInfo, setUserInfo] = useState(null);

  const containerRef = useRef(null);
  const prevScrollHeightRef = useRef(0);
  const isFetchingOlderRef = useRef(false);
  const isInitialLoadRef = useRef(true);
  const 페이징사이즈 = 30;

  const 채팅기록가져오기 = async (pageNum) => {
    try {
      setIsLoading(true);


      if (pageNum > 1 && containerRef.current) {
        isFetchingOlderRef.current = true;
        prevScrollHeightRef.current = containerRef.current.scrollHeight;
      }


      const res = await api.get(`/chat?page=${pageNum}&limit=${페이징사이즈}`);

      if (!res.data || res.data.length === 0) {
        setHasMore(false);
        return;
      }
      if (res.data.length < 페이징사이즈) {
        setHasMore(false);
      }
      setChats(prev => {
        if (pageNum === 1) return res.data;
        return [...res.data, ...prev];
      });
    } catch (e) {
      console.error(e);
      setHasMore(false);
    } finally {
      setIsLoading(false);
    }
  }
  const 전문AI모델가져오기 = async () => {
    const res = await api.get('/chat/models');
    setModels(res.data);
    setSelectedModel(res.data[0]);
  }
  const chatting = async () => {
    if (!chatInput.trim()) return;
    const currentInput = chatInput;
    setChatInput('');


    isFetchingOlderRef.current = false;
    setChats(p => [...p, { content: currentInput, role: "human" }]);

    try {
      const res = await api.post(`/chat?model_name=${selectedModel.name}`, currentInput);
      isFetchingOlderRef.current = false;
      setChats(p => [...p, { content: res.data.content, role: "ai" }]);
    } catch (e) {
      console.error(e);
    }
  }


  useLayoutEffect(() => {
    if (!containerRef.current) return;

    if (isFetchingOlderRef.current) {

      const currentScrollHeight = containerRef.current.scrollHeight;
      const heightDiff = currentScrollHeight - prevScrollHeightRef.current;
      containerRef.current.scrollTop += heightDiff;
      isFetchingOlderRef.current = false;
    } else {
      // 초기 접속 및 신규 대화 수발신 시
      if (isInitialLoadRef.current) {
        // 최초 로딩은 강제로 즉시 바닥에 꽂아줌
        containerRef.current.scrollTop = containerRef.current.scrollHeight;
        if (chats.length > 0) isInitialLoadRef.current = false;
      } else {
        // 채팅을 치거나 AI 답변을 받을 때는 부드럽게 밀리며 내려가게 구현
        containerRef.current.scrollTo({
          top: containerRef.current.scrollHeight,
          behavior: "smooth"
        });
      }
    }
  }, [chats]);

  const handleScroll = () => {
    if (!containerRef.current) return;

    // 사용자가 스크롤을 맨 위로 올리기 직전에 미리 다음 데이터를 당겨옴
    if (containerRef.current.scrollTop < 200 && hasMore && chats.length > 0 && !isLoading) {
      setPage(prev => prev + 1);
    }
  }

  const getCookie = (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
  };

  const handleLogout = () => {
    document.cookie = "jwt_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    navigate('/');
  }

  useEffect(() => {
    채팅기록가져오기(1);
    전문AI모델가져오기();

    const token = getCookie('jwt_token');
    if (token) {
      try {
        const decoded = jwtDecode(token);
        console.log(decoded);

        setUserInfo(decoded);
      } catch (e) {
        console.error("Token decoding failed:", e);
      }
    }
  }, [])

  useEffect(() => {
    if (page > 1) {
      채팅기록가져오기(page);
    }
  }, [page])

  return (
    <div className="home-container">
      {/* 화면 상단 사용자 프로필 & 우측 모델 선택 드롭다운 UI */}
      <div className="model-selector-wrapper" style={{ justifyContent: userInfo ? "space-between" : "flex-end", alignItems: "center" }}>

        {/* 접속한 사용자 정보 UI */}
        {userInfo && (
          <div style={{ display: "flex", alignItems: "center", gap: "12px", paddingLeft: "10px" }}>
            <img
              src={userInfo.profile_img || "https://img.freepik.com/free-vector/businessman-character-avatar-isolated_24877-60111.jpg"}
              alt="Profile"
              style={{ width: "45px", height: "45px", borderRadius: "50%", border: "2px solid var(--color-primary-light)", objectFit: "cover" }}
            />
            <div style={{ display: "flex", flexDirection: "column" }}>
              <span style={{ fontSize: "1.1rem", fontWeight: "700", color: "var(--color-text-main)" }}>
                {userInfo.name || "토끼 친구"}
              </span>
              <span style={{ fontSize: "0.85rem", color: "var(--color-primary)", fontWeight: "600" }}>
                {userInfo.role === "admin" ? "👑 Admin" : "👤 User"}
              </span>
            </div>

            {/* 어드민 버튼 및 로그아웃 버튼 */}
            <div style={{ display: "flex", gap: "8px", marginLeft: "15px" }}>
              {userInfo.role === "admin" && (
                <button
                  className="chat-send-btn"
                  onClick={() => navigate('/admin')}
                  style={{ padding: "6px 12px", fontSize: "0.85rem", borderRadius: "10px" }}
                >
                  Admin Setup
                </button>
              )}
              <button
                className="load-more-btn"
                onClick={handleLogout}
                style={{ padding: "6px 12px", fontSize: "0.85rem", borderRadius: "10px" }}
              >
                로그아웃
              </button>
            </div>
          </div>
        )}

        <select
          className="model-selector"
          value={selectedModel?.name || ""}
          onChange={e => {
            const found = models.find(m => m.name === e.target.value);
            setSelectedModel(found);
          }}
        >
          {models.map((model, idx) => (
            <option key={idx} value={model?.name}>{model?.name}</option>
          ))}
        </select>
      </div>
      <div className="glass-chat-card">
        <div className="chat-header">
          <h2>{selectedModel?.name}</h2>
          <h4>{selectedModel?.description}</h4>
          <span className="online-status">● Online</span>
        </div>

        <div
          className="chat-body"
          ref={containerRef}
          onScroll={handleScroll}
        >
          {/* 스크롤 여유 공간 (Prefetch Zone) 및 상태 표시 */}
          {hasMore && (
            <div className="loading-zone">
              {isLoading ? (
                <div className="loading-dots">
                  <div className="dot"></div><div className="dot"></div><div className="dot"></div>
                </div>
              ) : (
                <button className="load-more-btn" onClick={() => { if (!isLoading) setPage(p => p + 1) }}>
                  ↑ 과거의 기억 불러오기
                </button>
              )}
            </div>
          )}

          {chats.map((chat, idx) => (
            <div key={idx} className={`chat-bubble-wrapper ${chat.role === "ai" ? "ai-wrapper" : "human-wrapper"}`}>
              <div className={`chat-bubble ${chat.role === "ai" ? "chat-ai" : "chat-human"}`}>
                {chat.role === "ai" ? (
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {chat.content}
                  </ReactMarkdown>
                ) : (
                  chat.content
                )}
              </div>
            </div>
          ))}
        </div>

        <div className="chat-footer">
          <input
            className="chat-input"
            onChange={e => setChatInput(e.target.value)}
            value={chatInput}
            onKeyDown={e => {
              // 한글 조합 중(isComposing)일 때 발생하는 Enter 이벤트 무시
              if (e.nativeEvent.isComposing) return;
              if (e.key === "Enter" || e.code === "Enter") chatting();
            }}
            placeholder="토끼에게 물어보세요..."
          />
          <button className="chat-send-btn" onClick={chatting}>전송</button>
        </div>
      </div>
    </div>
  )
}

export default Home