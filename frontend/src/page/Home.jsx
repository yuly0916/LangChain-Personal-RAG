import { HiOutlineSpeakerphone } from "react-icons/hi";
import api from "../api";
import { useEffect,useState } from "react";
function Home() {
  const [chatQuestion, setChatQuestion] = useState([])
  const [chatResponse, setChatResponse] = useState([])
  const [chat, setChat] = useState('')
  async function 채팅내역가져오기(){
    const res = await api.get('/chat')
    setChatQuestion(res.data[1]["content"]);
    setChatResponse(res.data[0]["content"]);
  }
  const chating = (e)=> {
    setChat(e.target.value);
    console.log(chat)
  }
  useEffect(()=>{
    채팅내역가져오기();

  },[])
  return (
    <div>
        <div>궁금한게 있으면 물어봐<HiOutlineSpeakerphone/>
    </div>
    <div>
        <div>채팅 내역</div>
        <div>질문: {chatQuestion}</div>
        <div>대답: {chatResponse}</div>

    </div>
    <div>
        <input onChange={chating} value={chat} placeholder="질문을 입력해주세요." />
    </div>
    </div>
  )
}

export default Home