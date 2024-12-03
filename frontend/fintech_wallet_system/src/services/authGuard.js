
import React from 'react';
import { Navigate } from 'react-router-dom';
import { handleDecrypt } from '../components/encryptDecrypt';

const AuthGuard = ({ children }) => {
  const token = localStorage.getItem('token');
  const role = handleDecrypt(localStorage.getItem("role"))

  if (!token || role !=="user") {
    localStorage.clear()
    return <Navigate to="/" replace />;
  }

  return children;
};

const AdminAuthGuard = ({children})=>{
  const token = localStorage.getItem('token');
  const role = handleDecrypt(localStorage.getItem("role"))

  if (!token || role !=="admin") {
    localStorage.clear()
    return <Navigate to="/" replace />;
  }

  return children;

}

export{AuthGuard, AdminAuthGuard};