import React, { useState } from 'react';
// import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { register } from '../services/api';
import { handleEncrypt } from './encryptDecrypt';

function RegistrationForm() {
  const [formData, setFormData] = useState({ name: '', email: '', phone_number: '' });
  const [walletId, setWalletId] = useState('');
  const [errors, setErrors] = useState({}); 
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
    setErrors({ ...errors, [name]: '' });
  };

  const validate = () => {
    let tempErrors = {};
    let valid = true;

    // Name validation
    if (!formData.name.trim()) {
      tempErrors.name = 'Name is required';
      valid = false;
    }

    // Email validation
    if (!formData.email.trim()) {
      tempErrors.email = 'Email is required';
      valid = false;
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      tempErrors.email = 'Invalid email format';
      valid = false;
    }

    // Phone number validation
    if (!formData.phone_number.trim()) {
      tempErrors.phone_number = 'Phone number is required';
      valid = false;
    } else if (!/^\d{10}$/.test(formData.phone_number)) {
      tempErrors.phone_number = 'Phone number must be 10 digits';
      valid = false;
    }
    setErrors(tempErrors);
    return valid;
  };
  

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      console.log(formData)
      if (validate()) {
      await register(formData).then((response) => {
        console.log(response)
        localStorage.setItem("wallet_id", handleEncrypt(response.data.wallet_id))
        localStorage.setItem("token", handleEncrypt(response.data.token))
        localStorage.setItem("role",handleEncrypt("user"))
        setWalletId(response.data.wallet_id);
        setFormData({ name: '', email: '', phone_number: '' })
        navigate('/wallet');

      })
        .catch((error) =>
          console.log(error))
      }

    } catch (error) {
      console.error('Registration failed', error);
    }
  };

  return (
    <div className='container m-2'>
      <div class="d-flex justify-content-center align-items-center vh-100">
      
        
        <form className='card p-2 w-50' onSubmit={handleSubmit}>
        <h3 className='text-center'>Register</h3>
          <div className="form-group">
            <label for="name">Name</label>
            <input type="name" className="form-control" name="name" aria-describedby="nameHelp" placeholder="Enter name"  value={formData.name} onChange={handleChange} />
            {errors.name && <span className="text-danger">{errors.name}</span>}

            <label for="exampleInputEmail1">Email</label>
            <input type="email" className="form-control" name="email" aria-describedby="emailHelp" placeholder="Enter email" value={formData.email} onChange={handleChange} />
            {errors.email && <span className="text-danger">{errors.email}</span>}


            <label for="phone_number">Phone Number</label>
            <input type="" className="form-control" name="phone_number" aria-describedby="phoneHelp" placeholder="Enter phone number" value={formData.phone_number} onChange={handleChange} />
            {errors.phone_number && <span className="text-danger">{errors.phone_number}</span>}

          </div>
          <button type="submit" className="btn btn-primary mt-2">Submit</button>
        </form>
        {walletId && <p>Your Wallet ID: {walletId}</p>}
      </div>
    </div>
  );
}

export default RegistrationForm;
