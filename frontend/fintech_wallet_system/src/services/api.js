import axios from 'axios';
import { handleDecrypt } from '../components/encryptDecrypt';

const BASE_URL = process.env.REACT_APP_BASE_URL;
console.log(BASE_URL); 

const getConfig = ()=>{
    const token= handleDecrypt(localStorage.getItem('token'));
    const config = {
        headers:{
            Authorization: `Bearer ${token}`,
            "Content-Type":"application/json"
        }
    }
    return config
}

const register= async(payload)=>{
    return await axios.post(`${BASE_URL}/api/register`,payload)
}
const login = async(payload)=>{
    return await axios.post(`${BASE_URL}/api/login`,payload)
}

const getBalance =async(wallet_id)=>{
    const config = getConfig()
    return await axios.get(`${BASE_URL}/api/wallet/${wallet_id}/balance`, config)
}

const addMoney =async(payload)=>{
    const config = getConfig()
    return await axios.post(`${BASE_URL}/api/wallet/add-money`, payload, config)
}

const transferMoney =async(payload)=>{
    const config = getConfig()
    return await axios.post(`${BASE_URL}/api/wallet/transfer`,payload, config)
}

const getTransactions =async(wallet_id)=>{
    const config = getConfig()
    return await axios.get(`${BASE_URL}/api/wallet/${wallet_id}/transactions`,config)
}


const getAllWallets = async () => {
    const config = getConfig()
    return await axios.get(`${BASE_URL}/api/admin/wallets`, config)
}

const getAllTransactions = async () => {
    const config = getConfig()
    return await axios.get(`${BASE_URL}/api/admin/transactions`, config)
}

const getAnalytics = async () => {
    const config = getConfig()
    return await axios.get(`${BASE_URL}/api/admin/analytics`, config)
}



export {register,login, getAllWallets,getAllTransactions ,getAnalytics, getBalance, addMoney, getTransactions, transferMoney};