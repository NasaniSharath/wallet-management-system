// import logo from './logo.svg';
import './App.css';
import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import RegistrationForm from './components/RegistrationForm';
import WalletDashboard from './components/WalletDashboard';
import LoginForm from './components/login';
import AdminDashboard from './components/AdminDashboard';
import { AuthGuard, AdminAuthGuard } from './services/authGuard';

function App() {

  return (
    <div>
      <div className='bg-warning'>
        <h1 className='text-center my-2'>Wallet Management System</h1>
      </div>
      <Router>
        <Routes>
          <Route path='/' element={<LoginForm />} />
          <Route path="/register" element={
            <RegistrationForm />
          } />
          <Route path="/wallet" element={
            <AuthGuard>
              <WalletDashboard />
            </AuthGuard>} />
          <Route path='/admin/dashboard' element={
            <AdminAuthGuard>
              <AdminDashboard />
            </AdminAuthGuard>} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
