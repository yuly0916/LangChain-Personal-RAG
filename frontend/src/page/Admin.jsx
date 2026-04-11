import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";
import "./Home.css";

const Admin = () => {
    const navigate = useNavigate();
    const [activeTab, setActiveTab] = useState("upload");

    // Upload state
    const [file, setFile] = useState(null);
    const [modelInfor, setModelInfor] = useState({ model_name: '', model_description: '' });

    // Models & Users state
    const [models, setModels] = useState([]);
    const [users, setUsers] = useState([]);

    // Modal states for delete/update
    const [deleteModal, setDeleteModal] = useState({ isOpen: false, modelName: null });
    const [updateModal, setUpdateModal] = useState({ isOpen: false, modelName: null, newName: "" });

    const fetchModels = async () => {
        try {
            const res = await api.get('/chat/models');
            if (res.data) setModels(res.data);
        } catch (error) {
            console.error("Failed to fetch models", error);
        }
    }

    const fetchUsers = async () => {
        try {
            const res = await api.get('/admin/users');
            if (res.data) setUsers(res.data);
        } catch (error) {
            console.error("Failed to fetch users", error);
        }
    }

    useEffect(() => {
        fetchModels();
        fetchUsers();
    }, []);

    // ==========================================
    // 1. 모델 업로드 로직
    // ==========================================
    const handleModelInfor = (e) => {
        setModelInfor(p => ({ ...p, [e.target.name]: e.target.value }))
    }

    const createModel = async () => {
        if (!file || !modelInfor.model_name) return alert("모델 이름과 파일을 모두 첨부해주세요.");
        try {
            const form = new FormData();
            form.append("file", file);
            await api.post(`/admin/upload?model_name=${modelInfor.model_name}&model_description=${modelInfor.model_description}`, form);
            alert("모델 생성이 완료되었습니다.");
            setModelInfor({ model_name: '', model_description: '' });
            setFile(null);
            fetchModels();
        } catch (error) {
            console.error(error);
            alert("모델 생성에 실패했습니다.");
        }
    }

    // ==========================================
    // 2. 모델 수정/삭제 로직 (Custom Modals)
    // ==========================================
    const confirmDelete = async () => {
        const { modelName } = deleteModal;
        try {
            await api.delete(`/admin/models/${modelName}`);
            alert("삭제되었습니다.");
            fetchModels();
        } catch (e) {
            console.error(e);
            alert("API 호출 실패 (백엔드 미구현 상태입니다)");
        } finally {
            setDeleteModal({ isOpen: false, modelName: null });
        }
    }

    const confirmUpdate = async () => {
        const { modelName, newName } = updateModal;
        if (!newName || !newName.trim()) {
            alert("새로운 이름을 입력해주세요!");
            return;
        }
        try {
            await api.put(`/admin/models/${modelName}`, { model_name: newName });
            alert("수정되었습니다.");
            fetchModels();
        } catch (e) {
            console.error(e);
            alert("API 호출 실패 (백엔드 미구현 상태입니다)");
        } finally {
            setUpdateModal({ isOpen: false, modelName: null, newName: "" });
        }
    }

    // ==========================================
    // 3. 유저 권한 부여 로직
    // ==========================================
    const updateUserRole = async (userId, newRole) => {
        try {
            await api.put(`/admin/users/${userId}/role`, { role: newRole });
            alert("권한이 변경되었습니다.");
            fetchUsers();
        } catch (e) {
            console.error(e);
            alert("API 호출 실패 (백엔드 미구현 상태입니다)");
        }
    }

    return (
        <div className="home-container">
            
            {/* 삭제 확인 커스텀 모달 */}
            {deleteModal.isOpen && (
                <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,0.5)', zIndex: 9999, display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
                    <div className="glass-card" style={{ padding: '30px', width: '90%', maxWidth: '400px' }}>
                        <h3 style={{marginTop: 0, color: 'var(--color-text-main)'}}>모델 삭제 확인</h3>
                        <p style={{color: 'var(--color-text-muted)'}}><strong style={{color: 'var(--color-primary)'}}>{deleteModal.modelName}</strong> 모델을 정말 삭제하시겠습니까?</p>
                        <div style={{display: 'flex', justifyContent: 'center', gap: '10px', marginTop: '25px'}}>
                            <button className="admin-btn admin-btn-danger" style={{margin: 0}} onClick={confirmDelete}>삭제하기</button>
                            <button className="admin-btn" style={{background: 'var(--color-border)', margin: 0}} onClick={() => setDeleteModal({isOpen: false, modelName: null})}>취소</button>
                        </div>
                    </div>
                </div>
            )}

            {/* 이름 수정 커스텀 모달 */}
            {updateModal.isOpen && (
                <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,0.5)', zIndex: 9999, display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
                    <div className="glass-card" style={{ padding: '30px', width: '90%', maxWidth: '400px' }}>
                        <h3 style={{marginTop: 0, color: 'var(--color-text-main)'}}>모델 이름 수정</h3>
                        <p style={{color: 'var(--color-text-muted)', marginBottom: '10px'}}><strong style={{color: 'var(--color-primary)'}}>{updateModal.modelName}</strong> 의 새 이름을 입력하세요.</p>
                        <input 
                            className="admin-input" 
                            style={{width: '90%', marginBottom: '25px'}}
                            value={updateModal.newName} 
                            placeholder="새 이름 입력..."
                            onChange={(e) => setUpdateModal(p => ({...p, newName: e.target.value}))} 
                        />
                        <div style={{display: 'flex', justifyContent: 'center', gap: '10px'}}>
                            <button className="admin-btn" style={{margin: 0}} onClick={confirmUpdate}>수정하기</button>
                            <button className="admin-btn" style={{background: 'var(--color-border)', margin: 0}} onClick={() => setUpdateModal({isOpen: false, modelName: null, newName: ""})}>취소</button>
                        </div>
                    </div>
                </div>
            )}

            <div className="glass-admin-card">

                {/* 좌측 사이드바 탭 제어 */}
                <div className="admin-sidebar">
                    <div className="admin-sidebar-header">
                        <h2>Admin Panel</h2>
                        <button className="admin-btn" style={{ padding: '6px 12px', fontSize: '0.85rem' }} onClick={() => navigate('/')}>Home</button>
                    </div>
                    <div className={`admin-tab ${activeTab === 'upload' ? 'active' : ''}`} onClick={() => setActiveTab('upload')}>
                        모델 업로드
                    </div>
                    <div className={`admin-tab ${activeTab === 'models' ? 'active' : ''}`} onClick={() => setActiveTab('models')}>
                        모델 관리
                    </div>
                    <div className={`admin-tab ${activeTab === 'users' ? 'active' : ''}`} onClick={() => setActiveTab('users')}>
                        유저 권한 관리
                    </div>
                </div>

                {/* 우측 메인 컨텐츠 영역 */}
                <div className="admin-content">

                    {/* 탭 1: 모델 업로드 */}
                    {activeTab === 'upload' && (
                        <div>
                            <h3>신규 모델 업로드</h3>
                            <div className="admin-form-group">
                                <label>모델 이름</label>
                                <input className="admin-input" placeholder="새로운 AI 모델의 이름" name="model_name" value={modelInfor.model_name} onChange={handleModelInfor} />
                            </div>
                            <div className="admin-form-group">
                                <label>모델 설명</label>
                                <input className="admin-input" placeholder="어떤 페르소나를 가지나요?" name="model_description" value={modelInfor.model_description} onChange={handleModelInfor} />
                            </div>
                            <div className="admin-form-group">
                                <label>학습 데이터 파일 (.txt, .pdf 등)</label>
                                <input className="admin-input" type="file" onChange={e => setFile(e.target.files[0])} />
                            </div>
                            <button className="admin-btn" onClick={createModel} style={{ marginTop: '10px' }}>모델 생성하기</button>
                        </div>
                    )}

                    {/* 탭 2: 모델 조회 및 삭제/수정 */}
                    {activeTab === 'models' && (
                        <div>
                            <h3>등록된 모델 관리</h3>
                            <table className="admin-table">
                                <thead>
                                    <tr>
                                        <th>모델 이름</th>
                                        <th>설명</th>
                                        <th>관리 액션</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {models.length === 0 ? (
                                        <tr><td colSpan="3" style={{ textAlign: "center", padding: "40px", color: "var(--color-text-muted)" }}>현재 폴링된 모델 데이터가 없습니다.</td></tr>
                                    ) : (
                                        models.map((model, idx) => (
                                            <tr key={idx}>
                                                <td>{model.name}</td>
                                                <td>{model.description}</td>
                                                <td>
                                                    <button className="admin-btn" style={{ padding: '6px 12px', fontSize: '0.85rem' }} onClick={() => setUpdateModal({ isOpen: true, modelName: model.name, newName: "" })}>수정</button>
                                                    <button className="admin-btn admin-btn-danger" style={{ padding: '6px 12px', fontSize: '0.85rem' }} onClick={() => setDeleteModal({ isOpen: true, modelName: model.name })}>삭제</button>
                                                </td>
                                            </tr>
                                        ))
                                    )}
                                </tbody>
                            </table>
                        </div>
                    )}

                    {/* 탭 3: 유저 관리 */}
                    {activeTab === 'users' && (
                        <div>
                            <h3>가입 유저 권한(Role) 관리</h3>
                            <table className="admin-table">
                                <thead>
                                    <tr>
                                        <th>카카오 고유 ID</th>
                                        <th>유저 닉네임</th>
                                        <th>권한(Role) 할당</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {users.length === 0 ? (
                                        <tr><td colSpan="3" style={{ textAlign: "center", padding: "40px", color: "var(--color-text-muted)" }}>조회된 유저 데이터가 없습니다. (백엔드 연결 대기)</td></tr>
                                    ) : (
                                        users.map((user, idx) => (
                                            <tr key={idx}>
                                                <td>{user.user_k_id}</td>
                                                <td>{user.name}</td>
                                                <td>
                                                    <select
                                                        value={user.role || 'user'}
                                                        onChange={(e) => updateUserRole(user.user_k_id, e.target.value)}
                                                    >
                                                        <option value="user">일반 유저 (User)</option>
                                                        <option value="admin">최고 관리자 (Admin)</option>
                                                    </select>
                                                </td>
                                            </tr>
                                        ))
                                    )}
                                </tbody>
                            </table>
                        </div>
                    )}

                </div>

            </div>
        </div>
    )
}

export default Admin;