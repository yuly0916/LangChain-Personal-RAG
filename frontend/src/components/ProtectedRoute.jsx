import { Navigate } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';

const ProtectedRoute = ({ children, allowedRoles }) => {
  const getCookie = (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
  };

  const token = getCookie('jwt_token');

  if (!token) {
    // 토큰이 없으면 비로그인 상태이므로 로그인 페이지로 쫓아냅니다.
    return <Navigate to="/" replace />;
  }

  try {
    const decoded = jwtDecode(token);
    const userRole = decoded.role || 'user';

    // 권한 검사: allowedRoles 배열에 현재 유저의 role이 포함되어 있지 않다면 쫓아냅니다.
    if (allowedRoles && !allowedRoles.includes(userRole)) {
      // 엔터프라이즈 레벨 보안: 권한이 없는 자에게는 해당 라우트가 존재하는지조차 скры기 위해 
      // 403 Forbidden 대신 404 NotFound로 보내거나 /not-found 로 튕깁니다.
      return <Navigate to="/not-found" replace />;
    }

    return children;
  } catch (error) {
    console.error('Invalid Token:', error);
    return <Navigate to="/" replace />;
  }
};

export default ProtectedRoute;
