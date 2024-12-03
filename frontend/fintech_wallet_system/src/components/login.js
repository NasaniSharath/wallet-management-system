import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {login} from '../services/api';
import { handleEncrypt } from './encryptDecrypt';
function LoginForm() {
    const [formData, setFormData] = useState({ name: '', email: '', phone_number: '' });
    const [errMsg, setErrMsg] = useState(false);
    const navigate = useNavigate();


    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            console.log(formData)
            
            await login(formData).then((res)=>{
                if(res.status === 200){
                console.log(res)
                localStorage.setItem("token", handleEncrypt(res.data.token))
                localStorage.setItem("wallet_id", handleEncrypt(res.data.wallet_id))
                if(res.data.admin){
                    localStorage.setItem("role",handleEncrypt("admin"))
                    navigate('/admin/dashboard');
                }
                else{
                    localStorage.setItem("role",handleEncrypt("user"))
                    navigate('/wallet');
                }

                }
                
                errMsg(true)
            })
            .catch((err)=>{
                setErrMsg(true);
                console.log(err);
            })

            
            
        }
        catch (error) {
            setErrMsg(true);
            console.error('Login Failed', error);
        }
    };
    return (
        <div className='container-fluid'>
            
            <div className="d-flex justify-content-center align-items-center vh-100">
            <form onSubmit={handleSubmit} className='card p-2 w-50'>
            <h2 className="text-center mb-2">Login</h2>
                <div className="form-group">
                    <label htmlFor="email">Email</label>
                    <input type="email" className="form-control" name="email" aria-describedby="emailHelp" placeholder="Enter Email" onChange={handleChange} />
                </div>
                <button type="submit" className="btn btn-primary mt-2">Login</button>
                <span><a className='mt-2' href='/register'>Register</a></span>
                {
                    errMsg && <p className='text-danger text-center'> Invalid Email</p>

                }
                
            </form>
            </div>

        </div>
    );
}
export default LoginForm;